# 🤖 Agente Conversacional LLM Adaptativo con IA de Personalidad

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=fff" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009485.svg?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/OpenAI-74aa9c?logo=openai&logoColor=white" alt="OpenAI">
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff" alt="Docker">
  <img src="https://img.shields.io/badge/SQLite-%2307405e.svg?logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/GPT--5.1-412991?logo=openai&logoColor=white" alt="GPT-5.1">
</p>

## 📖 Descripción

API REST desarrollada con FastAPI que proporciona un **agente conversacional con IA adaptativa** que aprende sobre cada usuario y ajusta dinámicamente su personalidad, tono y conocimientos para convertirse en el **compañero perfecto** de cada persona. Utiliza **GPT-5.1** de OpenAI con sistema de perfiles inteligentes que extraen automáticamente información relevante de las conversaciones.

### ✨ Características Principales

####  Sistema Adaptativo Inteligente
-  **Extracción Automática de Perfil**: El LLM analiza conversaciones y extrae información permanente del usuario (edad, intereses, profesión, etc.)
-  **Adaptación de Personalidad**: El bot se convierte en "igual" del usuario (niño → amigo niño, adulto → colega adulto)
-  **Análisis Emocional**: GPT actúa como psicólogo experto detectando depresión, ansiedad, soledad y ajustando el tono
-  **System Prompt Dinámico**: Se regenera automáticamente cada mensaje basándose en el perfil actualizado
-  **Guardarraíles de Seguridad**: No copia comportamientos autodestructivos, ofrece apoyo emocional cuando detecta angustia

####  Gestión de Datos
-  **Memoria Persistente**: El agente recuerda todas las conversaciones previas de cada usuario
-  **Multi-Usuario**: Sistema de autenticación con perfiles independientes
-  **Múltiples Sesiones**: Cada usuario puede tener varias conversaciones separadas
-  **Perfiles JSON**: Almacenamiento flexible de perfiles complejos (político, religión, hechos importantes)

####  Interfaz y API
-  **Visualización de Perfil en Tiempo Real**: El frontend muestra el perfil extraído y se actualiza automáticamente
-  **Visor de System Prompt**: Los usuarios pueden ver el prompt personalizado generado para ellos
-  **API REST Completa**: Endpoints documentados con Swagger/OpenAPI
-  **Frontend Interactivo**: Interfaz web moderna en HTML/CSS sin frameworks
-  **Dockerizado**: Imagen lista para desplegar en cualquier entorno

---

##  Arquitectura

```
┌─────────────────────────────────┐
│   Frontend (HTML/CSS/JS)        │
│  - Chat Interface               │
│  - Profile Viewer (Real-time)   │
│  - System Prompt Modal          │
└───────────┬─────────────────────┘
            │ HTTP/REST
            ▼
┌───────────────────────────────────────────┐
│         FastAPI Backend                   │
│                                           │
│  ┌─────────────────────────────────────┐  │
│  │        API Endpoints                │  │
│  │  /chat, /profile, /system-prompt   │  │
│  └────────┬────────────────────────────┘  │
│           │                               │
│  ┌────────▼────────┐   ┌───────────────┐ │
│  │  Profile Service│   │  News Service │ │
│  │ - Extract Info  │   │   (NewsAPI)   │ │
│  │ - Generate Sys  │   └───────────────┘ │
│  │   Prompt        │                      │
│  │ - Adapt Identity│                      │
│  └────────┬────────┘                      │
│           │                               │
│  ┌────────▼────────┐   ┌───────────────┐ │
│  │   LLM Service   │   │   Database    │ │
│  │ - Chat Compl.   │   │   Module      │ │
│  │ - Emotional Anl │   │ - Users       │ │
│  │ - Psychologist  │   │ - Sessions    │ │
│  └────────┬────────┘   │ - Messages    │ │
│           │            │ - Profiles    │ │
│           │            └───────┬───────┘ │
└───────────┼────────────────────┼─────────┘
            │                    │
     ┌──────▼──────┐      ┌─────▼─────┐
     │   OpenAI    │      │  SQLite   │
     │  GPT-5.1    │      │ Database  │
     └─────────────┘      └───────────┘
```

### Componentes Principales

