"""Using Pydantic schemas to build JSON schema and validate data returned by the model"""

from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

class CustomerSupportTicket(BaseModel):
    customer_id: str
    message: str = Field(min_length=1)
    channel: Literal["email", "chat", "social_network", "web"]
    created_at: datetime
    sla_deadline: datetime | None = None

class TriageClassification(BaseModel):
    urgency: Literal["low", "medium", "high", "critical"]
    sentiment: Literal["positive", "neutral", "negative", "angry"]
    category: Literal[
        "billing",
        "technical",
        "general_inquiry",
        "feedback",
        "sales",
        "other"
    ]
    sensitive: bool
    summary: str
    suggested_respones: str
    confidence: float = Field(ge=0, le=1)

class TriageResponse(BaseModel):
    ticket_id: str
    triage: TriageClassification
    escalate: bool
    escalation_reason: str | None = None
