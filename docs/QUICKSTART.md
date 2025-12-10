# 🚀 QUICKSTART: Agente LLM Adaptativo

Guía rápida para poner en marcha el sistema y entender cómo funciona la adaptación de personalidad.

---

## ⚡ Inicio Rápido (3 minutos)

### 1. Configuración Inicial

```bash
# Clonar y entrar al proyecto
cd 2025-12-09_despliegue

# Configurar variables de entorno
cp .env.example .env
# Editar .env y añadir:
# OPENAI_API_KEY=tu_clave_aqui
# OPENAI_MODEL=gpt-5.1
# NEWS_API_KEY=tu_clave_newsapi (opcional)
```

### 2. Instalación

**Opción A: Con uv (recomendado)**
```bash
uv sync
cd src
uvicorn main:app --reload
```

**Opción B: Con Docker**
```bash
docker build -t llm-chat-agent .
docker run -d -p 8000:8000 --env-file .env llm-chat-agent
```

### 3. Acceder

Abrir en navegador: **http://localhost:8000/chat**

---

## 🎭 Cómo Funciona la Adaptación

El sistema tiene 3 mecanismos automáticos:

### 📊 Extracción de Perfil (cada 3 mensajes)

Cuando envías el **mensaje 3, 6, 9, 12...** el sistema:

1. GPT-5.1 analiza los últimos mensajes
2. Extrae información **permanente** (edad, intereses, profesión)
3. **NO** incluye eventos temporales (regalos, compras recientes)
4. Actualiza el perfil del usuario en la base de datos
5. Aparece un **indicador verde parpadeante** en "Tu Perfil Adaptativo"

**Qué se extrae:**
- ✅ Edad aproximada
- ✅ Intereses reales (pasiones que practica)
- ✅ Profesión/estudios
- ✅ Hechos importantes permanentes
- ❌ NO: regalos recientes, eventos puntuales

### 🧠 Análisis Emocional (cada 7 mensajes)

Cuando envías el **mensaje 7, 14, 21...**:

1. GPT-5.1 actúa como **psicólogo clínico experto**
2. Evalúa: depresión, ansiedad, soledad
3. Determina nivel de apoyo necesario
4. Cambia el modo si detecta angustia:
   - `normal` → conversación estándar
   - `supportive` → tono de apoyo
   - `empathetic` → muy comprensivo
   - `crisis` → sugiere ayuda profesional

### 🎨 Generación de System Prompt (cada mensaje)

En **CADA respuesta** el sistema:

1. Lee el perfil actualizado
2. Lee el estado emocional
3. Genera un system prompt personalizado que:
   - Adapta la **identidad** del bot (niño → amigo niño, adulto → colega)
   - Ajusta el **tono** (simple, juvenil, profesional)
   - Incluye **expertise** en los intereses del usuario
   - Activa **guardarraíles** si hay riesgo emocional

---

## 🧪 Prueba el Sistema Adaptativo

### Test 1: Usuario Niño

1. Registrarte como nuevo usuario
2. Enviar estos mensajes:

```
Mensaje 1: Hola, tengo 10 años y me gusta Minecraft
Mensaje 2: También juego fútbol-sala en mi equipo del cole
Mensaje 3: ¿Qué juegos te gustan?
```

3. **Después del mensaje 3**:
   - Verás un indicador verde en "Tu Perfil Adaptativo"
   - Haz clic y abre el perfil
   - Observa:
     ```json
     {
       "age_range": "~10 años (niño)",
       "interests": ["Minecraft", "Fútbol-sala"],
       "important_facts": ["Juega en equipo del cole"]
     }
     ```

4. **Ver el System Prompt**:
   - Clic en "🔍 Ver System Prompt" (arriba derecha)
   - Observa cómo el bot se convirtió en:
     ```
     IDENTIDAD: Eres un amigo de tu edad al que le encanta Minecraft.
     TONO: Usa lenguaje SIMPLE y AMIGABLE, emojis 😊🎮
     ```

5. **Continuar conversación**:
   - El bot ahora habla como niño
   - Usa emojis
   - Habla de Minecraft y fútbol

### Test 2: Usuario Profesional

1. Crear nueva sesión
2. Enviar:

```
Mensaje 1: Soy ingeniero de datos, trabajo con Python y Spark
Mensaje 2: Estoy optimizando pipelines ETL en producción
Mensaje 3: ¿Conoces buenas prácticas para Spark?
```

3. **Después del mensaje 3**:
   - Abrir perfil
   - Ver:
     ```json
     {
       "age_range": "adulto",
       "profession": "Ingeniero de datos",
       "interests": ["Python", "Spark", "ETL"]
     }
     ```

4. **Ver System Prompt**:
   ```
   IDENTIDAD: Eres alguien como tú, que trabaja en Ingeniería de Datos.
   TONO: Natural, equilibrado, profesional pero cercano
   EXPERTISE: Habla con conocimiento sobre Python, Spark, ETL
   ```

5. **Observar cambio**:
   - El bot ahora usa terminología técnica
   - No usa emojis
   - Responde con conocimiento profesional

### Test 3: Análisis Emocional

Para probar el análisis emocional (requiere 7+ mensajes):

```
Mensaje 1-6: Conversación normal
Mensaje 7: Últimamente me siento muy solo y triste
```

Después del mensaje 7:
- El sistema analiza el estado emocional
- Puede cambiar a modo "supportive" o "empathetic"
- El bot responde con más empatía
- Ver perfil → sección "Estado Emocional"

