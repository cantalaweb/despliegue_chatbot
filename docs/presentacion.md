#  Guía para Presentación: Agente LLM Adaptativo (8 minutos)

##  Cronograma Optimizado para IMPACTO

| Tiempo | Actividad | Puntos Clave | WOW Factor |
|--------|-----------|--------------|------------|
| 0-1 min | Introducción + Diferenciador | Sistema adaptativo con IA en TIEMPO REAL |  |
| 1-2 min | Arquitectura + Docker | Profile Service, Análisis Emocional |  |
| 2-6.5 min | ** DEMO ADAPTACIÓN** | Perfil INSTANTÁNEO tras cada mensaje, System Prompt dinámico |  |
| 6.5-8 min | Tecnologías + Q&A | GPT-5.1, endpoints, BD |  |

---

##  Checklist Pre-Presentación

### CRÍTICO - Preparar ANTES:
- [ ] `.env` con `OPENAI_API_KEY` y `OPENAI_MODEL=gpt-5.1`
- [ ] `.env` con `NEWS_API_KEY` (opcional)
- [ ] Docker Desktop funcionando
- [ ] **Base de datos VACÍA** (eliminar `chat_agent.db` para demo limpia)
- [ ] Navegador con pestañas:
  - [ ] `localhost:8000/chat`
  - [ ] `localhost:8000/docs`
- [ ] Terminal en el directorio del proyecto
- [ ] **Scripts de conversación copiados** (ver abajo) para copiar/pegar rápido
- [ ] Diagrama de arquitectura visible
- [ ] Cronómetro/reloj visible

### Scripts Pre-escritos (copiar a un archivo de texto):

**Script Niño:**
```
Hola, tengo 10 años y me encanta Minecraft
También juego fútbol-sala en mi equipo del cole
¿Qué juegos te gustan a ti?
```

**Script Profesional:**
```
Soy ingeniero de datos, trabajo con Python y Spark
Estoy optimizando pipelines ETL en AWS
¿Conoces buenas prácticas para optimización de Spark?
```

---

##  Script de Presentación MEJORADO

### 1. INTRODUCCIÓN - EL GANCHO (1 min)

**Decir (con energía):**
> "He desarrollado un **Agente Conversacional con IA Adaptativa** que no solo recuerda conversaciones, sino que **aprende automáticamente sobre cada usuario** y **transforma su personalidad** para convertirse en el compañero perfecto. Si le habla un niño de 10 años, el bot se convierte en un amigo niño. Si le habla un ingeniero, se convierte en un colega profesional. **Todo de forma automática usando GPT-5.1**."

**Mostrar rápidamente:**
- Diagrama de arquitectura destacando:
  - Profile Service (extracción automática)
  - Emotional Analysis (GPT como psicólogo)
  - Dynamic System Prompts

**Puntos clave (20 segundos):**
-  Extracción automática de perfil con IA
-  System prompts dinámicos regenerados cada mensaje
-  Análisis emocional (GPT actúa como psicólogo)
-  Adaptación de personalidad en tiempo real
-  Frontend con visualización de perfil

---

### 2. DOCKERIZACIÓN RÁPIDA (1 min)

**Decir:**
> "Todo está dockerizado. Vamos a levantarlo:"

**Ejecutar (si no está corriendo):**
```bash
docker build -t llm-chat-agent .
docker run -d --name chat-agent -p 8000:8000 --env-file .env llm-chat-agent
docker ps
```

**O si ya está corriendo:**
```bash
docker ps  # Mostrar que está activo
```

**Abrir:**
`http://localhost:8000/chat`

**Decir:**
> "La aplicación usa multi-stage Docker build, GPT-5.1, y una base de datos SQLite con perfiles JSON. Ahora vamos a lo impresionante."

---

### 3.  DEMO ADAPTACIÓN DE PERSONALIDAD (5.5 min) - **MOMENTO WOW**

####  Parte 1: Usuario Niño (2.5 min)

**Paso 1: Registro rápido (20 seg)**
1. Clic en "Crear Cuenta"
2. Usuario: `demo_niño` / Contraseña: `demo123`
3. Sesión automática creada

**Paso 2: Conversación inicial (40 seg)**

