"""Deterministic rule-based classifier used before an LLM is introduced."""
import re

from app.schemas import CustomerSupportTicket, TriageClassification

ANGRY_WORDS = {"unacceptable", "furious", "worst", "never again", "disappointed", "angry"}
URGENT_WORDS = {"immediately", "urgent", "now", "asap", "critical", "emergency"}
SENSITIVE_WORDS = {"legal", "discrimination", "harassment", "abuse", "threat", "safety", "kill"}


def _contains_phrase(text: str, phrases: set[str]) -> bool:
    """Match complete words/phrases so that e.g. ``now`` does not match ``knowledge``."""
    return any(re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", text) for phrase in phrases)

def classify_with_rules(ticket: CustomerSupportTicket) -> TriageClassification:
    text = ticket.message.casefold()

    sentiment = "angry" if _contains_phrase(text, ANGRY_WORDS) else "neutral"
    urgency = "high" if _contains_phrase(text, URGENT_WORDS) else "medium"
    sensitive = _contains_phrase(text, SENSITIVE_WORDS)
    
    if "billing" in text or "invoice" in text or "payment" in text or "refund" in text or "charge" in text:
        category = "billing"
    elif "technical" in text or "account" in text or "password" in text or "login" in text or "forgot password" in text:
        category = "technical"
    elif "general" in text or "question" in text or "how to" in text or "information" in text:
        category = "general_inquiry"
    else:
        category = "other"

    return TriageClassification(
        urgency=urgency,
        sentiment=sentiment,
        category=category,
        sensitive=sensitive,
        summary=ticket.message[:120],
        suggested_response="Thank you for reaching out. We are reviewing your case and will respond as soon as possible",
        confidence=0.6
    )
