from typing import Callable, List, Optional, Dict
from dataclasses import dataclass
import datetime
from . import models

# this class is not in models because it's very specific to the internal implementation of this file
@dataclass(eq=True, frozen=True)
class SatelliteComponentKey:
    """SatelliteComponentKey is used to find limit-breaking telemetry readings on a specific component for a specific satellite"""

    satellite_id: int
    component: str
    threshold: models.Threshold


class AlertFinder(models.AbstractAlertFinder):
    """AlertFinder is used to find alerts in telemetry data based on a time interval and frequency of limit-exceeding telemetry entries"""

    def __init__(
        self,
        interval: datetime.timedelta,
        frequency: int,
        filter_fn: Callable[[models.SatelliteStatusReading, models.Threshold], bool],
    ) -> None:
        self.interval = interval
        self.frequency = frequency
        self.filter_fn = filter_fn

    def __compile_alerts_for_component(
        self,
        i: int,
        key: SatelliteComponentKey,
        reading: models.SatelliteStatusReading,
        comp_readings: List[models.SatelliteStatusReading],
    ) -> Optional[models.SatelliteAlert]:
        num_clustered = 0
        for next in comp_readings[i:]:
            if reading.timestamp + self.interval > next.timestamp:
                num_clustered += 1
            # if frequency or more, then this particular component/threshhold should have an alert generated for it
            if num_clustered >= self.frequency:
                alert = models.SatelliteAlert(
                    satellite_id=key.satellite_id,
                    severity=key.threshold,
                    component=key.component,
                    timestamp=reading.timestamp,
                )
                return alert
        return None

    def find_alerts(
        self, tel_data: List[models.SatelliteStatusReading]
    ) -> List[models.SatelliteAlert]:
        """Finds clusters of limit-exceeding entries and creates a list of alerts
        Assumptions:
          interval is within 5-minutes which does not include 5-minute mark i.e. `23:00:00.000-23:04:59.999` but would not include a limit-breaking entry at `23:05:00.000`
          alerts are once per id/component/type per file; i.e. if there are multiple bursts of limit-breaking entries of the same
            type for a single component on the same satellite, then only ONE alert is made
        """

        limit_breaking_readings: Dict[
            SatelliteComponentKey, List[models.SatelliteStatusReading]
        ] = {}
        alerts: List[models.SatelliteAlert] = []

        for tel_row in tel_data:
            if tel_row.raw_value > tel_row.red_high_limit:
                key = SatelliteComponentKey(
                    satellite_id=tel_row.satellite_id,
                    component=tel_row.component,
                    threshold=models.Threshold.BEYOND_UPPER,
                )
            elif tel_row.raw_value < tel_row.red_low_limit:
                key = SatelliteComponentKey(
                    satellite_id=tel_row.satellite_id,
                    component=tel_row.component,
                    threshold=models.Threshold.BENEATH_LOWER,
                )
            else:
                continue

            if not self.filter_fn(
                tel_row, key.threshold
            ):  # rows that don't pass through the filter are excluded
                continue

            if not key in limit_breaking_readings:
                limit_breaking_readings[key] = []
            curr_comp_readings = limit_breaking_readings[key]
            curr_comp_readings.append(tel_row)

        for key, comp_readings in limit_breaking_readings.items():
            for i, reading in enumerate(comp_readings):
                alert = self.__compile_alerts_for_component(
                    i, key, reading, comp_readings
                )
                if alert:
                    alerts.append(alert)
                    break

        return alerts