**Pegar mensaje 1:**
```
Hola, tengo 10 años y me encanta Minecraft
```

**Decir mientras el bot responde:**
> "Observen la respuesta... y esperen... **BOOM!**"

**Paso 3:  PRIMER WOW - Perfil Extraído INSTANTÁNEAMENTE (1 min)**

**Decir:**
> "¡Miren! **INMEDIATAMENTE** después del primer mensaje, el sistema **ya extrajo mi perfil automáticamente**. Ni siquiera tuve que enviar un segundo mensaje..."

1. **Señalar el indicador verde** parpadeante en "Tu Perfil Adaptativo"
2. **Hacer clic** para expandir el perfil
3. **Mostrar perfil extraído:**

**ENFATIZAR:**
> "¡Miren esto! El sistema **usó GPT-5.1 como analista experto** y extrajo automáticamente **EN TIEMPO REAL**:
> - Mi edad: ~10 años (niño)
> - Mis intereses: Minecraft
> - **Todo esto EN UN SOLO MENSAJE. Sin formularios. Adaptación instantánea.**"

**Paso 4: Continuar conversación para mostrar actualización dinámica (30 seg)**

**Pegar mensaje 2:**
```
También juego fútbol-sala en mi equipo del cole
```

**Decir:**
> "Observen cómo el perfil se **actualiza nuevamente** tras este mensaje. Fútbol-sala se añade a mis intereses. **Cada mensaje refina el perfil más**."

**Paso 5:  SEGUNDO WOW - System Prompt (30 seg)**

1. **Hacer clic en " Ver System Prompt"** (botón arriba derecha)
2. **Mostrar el modal** con el system prompt generado

**ENFATIZAR (leer fragmentos):**
> "Ahora miren cómo el sistema **se reprogramó a sí mismo**:
>
> - 'IDENTIDAD: Eres un amigo de tu edad al que le encanta Minecraft'
> - 'TONO: Usa lenguaje SIMPLE y AMIGABLE, emojis '
> - 'EXPERTISE: Habla con conocimiento sobre Minecraft, Fútbol-sala'
>
> **El bot literalmente se convirtió en un niño de 10 años.**"

**Paso 6: Demostrar el cambio de personalidad (30 seg)**

**Enviar mensaje 3:**
```
Cuéntame sobre Minecraft
```

**Decir:**
> "Observen cómo responde ahora: usa lenguaje simple, habla como niño, es entusiasta. **La personalidad cambió completamente desde el PRIMER mensaje**."

---

####  Parte 2: Usuario Profesional (2 min)

**Paso 1: Nueva sesión (10 seg)**
1. Clic en "Nueva Conversación"
2. Nombre: "Trabajo"

**Decir:**
> "Ahora voy a actuar como un profesional."

**Paso 2: Conversación profesional (50 seg)**

**Pegar mensaje 1:**
```
Soy ingeniera de datos, trabajo con Python y Spark
```

**Decir mientras el bot responde:**
> "Observen... **Perfil actualizándose INSTANTÁNEAMENTE otra vez**..."

**Paso 3:  TERCER WOW - Perfil Profesional INSTANTÁNEO (40 seg)**

1. **Expandir "Tu Perfil Adaptativo"** (indicador verde ya parpadeando)
2. **Mostrar perfil extraído TRAS EL PRIMER MENSAJE:**
   - Género: femenino (detectado por "ingeniera")
   - Profesión: Ingeniera de datos
   - Intereses: Python, Spark
   - Tono: profesional pero cercano

**ENFATIZAR:**
> "El mismo sistema, pero **detectó INSTANTÁNEAMENTE que soy mujer profesional** (por la forma femenina 'ingeniera') y **cambió completamente**. **Un solo mensaje y ya se adaptó**."

3. **Abrir System Prompt nuevamente**

**Leer:**
> "Ahora dice:
> - 'IDENTIDAD: Eres alguien como tú, que trabaja en Ingeniería de Datos'
> - 'TONO: Natural, equilibrado, profesional pero cercano'
> - 'EXPERTISE: Habla con conocimiento sobre Python, Spark'
>
> **Es un bot completamente diferente para cada usuario. Y todo en TIEMPO REAL.**"

