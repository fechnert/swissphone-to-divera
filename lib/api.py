import logging
import requests
import time


log = logging.getLogger("main")


class DiveraConnector:

    base_url = "https://www.divera247.com/api"
    departments = dict()

    def __init__(self, config):
        self.config = config

        for name, key in self.config.divera["departments"].items():
            self.departments[name] = key

    def alert(self, rics, data):
        """Send an alert"""

        if self.config.general["debug"]:
            rics = self.config.get_rics("debug")

        calls = dict()
        for _department, _ric in rics:
            if _department in calls:
                if _ric not in calls[_department]:
                    calls[_department].append(_ric)
            else:
                calls[_department] = [_ric]

        log.info("Sending alarm to DIVERA 24/7!")
        for _department, _rics in calls.items():
            data = {"ric": ",".join(_rics), **data}

            log.info("  %s: %s", _department, ",".join(_rics))

            key = self.departments[_department]
            response = requests.post(
                url=f"{self.base_url}/alarm?accesskey={key}",
                json=data,
                timeout=30,
            )

            # looks strange, but ensures that divera has time to aggregate incoming transmissions
            time.sleep(1)
