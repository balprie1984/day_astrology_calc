"""Core daylight-period calculations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from astral import Observer
from astral.sun import sunrise, sunset

from vedic_times.timezones import ZoneLocation


@dataclass(frozen=True, slots=True)
class TimePeriod:
    name: str
    start: datetime
    end: datetime


@dataclass(frozen=True, slots=True)
class DailyTimes:
    date: date
    timezone: str
    latitude: float
    longitude: float
    sunrise: datetime
    sunset: datetime
    periods: tuple[TimePeriod, ...]
    abhijit_observance_note: str | None = None


# Python weekday (Monday=0) -> daylight segment number (zero-based).
_RAHU_SEGMENT = (1, 6, 4, 5, 3, 2, 7)
_GULIKA_SEGMENT = (5, 4, 3, 2, 1, 0, 6)
_YAMAGANDAM_SEGMENT = (3, 2, 1, 0, 6, 5, 4)


def _period(name: str, daybreak: datetime, length: timedelta, segment: int) -> TimePeriod:
    start = daybreak + segment * length
    return TimePeriod(name=name, start=start, end=start + length)


def calculate_daily_times(day: date, location: ZoneLocation) -> DailyTimes:
    """Calculate the requested periods using local astronomical sunrise/sunset."""
    timezone = ZoneInfo(location.timezone)
    observer = Observer(latitude=location.latitude, longitude=location.longitude)
    rise = sunrise(observer, date=day, tzinfo=timezone)
    set_ = sunset(observer, date=day, tzinfo=timezone)
    daylight = set_ - rise
    eighth = daylight / 8
    fifteenth = daylight / 15
    weekday = day.weekday()

    periods = (
        _period("Rahu Kalam", rise, eighth, _RAHU_SEGMENT[weekday]),
        _period("Gulika Kalam", rise, eighth, _GULIKA_SEGMENT[weekday]),
        _period("Yamagandam", rise, eighth, _YAMAGANDAM_SEGMENT[weekday]),
        _period("Abhijit Muhurat", rise, fifteenth, 7),
    )
    note = (
        "Abhijit Muhurat is traditionally not observed on Wednesday."
        if weekday == 2
        else None
    )
    return DailyTimes(
        date=day,
        timezone=location.timezone,
        latitude=location.latitude,
        longitude=location.longitude,
        sunrise=rise,
        sunset=set_,
        periods=periods,
        abhijit_observance_note=note,
    )

