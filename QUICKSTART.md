# Quick Start Guide

## Sistema Adaptativo en Tiempo Real

Este agente LLM extrae el perfil del usuario **TRAS CADA MENSAJE** y adapta su personalidad instantáneamente. Un solo mensaje puede ser suficiente para que el bot cambie completamente su tono y comportamiento.

---

## Opción 1: Ejecución Local (Desarrollo)

### 1. Configurar entorno
```bash
# Clonar el repositorio
git clone <url-del-repo>
cd 2025-12-09_despliegue

# Copiar y configurar variables de entorno
cp .env.example .env
# Editar .env y añadir tu OPENAI_API_KEY
```

### 2. Instalar dependencias
```bash
# Con uv (recomendado)
uv sync

# O con pip
pip install fastapi uvicorn openai python-dotenv python-multipart
```

### 3. Ejecutar aplicación
```bash
cd src
uvicorn main:app --reload
```

### 4. Acceder
- Frontend: http://localhost:8000/chat
- API Docs: http://localhost:8000/docs
- Landing: http://localhost:8000/

---

## 🐳 Opción 2: Docker (Recomendado para Demo)

### 1. Configurar entorno
```bash
cp .env.example .env
# Editar .env y añadir tu OPENAI_API_KEY
```

### 2. Construir y ejecutar
```bash
# Construir imagen
docker build -t llm-chat-agent .

# Ejecutar contenedor
docker run -d --name chat-agent -p 8000:8000 --env-file .env llm-chat-agent

# Verificar
docker ps
```

### 3. Acceder
http://localhost:8000/chat

---

##  Primera Prueba

### 1. Registrarse
- Abre http://localhost:8000/chat
- Click en "Crear Cuenta"
- Usuario: `demo`
- Password: `demo123`

### 2. Probar la memoria
```
Tú: Hola, me llamo Ana y me gusta el café
Bot: [responde]

Tú: ¿Qué te dije que me gusta?
Bot: Dijiste que te gusta el café

[Crear nueva sesión "Tema 2"]
Tú: ¿Qué tal el clima?
Bot: [responde sobre clima]

[Volver a la primera sesión]
Tú: ¿Recuerdas mi nombre?
Bot: Sí, te llamas Ana
```

---

##  Comandos Útiles

### Ver la base de datos
```bash
sqlite3 chat_agent.db
sqlite> .tables
sqlite> SELECT * FROM users;
sqlite> SELECT * FROM messages;
sqlite> .quit
```

### Logs del servidor
```bash
# Si usas Docker
docker logs -f chat-agent

# Si usas local
# Los logs aparecen en la terminal donde ejecutaste uvicorn
```

### Detener la aplicación
```bash
# Docker
docker stop chat-agent
docker rm chat-agent

# Local
# Ctrl+C en la terminal
```

---

##  Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/register` | Crear usuario |
| POST | `/api/login` | Autenticar |
| GET | `/api/sessions/{user_id}` | Listar sesiones |
| POST | `/api/chat` | Enviar mensaje |
| GET | `/docs` | Swagger UI |

---

## ❓ Troubleshooting

### Error: "OPENAI_API_KEY not provided"
→ Verifica que el archivo `.env` existe y tiene tu API key

### Error: "Port 8000 already in use"
```bash
# Encontrar y matar el proceso
lsof -i :8000
kill -9 <PID>
```

### El chat no responde
→ Verifica que tienes créditos en tu cuenta de OpenAI
→ Revisa los logs para ver errores

### No se guarda la base de datos en Docker
→ Usa volúmenes: `-v $(pwd)/data:/app/data`

---

##  Para la Presentación

1. **Antes de empezar** (5 min antes):
   ```bash
   docker build -t llm-chat-agent .
   docker run -d --name chat-agent -p 8000:8000 --env-file .env llm-chat-agent
   ```

2. **Verificar**:
   ```bash
   curl http://localhost:8000/health
   ```

3. **Abrir pestañas**:
   - http://localhost:8000/chat
   - http://localhost:8000/docs
   - docs/arquitectura.md

4. **Tener preparado**:
   - Usuario de prueba registrado
   - Al menos una conversación de ejemplo

---

**¿Necesitas ayuda?** Revisa el README.md completo o la documentación en `/docs`
