from app.core.schemas import AgentState, PriorityResult

def priority_node(state: AgentState) -> AgentState:
    """
    Determine request priority based on intent and risk keywords.
    """
    print(f"\n--- [NODE] Priority & Risk Detection ---")
    
    # Load data from State
    intent = state.intent_data.intent
    message = state.customer_message.lower()
    
    # Mapping Intent -> Priority
    HIGH_RISK_INTENTS = [
        "lost_or_stolen_card", 
        "lost_or_stolen_phone", 
        "compromised_card", 
        "card_swallowed", 
        "transaction_charged_twice",
        "declined_cash_withdrawal"
    ]
    
    MEDIUM_RISK_INTENTS = [
        "pin_blocked", 
        "failed_transfer", 
        "card_not_working", 
        "declined_card_payment",
        "verify_my_identity"
    ]
    
    # Classification logic
    priority_level = "low"
    reason = "Standard service request."

    # Check high priority
    if intent in HIGH_RISK_INTENTS or any(word in message for word in ["stolen", "urgent", "emergency", "fraud"]):
        priority_level = "high"
        reason = "Critical: Potential financial loss or security breach detected."
    
    # Check medium priority
    elif intent in MEDIUM_RISK_INTENTS or "blocked" in message:
        priority_level = "medium"
        reason = "Medium: Service interruption or identity verification required."
    
    # Encapsulate and save to State
    state.priority_data = PriorityResult(
        level=priority_level,
        reason=reason
    )
    
    # Log trace
    state.trace.append(f"Priority: {priority_level.upper()} (Reason: {reason})")
    
    print(f"Result: {priority_level.upper()}")
    return state