from dataclasses import dataclass
from typing import TextIO, List
from enum import Enum
import datetime
from abc import ABC, abstractmethod


class Threshold(Enum):
    """Threshold is used to denote whether a reading exceeds a maximum threshold or is beneath a minimum one"""

    BEYOND_UPPER = 1
    BENEATH_LOWER = 2


@dataclass
class SatelliteAlert:
    """SatelliteAlert is used to encapsulate alert data"""

    satellite_id: int
    severity: Threshold
    component: str
    timestamp: datetime.datetime


@dataclass(eq=True)
class SatelliteStatusReading:
    """SatelliteStatusReading is a single telemetry reading"""

    timestamp: datetime.datetime
    satellite_id: int
    red_high_limit: int  # threshold
    yellow_high_limit: int
    yellow_low_limit: int
    red_low_limit: int  # threshold
    raw_value: float
    component: str


class AbstractTelemetryProcessor(ABC):
    """AbstractTelemetryProcessor processes telemetry text data and return formatted information about it"""

    @abstractmethod
    def process(self, inf: TextIO) -> str:
        """Process telemetry text data and return formatted information about it"""
        ...


class AbstractTelemetryFileParser(ABC):
    """AbstractTelemetryFileParser is used to process messages from a telemetry file and return a list of readings"""

    @abstractmethod
    def parse_file(self, inf: TextIO) -> List[SatelliteStatusReading]:
        """Parses a telemetry row and returns a list of readings"""
        ...


class AbstractAlertFinder(ABC):
    """AbstractAlertFinder is used to find clusters of limit-exceeding entries and creates a list of alerts"""

    @abstractmethod
    def find_alerts(
        self, tel_data: List[SatelliteStatusReading]
    ) -> List[SatelliteAlert]:
        """Finds clusters of limit-exceeding entries and creates a list of alerts"""
        ...


class AbstractOutputFormatter(ABC):
    """AbstractOutputFormatter formats SatelliteAlert output into json based on parameters provided"""

    @abstractmethod
    def format_alerts(self, alerts: List[SatelliteAlert]) -> str:
        """Formats alerts and returns a json string"""
        ...
