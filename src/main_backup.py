"""
FastAPI application for LLM Chat Agent with Persistent Memory.
"""

import os
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from database import Database
from llm_service import LLMService

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Agente Conversacional LLM",
    description="API REST para un agente conversacional con memoria persistente multi-usuario",
    version="1.0.0"
)

# Initialize database and LLM service
db = Database()
llm_service = LLMService()

# Mount static files for frontend
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def landing_page():
    """Landing page with API documentation."""
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Agente Conversacional LLM - API</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 2rem;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 3rem;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                color: #667eea;
                margin-bottom: 1rem;
                font-size: 2.5rem;
            }
            .subtitle {
                color: #666;
                margin-bottom: 2rem;
                font-size: 1.1rem;
            }
            .section {
                margin: 2rem 0;
            }
            h2 {
                color: #764ba2;
                margin-bottom: 1rem;
                border-bottom: 2px solid #667eea;
                padding-bottom: 0.5rem;
            }
            .endpoint {
                background: #f8f9fa;
                padding: 1.5rem;
                margin: 1rem 0;
                border-radius: 10px;
                border-left: 4px solid #667eea;
            }
            .method {
                display: inline-block;
                padding: 0.3rem 0.8rem;
                border-radius: 5px;
                font-weight: bold;
                margin-right: 1rem;
                font-size: 0.9rem;
            }
            .get { background: #28a745; color: white; }
            .post { background: #007bff; color: white; }
            .delete { background: #dc3545; color: white; }
            .endpoint-path {
                font-family: 'Courier New', monospace;
                color: #333;
                font-weight: bold;
            }
            .description {
                margin-top: 0.5rem;
                color: #666;
            }
            .params {
                margin-top: 1rem;
                background: white;
                padding: 1rem;
                border-radius: 5px;
            }
            .params h4 {
                color: #764ba2;
                margin-bottom: 0.5rem;
                font-size: 0.9rem;
            }
            code {
                background: #e9ecef;
                padding: 0.2rem 0.5rem;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
            .link-button {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 1rem 2rem;
                border-radius: 10px;
                text-decoration: none;
                margin-top: 1rem;
                transition: background 0.3s;
            }
            .link-button:hover {
                background: #764ba2;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Agente Conversacional LLM</h1>
            <p class="subtitle">API REST con Memoria Persistente Multi-Usuario</p>

            <div class="section">
                <h2>📖 Descripción</h2>
                <p>Esta API proporciona un agente conversacional inteligente que utiliza modelos de lenguaje de OpenAI
                   con capacidad de memoria persistente. Cada usuario puede mantener múltiples sesiones de conversación
                   que se guardan en una base de datos SQLite.</p>
            </div>

            <div class="section">
                <h2>🔌 Endpoints Disponibles</h2>

                <div class="endpoint">
                    <span class="method post">POST</span>
                    <span class="endpoint-path">/api/register</span>
                    <p class="description">Registrar un nuevo usuario en el sistema.</p>
                    <div class="params">
                        <h4>Parámetros (Form Data):</h4>
                        <p><code>username</code>: Nombre de usuario (string)</p>
                        <p><code>password</code>: Contraseña (string)</p>
                    </div>
                </div>

                <div class="endpoint">
                    <span class="method post">POST</span>
                    <span class="endpoint-path">/api/login</span>
                    <p class="description">Autenticar un usuario existente.</p>
                    <div class="params">
                        <h4>Parámetros (Form Data):</h4>
                        <p><code>username</code>: Nombre de usuario (string)</p>
                        <p><code>password</code>: Contraseña (string)</p>
                    </div>
                </div>

                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="endpoint-path">/api/sessions/{user_id}</span>
                    <p class="description">Obtener todas las sesiones de chat de un usuario.</p>
                </div>

                <div class="endpoint">
                    <span class="method post">POST</span>
                    <span class="endpoint-path">/api/sessions</span>
                    <p class="description">Crear una nueva sesión de chat.</p>
                    <div class="params">
                        <h4>Parámetros (Form Data):</h4>
                        <p><code>user_id</code>: ID del usuario (int)</p>
                        <p><code>session_name</code>: Nombre de la sesión (string)</p>
                    </div>
                </div>

                <div class="endpoint">
                    <span class="method get">GET</span>
                    <span class="endpoint-path">/api/messages/{session_id}</span>
                    <p class="description">Obtener todos los mensajes de una sesión específica.</p>
                </div>

                <div class="endpoint">
                    <span class="method post">POST</span>
                    <span class="endpoint-path">/api/chat</span>
                    <p class="description">Enviar un mensaje y obtener respuesta del agente LLM con memoria.</p>
                    <div class="params">
                        <h4>Parámetros (Form Data):</h4>
                        <p><code>session_id</code>: ID de la sesión (int)</p>
                        <p><code>message</code>: Mensaje del usuario (string)</p>
                    </div>
                </div>

                <div class="endpoint">
                    <span class="method delete">DELETE</span>
                    <span class="endpoint-path">/api/sessions/{session_id}/{user_id}</span>
                    <p class="description">Eliminar una sesión y todos sus mensajes.</p>
                </div>
            </div>

            <div class="section">
                <h2>🎯 Características</h2>
                <ul style="margin-left: 2rem; color: #666;">
                    <li>Autenticación de usuarios con contraseñas hasheadas</li>
                    <li>Múltiples sesiones de chat por usuario</li>
                    <li>Memoria persistente de conversaciones</li>
                    <li>Integración con OpenAI GPT-3.5-turbo</li>
                    <li>Base de datos SQLite</li>
                    <li>Interfaz web interactiva</li>
                </ul>
            </div>

            <div class="section">
                <a href="/chat" class="link-button">🚀 Ir a la Aplicación de Chat</a>
                <a href="/docs" class="link-button" style="margin-left: 1rem; background: #764ba2;">📚 Documentación Swagger</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/api/register")
async def register(username: str = Form(...), password: str = Form(...)) -> Dict[str, Any]:
    """Register a new user."""
    result = db.create_user(username, password)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@app.post("/api/login")
async def login(username: str = Form(...), password: str = Form(...)) -> Dict[str, Any]:
    """Authenticate a user."""
    result = db.authenticate_user(username, password)

    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["error"])

    return result


@app.get("/api/sessions/{user_id}")
async def get_sessions(user_id: int) -> Dict[str, Any]:
    """Get all sessions for a user."""
    sessions = db.get_user_sessions(user_id)
    return {"sessions": sessions}


@app.post("/api/sessions")
async def create_session(user_id: int = Form(...), session_name: str = Form(...)) -> Dict[str, Any]:
    """Create a new chat session."""
    session_id = db.create_session(user_id, session_name)
    return {"success": True, "session_id": session_id}


@app.get("/api/messages/{session_id}")
async def get_messages(session_id: int) -> Dict[str, Any]:
    """Get all messages for a session."""
    messages = db.get_session_messages(session_id)
    return {"messages": messages}


@app.post("/api/chat")
async def chat(session_id: int = Form(...), message: str = Form(...)) -> Dict[str, Any]:
    """Send a message and get LLM response with memory."""
    # Store user message
    db.add_message(session_id, "user", message)

    # Get conversation history
    history = db.get_session_messages(session_id)

    # Format history for LLM
    formatted_history = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in history[:-1]  # Exclude the message we just added
    ]

    # Get LLM response
    response = llm_service.chat_with_memory(message, formatted_history)

    if response.get("error"):
        raise HTTPException(status_code=500, detail=response["content"])

    # Store assistant response
    db.add_message(session_id, "assistant", response["content"])

    return {
        "response": response["content"],
        "usage": response.get("usage", {}),
        "model": response.get("model", "unknown")
    }


@app.delete("/api/sessions/{session_id}/{user_id}")
async def delete_session(session_id: int, user_id: int) -> Dict[str, Any]:
    """Delete a session and all its messages."""
    success = db.delete_session(session_id, user_id)

    if not success:
        raise HTTPException(status_code=404, detail="Session not found or unauthorized")

    return {"success": True}


@app.get("/chat", response_class=HTMLResponse)
async def chat_interface():
    """Serve the chat interface."""
    with open("static/chat.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "LLM Chat Agent"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
