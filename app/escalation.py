"""Rule based escalation filtering logic"""
from datetime import datetime, timezone
from app.schemas import TriageClassification

def is_sla_expired(sla_deadline) -> bool:
    if sla_deadline is None:
        return False
    now = datetime.now(timezone.utc)
    return now > sla_deadline

def decide_escalation(
    classification: TriageClassification,
    sla_expired: bool
) -> tuple[bool, str | None]:
    """
    Determine if a ticket requires human escalation based on rules.

    Args:
        classification: TriageClassification instance
        sla_expired: Whether the SLA has expired

    Returns:
        tuple of (escalate: bool, reason: str | None)
    """
    if classification.sentiment == "angry":
        return True, "Angry customer"
    if classification.urgency == "critical":
        return True, "Critical urgency"
    if classification.sensitive:
        return True, "Sensitive content in message topic"
    if sla_expired:
        return True, "SLA deadline expired"
    if classification.confidence < 0.6:
        return True, "Low confidence score"

    return False, None
