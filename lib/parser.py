import logging


log = logging.getLogger("main")


class BaseParser:

    def __init__(self, config):
        self.config = config
        self.mapping = (
            ('title', self.get_title),
            ('text', self.get_text),
            ('address', self.get_address),
            ('number', self.get_number),
            ('priority', self.get_priority),
        )

    def parse_transmission(self, transmission: dict):

        log.info("Parsing transmission ...")
        result = dict()
        for key, func in self.mapping:
            value = func(**transmission)
            result[key] = value
            log.info("  %s: %r", key, str(value)[:64])

        return result

    def get_title(self, date, ric, subric, message) -> str:
        raise NotImplementedError()

    def get_text(self, date, ric, subric, message) -> str:
        raise NotImplementedError()

    def get_address(self, date, ric, subric, message) -> str:
        raise NotImplementedError()

    def get_number(self, date, ric, subric, message) -> str:
        raise NotImplementedError()

    def get_priority(self, date, ric, subric, message) -> bool:
        raise NotImplementedError()


class Parser(BaseParser):

    def _is_probealarm(self, message):
        return message.startswith('Probealarm;')

    def get_title(self, ric, subric, message, **data):
        if self._is_probealarm(message):
            return 'Probealarm'

        if len(message.split(';')) != 2:
            return f'{message[:10]}...'
        else:
            fixed_text, message = message.split(';')
            if len(message.split('*')) >= 2:
                keyword = message.split('*')[1].strip()
                return f'{fixed_text} ({keyword})'
            return f'{fixed_text}'

    def get_text(self, message, subric, **data):
        if self._is_probealarm(message):
            return 'Das ist ein Probealarm!'

        if len(message.split(';')) != 2:
            return message
        else:
            subric_text = self.config.subrics.get(subric, '') or ''
            fixed_text, message = message.split(';')
            text = f'{fixed_text} {subric_text}\n\n{message}'
            return text

    def get_address(self, **data):
        return ''

    def get_number(self, date, ric, subric, message):
        if self._is_probealarm(message):
            return None

        number = message.split('*')[-1]
        if not number.isnumeric():
            return None

        return number

    def get_priority(self, date, ric, subric, message):
        return False
