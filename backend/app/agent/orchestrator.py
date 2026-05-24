import uuid
from typing import Dict, Any
from app.core.schemas import AgentState
from app.nodes.intent_node import intent_node
from app.nodes.priority_node import priority_node
from app.nodes.policy_node import policy_node
from app.nodes.draft_node import draft_node
from app.nodes.validation_node import validation_node
from app.nodes.router_node import router_node

class BankingAgentOrchestrator:
    def __init__(self):
        print("--- [SYSTEM] Agentic Orchestrator Initialized ---")
        
    def format_final_response(self, state: AgentState) -> str:
        """
        Dựa vào quyết định của Router để chọn cách hiển thị phù hợp.
        """
        decision = state.metadata.get("final_decision")
        draft = state.draft_data.draft_response
        next_step = state.draft_data.next_step
        missing = state.draft_data.missing_info

        if decision == "send_reply_directly":
            return f"{draft}\n\n Next step: {next_step}"
        
        elif decision == "ask_for_more_info":
            # --- ĐOẠN CODE MỚI ---
            if isinstance(missing, list):
                # Nếu LLM ngoan ngoãn trả về List thì nối bằng dấu phẩy
                missing_str = ", ".join(missing)
            elif isinstance(missing, str):
                # Nếu LLM lỡ trả về String (ví dụ có sẵn gạch đầu dòng) thì lấy xài luôn
                missing_str = missing
            else:
                missing_str = "some specific details"
            # ----------------------
            return (f"I understand your request, but I need a bit more information to help you properly. "
                    f"Could you please provide:\n**{missing_str}**?")
        
        elif decision == "escalate_to_human":
            return ("I'm connecting you to a human specialist who can handle this complex request. "
                    "Please wait a moment while I transfer your data...")
        
        return "I'm having trouble processing this. Let me connecting you to a human to help you."

    def run(self, customer_message: str) -> AgentState:
        """
        Điều phối luồng chạy xuyên suốt qua tất cả các Node.
        """
        # 0. Khởi tạo State ban đầu
        state = AgentState(
            request_id=str(uuid.uuid4()),
            customer_message=customer_message
        )
        
        print(f"\n🚀 Starting Pipeline for Request: {state.request_id}")
        print(f"Message: {customer_message}")

        try:
            # 1. Intent Detection: Xác định khách hàng muốn gì
            state = intent_node(state)

            # 2. Priority Detection: Đánh giá rủi ro
            state = priority_node(state)

            # 3. Policy Retrieval: Tra cứu quy định chính xác
            state = policy_node(state)

            # 4. Response Drafting: LLM soạn thảo câu trả lời
            state = draft_node(state)

            # 5. Validation: Kiểm tra chất lượng bản thảo (Grounding)
            state = validation_node(state)

            # 6. Routing: Đưa ra quyết định cuối cùng (Send/Ask/Escalate)
            state = router_node(state)

        except Exception as e:
            error_msg = f"Pipeline failed at some point: {str(e)}"
            state.trace.append(f"ERROR: {error_msg}")
            print(f"Error: {error_msg}")
            # Fallback nếu lỗi: Chuyển thẳng cho người thật
            state.metadata["final_decision"] = "escalate_to_human"

        final_text = self.format_final_response(state)
        state.metadata["display_response"] = final_text

        return state

    def stream_run(self, customer_message: str):
        """
        Streaming version of the orchestrator run. Yields progress updates.
        """
        import uuid
        state = AgentState(
            request_id=str(uuid.uuid4()),
            customer_message=customer_message
        )
        
        try:
            yield {"status": "running", "node": "Intent Detection"}
            state = intent_node(state)

            yield {"status": "running", "node": "Priority Detection"}
            state = priority_node(state)

            yield {"status": "running", "node": "Policy Retrieval"}
            state = policy_node(state)

            yield {"status": "running", "node": "Response Drafting"}
            state = draft_node(state)

            yield {"status": "running", "node": "Validation"}
            state = validation_node(state)

            yield {"status": "running", "node": "Routing"}
            state = router_node(state)

        except Exception as e:
            error_msg = f"Pipeline failed at some point: {str(e)}"
            state.trace.append(f"ERROR: {error_msg}")
            state.metadata["final_decision"] = "escalate_to_human"

        final_text = self.format_final_response(state)
        state.metadata["display_response"] = final_text

        yield {
            "status": "completed",
            "request_id": state.request_id,
            "response": final_text,
            "decision": state.metadata.get("final_decision", "unknown"),
            "trace": state.trace
        }

orchestrator = BankingAgentOrchestrator()