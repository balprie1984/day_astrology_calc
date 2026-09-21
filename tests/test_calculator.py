from datetime import date, datetime, timedelta, timezone

import pytest

from vedic_times import calculator
from vedic_times.timezones import ZoneLocation, _coordinate, _split_coordinates


def test_coordinate_parsing():
    assert _coordinate("+404251", 2) == pytest.approx(40.714167)
    assert _coordinate("-0740023", 3) == pytest.approx(-74.006389)
    assert _split_coordinates("+2232+08822") == pytest.approx((22.533333, 88.366667))


def test_monday_segments(monkeypatch):
    day = date(2026, 9, 21)  # Monday
    rise = datetime(2026, 9, 21, 6, tzinfo=timezone.utc)
    set_ = datetime(2026, 9, 21, 18, tzinfo=timezone.utc)
    monkeypatch.setattr(calculator, "sunrise", lambda *args, **kwargs: rise)
    monkeypatch.setattr(calculator, "sunset", lambda *args, **kwargs: set_)

    result = calculator.calculate_daily_times(
        day, ZoneLocation("UTC", 0.0, 0.0)
    )
    periods = {item.name: item for item in result.periods}

    assert periods["Rahu Kalam"].start == rise + timedelta(hours=1.5)
    assert periods["Gulika Kalam"].start == rise + timedelta(hours=7.5)
    assert periods["Yamagandam"].start == rise + timedelta(hours=4.5)
    assert periods["Abhijit Muhurat"].start == rise + timedelta(hours=5.6)
    assert periods["Abhijit Muhurat"].end == rise + timedelta(hours=6.4)


def test_wednesday_observance_note(monkeypatch):
    day = date(2026, 9, 23)
    rise = datetime(2026, 9, 23, 6, tzinfo=timezone.utc)
    monkeypatch.setattr(calculator, "sunrise", lambda *args, **kwargs: rise)
    monkeypatch.setattr(calculator, "sunset", lambda *args, **kwargs: rise + timedelta(hours=12))

    result = calculator.calculate_daily_times(day, ZoneLocation("UTC", 0, 0))
    assert "not observed" in result.abhijit_observance_note