- **Frontend Adaptativo**: Interfaz que visualiza el perfil del usuario en tiempo real y permite ver el system prompt generado
- **Profile Service** : Motor de extracción inteligente que analiza conversaciones y genera system prompts personalizados
- **LLM Service Enhanced**: Gestiona chat con prompts personalizados, análisis emocional como psicólogo experto
- **News Service** : Integración con NewsAPI para saludos proactivos basados en intereses del usuario
- **Database Module**: Gestión de usuarios, sesiones, mensajes y perfiles JSON con estado emocional
- **OpenAI GPT-5.1**: Modelo con razonamiento adaptativo para conversaciones naturales y análisis psicológico

---

##  Estructura del Proyecto

```
.
├── src/
│   ├── main.py              # Aplicación FastAPI con sistema adaptativo
│   ├── database.py          # Gestión de BD (users, sessions, messages, profiles)
│   ├── llm_service.py       # OpenAI GPT-5.1 + análisis emocional
│   ├── profile_service.py   #  Extracción de perfil + generación system prompt
│   └── news_service.py      #  Integración NewsAPI
├── static/
│   └── chat.html            # Frontend con visualización de perfil
├── docs/                    #  Documentación adicional
│   ├── QUICKSTART.md
│   └── presentacion.md
├── .env                     # Variables de entorno (NO subir a Git)
├── .env.example             # Incluye OPENAI_API_KEY + NEWS_API_KEY
├── Dockerfile               # Configuración de Docker multi-stage
├── .dockerignore            # Archivos excluidos del build
├── pyproject.toml           # Dependencias (FastAPI, OpenAI, requests)
├── uv.lock                  # Lock file de dependencias
└── README.md                # Este archivo
```

---

##  Instalación y Uso

### Requisitos Previos

