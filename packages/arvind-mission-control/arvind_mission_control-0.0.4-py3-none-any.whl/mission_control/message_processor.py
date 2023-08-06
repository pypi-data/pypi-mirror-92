from typing import BinaryIO, List, Optional, Dict
from dataclasses import dataclass, field
from enum import Enum
import datetime
from marshmallow import fields
from dataclasses_json import dataclass_json, config


class InvalidFileError(RuntimeError):
    """Error generated if an invalid file input is given."""

class InvalidRowError(RuntimeError):
    """Error generated if an invalid row is given."""
class InvalidThresholdError(RuntimeError):
    """Error generated if invalid threshold is given."""

# Threshold is to denote whether the limit-breaking reading exceeds the upper threshold or is beneath the lower threshold
class Threshold(Enum):
    BEYOND_UPPER = 1
    BENEATH_LOWER = 2

@dataclass_json
@dataclass
class SatelliteAlert:
    satellite_id: int
    severity: str
    component: str
    timestamp: datetime.datetime


@dataclass(eq=True)
class SatelliteStatusReading:
    timestamp: datetime.datetime
    satellite_id: int
    red_high_limit: int  # threshold
    yellow_high_limit: int
    yellow_low_limit: int
    red_low_limit: int  # threshold
    raw_value: float
    component: str

@dataclass(eq=True, unsafe_hash=True)
class SatelliteComponentKey:
    satellite_id: int
    component: str
    threshold: Threshold

def parse_reading(row: str) -> SatelliteStatusReading:
    """Parses a telemetry row in the format <timestamp>|<satellite-id>|<red-high-limit>|<yellow-high-limit>|<yellow-low-limit>|<red-low-limit>|<raw-value>|<component>
    timestamp example format: 20180101 23:01:05.001
    Args:
        row: the row in the expected format
    Raises:
        InvalidRowError: If row is not in expected format #FIXME: throw it
    Returns:
        SatelliteStatusReading containing fields set to the various values of the row
    """
    r = row.strip().split('|')
    dt = ingest_time(r[0])
    return SatelliteStatusReading(
        timestamp=dt,
        satellite_id=int(r[1]),
        red_high_limit=int(r[2]),
        yellow_high_limit=int(r[3]),
        yellow_low_limit=int(r[4]),
        red_low_limit=int(r[5]),
        raw_value=float(r[6]),
        component=r[7],
    )


def ingest_time(t: str) -> datetime.datetime:
    return datetime.datetime.strptime(t, '%Y%m%d %H:%M:%S.%f')

def format_time(dt: datetime.datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

def format_threshold(threshold: Threshold) -> str:
    if threshold == Threshold.BENEATH_LOWER:
        return 'RED LOW'
    elif threshold == Threshold.BEYOND_UPPER:
        return 'RED HIGH'
    else:
        raise InvalidThresholdError

def process(inf: BinaryIO) -> List[Dict]: #TODO: change to use SatelliteAlert
    """Processes a file for telemetry data. Assumes timestamp sorted data.
    Args:
        inf: an opened file for reading.
    Raises:
        InvalidFileError: If inf is not valid for reading #FIXME: remove
    Returns:
        List containing alerts from processing
    """
    result: List[Dict] = []
    limit_breaking_readings :Dict[SatelliteComponentKey,List[SatelliteStatusReading]] = {}

    for line in inf:
        r = parse_reading(line)
        key = None
        if r.raw_value > r.red_high_limit:
            key = SatelliteComponentKey(satellite_id=r.satellite_id, component=r.component, threshold=Threshold.BEYOND_UPPER)
        elif r.raw_value < r.red_low_limit:
            key = SatelliteComponentKey(satellite_id=r.satellite_id, component=r.component, threshold=Threshold.BENEATH_LOWER)
        else:
            continue
        if not key in limit_breaking_readings:
            limit_breaking_readings[key] = []
        curr_comp_readings = limit_breaking_readings[key]
        curr_comp_readings.append(r)
    
    five_min = datetime.timedelta(0,0,0,0,5)
    for key, comp_readings in limit_breaking_readings.items():
        for i, reading in enumerate(comp_readings):
            alert = find_alerts(i, key, reading, comp_readings)
            if alert:
                result.append(alert)
    
    return sorted(result, key=lambda k: k['timestamp'], reverse=True)

def find_alerts(i: int, key: SatelliteComponentKey, reading: SatelliteStatusReading, comp_readings: List[SatelliteStatusReading]) -> Optional[SatelliteAlert]:
    num_clustered = 0
    five_min = datetime.timedelta(0,0,0,0,5)
    for next in comp_readings[i:]:
        if reading.timestamp + five_min > next.timestamp:
            num_clustered += 1
        # if 3 or more, then this particular component/threshhold should have an alert generated for it
        if num_clustered >= 3:
            alert = SatelliteAlert(satellite_id=key.satellite_id, severity=format_threshold(key.threshold), component=key.component, timestamp=reading.timestamp)
            #alert = {'satelliteId': key.satellite_id, 'severity': format_threshold(key.threshold), 'component': key.component, 'timestamp': format_time(reading.timestamp)}
            return alert
    
    return None