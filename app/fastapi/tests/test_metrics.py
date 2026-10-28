from fastapi.testclient import TestClient
from main import app


def test_metrics_endpoint():
    with TestClient(app) as client:
        response = client.get("/metrics")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "# HELP" in response.text


def test_http_requests_are_instrumented():
    with TestClient(app) as client:
        response = client.get("/openapi.json")
        assert response.status_code == 200

        metrics = client.get("/metrics")

    assert metrics.status_code == 200
    assert "http_requests_total" in metrics.text