---

## 🔍 Entender el Frontend

### Sidebar Izquierdo

1. **Mis Conversaciones**
   - Lista de sesiones del usuario
   - Crear nueva conversación

2. **Tu Perfil Adaptativo** (colapsable)
   - Se actualiza automáticamente cada 3 mensajes
   - Indicador verde cuando se actualiza
   - Muestra:
     - 📅 Edad
     - 💼 Profesión
     - 🎮 Intereses
     - 📝 Hechos importantes
     - 🧠 Estado emocional

### Área de Chat

1. **Header**
   - Nombre de la sesión
   - Botón "🔍 Ver System Prompt"
     - Abre modal con el prompt completo
     - Puedes ver exactamente cómo el sistema te percibe

2. **Mensajes**
   - Burbuja azul: tus mensajes
   - Burbuja blanca: respuestas del bot

---

## 📊 Ver los Datos en la Base de Datos

```bash
# Abrir SQLite
cd src
sqlite3 chat_agent.db

# Ver usuarios
SELECT * FROM users;

# Ver perfiles
SELECT user_id,
       json_extract(profile_json, '$.age_range') as edad,
       json_extract(profile_json, '$.interests') as intereses,
       last_updated
FROM user_profiles;

# Ver estado emocional
SELECT user_id,
       json_extract(emotional_state_json, '$.recommended_mode') as modo,
       json_extract(emotional_state_json, '$.support_needed') as apoyo,
       last_emotional_check
FROM user_profiles
WHERE emotional_state_json IS NOT NULL;

# Salir
.quit
```

---

## 🎯 API REST: Endpoints Clave

### Ver perfil de usuario

```bash
curl http://localhost:8000/api/profile/1
```

**Respuesta:**
```json
{
  "profile": {
    "age_range": "~10 años (niño)",
    "interests": ["Minecraft", "Fútbol-sala"],
    "important_facts": ["Juega en equipo del cole"],
    "tone_preference": "simple y entusiasta"
  }
}
```

### Ver system prompt generado

```bash
curl http://localhost:8000/api/system-prompt/1
```

**Respuesta:**
```json
{
  "system_prompt": "IDENTIDAD Y ROL:\nEres un amigo de tu edad...",
  "emotional_state": {
    "recommended_mode": "normal",
    "support_needed": "none"
  }
}
```

### Enviar mensaje

```bash
curl -X POST http://localhost:8000/api/chat \
  -F "session_id=1" \
  -F "message=Hola, cómo estás?"
```

**Respuesta:**
```json
{
  "response": "¡Hola! 😊 Estoy bien, ¿y tú?...",
  "model": "gpt-5.1",
  "profile_updated": false,
  "usage": {
    "total_tokens": 225
  }
}
```

---

## ⚙️ Configuración Avanzada

### Cambiar frecuencia de actualizaciones

Editar `src/main.py`:

```python
# Actualizar perfil cada N mensajes (default: 3)
if count % 3 == 0 and len(history) >= 4:
    # Cambiar el 3 por otro número

# Análisis emocional cada N mensajes (default: 7)
if count % 7 == 0 and len(history) >= 10:
    # Cambiar el 7 por otro número
```

### Cambiar modelo de OpenAI

En `.env`:
```bash
# Usar GPT-4
OPENAI_MODEL=gpt-4

# Usar GPT-4 Turbo
OPENAI_MODEL=gpt-4-turbo

# Usar GPT-5.1 (recomendado)
OPENAI_MODEL=gpt-5.1
```

### Personalizar extraction prompt

Editar `src/profile_service.py` línea 39:
- Modificar reglas de extracción
- Añadir/quitar campos del perfil
- Ajustar criterios de relevancia

---

## 🐛 Troubleshooting

### El perfil no se actualiza

**Causa:** No has enviado suficientes mensajes
**Solución:** Envía al menos 3 mensajes (el perfil se actualiza en el 3º, 6º, 9º...)

### El bot no cambia de tono

**Causa:** El perfil no tiene suficiente información
**Solución:**
1. Menciona explícitamente tu edad o profesión
2. Envía al menos 3 mensajes para trigger la extracción
3. Verifica el perfil en el sidebar

### Error "insufficient_data" en análisis emocional

**Causa:** No hay suficientes mensajes para análisis
**Solución:** El análisis emocional requiere 10+ mensajes de historial

### No veo el indicador verde

**Causa:** El navegador no refrescó
**Solución:** El indicador aparece por 5 segundos después de actualización

---

## 📚 Recursos

- **Swagger Docs**: http://localhost:8000/docs
- **README completo**: `../README.md`
- **Guía de presentación**: `presentacion.md`
- **Código fuente**:
  - Sistema adaptativo: `src/profile_service.py`
  - Análisis emocional: `src/llm_service.py` (línea 83)
  - Endpoints: `src/main.py`

---

## 💡 Tips para la Demo

1. **Prepara dos usuarios**:
   - Usuario niño (10 años, videojuegos)
   - Usuario profesional (ingeniero, Python)

2. **Mensajes pre-escritos**:
   - Copia los scripts de test en un archivo
   - Pega rápidamente durante la demo

3. **Muestra el WOW**:
   - El perfil extraído automáticamente
   - El system prompt generado
   - El cambio de tono entre usuarios

4. **Destaca la IA**:
   - "El LLM analiza y extrae solo información permanente"
   - "GPT actúa como psicólogo experto"
   - "El system prompt se regenera cada mensaje"

---

**¡Listo para la demo! 🚀**
