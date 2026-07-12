"""Unit tests for human handoff and SLA rules."""

from datetime import datetime, timedelta, timezone

import pytest

from app.schemas import TriageClassification
from app.triage.escalation import decide_escalation, is_sla_expired


def classification(**overrides) -> TriageClassification:
    values = {
        "urgency": "medium",
        "sentiment": "neutral",
        "category": "other",
        "sensitive": False,
        "summary": "Summary",
        "suggested_response": "Suggested response",
        "confidence": 0.6,
    }
    values.update(overrides)
    return TriageClassification(**values)


@pytest.mark.parametrize(
    ("overrides", "sla_expired", "reason"),
    [
        ({"sentiment": "angry"}, False, "Angry customer"),
        ({"urgency": "critical"}, False, "Critical urgency"),
        ({"sensitive": True}, False, "Sensitive content in message topic"),
        ({}, True, "SLA deadline expired"),
        ({"confidence": 0.59}, False, "Low confidence score"),
    ],
)
def test_escalation_rules(overrides, sla_expired, reason):
    assert decide_escalation(classification(**overrides), sla_expired) == (True, reason)


def test_non_risky_ticket_is_not_escalated_at_confidence_boundary():
    assert decide_escalation(classification(confidence=0.6), False) == (False, None)


def test_escalation_uses_documented_priority_order():
    risky = classification(sentiment="angry", urgency="critical", sensitive=True)
    assert decide_escalation(risky, True) == (True, "Angry customer")


def test_sla_expiration_is_deterministic_for_aware_dates():
    now = datetime(2026, 7, 10, 12, tzinfo=timezone.utc)
    assert is_sla_expired(now - timedelta(seconds=1), now) is True
    assert is_sla_expired(now, now) is False
    assert is_sla_expired(now + timedelta(seconds=1), now) is False
    assert is_sla_expired(None, now) is False


def test_naive_sla_dates_are_interpreted_as_utc():
    now = datetime(2026, 7, 10, 12, tzinfo=timezone.utc)
    assert is_sla_expired(datetime(2026, 7, 10, 11, 59), now) is True
