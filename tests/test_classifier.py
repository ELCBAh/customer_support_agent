"""Unit tests for deterministic ticket classification."""

from datetime import datetime, timezone

import pytest

from app.schemas import CustomerSupportTicket
from app.triage.classifier import classify_with_rules


def make_ticket(message: str) -> CustomerSupportTicket:
    return CustomerSupportTicket(
        customer_id="customer-1",
        message=message,
        channel="email",
        created_at=datetime.now(timezone.utc),
    )


@pytest.mark.parametrize(
    ("message", "category"),
    [
        ("Please send a refund for this invoice", "billing"),
        ("I forgot my password and cannot login", "technical"),
        ("How to find more information?", "general_inquiry"),
        ("I would like to leave feedback", "other"),
    ],
)
def test_classifies_business_categories(message, category):
    assert classify_with_rules(make_ticket(message)).category == category


def test_matching_is_case_insensitive():
    result = classify_with_rules(make_ticket("I am FURIOUS and need help ASAP"))
    assert result.sentiment == "angry"
    assert result.urgency == "high"


def test_keywords_do_not_match_inside_unrelated_words():
    assert classify_with_rules(make_ticket("Update your knowledge base")).urgency == "medium"


def test_sensitive_content_is_flagged():
    assert classify_with_rules(make_ticket("This concerns harassment")).sensitive is True


def test_summary_is_capped_at_120_characters():
    assert classify_with_rules(make_ticket("x" * 150)).summary == "x" * 120
