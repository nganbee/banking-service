from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any
from datetime import datetime

# Node Class

class IntentResult(BaseModel):
    intent: str = Field(..., description="Customer Intent")
    confidence: float

class PriorityResult(BaseModel):
    level: Literal["low", "medium", "high"] = Field(..., description="Piority of issue")
    reason: str

class PolicyResult(BaseModel):
    content: str = Field(..., description="Relevant FAQ entry, policy snippet, support guidline")
    source: Optional[str] = None

class DraftResult(BaseModel):
    draft_response: str
    missing_info: str = "None"
    next_step: str = "Follow policy"
    tone: str = "professional"

class ValidationResult(BaseModel):
    is_valid: bool = Field(..., description="Check generated response is consistent with the policy")
    feedback: Optional[str] = Field(None, description="Reason if invalid")
    missing_info: List[str] = []

class RoutingResult(BaseModel):
    next_action: Literal["respond", "escalate", "retry"]
    reason: str

# Schema
class AgentState(BaseModel):
    request_id: str
    customer_message: str
    
    # Result of node
    intent_data: Optional[IntentResult] = None
    priority_data: Optional[PriorityResult] = None
    policy_data: Optional[PolicyResult] = None
    draft_data: Optional[DraftResult] = None
    validation_data: Optional[ValidationResult] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Tracking
    is_escalated: bool = False
    trace: List[str] = Field(default_factory=list, description="Save history")
    created_at: datetime = Field(default_factory=datetime.now)

class CustomerRequest(BaseModel):
    message: str
    customer_id: str

class FinalResponse(BaseModel):
    request_id: str
    response: str
    status: Literal["completed", "escalated"]
    metadata: dict = {}