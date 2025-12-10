# 🏗️ Arquitectura del Sistema

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO                                  │
│                            │                                     │
│                            ▼                                     │
│  ┌──────────────────────────────────────────────────────┐       │
│  │              NAVEGADOR WEB                            │       │
│  │  ┌────────────────────────────────────────────────┐  │       │
│  │  │     FRONTEND (HTML/CSS/JavaScript)             │  │       │
│  │  │  • Interfaz de Login/Registro                  │  │       │
│  │  │  • Chat Interface                               │  │       │
│  │  │  • Gestión de Sesiones                         │  │       │
│  │  └────────────────────────────────────────────────┘  │       │
│  └──────────────────┬───────────────────────────────────┘       │
│                     │                                            │
│                     │ HTTP/REST API                              │
│                     ▼                                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND - FASTAPI                             │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  CAPA DE ENDPOINTS (main.py)                              │  │
│  │                                                            │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │  │
│  │  │    Auth     │  │  Sessions   │  │    Chat     │      │  │
│  │  │  Endpoints  │  │  Endpoints  │  │  Endpoints  │      │  │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘      │  │
│  └─────────┼────────────────┼────────────────┼──────────────┘  │
│            │                │                │                  │
│            ▼                ▼                ▼                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           CAPA DE SERVICIOS                               │  │
│  │  ┌──────────────────┐        ┌──────────────────┐        │  │
│  │  │   database.py    │        │  llm_service.py  │        │  │
│  │  │                  │        │                  │        │  │
│  │  │ • create_user    │        │ • chat()         │        │  │
│  │  │ • authenticate   │        │ • chat_with_     │        │  │
│  │  │ • create_session │        │   memory()       │        │  │
│  │  │ • add_message    │        │                  │        │  │
│  │  │ • get_messages   │        │                  │        │  │
│  │  └────────┬─────────┘        └────────┬─────────┘        │  │
│  └───────────┼──────────────────────────┼───────────────────┘  │
│              │                          │                       │
│              ▼                          ▼                       │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┐        ┌──────────────────────────────┐
│   BASE DE DATOS      │        │   SERVICIOS EXTERNOS          │
│                      │        │                               │
│  ┌────────────────┐  │        │  ┌────────────────────────┐  │
│  │    SQLite      │  │        │  │      OpenAI API        │  │
│  │                │  │        │  │                        │  │
│  │ • users        │  │        │  │  Model:                │  │
│  │ • sessions     │  │        │  │  gpt-3.5-turbo        │  │
│  │ • messages     │  │        │  │                        │  │
│  └────────────────┘  │        │  └────────────────────────┘  │
│                      │        │                               │
└──────────────────────┘        └──────────────────────────────┘
```

---

## Flujo de Datos - Conversación con Memoria

```
┌──────────┐
│ Usuario  │
│ escribe  │
│ mensaje  │
└────┬─────┘
     │
     ▼
┌─────────────────────────────────────────┐
│  1. Frontend envía POST /api/chat       │
│     {session_id: 1, message: "..."}     │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  2. Backend (main.py)                   │
│     • Guarda mensaje del usuario en BD  │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  3. database.py                         │
│     • add_message(session_id, "user",   │
│       message)                          │
│     • get_session_messages(session_id)  │
│       → Retorna TODOS los mensajes      │
└────────────────┬────────────────────────┘
                 │
                 │ [Historial completo]
                 ▼
┌─────────────────────────────────────────┐
│  4. llm_service.py                      │
│     • Recibe historial completo         │
│     • Añade mensaje actual              │
│     • Prepara prompt con contexto       │
└────────────────┬────────────────────────┘
                 │
                 │ [Prompt + Historial]
                 ▼
┌─────────────────────────────────────────┐
│  5. OpenAI API                          │
│     • Procesa contexto completo         │
│     • Genera respuesta coherente        │
│     • Retorna respuesta                 │
└────────────────┬────────────────────────┘
                 │
                 │ [Respuesta del LLM]
                 ▼
┌─────────────────────────────────────────┐
│  6. Backend guarda respuesta            │
│     • add_message(session_id,           │
│       "assistant", response)            │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  7. Retorna al Frontend                 │
│     {response: "...", usage: {...}}     │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  8. Frontend muestra respuesta          │
│     • Añade burbuja del asistente       │
│     • Usuario puede seguir conversando  │
└─────────────────────────────────────────┘
```

---

## Tecnologías por Capa

### Frontend
- **HTML5**: Estructura de la aplicación
- **CSS3**: Estilos modernos con gradientes y animaciones
- **JavaScript (Vanilla)**: Lógica de interacción y llamadas API
- **Fetch API**: Comunicación con el backend

### Backend
- **FastAPI 0.115+**: Framework web moderno y rápido
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **python-dotenv**: Gestión de variables de entorno
- **python-multipart**: Procesamiento de formularios

### Base de Datos
- **SQLite3**: Base de datos relacional ligera
- **sqlite3 (Python)**: Driver nativo de Python

### Servicios Externos
- **OpenAI API**: Modelos de lenguaje GPT
- **gpt-3.5-turbo**: Modelo seleccionado

### DevOps
- **Docker**: Containerización
- **uv**: Gestión de dependencias
- **Git**: Control de versiones

---

## Esquema de Base de Datos

```sql
┌─────────────────────┐
│       users         │
├─────────────────────┤
│ id (PK)             │
│ username (UNIQUE)   │
│ password_hash       │
│ created_at          │
└──────────┬──────────┘
           │
           │ 1:N
           │
