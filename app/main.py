"""Customer Support Agent API (Triage)"""

from fastapi import FastAPI
from app.schemas import CustomerSupportTicket, TriageResponse
from app.triage.service import process_support_ticket

app = FastAPI(title="Customer Support Agent API")

@app.post("/triage", response_model=TriageResponse)
def triage_message(ticket: CustomerSupportTicket):
    return process_support_ticket(ticket)
