"""End-to-end contract tests for the FastAPI application."""

from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def ticket_payload(**overrides):
    payload = {
        "customer_id": "customer-42",
        "message": "I have a question about your opening hours",
        "channel": "chat",
        "created_at": "2026-07-10T12:00:00Z",
    }
    payload.update(overrides)
    return payload


def test_triage_returns_the_documented_response_contract():
    response = client.post("/triage", json=ticket_payload())
    assert response.status_code == 200
    body = response.json()
    assert body["ticket_id"].startswith("TCK-")
    assert len(body["ticket_id"]) == 12
    assert body["triage"]["category"] == "general_inquiry"
    assert body["triage"]["confidence"] == 0.6
    assert body["escalate"] is False
    assert body["escalation_reason"] is None


def test_triage_escalates_an_angry_billing_request():
    response = client.post(
        "/triage",
        json=ticket_payload(message="This duplicate charge is unacceptable. Refund me ASAP."),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["triage"]["category"] == "billing"
    assert body["triage"]["urgency"] == "high"
    assert body["triage"]["sentiment"] == "angry"
    assert body["escalation_reason"] == "Angry customer"


def test_triage_escalates_an_expired_naive_sla_deadline():
    expired = (datetime.now(timezone.utc) - timedelta(days=1)).replace(tzinfo=None).isoformat()
    response = client.post("/triage", json=ticket_payload(sla_deadline=expired))
    assert response.status_code == 200
    assert response.json()["escalation_reason"] == "SLA deadline expired"


def test_triage_rejects_invalid_input():
    assert client.post("/triage", json=ticket_payload(message="")).status_code == 422
    assert client.post("/triage", json=ticket_payload(channel="phone")).status_code == 422


def test_each_request_gets_a_unique_ticket_id():
    first = client.post("/triage", json=ticket_payload()).json()["ticket_id"]
    second = client.post("/triage", json=ticket_payload()).json()["ticket_id"]
    assert first != second
