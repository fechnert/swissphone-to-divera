import logging
import logging.config
import yaml

from datetime import datetime, timedelta

from lib.api import DiveraConnector
from lib.config import Config
from lib.exceptions import ValidationError, ReadTimeout
from lib.parser import Parser
from lib.reader import Boss925Reader


LOGGING_CONF = 'conf/logging.yml'
PROJECT_CONF = 'conf/config.yml'

with open(LOGGING_CONF, 'r') as logging_conf_file:
    logging_conf = yaml.safe_load(logging_conf_file.read())
logging.config.dictConfig(logging_conf)

log = logging.getLogger("main")


class AlertController:

    def __init__(self, config):
        self.config = config
        self.divera = DiveraConnector(config)
        self.reader = Boss925Reader(config)
        self.parser = Parser(config)

        self._last_ping = datetime.now()
        self._last_ping_alarmed = False

    def run(self) -> None:
        """Main loop"""

        log.info("Listening for alarms ...")
        while True:
            try:
                self.reader.read_line()
            except ReadTimeout:
                self._process_timeout()
            else:
                if self.reader.is_complete():
                    self._process_transmission(self.reader.get_transmission())
                    self.reader.reset_store()

    def _process_transmission(self, transmission: dict) -> None:
        """Process an incoming transmission after it was received completely"""

        if self.reader.is_ping():
            self._process_ping()

        else:
            log.info("Incoming alarm detected!")
            log.info("  RIC = %s%s", transmission["ric"], transmission["subric"])
            log.info("  MSG = %s...", transmission["message"][:64])
            rics = self.config.get_rics(transmission['ric'])
            data = self.parser.parse_transmission(transmission)

            self.divera.alert(rics, data)

    def _process_timeout(self) -> None:
        log.debug("Read timeout ...")
        if (datetime.now() - self._last_ping) > timedelta(minutes=15):
            delay = datetime.now() - self._last_ping
            log.error("Ping delay too high! Delay is %s", delay)

            if not self._last_ping_alarmed:
                self._last_ping_alarmed = True
                rics = self.config.get_rics('ping')
                data = {
                    'title': 'Keine Meldungen!',
                    'text': f'Keine Rückmeldung vom DME!\n\nLetzter Ping: {self._last_ping}\nDelay: {delay}',
                    'priority': False
                }

                self.divera.alert(rics, data)

    def _process_ping(self) -> None:
        delay = datetime.now() - self._last_ping
        log.debug("Received ping (Delay was %s)", delay)
        self._last_ping = datetime.now()
        self._last_ping_alarmed = False


if __name__ == '__main__':

    try:
        config = Config.from_file(filename=PROJECT_CONF)
        controller = AlertController(config)
        controller.run()
    except ValidationError as e:
        log.error("Config is not valid!")
        log.error(e)
    except NotImplementedError:
        log.error("Parser not compatible!")
    except KeyboardInterrupt:
        pass

    log.info("Shutting down ...")
