"""Flask web UI for the Vedic daylight calculator."""

from __future__ import annotations

import os
from datetime import date, timedelta

from flask import Flask, render_template, request

from vedic_times.calculator import calculate_daily_times
from vedic_times.timezones import load_zone_locations, timezone_names


def _date_options(today: date) -> list[date]:
    start = today - timedelta(days=366)
    return [start + timedelta(days=offset) for offset in range(366 * 3)]


def create_app() -> Flask:
    app = Flask(__name__)
    locations = load_zone_locations()
    zones = timezone_names(locations)

    @app.route("/", methods=["GET", "POST"])
    def index():
        today = date.today()
        selected_date = request.form.get("date", today.isoformat())
        default_zone = "Asia/Kolkata" if "Asia/Kolkata" in locations else zones[0]
        selected_zone = request.form.get("timezone", default_zone)
        result = None
        error = None

        if request.method == "POST":
            try:
                day = date.fromisoformat(selected_date)
                location = locations[selected_zone]
                result = calculate_daily_times(day, location)
            except KeyError:
                error = "Please choose a valid date and timezone."
            except ValueError as exc:
                if "sun" in str(exc).lower():
                    error = "Sunrise or sunset does not occur at this location on this date."
                else:
                    error = "Please choose a valid date and timezone."

        return render_template(
            "index.html",
            dates=_date_options(today),
            zones=zones,
            selected_date=selected_date,
            selected_zone=selected_zone,
            result=result,
            error=error,
        )

    return app


def main() -> None:
    app = create_app()
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "8000")), debug=False)


if __name__ == "__main__":
    main()
