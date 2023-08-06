"""Bridge MCE IR remote events to a Horimote client."""

import signal
import socket
import logging
import traceback
import time
import random
import argparse
from threading import Timer
import horimote
from .keys import HORIZON_KEY_MAP

APP_NAME = "horimotemce"
VERSION = "0.1.1"
_LOGGER = logging.getLogger(APP_NAME)
_DEFAULT_LOG_LEVEL = logging.WARN

LIRC_SOCK_PATH = "/var/run/lirc/lircd"
HORIZON_MEDIA_HOST = "horizon-media"
SOCK_BUFSIZE = 4096
RECONNECT_DELAY_MAX = 64
MIN_REPEAT_TIME_MS = 740
CACHED_EVENT_EXPIRE_TIME = 5
HORIMOTE_KEEPALIVE_TIME = 15.0


class ExitApp(Exception):
    pass


class HorimoteDisconnected(Exception):
    pass


class LircDisconnected(Exception):
    pass


## https://stackoverflow.com/questions/12248132/how-to-change-tcp-keepalive-timer-using-python-script
def set_tcp_keepalive(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    """Set TCP keepalive on an open socket.

    It activates after 1 second (after_idle_sec) of idleness,
    then sends a keepalive ping once every 3 seconds (interval_sec),
    and closes the connection after 5 failed ping (max_fails), or 15 seconds.

    NOTE: Closed connection results in the next read/write failing immediately
          if it is not currently blocking.
    """
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)


class HorimoteClient(horimote.Client):
    """Extended Horimote client that supports keepalive."""

    def __init__(self, ip, port=5900, keepalive=False):
        self._keepalive_timer = None
        self._keepalive = keepalive

        ## Replicate constructor but don't connect/authorize yet
        self.ip = ip
        self.port = port
        self.con = None

    def connect(self):
        """Start keepalive timer after successfully connecting."""
        super().connect()
        self.authorize()
        if self._keepalive:
            self.init_keepalive_timer()
        set_tcp_keepalive(self.con, 15, 1, 5)

    def disconnect(self):
        """Disconnect and free socket on disconnect."""
        if self._keepalive_timer:
            _LOGGER.debug("stopping existing keepalive timer")
            self._keepalive_timer.cancel()
        super().disconnect()
        del self.con

    def send_key(self, key):
        """Start keepalive timer after sending a key."""
        super().send_key(key)
        # self.init_keepalive_timer()

    def init_keepalive_timer(self):
        """Initialise keepalive."""
        if self._keepalive_timer:
            self._keepalive_timer.cancel()
            _LOGGER.debug("stopped existing keepalive timer")
            del self._keepalive_timer
        self._keepalive_timer = Timer(HORIMOTE_KEEPALIVE_TIME, self.send_keepalive)
        self._keepalive_timer.start()
        _LOGGER.debug(f"started keepalive timer for {HORIMOTE_KEEPALIVE_TIME}s")

    def send_keepalive(self):
        """Send a keepalive packet."""
        self._keepalive_timer = None
        if self.con != None:
            try:
                _LOGGER.debug("sending keepalive")
                self.con.send(b"")
            except OSError as e:
                _LOGGER.error("could not send to Horizon: %s", e)
                ## TODO: does not work as timer tasks run in a different
                ##       context. Need to signal main thread, and refactor
                ##       recv() on LIRC socket to check for signal.
                raise HorimoteDisconnected
        self.init_keepalive_timer()


class LircClient:
    """Class for lirc socket."""

    _last_event_timestamp = 0
    _retry_event = None  ## received event to be retried
    _retry_event_timestamp = 0

    def __init__(self, sock_path):
        self._sock_path = sock_path
        self._sock = None

    def connect(self):
        """Connect to LIRC socket."""
        if not self._sock:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(self._sock_path)
            self._sock = sock
        else:
            _LOGGER.warning("LIRC socket %s already connected", self._sock_path)

    def disconnect(self):
        """Disconnect from LIRC socket."""
        if self._sock:
            self._sock.close()
            self._sock = None

    def send_event(self, horimote_client, event=None):
        """Send an event to HorimoteClient."""
        if event is None:
            ## Process any saved event if event is None
            if LircClient._retry_event:
                event = LircClient._retry_event
                event_timestamp = LircClient._retry_event_timestamp
                LircClient._retry_event = None

                event_timedelta = round(time.time() - event_timestamp, 3)
                if event_timedelta >= CACHED_EVENT_EXPIRE_TIME:
                    _LOGGER.debug(
                        "ignoring expired event: '%s' (expired: %.3fs ago)",
                        event,
                        event_timedelta,
                    )
                    return
                _LOGGER.debug("processing saved event: '%s'", event)
            else:
                ## No saved event to process
                return
        else:
            event_timestamp = time.time()

        event_timedelta_ms = (event_timestamp - LircClient._last_event_timestamp) * 1000
        try:
            event_info = str(event).split(" ", 4)
            repeat_flag = event_info[1] != "0"
            mce_key = event_info[2]

            if repeat_flag and event_timedelta_ms < MIN_REPEAT_TIME_MS:
                ## Ignore repeated key
                _LOGGER.debug("ignoring repeated key: %s", mce_key)
                return

            LircClient._last_event_timestamp = event_timestamp
            horizon_key = HORIZON_KEY_MAP.get(mce_key)
            if horizon_key:
                _LOGGER.info(
                    "map key: %s to: %s (+%dms)",
                    mce_key,
                    str(horizon_key),
                    round(event_timedelta_ms),
                )
                horimote_client.send_key(horizon_key)
            else:
                _LOGGER.debug("ignoring unmapped key: %s", mce_key)
        except OSError as e:
            _LOGGER.error("could not send to Horizon: %s", e)
            LircClient._retry_event = event  ## Save event to replay
            LircClient._retry_event_timestamp = event_timestamp
            raise HorimoteDisconnected

    def event_loop(self, horimote_client):
        """Main event loop."""
        while True:
            self.send_event(horimote_client)  ## Process saved event if any
            try:
                ## Read a key event from the socket
                event = self._sock.recv(SOCK_BUFSIZE)
                _LOGGER.debug("received LIRC event: '%s'", event)
            except OSError as e:
                ## Socket error, mark disconnected
                _LOGGER.error("could not read from LIRC: %s", e)
                raise LircDisconnected

            if event:
                self.send_event(horimote_client, event)  ## Map and send to horimote
            else:
                _LOGGER.error(f"empty event received from LIRC, disconnecting")
                raise LircDisconnected


