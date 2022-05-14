import logging
import yaml

from lib.exceptions import ValidationError


log = logging.getLogger("main")


class Config:
    """Data object which contains the config content"""

    @classmethod
    def from_file(cls, filename):
        """Read config variables from given yaml file"""

        log.info("Loading config ...")

        with open(filename, 'r') as config_file:
            raw_config = yaml.safe_load(config_file.read())

        instance = cls()
        for key, values in raw_config.items():
            setattr(instance, key, values)

        instance._fix_rics()
        instance._validate_ric_groups()
        instance._validate_ric_departments()
        return instance

    def get_rics(self, position):
        """Get the department and rics for a given position"""

        try:
             if str(position).isnumeric():
                 rics = self.rics[int(position)]
             else:
                 rics = self.rics[str(position)]
        except KeyError:
            return None

        if not rics:
            return None

        groups = list()
        for ric in rics.split(','):
            ric = ric.strip()
            groups.append(ric.split(':', 1))

        return groups

    def _fix_rics(self):
        """This brings comfort to the config yaml as low integer values can be prefixed with a zero"""

        for ric, values in list(self.rics.items()):
            if isinstance(ric, str) and ric.isnumeric():
                self.rics[int(ric)] = values
                del self.rics[ric]

    def _validate_ric_groups(self):
        """check that the configured rics are usable"""

        for position, targets in self.rics.items():
            if not targets:
                continue

            for ric in targets.split(','):
                if ':' not in ric:
                    raise ValidationError(f'No department mentioned for ric "{position}" ({targets})')

    def _validate_ric_departments(self):
        """check that the configured ric departments have assigned access keys"""

        for position, targets in self.rics.items():
            groups = self.get_rics(position)
            if not groups:
                continue

            for department, _ in groups:
                if department not in self.divera['departments'].keys():
                    raise ValidationError(f'Unknown department "{department}" for ric "{position}" ({targets})!')
