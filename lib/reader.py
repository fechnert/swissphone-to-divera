import re
import serial

from lib.exceptions import ReadTimeout


class Boss925Reader:

    config = None
    _stored_transmission = None

    def __init__(self, config):
        self.config = config
        self.reset_store()

        if self.config.general["debug"]:
            self.buffer = open("transmissions.txt", "rb")
        else:
            self.buffer = serial.Serial(
                port=self.config.serial["port"],
                baudrate=self.config.serial["baud"],
                timeout=30,
            )

    def read_line(self) -> None:
        """read a single line from buffer"""

        line = self.buffer.readline()
        self._process_line(line)

    def _process_line(self, line: bytes) -> None:
        """process a single given line"""

        # decode the given line properly
        if isinstance(line, bytes):
            line = line.decode("iso-8859-1")

        # strip the annoying "\r\n"
        line = line.strip()

        # completely empty line is produced by the serial read timeout
        # nullbyte is sent after complete transmission but does not include a newline, so treat it as a timeout
        if line == "" or line.encode() == b"\x00":
            raise ReadTimeout()

        # read the ric and split it into ric and subric
        elif m := re.match(r"^([0-9]{2})([A-D])$", line):
            self._store("ric", m.group(1))
            self._store("subric", m.group(2))

        # read the date but don't store it
        elif m := re.match(r"^[0-9]{2}:[0-9]{2} [0-9]{2}\.[0-9]{2}\.[0-9]{2}$", line):
            self._store("date", m.group(0))

        # everything else will probably be the message
        else:
            self._store("message", line)

    def reset_store(self) -> None:
        self._stored_transmission = {
            "date": None,
            "ric": None,
            "subric": None,
            "message": None,
        }

    def _store(self, key, value):
        self._stored_transmission[key] = value

    def get_transmission(self):
        return self._stored_transmission

    def is_ping(self) -> bool:
        """check if the stored transmission is a ping"""

        if message := self._stored_transmission.get("message", ""):
            return message.startswith("Ping;")
        else:
            return False

    def is_complete(self) -> bool:
        """check if the stored transmission is complete"""

        return all([v for k, v in self._stored_transmission.items()])
