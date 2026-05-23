import re
from app.core.schemas import AgentState, ValidationResult

def validation_node(state: AgentState) -> AgentState:
    """
    Check response quality before finishing workflow.
    """
    print(f"\n--- [NODE] Validation ---")

    # 1. Get data to validate
    intent_confidence = state.intent_data.confidence
    draft_text = state.draft_data.draft_response.lower()
    policy_content = state.policy_data.content.lower()

    # Validation flags
    is_valid = True
    feedback = []
    missing_info = []

    # --- CHECK 1: Intent confidence (Confidence Threshold) ---
    # If model predicts intent with low confidence (e.g., < 0.6)
    CONFIDENCE_THRESHOLD = 0.6
    if intent_confidence < CONFIDENCE_THRESHOLD:
        is_valid = False
        feedback.append("Low intent confidence. Response might be irrelevant.")

    # --- CHECK 2: Response length (Length Check) ---
    # Very short responses (e.g., < 20 chars) usually indicate errors
    if len(draft_text.strip()) < 20:
        is_valid = False
        feedback.append("The generated draft is too short.")

    # --- CHECK 3: Important info presence (Keyword Check) ---
    # If policy mentions 'app' but draft doesn't, AI might have missed it
    policy_words = re.findall(r'\b\w{5,}\b|\d+', policy_content)
    unique_policy_words = set(policy_words)
    
    matched_words = [word for word in unique_policy_words if word in draft_text]
    coverage_score = len(matched_words) / len(unique_policy_words) if unique_policy_words else 1.0
    
    # missing_info = list(unique_policy_words - set(matched_words))[:5]
    
    if unique_policy_words:
        matched_words = [word for word in unique_policy_words if word in draft_text]
        coverage_score = len(matched_words) / len(unique_policy_words)
        
        if coverage_score < 0.5:
            is_valid = False
            missing_count = len(unique_policy_words) - len(matched_words)
            missing_info = list(unique_policy_words - set(matched_words))[:5]
            feedback.append(f"Low grounding score ({coverage_score:.2f}). Missing key terms: {', '.join(missing_info)}")

    # 2. Pack result into State
    state.validation_data = ValidationResult(
        is_valid=is_valid,
        feedback="; ".join(feedback) if feedback else "Response looks good.",
        missing_info=missing_info
    )

    # 3. Log trace
    status = "PASSED" if is_valid else "FAILED"
    state.trace.append(f"Validation: {status}. Feedback: {state.validation_data.feedback}")
    
    print(f"Result: {status}")
    if not is_valid:
        print(f"Issues: {state.validation_data.feedback}")

    return state