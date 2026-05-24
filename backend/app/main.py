from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent.orchestrator import orchestrator

app = FastAPI(title="Banking Agent API")

class RunAgentRequest(BaseModel):
    message: str

@app.get("/health")
async def health_check():
    """Kiểm tra xem hệ thống có đang hoạt động hay không."""
    return {"status": "running", "message": "API Gateway is healthy"}

@app.get("/config")
async def get_config():
    """Trả về cấu hình hệ thống hiện tại."""
    # Bạn có thể điều chỉnh cấu hình này dựa trên biến môi trường (env) thực tế
    return {
        "status": "success",
        "config": {
            "llm_service": "ollama",
            "intent_service": "grpc",
        }
    }

@app.post("/run-agent")
async def run_agent_endpoint(request: RunAgentRequest):
    """Thực thi toàn bộ agentic workflow."""
    try:
        # Gọi orchestrator điều phối luồng xử lý
        state = orchestrator.run(request.message)
        
        # Trả về kết quả đầu ra có cấu trúc cuối cùng
        return {
            "request_id": state.request_id,
            "response": state.metadata.get("display_response"),
            "decision": state.metadata.get("final_decision"),
            "trace": state.trace
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stream-agent")
async def stream_agent_endpoint(request: RunAgentRequest):
    import json
    from fastapi.responses import StreamingResponse
    
    def event_generator():
        for update in orchestrator.stream_run(request.message):
            yield f"data: {json.dumps(update)}\n\n"
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")