import re
from app.clients.ollama_client import ollama_client
from app.core.settings import settings
from app.core.schemas import AgentState, DraftResult

def draft_node(state: AgentState) -> AgentState:
    """
    Use LLM to draft customer response based on:
    Message, Intent, Priority, and Policy.
    """
    print(f"\n--- [NODE] Response Drafting ---")

    # 1. Prepare context for prompt
    customer_msg = state.customer_message
    intent = state.intent_data.intent
    priority = state.priority_data.level
    policy_content = state.policy_data.content

    # 2. Build system prompt to define AI personality
    system_prompt = (
        "You are a professional, empathetic, and efficient Virtual Banking Assistant. "
        "Your goal is to provide accurate support based ONLY on the provided policy. "
        "Format your output as a clear response to the customer."
    )

    # 3. Build detailed user prompt
    user_prompt = f"""
    CONTEXT:
    - Customer Message: "{customer_msg}"
    - Detected Intent: {intent}
    - Priority Level: {priority.upper()}
    - Official Policy: "{policy_content}"

    TASK:
    Draft a professional reply to the customer. 
    1. If the priority is HIGH, ensure the tone is urgent and reassuring.
    2. If any information is missing from the customer's request to fulfill the policy requirement, mention it.
    3. Suggest the next step (e.g., waiting for delivery, checking the app, or speaking to a human agent).

    RESPONSE STRUCTURE:
    - Draft Response: [Your message here]
    - Missing Information: [List any missing data or 'None']
    - Next Action: [The suggested next step]
    """

    # 4. Call Ollama (using generation model from settings)
    raw_response = ollama_client.generate(
        model=settings.GENERATION_MODEL,
        prompt=user_prompt,
        system_prompt=system_prompt,
        options={
            "temperature": 0,
            "top_p": 0.9
        }
    )
    
    draft_pattern = r"\**Draft Response:\**\s*(.*?)(?=\**Missing Information:|$)"
    missing_pattern = r"\**Missing Information:\**\s*(.*?)(?=\**Next Action:|$)"
    next_action_pattern = r"\**Next Action:\**\s*(.*)"

    draft_match = re.search(draft_pattern, raw_response, re.DOTALL | re.IGNORECASE)
    missing_match = re.search(missing_pattern, raw_response, re.DOTALL | re.IGNORECASE)
    next_action_match = re.search(next_action_pattern, raw_response, re.DOTALL | re.IGNORECASE)

    final_draft = draft_match.group(1).strip() if draft_match else raw_response
    missing_info_text = missing_match.group(1).strip() if missing_match else "None"
    next_step = next_action_match.group(1).strip() if next_action_match else "Follow policy"
    
    final_draft = re.sub(r"^Result:\s*", "", final_draft, flags=re.IGNORECASE).strip()

    #missing_info_list = [i.strip("- ") for i in missing_info_text.split("\n") if i.strip() and "none" not in i.lower()]

    # 5. Save result to State
    state.draft_data = DraftResult(
        draft_response=final_draft,
        missing_info=missing_info_text,
        next_step=next_step,
        tone="empathetic" if priority == "high" else "professional"
    )

    state.trace.append("Draft response generated using LLM.")
    print(f"Result: {final_draft} \n Missing Info: {missing_info_text} \n Next step: {next_step}")

    return state