**Paso 4: Enviar mensaje 2 para mostrar evolución (20 seg)**

**Pegar mensaje 2:**
```
Estoy optimizando pipelines ETL en AWS
```

**Decir:**
> "Observen cómo el bot responde como colega técnico, sin emojis, con tono profesional. **Perfil se refina con cada mensaje**."

**Paso 5: Comparación final (20 seg)**

**Volver a la primera sesión** (usuario niño)

**Enviar:**
```
¿Recuerdas qué me gusta?
```

**Decir:**
> "Y mantiene la memoria de cada sesión independiente. **Adaptación + Persistencia**."

---

### 4. TECNOLOGÍAS Y ARQUITECTURA (1.5 min)

**Abrir Swagger:**
`http://localhost:8000/docs`

**Mostrar endpoints nuevos:**
- `/api/profile/{user_id}` - Ver perfil extraído
- `/api/system-prompt/{user_id}` - Ver prompt generado
- `/api/chat` - Incluye `profile_updated: true/false`

**Decir:**
> "El sistema tiene 3 capas de inteligencia:"

**Explicar rápido:**

1. **Extracción de Perfil (tras CADA mensaje del usuario)**
   - GPT-5.1 analiza conversación EN TIEMPO REAL
   - Extrae solo información **permanente**
   - **Reglas CRÍTICAS**:
     * Distingue "tiene" vs "quiere tener"
     * NO extrae política/religión a menos que se mencione EXPLÍCITAMENTE
     * NO duplica ocupación en important_facts
     * Limpieza automática de entradas vagas
   - **Actualización instantánea**: Dices "soy médica" → perfil se actualiza AL INSTANTE

2. **Análisis Emocional (cada 7 mensajes)**
   - GPT-5.1 actúa como psicólogo clínico
   - Detecta depresión, ansiedad, soledad
   - Recomienda modo: normal/supportive/empathetic/crisis
   - Activa guardarraíles de seguridad

3. **Generación de System Prompt (cada mensaje)**
   - Crea identidad adaptada
   - Ajusta tono según edad/contexto
   - Añade expertise en intereses del usuario

**Mostrar BD (si tienes tiempo):**
```bash
docker exec -it chat-agent sh -c "sqlite3 chat_agent.db 'SELECT user_id, json_extract(profile_json, \"$.age_range\") as edad, json_extract(profile_json, \"$.interests\") as intereses FROM user_profiles;'"
```

**Decir:**
> "Los perfiles se guardan en JSON en SQLite, permitiendo estructura flexible."

---

##  Puntos Clave a ENFATIZAR

### Lo que hace especial este proyecto:

1. **IA que aprende de IA**
   > "Uso GPT-5.1 no solo para conversar, sino como **analista de datos**, **psicólogo** y **generador de prompts**."

2. **Adaptación INSTANTÁNEA, no simulada**
   > "No es un simple cambio de tono. El perfil se extrae **tras cada mensaje** y el system prompt se **regenera completamente** en tiempo real. **Adaptación al instante**."

3. **Sin intervención manual**
   > "El usuario nunca completa formularios. Todo se extrae **automáticamente** de las conversaciones naturales. **Un solo mensaje puede ser suficiente**."

4. **Extracción inteligente con reglas estrictas**
   > "El sistema NO inventa información. **NO extrae política o religión** a menos que se mencione explícitamente. **NO duplica datos** entre campos. Precisión absoluta."

5. **Guardarraíles éticos**
   > "El sistema **detecta angustia emocional** y cambia a modo de apoyo, sugiriendo ayuda profesional si es necesario. **No copia comportamientos autodestructivos**."

6. **Arquitectura modular**
   > "Profile Service, LLM Service, News Service... cada componente con responsabilidad única."

---

##  Frases de IMPACTO

### Al inicio:
> "¿Qué tal un chatbot que **aprende quién eres automáticamente** y **se adapta EN TIEMPO REAL para ser tu compañero perfecto**?"

### Al mostrar primer perfil:
> "Miren esto: **CON UN SOLO MENSAJE**, la IA extrajo mi edad, intereses y contexto. **Sin formularios. Instantáneo**."

