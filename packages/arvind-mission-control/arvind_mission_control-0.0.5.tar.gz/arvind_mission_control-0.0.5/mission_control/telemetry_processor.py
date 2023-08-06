from typing import TextIO
from . import models


class TelemetryProcessor(models.AbstractTelemetryProcessor):
    """TelemetryProcessor is the class used to perform the full workflow of the project"""

    def __init__(
        self,
        parser: models.AbstractTelemetryFileParser,
        alert_finder: models.AbstractAlertFinder,
        outputter: models.AbstractOutputFormatter,
    ) -> None:
        self.parser = parser
        self.alert_finder = alert_finder
        self.outputter = outputter

    def process(self, inf: TextIO) -> str:
        tel_data = self.parser.parse_file(inf)
        alerts = self.alert_finder.find_alerts(tel_data)
        out = self.outputter.format_alerts(alerts)
        return out
