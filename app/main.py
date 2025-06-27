from fastapi import FastAPI, Request, Response
import uvicorn
from app.agent import agent
from app.instagram import send_instagram_message
from config import WEBHOOK_VERIFY_TOKEN
import json

app = FastAPI()

@app.get("/webhook")
def verify_webhook(request: Request):
    """Verify the webhook subscription."""
    if request.query_params.get("hub.mode") == "subscribe" and request.query_params.get("hub.challenge"):
        if not request.query_params.get("hub.verify_token") == WEBHOOK_VERIFY_TOKEN:
            return Response(content="Verification token mismatch", status_code=403)
        return Response(content=request.query_params["hub.challenge"])
    return Response(content="Failed to verify webhook", status_code=400)

@app.post("/webhook")
async def handle_webhook(request: Request):
    """Handle incoming messages from Instagram."""
    data = await request.json()
    if data.get("object") == "instagram":
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"]["text"]
                    
                    # Use the sender_id as the thread_id for conversation history
                    response = agent.run(message_text, sender_id)
                    
                    # Extract the AI's response and send it back to the user
                    ai_message = response['messages'][-1].content
                    send_instagram_message(sender_id, ai_message)
    return Response(status_code=200)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 