- Python 3.11 o superior
- OpenAI API Key con acceso a GPT-5.1 ([Obtener aquí](https://platform.openai.com/api-keys))
- NewsAPI Key (opcional, para saludos proactivos) ([Obtener gratis aquí](https://newsapi.org/register))
- Docker (opcional, para despliegue containerizado)

### Opción 1: Instalación Local

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd 2025-12-09_despliegue
```

2. **Configurar variables de entorno**
```bash
cp .env.example .env
# Edita .env y añade:
# - OPENAI_API_KEY (requerido)
# - OPENAI_MODEL=gpt-5.1 (o el modelo que prefieras)
# - NEWS_API_KEY (opcional)
```

3. **Instalar dependencias** (con uv - recomendado)
```bash
uv sync
```

O con pip:
```bash
pip install fastapi uvicorn openai python-dotenv python-multipart requests
```

4. **Ejecutar la aplicación**
```bash
uvicorn src.main:app --reload
```

5. **Acceder a la aplicación**
- Frontend: http://localhost:8000/chat
- API Docs: http://localhost:8000/docs
- Landing Page: http://localhost:8000/

### Opción 2: Docker

1. **Crear archivo .env**
```bash
cp .env.example .env
# Edita .env y añade tu OPENAI_API_KEY
```

2. **Construir la imagen**
```bash
docker build -t llm-chat-agent .
```

3. **Ejecutar el contenedor**
```bash
docker run -d \
  --name chat-agent \
  -p 8000:8000 \
  --env-file .env \
  llm-chat-agent
```

4. **Acceder a la aplicación**
- http://localhost:8000/chat

### Opción 3: Descargar desde DockerHub

```bash
# Descargar la imagen
docker pull <tu-usuario>/llm-chat-agent:latest

# Ejecutar con tu API key
docker run -d \
  --name chat-agent \
  -p 8000:8000 \
  -e OPENAI_API_KEY=tu_api_key_aqui \
  <tu-usuario>/llm-chat-agent:latest
```

---

##  Sistema Adaptativo en Detalle

### Cómo Funciona la Adaptación

El sistema utiliza un flujo inteligente de 3 etapas:

1. **Extracción de Perfil** (tras CADA mensaje del usuario)
   - GPT-5.1 analiza los últimos mensajes buscando información **permanente**
   - Extrae: edad, género, intereses reales, profesión (SOLO si se menciona explícitamente)
   - **Reglas CRÍTICAS**:
     * Distingue entre "tiene" vs "quiere", evita eventos temporales
     * NO extrae política/religión a menos que se mencione EXPLÍCITAMENTE
     * NO duplica ocupación en important_facts si ya está en profession
     * Limpieza automática de entradas vagas ("Trabaja", "Trabaja como trabajador")
   - Se fusiona con el perfil existente sin perder información previa
   - **Actualización instantánea**: Si el usuario dice "soy médica", el perfil se actualiza inmediatamente

2. **Análisis Emocional** (cada 7 mensajes)
   - GPT-5.1 actúa como **psicólogo clínico experto**
   - Detecta: depresión, ansiedad, soledad, necesidad de apoyo
   - Recomienda modo: normal/friendly/empathetic/supportive/crisis
   - Activa guardarraíles de seguridad si detecta riesgo

3. **Generación de System Prompt** (cada mensaje)
   - Crea identidad adaptada (niño → amigo niño, adulto → colega con experiencia similar)
   - Ajusta tono y lenguaje según edad y contexto
   - Incluye expertise en los intereses del usuario
   - Añade instrucciones de comportamiento personalizadas
   - Activa modo de apoyo emocional si es necesario

### Ejemplo de Adaptación

**Usuario niño (10 años) que juega fútbol-sala:**
```
IDENTIDAD: Eres un amigo de tu edad al que le encanta Fútbol-sala.
TONO: Usa lenguaje SIMPLE y AMIGABLE, emojis 
EXPERTISE: Habla con conocimiento sobre Fútbol-sala, Minecraft
```

**Usuario adulto profesional:**
```
IDENTIDAD: Eres alguien como tú, que trabaja en Ingeniería de Datos.
TONO: Natural, equilibrado, profesional pero cercano
EXPERTISE: Conocimientos técnicos relevantes a su campo
```

---

##  API Endpoints

### Autenticación

#### `POST /api/register`
Registrar un nuevo usuario.

**Body (form-data):**
- `username`: string
- `password`: string

**Response:**
```json
{
  "success": true,
  "user_id": 1,
  "username": "usuario"
}
```

#### `POST /api/login`
Autenticar usuario existente.

**Body (form-data):**
- `username`: string
- `password`: string

**Response:**
```json
{
  "success": true,
  "user_id": 1,
  "username": "usuario"
}
```

### Sesiones

#### `GET /api/sessions/{user_id}`
Obtener todas las sesiones de un usuario.

**Response:**
```json
{
  "sessions": [
    {
      "id": 1,
      "session_name": "Mi conversación",
      "created_at": "2025-12-09 10:00:00",
      "updated_at": "2025-12-09 11:30:00"
    }
  ]
}
```

#### `POST /api/sessions`
Crear una nueva sesión.

**Body (form-data):**
- `user_id`: int
- `session_name`: string

**Response:**
```json
{
  "success": true,
  "session_id": 2
}
```

#### `DELETE /api/sessions/{session_id}/{user_id}`
Eliminar una sesión y todos sus mensajes.

### Chat

#### `GET /api/messages/{session_id}`
Obtener todos los mensajes de una sesión.

**Response:**
```json
{
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "Hola, ¿cómo estás?",
      "created_at": "2025-12-09 10:00:00"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "¡Hola! Estoy bien, gracias por preguntar.",
      "created_at": "2025-12-09 10:00:05"
    }
  ]
}
```

#### `POST /api/chat`
Enviar mensaje y obtener respuesta del LLM con system prompt adaptativo.

**Body (form-data):**
- `session_id`: int
- `message`: string

**Response:**
```json
{
  "response": "Esta es la respuesta del agente...",
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 75,
    "total_tokens": 225
  },
  "model": "gpt-5.1",
  "profile_updated": false
}
```

### Perfil y Adaptación 

#### `GET /api/profile/{user_id}`
Obtener el perfil completo del usuario.

**Response:**
```json
{
  "profile": {
    "age_range": "~10 años (niño)",
    "gender": null,
    "profession": null,
    "education": null,
    "interests": ["Fútbol-sala", "Minecraft"],
    "political_stance": {
      "spectrum": null,
      "intensity": null,
      "approach": null
    },
    "religion": {
      "faith": null,
      "intensity": null,
      "approach": null
    },
    "important_facts": ["Juega en el equipo del cole"],
    "sensitive_topics": [],
    "personality_traits": ["Entusiasta", "Juguetón"],
    "needs": ["Conversación amigable y divertida"],
    "tone_preference": "simple y entusiasta",
    "emotional_state": {
      "recommended_mode": "normal",
      "support_needed": "none"
    }
  }
}
```

#### `GET /api/system-prompt/{user_id}`
Obtener el system prompt generado dinámicamente para el usuario.

**Response:**
```json
{
  "system_prompt": "IDENTIDAD Y ROL:\nEres un amigo de tu edad al que le encanta Fútbol-sala...",
  "emotional_state": {
    "recommended_mode": "normal",
    "support_needed": "none"
  }
}
```

### Utilidades

#### `GET /health`
Health check del servicio.

**Response:**
```json
{
  "status": "healthy",
  "service": "LLM Chat Agent"
}
```

---

##  Base de Datos

### Esquema SQLite

#### Tabla: `users`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER PRIMARY KEY | ID único del usuario |
| username | TEXT UNIQUE | Nombre de usuario |
| password_hash | TEXT | Hash SHA-256 de la contraseña |
| created_at | TIMESTAMP | Fecha de creación |

#### Tabla: `sessions`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER PRIMARY KEY | ID único de la sesión |
| user_id | INTEGER FK | ID del usuario propietario |
| session_name | TEXT | Nombre de la sesión |
| created_at | TIMESTAMP | Fecha de creación |
| updated_at | TIMESTAMP | Última actualización |

#### Tabla: `messages`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER PRIMARY KEY | ID único del mensaje |
| session_id | INTEGER FK | ID de la sesión |
| role | TEXT | "user" o "assistant" |
| content | TEXT | Contenido del mensaje |
| created_at | TIMESTAMP | Fecha de creación |

#### Tabla: `user_profiles` 
| Campo | Tipo | Descripción |
|-------|------|-------------|
| user_id | INTEGER PRIMARY KEY FK | ID del usuario |
| profile_json | TEXT | Perfil completo en JSON (edad, intereses, etc.) |
| emotional_state_json | TEXT | Estado emocional analizado en JSON |
| last_updated | TIMESTAMP | Última actualización del perfil |
| last_emotional_check | TIMESTAMP | Último análisis emocional |

---

##  Tecnologías Utilizadas

- **Backend**: FastAPI 0.115+
- **LLM**: OpenAI GPT-5.1 (modelo con razonamiento adaptativo)
- **APIs Externas**: NewsAPI (para saludos proactivos)
- **Base de Datos**: SQLite3 con almacenamiento JSON
- **Frontend**: HTML5 + CSS3 + JavaScript (Vanilla) con visualización dinámica
- **Servidor**: Uvicorn ASGI
- **Containerización**: Docker multi-stage build
- **Gestión de dependencias**: uv (ultrafast package manager)

---

##  Demostración para Presentación

### Escenario de Demo (8 minutos)

1. **Intro: Arquitectura Adaptativa** (1 min)
   - Mostrar diagrama destacando Profile Service y análisis emocional
   - Explicar flujo: extracción tras CADA mensaje (actualización instantánea), análisis emocional cada 7

2. **Dockerización** (1 min)
   - Mostrar Dockerfile multi-stage
   - Ejecutar contenedor
   - Verificar acceso en localhost:8000/chat

3. ** Demo Adaptación de Personalidad** (5 min) - **MOMENTO WOW**
   - Registrar como "Niño de 10 años"
   - Conversación inicial:
     * "Hola, tengo 10 años y me encanta el fútbol-sala. Juego en mi equipo del cole"
     * **INMEDIATAMENTE** después del primer mensaje: Indicador verde en "Tu Perfil Adaptativo"
     * Hacer clic en "Tu Perfil Adaptativo" en sidebar
     * **Mostrar perfil extraído AUTOMÁTICAMENTE EN TIEMPO REAL**: edad ~10 años, interés en fútbol-sala
     * Hacer clic en " Ver System Prompt"
     * **Mostrar cómo el bot se convirtió en "amigo de su edad" INSTANTÁNEAMENTE**
   - Continuar conversación:
     * El bot ahora habla como niño, pregunta sobre fútbol
     * **Demostrar que la personalidad cambió dinámicamente**
   - Crear nueva sesión como adulto profesional:
     * "Soy ingeniero de datos, trabajo con Python y Spark"
     * **ACTUALIZACIÓN INSTANTÁNEA** del perfil tras el mensaje
     * Observar cómo cambia completamente el tono
     * Ver perfil actualizado (profesión, tono profesional) EN TIEMPO REAL

4. **Endpoints y BD** (1 min)
   - Swagger: mostrar `/api/profile/{user_id}` y `/api/system-prompt/{user_id}`
   - SQLite: mostrar tabla `user_profiles` con JSON
   - Explicar persistencia del perfil

### Scripts de Ejemplo con Adaptación

**Demo 1: Niño adaptativo**
```
[Mensaje 1]
Usuario: Hola, tengo 10 años y me gusta Minecraft
Bot: ¡Hola!  ¡Qué guay que te guste Minecraft! Es super divertido...
[ACTUALIZACIÓN INSTANTÁNEA: Indicador verde parpadeante en "Tu Perfil Adaptativo"]

[Ver perfil extraído INMEDIATAMENTE]
{
  "age_range": "~10 años (niño)",
  "interests": ["Minecraft"],
  "tone_preference": "simple y entusiasta"
}

[Ver system prompt generado]
"IDENTIDAD Y ROL:
Eres un amigo de tu edad al que le encanta Minecraft.
TONO: Usa lenguaje SIMPLE y AMIGABLE, emojis MUY OCASIONALMENTE"

[Mensaje 2]
Usuario: También juego fútbol-sala en el cole
Bot: ¡Genial!  Yo también me encanta el fútbol-sala...
[PERFIL ACTUALIZADO nuevamente con interés añadido]
```

**Demo 2: Profesional adaptativo**
```
[Mensaje 1]
Usuario: Soy ingeniera de datos, trabajo con Python y Spark
Bot: Interesante. ¿Qué tipo de pipelines estás implementando con Spark?
[ACTUALIZACIÓN INSTANTÁNEA DEL PERFIL]

[Perfil actualizado inmediatamente]
{
  "age_range": "adulto",
  "gender": "femenino",  # Detectado por "ingeniera"
  "profession": "Ingeniera de datos",
  "interests": ["Python", "Spark"],
  "tone_preference": "profesional pero cercano"
}

[System prompt cambia a]
"IDENTIDAD: Eres alguien como tú, que trabaja en Ingeniería de Datos.
TONO: Natural, equilibrado, profesional pero cercano
EXPERTISE: Habla con conocimiento sobre Python, Spark"
```

---

##  Extras Implementados

### Requisitos Base
-  **Sin Pydantic**: Validación manual con diccionarios
-  **Base de Datos**: SQLite con esquema completo + tabla de perfiles
-  **Dockerización**: Imagen multi-stage lista para DockerHub
-  **Frontend**: HTML/CSS/JS sin frameworks (con visualización avanzada)
-  **Documentación**: README completo + Swagger + QUICKSTART

### Features Avanzadas 
-  **Sistema de IA Adaptativa**: Extracción automática de perfiles usando GPT-5.1
-  **Análisis Emocional Inteligente**: LLM actúa como psicólogo clínico experto
-  **System Prompts Dinámicos**: Regenerados automáticamente por mensaje
-  **Adaptación de Personalidad**: Bot se convierte en "igual" del usuario
-  **Guardarraíles de Seguridad**: Detección de riesgo emocional y apoyo
-  **Visualización en Tiempo Real**: Frontend muestra perfil y permite ver system prompt
-  **Integración NewsAPI**: Para saludos proactivos (preparado)
-  **Perfiles Complejos**: Incluye político, religión, hechos importantes, temas sensibles

---

##  Seguridad

- Contraseñas hasheadas con SHA-256
- Variables de entorno para API keys
- .env excluido de Git
- Validación de sesiones por usuario

---

##  Soporte

Para dudas o problemas, consultar la documentación de Swagger en `/docs` cuando la aplicación esté corriendo.

---

##  Licencia

Este proyecto fue desarrollado como parte de un ejercicio académico de Data Engineering.

---

**Desarrollado con ❤ usando FastAPI y OpenAI**
