from app.core.schemas import AgentState, IntentResult
from app.clients.grpc_intent_client import grpc_intent_client

def intent_node(state: AgentState) -> AgentState:
    print(f"\n--- [NODE] Intent Detection (via gRPC) ---")
    
    # Gửi tin nhắn qua gRPC tới Intent Service (Lấy cả 3 biến)
    predicted_intent, cofi, reason = grpc_intent_client.predict_intent(state.customer_message)
    
    # Cập nhật kết quả vào state
    state.intent_data = IntentResult(intent=predicted_intent, confidence=cofi)
    
    # Ghi log kèm theo reason
    state.trace.append(f"Intent: {predicted_intent} (Reason: {reason})")
    
    print(f"Result: {predicted_intent}")
    print(f"Confidence: {cofi}")
    print(f"Reason: {reason}")
    
    return state