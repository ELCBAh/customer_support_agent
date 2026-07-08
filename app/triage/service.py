"""connecting the workflow"""

from app.schemas import CustomerSupportTicket, TriageClassification, TriageResponse
from app.triage.classifier import classify_with_rules
from app.triage.escalation import decide_escalation, is_sla_expired


def process_support_ticket(ticket: CustomerSupportTicket) -> TriageResponse:
    classification = classify_with_rules(ticket)
    sla_expired = is_sla_expired(ticket.sla_deadline)
    escalate, reason = decide_escalation(classification, sla_expired)
    
    return TriageResponse(
        ticket_id="TCK-0001",
        urgency=classification.urgency,
        sentiment=classification.sentiment,
        category=classification.category,
        sensitive=classification.sensitive,
        summary=classification.summary,
        suggested_response=classification.suggested_respones,
        confidence=classification.confidence,
        escalate=escalate,
        escalation_reason=reason,
    )