def get_backoff_delay(retry_count):
    """Calculate exponential backoff with random jitter delay."""
    delay = round(
        min(RECONNECT_DELAY_MAX, (2 ** retry_count) - 1)
        + (random.randint(0, 1000) / 1000),
        3,
    )
    return delay


def main_loop():
    ## Create horimote client
    lirc_sock_path = LIRC_SOCK_PATH
    lirc_client = LircClient(lirc_sock_path)
    lirc_connected = False
    lirc_retry = 0

    horimote_host = HORIZON_MEDIA_HOST
    horimote_client = HorimoteClient(horimote_host)
    horimote_connected = False
    horimote_retry = 0

    while True:
        ## Connect to LIRC
        if not lirc_connected:
            try:
                _LOGGER.debug("connecting to LIRC socket %s", lirc_sock_path)
                lirc_client.connect()
                _LOGGER.info("connected to LIRC socket %s", lirc_sock_path)
                lirc_connected = True
                lirc_retry = 0
            except OSError as e:
                if lirc_retry == 0:
                    _LOGGER.error("could not connect to LIRC: %s, retrying", e)
                else:
                    _LOGGER.debug("LIRC connect retry #%d failed: %s", lirc_retry, e)
                lirc_delay = get_backoff_delay(horimote_retry)
                _LOGGER.debug("waiting %ds before retrying LIRC", lirc_delay)
                time.sleep(lirc_delay)
                lirc_retry += 1
                continue

        ## Connect to horimote
        if not horimote_connected:
            try:
                _LOGGER.debug("connecting to Horizon host %s", horimote_host)
                horimote_client.connect()
                _LOGGER.info("connected to Horizon host %s", horimote_host)
                horimote_connected = True
                horimote_retry = 0
            except OSError as e:
                if horimote_retry == 0:
                    _LOGGER.error("could not connect to Horizon: %s, retrying", e)
                else:
                    _LOGGER.debug(
                        "Horizon connect retry #%d failed: %s", horimote_retry, e
                    )
                horimote_delay = get_backoff_delay(horimote_retry)
                _LOGGER.debug("waiting %ds before retrying Horizon", horimote_delay)
                time.sleep(horimote_delay)
                horimote_retry += 1
                continue

        try:
            lirc_client.event_loop(horimote_client)
        except LircDisconnected:
            lirc_connected = False
            lirc_client.disconnect()
        except HorimoteDisconnected:
            horimote_connected = False
            horimote_client.disconnect()
        except Exception as e:
            lirc_client.disconnect()
            horimote_client.disconnect()
            raise e


def sigterm_handler(signal, frame):
    _LOGGER.warning("SIGTERM received, exiting")
    raise ExitApp


def parse_args():
    """ Parse command line arguments. """
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument(
        "-k", "--keepalive", help="enable keepalive timer", action="store_true"
    )
    parser.add_argument(
        "-d", "--debug", help="enable console debug logging", action="store_true"
    )
    parser.add_argument(
        "-I", "--info", help="enable console info logging", action="store_true"
    )
    parser.add_argument(
        "-v",
        "--version",
        help="show application version",
        action="version",
        version="%(prog)s " + VERSION,
    )
    args = vars(parser.parse_args())
    return args


def main():
    log_level = _DEFAULT_LOG_LEVEL
    args = parse_args()
    log_level_name = "(none)"
    if args.get("debug"):
        log_level = logging.DEBUG
        log_level_name = "debug"
    elif args.get("info"):
        log_level = logging.INFO
        log_level_name = "info"
    try:
        ## Catch SIGTERM and enable logging
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s %(levelname)s[%(threadName)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        _LOGGER.setLevel(log_level)
        _LOGGER.info("setting log level to %s", log_level_name)
        signal.signal(signal.SIGTERM, sigterm_handler)

        ## Start main loop
        main_loop()
    except KeyboardInterrupt:
        _LOGGER.warning("Keyboard interrupt, exiting")
        exit(255)
    except ExitApp:
        exit(0)
    except Exception as e:
        _LOGGER.error(f"Exception: {e}")
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()