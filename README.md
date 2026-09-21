# Vedic Daylight Times

A small Flask web application that calculates **Rahu Kalam**, **Gulika Kalam**,
**Yamagandam**, and **Abhijit Muhurat** for a selected date and IANA timezone.
It targets Python **3.14.7**.

## Calculation model

The app calculates astronomical sunrise and sunset with Astral at the IANA
timezone database's representative coordinate for the selected timezone.
Daylight is split into eight equal segments; weekday-specific segments give
Rahu Kalam, Gulika Kalam, and Yamagandam. Abhijit Muhurat is the central
one-fifteenth of daylight (the eighth of 15 muhurtas). The UI notes the common
tradition that Abhijit Muhurat is not observed on Wednesday.

A timezone can cover a large area, so these are reference-point estimates.
Exact city coordinates may produce slightly different times.

## Run with Python 3.14.7

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python3.14 -m pip install --upgrade pip
python3.14 -m pip install -r requirements.txt
python3.14 -m pip install -e .
python3.14 -m vedic_times
```

Open <http://127.0.0.1:8000>.

If your executable includes the patch version in its name, replace
`python3.14` with `python3.14.7` in the commands above.

## Test

```bash
python3.14 -m pip install -r requirements-dev.txt
python3.14 -m pytest
```

## Project layout

```text
.
├── src/vedic_times/       # application package, UI templates, and styles
├── tests/                 # unit and integration tests
├── pyproject.toml         # package/build configuration
├── requirements.txt       # runtime dependencies
├── requirements-dev.txt   # development dependencies
└── .python-version        # requested interpreter version
```

## License

This project is available under the [MIT License](LICENSE).
