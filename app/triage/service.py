"""Connect classification and escalation into the ticket workflow."""

from uuid import uuid4

from app.schemas import CustomerSupportTicket, TriageResponse
from app.triage.classifier import classify_with_rules
from app.triage.escalation import decide_escalation, is_sla_expired


def process_support_ticket(ticket: CustomerSupportTicket) -> TriageResponse:
    classification = classify_with_rules(ticket)
    sla_expired = is_sla_expired(ticket.sla_deadline)
    escalate, reason = decide_escalation(classification, sla_expired)
    
    return TriageResponse(
        ticket_id=f"TCK-{uuid4().hex[:8].upper()}",
        triage=classification,
        escalate=escalate,
        escalation_reason=reason,
    )
