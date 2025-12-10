"""
FastAPI application for Adaptive LLM Chat Agent.
"""

import os
from typing import Dict, Any
from datetime import datetime
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from database import Database
from llm_service import LLMService
from profile_service import ProfileService
from news_service import NewsService

load_dotenv()

app = FastAPI(
    title="Agente Conversacional LLM Adaptativo",
    description="API con perfil inteligente y análisis emocional",
    version="2.0.0"
)

# Services
db = Database()
llm_service = LLMService()
profile_service = ProfileService(llm_service)
news_service = NewsService()

app.mount("/static", StaticFiles(directory="../static"), name="static")

# Track messages per session for profile updates
message_counters = {}


@app.get("/")
async def root():
    """Redirect to chat."""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="0;url=/chat">
    </head>
    <body>
        <p>Redirigiendo a <a href="/chat">/chat</a>...</p>
    </body>
    </html>
    """)


@app.post("/api/register")
async def register(username: str = Form(...), password: str = Form(...)):
    result = db.create_user(username, password)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    # Create empty profile
    user_id = result["user_id"]
    db.create_user_profile(user_id, profile_service._get_empty_profile())
    
    return result


@app.post("/api/login")
async def login(username: str = Form(...), password: str = Form(...)):
    result = db.authenticate_user(username, password)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["error"])
    return result


@app.get("/api/profile/{user_id}")
async def get_profile(user_id: int):
    """Get user profile."""
    profile = db.get_user_profile(user_id)
    if not profile:
        profile = profile_service._get_empty_profile()
        db.create_user_profile(user_id, profile)
    return {"profile": profile}


@app.get("/api/system-prompt/{user_id}")
async def get_system_prompt(user_id: int):
    """Get current system prompt for UI display."""
    profile = db.get_user_profile(user_id) or profile_service._get_empty_profile()
    emotional_state = profile.get("emotional_state")
    system_prompt = profile_service.generate_system_prompt(profile, emotional_state)
    return {"system_prompt": system_prompt, "emotional_state": emotional_state}


@app.get("/api/sessions/{user_id}")
async def get_sessions(user_id: int):
    sessions = db.get_user_sessions(user_id)
    return {"sessions": sessions}


@app.post("/api/sessions")
async def create_session(user_id: int = Form(...), session_name: str = Form(...)):
    session_id = db.create_session(user_id, session_name)
    return {"success": True, "session_id": session_id}


@app.get("/api/messages/{session_id}")
async def get_messages(session_id: int):
    messages = db.get_session_messages(session_id)
    return {"messages": messages}


@app.post("/api/chat")
async def chat(session_id: int = Form(...), message: str = Form(...)):
    """
    Adaptive chat with profile extraction and emotional analysis.
    """
    # Get user_id from session
    user_id = db.get_user_id_from_session(session_id)
    if not user_id:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Store user message
    db.add_message(session_id, "user", message)
    
    # Initialize or increment message counter
    if session_id not in message_counters:
        message_counters[session_id] = 0
    message_counters[session_id] += 1
    count = message_counters[session_id]
    
    # Get conversation history
    history = db.get_session_messages(session_id)
    
    # Get or create profile
    profile = db.get_user_profile(user_id)
    if not profile:
        profile = profile_service._get_empty_profile()
        db.create_user_profile(user_id, profile)
    
    # Update profile AFTER EVERY user message (critical for demo - immediate adaptation)
    profile_updated = False
    if len(history) >= 2:  # Need at least 1 exchange to extract info
        print(f"🔄 Updating profile for user {user_id}...")
        recent_conv = [{"role": m["role"], "content": m["content"]} for m in history[-10:]]
        updated_profile = profile_service.extract_profile_from_conversation(recent_conv, profile)
        db.update_user_profile(user_id, updated_profile)
        profile = updated_profile
        profile_updated = True
        print("✅ Profile updated")
    
    # Emotional check every 7 messages
    if count % 7 == 0 and len(history) >= 10:
        print(f"🧠 Analyzing emotional state for user {user_id}...")
        recent_conv = [{"role": m["role"], "content": m["content"]} for m in history[-15:]]
        emotional_state = llm_service.analyze_emotional_state(recent_conv)
        if emotional_state and not emotional_state.get("insufficient_data"):
            db.update_emotional_state(user_id, emotional_state)
            profile["emotional_state"] = emotional_state
            print(f"✅ Emotional state: {emotional_state.get('recommended_mode', 'normal')}")
    
    # Generate adaptive system prompt
    emotional_state = profile.get("emotional_state")
    system_prompt = profile_service.generate_system_prompt(profile, emotional_state)
    
    # Format history for LLM (exclude last message as we'll add it separately)
    formatted_history = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in history[:-1]
    ]
    
    # Add current message
    formatted_history.append({"role": "user", "content": message})
    
    # Get response with custom system prompt
    response = llm_service.chat_with_custom_system(formatted_history, system_prompt)
    
    if response.get("error"):
        raise HTTPException(status_code=500, detail=response["content"])
    
    # Store assistant response
    db.add_message(session_id, "assistant", response["content"])
    
    return {
        "response": response["content"],
        "usage": response.get("usage", {}),
        "model": response.get("model", "unknown"),
        "profile_updated": profile_updated
    }


@app.delete("/api/sessions/{session_id}/{user_id}")
async def delete_session(session_id: int, user_id: int):
    success = db.delete_session(session_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"success": True}


@app.get("/chat", response_class=HTMLResponse)
async def chat_interface():
    with open("../static/chat.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Adaptive LLM Chat Agent",
        "features": {
            "profile_extraction": True,
            "emotional_analysis": True,
            "adaptive_identity": True,
            "news_integration": news_service.is_available()
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