┌──────────▼──────────┐
│     sessions        │
├─────────────────────┤
│ id (PK)             │
│ user_id (FK)        │
│ session_name        │
│ created_at          │
│ updated_at          │
└──────────┬──────────┘
           │
           │ 1:N
           │
┌──────────▼──────────┐
│     messages        │
├─────────────────────┤
│ id (PK)             │
│ session_id (FK)     │
│ role                │ ← "user" | "assistant"
│ content             │
│ created_at          │
└─────────────────────┘
```

---

## Endpoints API

### Autenticación
- `POST /api/register` - Registrar usuario
- `POST /api/login` - Autenticar usuario

### Sesiones
- `GET /api/sessions/{user_id}` - Listar sesiones
- `POST /api/sessions` - Crear sesión
- `DELETE /api/sessions/{session_id}/{user_id}` - Eliminar sesión

### Chat
- `GET /api/messages/{session_id}` - Obtener mensajes
- `POST /api/chat` - Enviar mensaje y recibir respuesta

### UI
- `GET /` - Landing page con documentación
- `GET /chat` - Interfaz de chat
- `GET /docs` - Swagger UI

### Utilidades
- `GET /health` - Health check

---

## Características Técnicas Destacadas

### 🧠 Memoria Persistente
- Cada mensaje se almacena en la BD
- El historial completo se envía al LLM en cada petición
- El modelo puede referenciar conversaciones de días/semanas atrás
- Límite configurable de mensajes históricos (por defecto: 10)

### 👥 Multi-Usuario
- Sistema de autenticación con hashing SHA-256
- Sesiones aisladas por usuario
- Cada usuario puede tener múltiples conversaciones

### 🔒 Seguridad
- Passwords hasheados (SHA-256)
- API Key en variables de entorno
- Validación de propiedad de sesiones
- .env excluido del repositorio

### 📊 Escalabilidad
- Arquitectura modular y desacoplada
- Fácil migración de SQLite a PostgreSQL/MySQL
- Stateless API (escalable horizontalmente)
- Docker para despliegue en cualquier plataforma

### 🚀 Performance
- Respuestas asíncronas con FastAPI
- Frontend SPA sin recargas de página
- Índices en claves foráneas de la BD
- Health check para monitoreo

---

## Decisiones de Diseño

### ¿Por qué SQLite?
- Cumple requisitos del ejercicio
- Sin infraestructura adicional
- Perfecto para demos y desarrollo
- Fácil migración a BD en producción

### ¿Por qué GPT-3.5-turbo?
- Más rápido que GPT-4
- Más económico
- Suficiente para conversaciones naturales
- Mejor experiencia en demos (respuestas rápidas)

### ¿Por qué FastAPI?
- Documentación automática (Swagger)
- Tipado moderno
- Alto rendimiento
- Fácil de aprender y usar

### ¿Por qué frontend vanilla?
- Sin dependencias adicionales
- Más ligero y rápido
- Demuestra conocimientos fundamentales
- Requisito del ejercicio (simple)

---

## Posibles Mejoras Futuras

### Backend
- [ ] Implementar JWT para autenticación
- [ ] Rate limiting por usuario
- [ ] Caché de respuestas frecuentes
- [ ] WebSockets para streaming de respuestas
- [ ] Migrar a PostgreSQL

### Frontend
- [ ] PWA (Progressive Web App)
- [ ] Markdown rendering en mensajes
- [ ] Exportar conversaciones a PDF
- [ ] Tema oscuro/claro
- [ ] Búsqueda en historial

### LLM
- [ ] Soporte para GPT-4
- [ ] Streaming de respuestas
- [ ] Ajuste de temperatura por sesión
- [ ] System prompts personalizables
- [ ] Múltiples modelos (Anthropic, Google)

### DevOps
- [ ] CI/CD con GitHub Actions
- [ ] Despliegue en cloud (AWS/GCP/Azure)
- [ ] Monitoring con Prometheus
- [ ] Logs estructurados
- [ ] Tests unitarios y de integración

---

**Fecha**: Diciembre 2025
**Proyecto**: Despliegue Modelo LLM - Data Engineering
