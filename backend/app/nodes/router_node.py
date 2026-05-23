from app.core.schemas import AgentState, ValidationResult

def router_node(state: AgentState) -> AgentState:
    print(f"\n--- [NODE] Final Routing Decision ---")
    
    # Lấy dữ liệu từ cả 2 nguồn "thông tin thiếu"
    customer_missing = state.draft_data.missing_info    # Khách hàng thiếu
    ai_missing_policy = state.validation_data.missing_info # AI viết thiếu
    is_valid = state.validation_data.is_valid
    priority = state.priority_data.level
    confidence = state.intent_data.confidence

    decision = ""
    reason = ""
    
    # 1. TRƯỜNG HỢP CHUYỂN NGƯỜI THẬT NGAY LẬP TỨC (Ưu tiên hàng đầu)
    # Cứ là High Priority (ví dụ: báo gian lận, mất tiền) thì không cần biết AI tự tin hay không, 
    # bắt buộc chuyển thẳng cho nhân viên thật xử lý.
    if priority == "high":
        decision = "escalate_to_human"
        reason = "High priority case. Mandated immediate escalation to human agent."
        
    # 2. TRƯỜNG HỢP SAI CHÍNH SÁCH / ẢO GIÁC (Safety Net)
    # Dù là Low/Medium, nhưng nếu Validation báo AI trả lời sai quy định, cũng phải chuyển người thật.
    elif not is_valid:
        decision = "escalate_to_human"
        reason = f"Quality check failed: {state.validation_data.feedback}"

    # 3. TRƯỜNG HỢP HỎI THÊM THÔNG TIN (Giảm tải cho nhân viên)
    # Rủi ro Low/Medium nhưng khách hàng nói chung chung, để AI tự hỏi thêm thông tin.
    elif customer_missing.lower() != "none":
        decision = "ask_for_more_info"
        reason = f"AI identified missing customer data: {customer_missing}"

    # 4. TRƯỜNG HỢP GỬI THẲNG (Tự động hóa hoàn toàn)
    # Low/Medium, khách cung cấp đủ thông tin, AI làm đúng (valid) và tự tin cao.
    elif is_valid and confidence > 0.7:
        decision = "send_reply_directly"
        reason = "Validated response with high confidence. Safe to automate."

    # 5. TRƯỜNG HỢP DỰ PHÒNG (Fallback)
    else:
        # Xử lý các case an toàn còn lại
        decision = "send_reply_directly"
        reason = "Standard Low/Medium case handled by AI."

    state.metadata["final_decision"] = decision
    print(f"Final Decision: {decision.upper()} ({reason})")
    return state