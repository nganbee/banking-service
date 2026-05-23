from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent.orchestrator import orchestrator

app = FastAPI(title="Banking Agent API")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        state = orchestrator.run(request.message)
        
        return {
            "request_id": state.request_id,
            "response": state.metadata.get("display_response"),
            "decision": state.metadata.get("final_decision"),
            # "intent": state.intent_data.get("intent")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def health_check():
    return {"status": "running"}