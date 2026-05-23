from app.core.schemas import AgentState, PolicyResult
from app.data.policies import get_policy_by_intent

def policy_node(state: AgentState) -> AgentState:
    """
    Retrieve relevant policies/FAQs based on predicted intent.
    """
    print(f"\n--- [NODE] Policy Retrieval ---")
    
    # 1. Get intent from previous step, default to 'general_policy' if empty
    current_intent = "general_policy"
    if state.intent_data and state.intent_data.intent:
        current_intent = state.intent_data.intent
        
    # 2. Query data from policies.py using get_policy_by_intent (mocks database)
    retrieved_content = get_policy_by_intent(current_intent)
    
    # 3. Pack into PolicyResult and save to State
    state.policy_data = PolicyResult(
        content=retrieved_content,
        source="Internal Knowledge Base"
    )
    
    # 4. Log trace for tracking
    state.trace.append(f"Policy grounded for intent: {current_intent}")
    
    print(f"Result: Retrieved policy for '{current_intent}'")
    
    return state