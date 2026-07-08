"""Customer Support Agent API (Triage)"""

from fastapi import FastAPI
from app.schemas import CustomerSupportTicket, TriageResponse

app = FastAPI(title="Customer Support Agent API")

@app.post("/triage", response_model=TriageResponse)
def triage_message(ticket: CustomerSupportTicket):
    return TriageResponse(
        ticket_id="TCK-0001",
        urgency="high",
        sentiment="neutral",
        category="billing",
        sensitive=False,
        summary="Customer reports an issue with their latest bill",
        suggested_response="Please provide more details about the issue with your latest bill",
        confidence=0.95,
        escalate=False,
        escalation_reason=None,
    )
