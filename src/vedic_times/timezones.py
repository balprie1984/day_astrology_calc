"""Load representative coordinates for IANA timezones."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from zoneinfo import available_timezones


@dataclass(frozen=True, slots=True)
class ZoneLocation:
    timezone: str
    latitude: float
    longitude: float
    country_codes: str = ""
    comment: str = ""


def _coordinate(value: str, degree_digits: int) -> float:
    """Convert ISO-6709 compact degrees/minutes[/seconds] to decimal degrees."""
    sign = -1 if value[0] == "-" else 1
    digits = value[1:]
    degree = int(digits[:degree_digits])
    remainder = digits[degree_digits:]
    if len(remainder) == 2:
        minutes, seconds = int(remainder), 0
    elif len(remainder) == 4:
        minutes, seconds = int(remainder[:2]), int(remainder[2:])
    else:
        raise ValueError(f"Unsupported coordinate: {value}")
    return sign * (degree + minutes / 60 + seconds / 3600)


def _split_coordinates(value: str) -> tuple[float, float]:
    split_at = max(value.find("+", 1), value.find("-", 1))
    if split_at < 0:
        raise ValueError(f"Invalid coordinates: {value}")
    return _coordinate(value[:split_at], 2), _coordinate(value[split_at:], 3)


def _zone_table_text() -> str:
    try:
        return resources.files("tzdata.zoneinfo").joinpath("zone1970.tab").read_text(
            encoding="utf-8"
        )
    except (ModuleNotFoundError, FileNotFoundError):
        for base in (Path("/usr/share/zoneinfo"), Path("/usr/share/lib/zoneinfo")):
            for filename in ("zone1970.tab", "zone.tab"):
                candidate = base / filename
                if candidate.exists():
                    return candidate.read_text(encoding="utf-8")
    raise RuntimeError("Timezone coordinate data is unavailable; install tzdata.")


def load_zone_locations() -> dict[str, ZoneLocation]:
    locations: dict[str, ZoneLocation] = {}
    for line in _zone_table_text().splitlines():
        if not line or line.startswith("#"):
            continue
        columns = line.split("\t")
        latitude, longitude = _split_coordinates(columns[1])
        locations[columns[2]] = ZoneLocation(
            timezone=columns[2],
            latitude=latitude,
            longitude=longitude,
            country_codes=columns[0],
            comment=columns[3] if len(columns) > 3 else "",
        )
    return locations


def timezone_names(locations: dict[str, ZoneLocation]) -> list[str]:
    """Return zones for which both a UTC rule and representative point exist."""
    valid = available_timezones()
    return sorted(zone for zone in locations if zone in valid)