### Al mostrar system prompt:
> "El bot literalmente se **reprogramó a sí mismo INMEDIATAMENTE** para hablar como un niño de 10 años."

### Al cambiar a profesional:
> "**Mismo sistema, personalidad completamente diferente. Y otra vez: INSTANTÁNEO**. Un mensaje y ya detectó que soy mujer profesional por la forma femenina 'ingeniera'."

### Al mostrar endpoints:
> "Pueden ver el perfil y el system prompt en tiempo real vía API. **Total transparencia. Cada petición refleja la última actualización**."

### Cierre:
> "En resumen: un agente LLM que **se adapta INSTANTÁNEAMENTE a cada usuario**, usando **GPT-5.1 como motor de análisis en tiempo real**, con **memoria persistente**, **visualización dinámica**, **extracción tras cada mensaje**, **reglas estrictas anti-invención**, y **guardarraíles de seguridad**. Todo dockerizado y listo para producción."

---

##  Troubleshooting Durante Demo

### Si el perfil no se actualiza:
- El perfil se extrae tras CADA mensaje (no cada 3)
- El indicador verde tarda 1-2 segundos en aparecer
- Refrescar la página si no aparece después de 2 segundos

### Si el bot no cambia de tono:
- Mencionar explícitamente edad/profesión en el PRIMER mensaje
- El perfil se actualiza INMEDIATAMENTE tras el mensaje
- Verificar perfil en sidebar (debería aparecer indicador verde)

### Si algo falla:
- Tener screenshots preparados de:
  - Perfil niño extraído
  - System prompt niño
  - Perfil profesional
  - System prompt profesional
- Mostrar los screenshots y explicar qué harían

---

##  Estadísticas para Mencionar

- **4 tablas** en SQLite (users, sessions, messages, **user_profiles**)
- **10 endpoints** API REST
- **5 archivos Python** (main, database, llm_service, **profile_service**, **news_service**)
- **~800 líneas** código backend
- **~600 líneas** código frontend con visualización
- **GPT-5.1** (modelo más avanzado con razonamiento adaptativo)
- **Perfiles JSON flexibles** (político, religión, hechos importantes)

---

##  Respuestas a Preguntas Frecuentes

### ¿Cómo se extrae el perfil?
> "GPT-5.1 recibe un prompt especializado con **reglas muy estrictas**: distingue 'tiene' vs 'quiere', ignora eventos temporales, extrae solo información permanente. Luego parseo el JSON y lo guardo en SQLite."

### ¿Cuánto cuesta la extracción?
> "Se hace cada 3 mensajes, con prompts de ~300 tokens. Muy eficiente. El ahorro viene de **perfiles que se reutilizan** en lugar de enviar contexto completo cada vez."

### ¿Qué pasa si extrae mal?
> "El sistema tiene **reglas de fusión**: nueva info se añade sin borrar anterior. Y se actualiza cada 3 mensajes, autocorrigiéndose."

### ¿Es escalable?
> "Completamente. API stateless, base de datos optimizada con índices, system prompts se generan on-the-fly. Fácil de escalar horizontalmente."

### ¿Por qué GPT-5.1?
> "Razonamiento adaptativo superior, mejor análisis contextual para extracción de perfiles, y capacidad de actuar como experto psicólogo para análisis emocional."

---

##  Checklist Final (antes de empezar)

- [ ] Docker corriendo
- [ ] `chat_agent.db` **eliminado** (para demo limpia)
- [ ] Scripts copiados en archivo de texto
- [ ] Navegador en `localhost:8000/chat`
- [ ] Swagger en otra pestaña
- [ ] Cronómetro preparado
- [ ] Respirar profundo 

---

##  GOLDEN RULE

**El WOW factor NO es la memoria persistente.**
**El WOW factor ES la adaptación INSTANTÁNEA y automática de personalidad.**

Dedica el 60% del tiempo a mostrar:
1. Perfil extraído INSTANTÁNEAMENTE tras el PRIMER mensaje
2. System prompt generado EN TIEMPO REAL
3. Cambio visible de tono INMEDIATO
4. Comparación niño vs profesional (ambos con actualización instantánea)
5. ENFATIZAR: "Un solo mensaje → perfil completo → bot adaptado"

---

**¡Vas a impresionar! **
