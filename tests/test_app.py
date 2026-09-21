from vedic_times.app import create_app


def test_index_loads():
    app = create_app()
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Vedic Daylight Times" in response.data
    assert b"Asia/Kolkata" in response.data


def test_calculation_submission():
    app = create_app()
    client = app.test_client()
    response = client.post(
        "/", data={"date": "2026-09-21", "timezone": "Asia/Kolkata"}
    )
    assert response.status_code == 200
    assert b"Rahu Kalam" in response.data
    assert b"Abhijit Muhurat" in response.data

