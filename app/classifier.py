"""simple classifier without using LLM yet"""
from app.schemas import CustomerSupportTicket, TriageClassification

ANGRY_WORDS = {"unacceptable", "furious", "worst", "never again", "disappointed"}
URGENT_WORDS = {"immediately", "urgent", "now", "ASAP", "critical", "emergency"}
SENSITIVE_WORDS = {"legal", "discrimination", "harassment", "abuse", "threat", "safety"}

def classify_with_rules(ticket: CustomerSupportTicket) -> TriageClassification:
    text = ticket.message.lower()

    sentiment = "angry" if any(word in text for word in ANGRY_WORDS) else "neutral"
    urgency = "high" if any(word in text for word in URGENT_WORDS) else "medium"
    sensitive = any(word in text for word in SENSITIVE_WORDS)
    
    if "refund" in text:
        category = "refund"
    elif "billing" in text or "invoice" in text or "payment" in text:
        category = "billing"
    elif "technical" in text or "account" in text:
        category = "technical"
    elif "general" in text:
        category = "general"
    else:
        category = "other"

    return TriageClassification(
        urgency=urgency,
        sentiment=sentiment,
        category=category,
        sensitive=sensitive,
        summary=ticket.message[:120],
        suggested_respones="Thank you for reaching out. We are reviewing your case and will respond as soon as possible",
        confidence=0.6,
    )
