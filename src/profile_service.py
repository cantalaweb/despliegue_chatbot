"""
Profile Service for intelligent user profile extraction and system prompt generation.
This is the core of the adaptive personality system.
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime


class ProfileService:
    """Service for profile extraction and adaptive system prompt generation."""

    def __init__(self, llm_service):
        """Initialize with LLM service for AI-powered extraction."""
        self.llm_service = llm_service

    def extract_profile_from_conversation(self, conversation: List[Dict[str, str]],
                                         existing_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract relevant user information from conversation using LLM.

        Args:
            conversation: Recent conversation messages
            existing_profile: Existing profile to update (if any)

        Returns:
            Updated profile dict
        """
        if len(conversation) < 2:
            return existing_profile or self._get_empty_profile()

        # Format conversation
        conv_text = "\n".join([
            f"{'Usuario' if msg['role'] == 'user' else 'Asistente'}: {msg['content']}"
            for msg in conversation[-10:]  # Last 10 messages
        ])

        extraction_prompt = f"""Actúa como un ANALISTA EXPERTO extrayendo información PERMANENTE sobre el usuario.

🚨🚨🚨 PASO 1 - DETECTAR GÉNERO (HACER PRIMERO):
Lee TODA la conversación buscando palabras terminadas en -A o -O que describan al usuario:
- Si ves "aburrida", "cansada", "contenta", "entretenida", "ocupada", "satisfecha", etc. → gender = "femenino"
- Si ves "aburrido", "cansado", "contento", "entretenido", "ocupado", "satisfecho", etc. → gender = "masculino"
- Si ves "ingeniera", "médica", "doctora" → gender = "femenino"
- Si ves "madre", "mamá", "esposa", "hija" → gender = "femenino"
- Si ves "padre", "papá", "esposo", "hijo" → gender = "masculino"
EJEMPLOS:
"He estado entretenida" → FEMENINO
"Estoy aburrido" → MASCULINO
"Soy ingeniera" → FEMENINO

⚠️ REGLAS CRÍTICAS:
1. NO INVENTES información que no esté explícitamente en la conversación
2. DISTINGUE entre "tiene" y "quiere tener" - son MUY diferentes
3. NO incluyas eventos temporales (regalos recientes, compras, actividades puntuales)
4. SÉ PRECISO con la edad - analiza el contexto cuidadosamente
5. SOLO incluye hechos PERMANENTES que definan a la persona

🚨 POLÍTICA Y RELIGIÓN - REGLA MÁXIMA PRIORIDAD:
- SOLO extrae political_stance o religion si el usuario lo menciona EXPLÍCITA y DIRECTAMENTE
- Si el usuario NO dice "soy ateo", "soy católico", "soy de izquierdas", etc. → deja en null
- NUNCA deduzcas política/religión por edad, ocupación o intereses
- NUNCA extraigas política/religión de niños (menores de 18) aunque lo mencionen
- Ejemplos de NO extraer:
  * "No voy a misa" → NO significa ateo (puede ser católico no practicante)
  * "Me gusta la ciencia" → NO significa ateo
  * Usuario no menciona religión → null (NO "secular", NO "ateo")

CRITERIOS ESTRICTOS - Incluye SOLO si cumple al menos uno:
1. IDENTIDAD PERMANENTE: Edad ACTUAL, género, profesión estable, estudios completados
2. FORMATIVO: Trauma, logro importante, cambio vital significativo
3. CONDICIÓN DURADERA: Salud crónica, situación familiar permanente, creencia profunda
4. PASIÓN CONSISTENTE: Interés que practica regularmente (no deseo casual)
5. CONTEXTO ESENCIAL: Info necesaria para interactuar apropiadamente

📝 IMPORTANT_FACTS vs INTERESTS - REGLAS DE CLASIFICACIÓN:

🚨 SI ES UNA PASIÓN/INTERÉS/HOBBY → VA A "interests", NO A "important_facts":
- Si dice "me gusta X", "me encanta X", "X es mi pasión", "disfruto X" → interests
- Ejemplos: "me encanta cocinar" → interests: ["Cocinar"]
- Ejemplos: "la cocina es mi pasión" → interests: ["Cocina"]
- Ejemplos: "me gusta leer" → interests: ["Lectura"]

🚨 IMPORTANT_FACTS es SOLO para:
- Hechos sobre SITUACIÓN: "Tiene un perro", "Vive en Madrid", "Tiene dos hijos"
- CONDICIONES permanentes: "Es diabético", "Es alérgico a los gatos"
- CONTEXTO esencial: "Trabaja desde casa", "Viaja mucho por trabajo"

🚨 NO DUPLICAR ENTRE CAMPOS:
- NO incluyas ocupación en important_facts si ya está en "profession"
- NO incluyas intereses/pasiones en important_facts si ya están en "interests"
- NO incluyas estudios en important_facts si ya están en "education"
- Important_facts es SOLO para información que NO cabe en otros campos

✅ EJEMPLOS CORRECTOS de information_facts:
- "Tiene un perro llamado Max" (mascota = relación permanente)
- "Es diabético tipo 1" (condición médica permanente)
- "Vive en Barcelona" (ubicación estable)
- "Tiene dos hijos" (familia permanente)
- "Practica yoga regularmente" (hábito consistente)

❌❌❌ EJEMPLOS INCORRECTOS - NUNCA INCLUIR EN IMPORTANT_FACTS:
- "Le regalaron Minecraft por su cumpleaños" → Evento puntual temporal
- "Tiene Nintendo Switch" cuando dijo "PEDIRÉ una Switch" → ¡NO LA TIENE AÚN!
- "Comió pizza ayer" → Evento de un solo día
- "Ha estado entretenida todo el día" → Estado temporal de HOY (NO es permanente)
- "Está cansada" → Estado temporal del MOMENTO
- "Tuvo un buen día" → Evento de UN DÍA
- "Se fue de vacaciones" → Evento temporal
- "Está viendo una serie" → Actividad temporal
- "Hoy trabajó mucho" → Evento de HOY

🚨 REGLA ABSOLUTA PARA IMPORTANT_FACTS:
SI ES ALGO DE HOY, AYER, ESTA SEMANA, UN MOMENTO ESPECÍFICO → NO LO INCLUYAS
SI ES UN ESTADO TEMPORAL (cansada, aburrida, entretenida) → NO LO INCLUYAS
SOLO incluye hechos que serán ciertos dentro de 1 MES o más

🎯 EDAD - SÉ MUY PRECISO:

⚡ DETECCIÓN AUTOMÁTICA POR JERGA JUVENIL (PRIORIDAD ALTA):
Si NO menciona su edad explícitamente PERO usa jerga juvenil española 2024-2025, INFIERE edad automáticamente:

🔍 INDICADORES DE EDAD JOVEN (10-17 años):
Si detectas 2 o más de estas palabras/expresiones → age_range: "~10-17 años (preadolescente/adolescente)"
- "Literal" como intensificador: "literal estoy aburrido", "literal me encanta"
- "En plan": "en plan no me apetece", "juegos en plan Minecraft"
- "Bro" / "Tete" / "Socio" / "Nano" como apelativo de amistad
- "Me renta / No me renta": "¿te renta salir?"
- "PEC": "ese plan es PEC"
- "Cringe" / "Lache": "qué cringe", "me da lache"
- "Rizz": "tienes buen rizz"
- "Crush": "es mi crush"
- "Tipo" / "Rollo": "música tipo indie", "no es mi rollo"
- "Chetado": "está chetado"
- "Random": "qué random"
- "Skibidi", "Sigma", "Gyatt" → 100% Generación Alfa (10-13 años específicamente)

EJEMPLOS:
- "Bro literal estoy aburrido" → age_range: "~10-17 años (preadolescente/adolescente)"
- "Tete, no me renta salir hoy" → age_range: "~14-17 años (adolescente)"
- "Es que en plan me da cringe" → age_range: "~10-17 años (preadolescente/adolescente)"
- "Ese plan es PEC" → age_range: "~14-17 años (adolescente)"

⚠️ IMPORTANTE: Esta inferencia te permite empezar a hablar CON SU JERGA inmediatamente, aunque no sepas su edad exacta.

📅 EDAD EXPLÍCITA (si la menciona):
- Si dice "cuando cumpla 11" → tiene 10 años AHORA
- Si dice "tengo 9" pero luego "cuando cumpla 11" → CORRIGE a 10 años
- Edad aproximada: usa "~10 años (niño)" no "~9 años"

👤 NOMBRE Y GÉNERO - DEDUCCIÓN INTELIGENTE:
- Si menciona su nombre, guárdalo en "name"
- DEDUCE el género usando estas pistas en ORDEN DE PRIORIDAD:

1. **CONCORDANCIA DE GÉNERO** (🚨 MÁXIMA PRIORIDAD ABSOLUTA 🚨):

   ⚠️⚠️⚠️ REGLA CRÍTICA: Busca TODAS las palabras con terminación -a/-o que describan al usuario ⚠️⚠️⚠️

   SI VES TERMINACIÓN EN "-A" (aburrida, cansada, contenta, entretenida, ocupada, etc.) → FEMENINO 100%
   SI VES TERMINACIÓN EN "-O" (aburrido, cansado, contento, entretenido, ocupado, etc.) → MASCULINO 100%

   FEMENINO (detectar CUALQUIERA de estas formas):
   * "aburrida", "cansada", "contenta", "emocionada", "preocupada", "estresada",
   * "nerviosa", "tranquila", "segura", "lista", "preparada", "ENTRETENIDA", "ocupada",
   * "feliz porque estoy satisfecha", "agotada", "motivada", "ilusionada", "asustada"
   * Participios: "he estado ocupada", "estoy acostumbrada", "quedé sorprendida", "he estado entretenida"

   MASCULINO (detectar CUALQUIERA de estas formas):
   * "aburrido", "cansado", "contento", "emocionado", "preocupado", "estresado",
   * "nervioso", "tranquilo", "seguro", "listo", "preparado", "ENTRETENIDO", "ocupado",
   * "agotado", "motivado", "ilusionado", "asustado"
   * Participios: "he estado ocupado", "estoy acostumbrado", "quedé sorprendido", "he estado entretenido"

   🔍 MÉTODO: Lee TODA la conversación buscando palabras terminadas en -a/-o que modifiquen al usuario.
   NO importa si es en pasado, presente o futuro. Si dice "estuve cansada", "estoy cansada", "estaré cansada" → FEMENINO.

2. **OCUPACIÓN Y ROL FAMILIAR**:
   * Forma femenina CONFIRMA género femenino al 100%:
     "ingeniera", "profesora", "médica", "enfermera", "abogada", "ama de casa", "doctora", "arquitecta",
     "madre", "mamá", "esposa", "mujer" (de alguien), "hija", "hermana", "tía", "abuela"
     → "femenino" (SEGURO)

   * Forma masculina es indicativa pero NO definitiva:
     "ingeniero", "profesor", "médico", "abogado", "arquitecto" → PROBABLEMENTE masculino
     PERO: algunas mujeres usan forma masculina (ej: "soy médico")
     → Solo confirma masculino si se combina con otras pistas (nombre masculino, adjetivo masculino)

   * Rol familiar masculino SÍ confirma:
     "padre", "papá", "esposo", "marido", "hijo", "hermano", "tío", "abuelo" → masculino (SEGURO)

   * Ejemplos:
     - "Soy ingeniera" → femenino (100% seguro)
     - "Estoy aburrida" → femenino (100% seguro por adjetivo)
     - "Soy médico" + nombre Alex → AMBIGUO (puede ser mujer usando forma masculina)
     - "Soy madre de dos hijos" → femenino (100% seguro por "madre")

3. **NOMBRE** (si concordancia y ocupación no revelan género):
   * Nombres claramente masculinos: Juan, Carlos, Miguel, Pedro, José, Antonio → "masculino"
   * Nombres claramente femeninos: María, Ana, Carmen, Laura, Isabel, Rosa → "femenino"
   * Nombres ambiguos: Alex, Andrea, Asier, etc. → marca como "ambiguo"

4. **PRONOMBRES** (último recurso):
   * Si usa "yo misma", "yo mismo", referencias explícitas

- Si NINGUNA pista es clara → "ambiguo" (NO "null")
- Si no hay información → "null"

CONVERSACIÓN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━
{conv_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 ANTES DE RESPONDER - VERIFICA GÉNERO:
¿Hay palabras terminadas en -A describiendo al usuario? (aburrida, cansada, entretenida, ocupada, contenta, etc.) → gender = "femenino"
¿Hay palabras terminadas en -O describiendo al usuario? (aburrido, cansado, entretenido, ocupado, contento, etc.) → gender = "masculino"

Responde SOLO con este JSON (sin explicaciones):
{{
  "name": "nombre del usuario si lo mencionó, sino null",
  "age_range": "edad aproximada + contexto (ej: '~9 años (niño)', '~45 años (adulto)')",
  "gender": "masculino|femenino|ambiguo|null (busca terminaciones -a/-o: aburrida=femenino, aburrido=masculino)",
  "profession": "trabajo actual o null",
  "education": "estudios relevantes o null",
  "interests": ["solo pasiones reales y consistentes"],
  "political_stance": {{
    "spectrum": "izquierda|centro-izquierda|centro|centro-derecha|derecha|apolitico|null",
    "intensity": "bajo|moderado|alto|null",
    "approach": "avoid|neutral|align|null"
  }},
  "religion": {{
    "faith": "catolico|musulman|judio|protestante|budista|hindu|ateo|agnostico|espiritual|null",
    "intensity": "muy religioso|moderadamente religioso|poco religioso|secular|null",
    "approach": "avoid|respectful|engage|null"
  }},
  "important_facts": [
    "SOLO hechos PERMANENTES (NO eventos de hoy/ayer, NO estados temporales como 'cansada' o 'entretenida')"
  ],
  "sensitive_topics": ["temas a evitar o tratar con cuidado"],
  "personality_traits": ["rasgos consistentes observados"],
  "needs": ["qué busca en las conversaciones"],
  "tone_preference": "descripción del tono apropiado"
}}"""

        try:
            response = self.llm_service.client.chat.completions.create(
                model=self.llm_service.model,
                messages=[{"role": "user", "content": extraction_prompt}],
                max_tokens=600,
                temperature=0.3
            )

            extracted = json.loads(response.choices[0].message.content)

            # Merge with existing profile if available
            if existing_profile and existing_profile.get("age_range"):
                return self._merge_profiles(existing_profile, extracted)
            else:
                return extracted

        except Exception as e:
            print(f"Error extracting profile: {str(e)}")
            return existing_profile or self._get_empty_profile()

    def _merge_profiles(self, existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """Merge new extracted info with existing profile, keeping what's valuable."""
        merged = existing.copy()

        # Update scalar fields if new info is more specific
        for key in ["name", "age_range", "gender", "profession", "education", "tone_preference"]:
            if new.get(key) and new[key] != "null":
                merged[key] = new[key]

        # Merge arrays (deduplicate)
        for key in ["interests", "important_facts", "sensitive_topics", "personality_traits", "needs"]:
            if key in new and new[key]:
                existing_items = set(merged.get(key, []))
                new_items = set(new[key]) if isinstance(new[key], list) else set()
                merged[key] = list(existing_items | new_items)

        # CRITICAL: Clean up important_facts to avoid duplication with other fields
        facts = merged.get("important_facts", [])
        cleaned_facts = []

        # Get all other fields for comparison
        profession = merged.get("profession", "").lower() if merged.get("profession") else ""
        education = merged.get("education", "").lower() if merged.get("education") else ""
        interests = [i.lower() for i in merged.get("interests", [])]

        for fact in facts:
            fact_lower = fact.lower()
            should_skip = False

            # Skip if it's about profession
            if profession and profession != "null":
                if any(word in fact_lower for word in ["trabaja como", "trabaja de", "es un", "es una", "su trabajo", "su ocupación"]):
                    if profession in fact_lower or "trabajador" in fact_lower:
                        should_skip = True
                if fact_lower in ["trabaja", "tiene trabajo", "trabaja como trabajador"]:
                    should_skip = True

            # Skip if it's about an interest/hobby (redundant with interests field)
            for interest in interests:
                # Check if the fact mentions this interest
                if interest in fact_lower or fact_lower in interest:
                    should_skip = True
                    break
                # Check common patterns for interests
                if any(pattern.format(interest) in fact_lower for pattern in [
                    "le gusta {}", "le encanta {}", "{} es su pasión", "disfruta {}",
                    "le apasiona {}", "practica {}", "{}"
                ]):
                    should_skip = True
                    break

            # Skip if it's about education (redundant with education field)
            if education and education != "null":
                if any(word in fact_lower for word in ["estudió", "graduado en", "título en", "carrera de"]):
                    if education in fact_lower:
                        should_skip = True

            if not should_skip:
                cleaned_facts.append(fact)

        # Additional deduplication: remove semantically similar facts
        final_facts = []
        for fact in cleaned_facts:
            # Check if this fact is not already represented by a similar one
            is_duplicate = False
            for existing_fact in final_facts:
                # Simple similarity check: if facts share many words, they're duplicates
                fact_words = set(fact.lower().split())
                existing_words = set(existing_fact.lower().split())
                overlap = len(fact_words & existing_words)
                if overlap >= 2 and overlap >= len(fact_words) * 0.5:
                    is_duplicate = True
                    break
            if not is_duplicate:
                final_facts.append(fact)

        merged["important_facts"] = final_facts

        # Update nested objects
        if new.get("political_stance") and any(v for v in new["political_stance"].values() if v and v != "null"):
            merged["political_stance"] = new["political_stance"]

        if new.get("religion") and any(v for v in new["religion"].values() if v and v != "null"):
            merged["religion"] = new["religion"]

        return merged

    def generate_system_prompt(self, profile: Dict[str, Any],
                              emotional_state: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate adaptive system prompt based on user profile and emotional state.

        This is the core of the personality adaptation system.
        """
        # Check emotional state for guardrails
        mode = "normal"
        if emotional_state:
            mode = emotional_state.get("recommended_mode", "normal")
            support_needed = emotional_state.get("support_needed", "none")

        # Generate identity section
        identity = self._generate_identity_section(profile, mode)

        # Generate profile summary
        profile_summary = self._generate_profile_summary(profile)

        # Generate behavior instructions
        behavior = self._generate_behavior_instructions(profile, mode)

        # Generate guardrails
        guardrails = self._generate_guardrails(emotional_state)

        # Generate proactive questions to fill profile
        proactive_questions = self.generate_proactive_questions(profile)

        # Check if user is young to add slang reminder
        age = profile.get("age_range") or ""
        is_young = any(word in age.lower() for word in ["niño", "adolescente", "preadolescente"]) or any(str(n) in age for n in range(10, 21))

        slang_reminder = ""
        if is_young:
            slang_reminder = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨🚨🚨 ADVERTENCIA CRÍTICA - LEER ANTES DE RESPONDER 🚨🚨🚨
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌❌❌ PALABRAS QUE TE HACEN PARECER VIEJO Y CRINGE ❌❌❌
BAJO NINGUNA CIRCUNSTANCIA uses estas palabras:

🚫 "GUAY" → TE HACE PARECER DE 40 AÑOS
🚫 "MOLA" → TE HACE PARECER DE 40 AÑOS
🚫 "CHACHI" → TE HACE PARECER DE 50 AÑOS
🚫 "GENIAL" → TE HACE PARECER FORMAL/VIEJO
🚫 "UNA PASADA" → TE HACE PARECER DE 35+ AÑOS
🚫 "FLIPAR" (como verbo activo) → TE HACE PARECER MILLENNIAL VIEJO

✅✅✅ USA ESTAS EN SU LUGAR ✅✅✅
→ En lugar de "guay": "PEC", "brutal", "increíble"
→ En lugar de "mola": "me gusta", "es PEC", "me renta"
→ En lugar de "una pasada": "PEC", "brutal", "chetado"
→ En lugar de "flipar": "alucinar", "es una locura"
→ En lugar de "genial": "PEC", "brutal", "increíble"

⚡ USA FRECUENTEMENTE:
✅ "Literal" → ÚSALO MUCHO: "Literal te entiendo", "Es literal lo mejor"
✅ "En plan" → ÚSALO PARA TODO: "en plan Creativo", "en plan sí"
✅ "Bro/Tete" → ÚSALO COMO VOCATIVO: "Bro, escucha", "Tete, mira"
✅ "PEC" → SUSTITUTO DE "GUAY": "Eso es PEC", "Un mapa PEC"

EJEMPLO CORRECTO: "Literal, el Creativo es PEC. ¿Has creado algún mapa brutal?"
EJEMPLO INCORRECTO: "¡Literal, el Creativo es una pasada! ¿Has creado algún mapa guay?"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        # Assemble full system prompt
        system_prompt = f"""{identity}
{slang_reminder}
{profile_summary}

{behavior}

{guardrails}

{proactive_questions}
{slang_reminder}
RECUERDA:
- Eres su igual, pero con expertise en sus intereses
- Habla naturalmente como alguien de su edad y contexto
- Sé proactivo sobre temas que le apasionan
- SIEMPRE prioriza su bienestar sobre "actuar como él"
- Mantén consistencia con conversaciones previas
- Si algo no encaja con su perfil, el usuario puede haber cambiado - adapta

¡Ahora conversa naturalmente!"""

        return system_prompt

    def _generate_identity_section(self, profile: Dict[str, Any], mode: str) -> str:
        """Generate the identity/role section of system prompt."""
        age = profile.get("age_range") or "adulto"
        interests = profile.get("interests") or []
        profession = profile.get("profession")

        if mode in ["supportive", "empathetic", "crisis"]:
            return f"""IDENTIDAD Y ROL:
Eres un amigo cercano y comprensivo.
Te preocupas genuinamente por el usuario y quieres ayudar.

🚨 MODO: APOYO EMOCIONAL ACTIVADO
- Prioriza el bienestar emocional sobre todo
- Sé empático, paciente, y cálido
- Ofrece ayuda práctica si es apropiado
- No minimices sus sentimientos
- Si detectas riesgo grave, sugiere ayuda profesional"""

        # Normal/friendly mode
        if "niño" in age.lower() or any(x in age for x in ["8", "9", "10", "11", "12"]):
            peer = f"un amigo de tu edad"
            if interests:
                peer += f" al que le encanta {interests[0]}"
        elif "adolescente" in age.lower() or any(x in age for x in ["13", "14", "15", "16", "17"]):
            peer = f"un colega adolescente"
            if interests:
                peer += f" experto en {interests[0]}"
        elif profession:
            peer = f"alguien como tú, que trabaja en {profession}"
            if interests:
                peer += f" y le apasiona {interests[0]}"
        else:
            peer = "alguien de tu edad"
            if interests:
                peer += f" con pasión por {interests[0]}"

        return f"""IDENTIDAD Y ROL:
Eres {peer}.
Compartes intereses y hablas como {self._get_language_style(age)}.

TU PERSONALIDAD:
- Edad: Similar a {age}
- Intereses compartidos: {', '.join(interests[:3]) if interests else 'varios temas'}
- Rol: Amigo/igual que además es experto en {interests[0] if interests else 'muchos temas'}"""

    def _get_language_style(self, age: str) -> str:
        """Get appropriate language style for age."""
        if not age:
            return "un español (natural, amigable)"

        age_lower = age.lower()
        # Detectar edad numérica
        age_number = None
        for num in ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]:
            if num in age:
                age_number = int(num)
                break

        # Generación Alfa (10-13) - incluye "preadolescente" para rango amplio
        if "niño" in age_lower or "preadolescente" in age_lower or (age_number and 10 <= age_number <= 13):
            return "un colega de tu edad de la Generación Alfa española (usa jerga viral 2024-2025: literal, en plan, rizz, PEC, cringe, chetado, bro)"
        # Generación Z (14-20)
        elif "adolescente" in age_lower or (age_number and 14 <= age_number <= 20):
            return "un colega de tu edad de la Generación Z española (usa jerga natural 2024-2025: en plan, literal, me renta, PEC, cringe, crush, tete, bro)"
        # Adultos mayores
        elif "senior" in age_lower or any(x in age for x in ["70", "75", "80"]):
            return "un adulto mayor español (cálido, experimentado - sin emojis ni jerga)"
        # Adultos normales
        else:
            return "un adulto español (natural, equilibrado - sin emojis ni jerga juvenil)"

    def _generate_profile_summary(self, profile: Dict[str, Any]) -> str:
        """Generate formatted profile summary."""
        parts = ["PERFIL COMPLETO DEL USUARIO:", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"]

        if profile.get("age_range"):
            parts.append(f"📅 Edad: {profile['age_range']}")

        if profile.get("gender"):
            parts.append(f"👤 Género: {profile['gender']}")

        if profile.get("profession"):
            parts.append(f"💼 Profesión: {profile['profession']}")

        if profile.get("education"):
            parts.append(f"🎓 Estudios: {profile['education']}")

        interests = profile.get("interests", [])
        if interests:
            parts.append(f"\n🎮 INTERESES Y PASIONES:")
            for interest in interests:
                parts.append(f"   • {interest}")

        # Political stance
        political = profile.get("political_stance", {})
        if political.get("spectrum") and political["spectrum"] != "null":
            parts.append(f"\n🏛️ POSTURA POLÍTICA:")
            parts.append(f"   Tendencia: {political['spectrum']} (intensidad: {political.get('intensity', 'moderado')})")
            if political.get("approach") == "align":
                parts.append(f"   → Muestra empatía con su perspectiva política")
            elif political.get("approach") == "avoid":
                parts.append(f"   → EVITA temas políticos salvo que él los mencione")

        # Religion
        religion = profile.get("religion", {})
        if religion.get("faith") and religion["faith"] != "null":
            parts.append(f"\n⛪ RELIGIÓN:")
            parts.append(f"   Fe: {religion['faith']} ({religion.get('intensity', 'moderado')})")
            if religion.get("approach") == "engage":
                parts.append(f"   → Puedes usar referencias apropiadas a su fe")
            elif religion.get("approach") == "respectful":
                parts.append(f"   → Respeta profundamente sus creencias")

        # Important facts
        facts = profile.get("important_facts", [])
        if facts:
            parts.append(f"\n📝 HECHOS IMPORTANTES:")
            for fact in facts:
                parts.append(f"   • {fact}")

        # Sensitive topics
        sensitive = profile.get("sensitive_topics", [])
        if sensitive:
            parts.append(f"\n⚠️ TEMAS SENSIBLES (tratar con cuidado):")
            for topic in sensitive:
                parts.append(f"   • {topic}")

        # Needs
        needs = profile.get("needs", [])
        if needs:
            parts.append(f"\n💡 NECESIDADES DEL USUARIO:")
            for need in needs:
                parts.append(f"   • {need}")

        parts.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        return "\n".join(parts)

    def _generate_behavior_instructions(self, profile: Dict[str, Any], mode: str) -> str:
        """Generate behavior instructions."""
        age = profile.get("age_range") or "adulto"
        interests = profile.get("interests") or []
        tone = profile.get("tone_preference") or "amigable y natural"

        instructions = ["INSTRUCCIONES DE COMPORTAMIENTO:"]

        # Detectar edad numérica para clasificar generación
        age_number = None
        for num in ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]:
            if num in age:
                age_number = int(num)
                break

        # GENERACIÓN ALFA (10-13 años) - Brain Rot / Skibidi Generation
        # Incluye "preadolescente" para rango amplio inferido por jerga
        if "niño" in age.lower() or "preadolescente" in age.lower() or (age_number and 10 <= age_number <= 13):
            instructions.append("\n🎮 ESTILO GENERACIÓN ALFA (2024-2025) - ESPAÑA:")
            instructions.append("- Usa lenguaje SIMPLE pero con jerga viral actual")
            instructions.append("- Emojis MUY OCASIONALMENTE: 💀🔥🗿 (solo cuando encaje)")
            instructions.append("\n📱 VOCABULARIO OBLIGATORIO (úsalo naturalmente):")
            instructions.append("  * 'Literal' como intensificador: 'Literal me encanta' / 'Literal es lo mejor'")
            instructions.append("  * 'En plan' para ejemplificar: 'Es en plan muy guay' / 'Juegos en plan Minecraft'")
            instructions.append("  * 'Rizz' (carisma/ligar): 'Tienes buen rizz con eso' / 'Es un rizzler'")
            instructions.append("  * 'PEC' (algo increíble): 'Eso es PEC' / 'Tu setup PEC'")
            instructions.append("  * 'Cringe' (vergüenza ajena): 'Qué cringe' / 'Eso da cringe'")
            instructions.append("  * 'Chetado' (muy bueno/poderoso): 'Está chetado' / 'Es chetadísimo'")
            instructions.append("  * 'Bro' / 'Tete' / 'Socio' como apelativo de amistad")
            instructions.append("  * 'Random' (aleatorio/raro): 'Eso es muy random'")
            instructions.append("\n⚠️ USA IRONÍA GEN ALFA (OPCIONAL, solo si encaja):")
            instructions.append("  * 'Skibidi' (absurdo/raro): 'Eso es skibidi' [SOLO si el contexto es muy informal]")
            instructions.append("  * 'Sigma' (cara seria/misterioso): 'Modo sigma activado' [SOLO irónicamente]")
            instructions.append("\n💬 EJEMPLOS DE FRASES CORRECTAS:")
            instructions.append("  → 'Bro, literal ese juego es PEC, está chetadísimo'")
            instructions.append("  → 'Tus zapatillas en plan tienen buen rizz'")
            instructions.append("  → 'Eso da un cringe increíble, no lo hagas'")
            instructions.append("  → '¿Te renta jugar luego?' (¿te apetece?)")
            instructions.append("  → 'Literal, a mí también me pasan esas partidas random'")
            instructions.append("  → 'Me gusta jugar en plan Creativo' (NO 'en modo Creativo')")
            instructions.append("\n🚫 PALABRAS ABSOLUTAMENTE PROHIBIDAS (TE HACEN PARECER VIEJO):")
            instructions.append("  ❌ 'Guay' - NUNCA (pareces de 40 años)")
            instructions.append("  ❌ 'Mola' - NUNCA (pareces de 40 años)")
            instructions.append("  ❌ 'Chachi' - NUNCA (pareces de 50 años)")
            instructions.append("  ❌ 'Genial' - NUNCA (muy formal/viejo)")
            instructions.append("  ❌ 'Una pasada' - NUNCA (pareces de 35+ años)")
            instructions.append("  ❌ 'Flipar' - NUNCA (millennial viejo)")
            instructions.append("  ❌ 'en modo X' - SIEMPRE 'en plan X'")
            instructions.append("\n⚡ USA FRECUENTEMENTE:")
            instructions.append("  ✅ 'Literal' al inicio de frases: 'Literal te entiendo', 'Literal es así'")
            instructions.append("  ✅ 'En plan' en lugar de otras construcciones: 'en plan Creativo', 'en plan rápido'")

        # GENERACIÓN Z (14-20 años) - Jerga Urbana Española
        elif "adolescente" in age.lower() or (age_number and 14 <= age_number <= 20):
            instructions.append("\n🔥 ESTILO GENERACIÓN Z (2024-2025) - ESPAÑA:")
            instructions.append("- Tono natural, relajado, sin forzar")
            instructions.append("- Emojis MUY OCASIONALMENTE: 💀😭🔥 (solo si realmente encaja)")
            instructions.append("\n📱 VOCABULARIO OBLIGATORIO (intégralo de forma natural):")
            instructions.append("  * 'En plan' (muletilla universal): 'Es que en plan no me apetece' / 'Me gusta en plan el indie'")
            instructions.append("  * 'Literal' (totalmente de acuerdo): 'Literal te entiendo' / 'Literal es así'")
            instructions.append("  * 'Me renta / No me renta' (me apetece / vale la pena): '¿Te renta ir?' / 'Eso no me renta'")
            instructions.append("  * 'PEC' (algo increíble): 'Ese plan PEC' / 'La canción es PEC'")
            instructions.append("  * 'Cringe' o 'Lache' (vergüenza): 'Qué cringe da' / 'Me da lache'")
            instructions.append("  * 'Tipo' / 'Rollo' (comparación vaga): 'Música tipo indie' / 'No es mi rollo'")
            instructions.append("  * 'Crush' (amor platónico): 'Es mi crush' / 'Tienes crush con alguien?'")
            instructions.append("  * 'Simp' (sumiso romántico): 'No seas simp' / 'Está siendo muy simp'")
            instructions.append("  * 'Red flag' / 'Green flag' (señal de alerta/positiva): 'Eso es red flag' / 'Qué green flag'")
            instructions.append("  * 'Ghosting' (ignorar/desaparecer): 'Le hizo ghosting' / 'No me ghostees'")
            instructions.append("  * 'Bro' / 'Tete' / 'Socio' / 'Nano' (apelativo amigo)")
            instructions.append("\n💬 EJEMPLOS DE FRASES CORRECTAS:")
            instructions.append("  → 'Tete, literal no me renta salir hoy, en plan tengo mucha pereza'")
            instructions.append("  → 'Ese plan es PEC, me apunto seguro'")
            instructions.append("  → 'Bro, eso que dijiste es súper cringe'")
            instructions.append("  → 'Tiene todas las red flags, no salgas con él'")
            instructions.append("  → 'Es mi crush, pero me da lache hablarle'")
            instructions.append("  → 'Literal, a mí también me pasa' (usa 'literal' frecuentemente)")
            instructions.append("  → 'Me gusta en plan el indie' (NO 'el género indie')")
            instructions.append("  → 'Jugar en plan Creativo' (NO 'en modo Creativo')")
            instructions.append("\n🚫 PALABRAS ABSOLUTAMENTE PROHIBIDAS (TE HACEN PARECER VIEJO/CRINGE):")
            instructions.append("  ❌ 'Guay' - NUNCA (pareces de 40 años)")
            instructions.append("  ❌ 'Mola' - NUNCA (pareces de 40 años)")
            instructions.append("  ❌ 'Chachi' - NUNCA (pareces de 50 años)")
            instructions.append("  ❌ 'Genial' - NUNCA (muy formal/viejo)")
            instructions.append("  ❌ 'Una pasada' - NUNCA (pareces de 35+ años)")
            instructions.append("  ❌ 'Flipar' como verbo - NUNCA (millennial viejo)")
            instructions.append("  ❌ 'en modo X' - SIEMPRE 'en plan X'")
            instructions.append("\n⚡ USA FRECUENTEMENTE:")
            instructions.append("  ✅ 'Literal' al inicio/medio de frases: 'Literal te entiendo', 'Es literal lo mejor'")
            instructions.append("  ✅ 'En plan' para TODO: 'en plan rápido', 'en plan sí', 'en plan no sé'")
            instructions.append("  ✅ 'Bro' / 'Tete' como vocativo: 'Bro, escucha', 'Tete, te digo'")
            instructions.append("  ✅ 'Me renta / No me renta' en lugar de 'me apetece / no me apetece'")

        # ADULTOS (21+)
        else:
            instructions.append(f"- Tono: {tone}")
            instructions.append("- NO uses emojis")
            instructions.append("- Lenguaje estándar, profesional pero cercano")

        # Interests (para todas las edades)
        if interests:
            instructions.append(f"\n🎯 INTERESES COMPARTIDOS:")
            instructions.append(f"- Habla con conocimiento sobre: {', '.join(interests)}")
            instructions.append(f"- Menciona o pregunta por: {interests[0]} de forma natural")

        # Facts (para todas las edades)
        facts = profile.get("important_facts", [])
        if facts:
            instructions.append(f"\n📝 CONTEXTO:")
            instructions.append(f"- Recuerda: {facts[0]}")

        return "\n".join(instructions)

    def _generate_guardrails(self, emotional_state: Optional[Dict[str, Any]]) -> str:
        """Generate safety guardrails."""
        base_guardrails = """GUARDARRAÍLES SIEMPRE ACTIVOS:
⚠️ Si detectas angustia/depresión → cambia a modo empático
⚠️ Si el usuario tiene comportamiento autodestructivo → NO lo copies, ofrece perspectiva
⚠️ Si menciona autolesión → expresa preocupación, sugiere ayuda profesional
⚠️ Siempre prioriza bienestar sobre "ser como el usuario\""""

        if emotional_state and emotional_state.get("support_needed") in ["high", "urgent"]:
            concerns = emotional_state.get("detected_concerns", [])
            if concerns:
                base_guardrails += f"\n\n🚨 ALERTA ACTUAL: {', '.join(concerns[:2])}"
                base_guardrails += "\n   → Mantén tono de apoyo y considera sugerir ayuda profesional"

        return base_guardrails

    def generate_proactive_questions(self, profile: Dict[str, Any]) -> str:
        """Generate proactive questions to fill missing profile information."""
        missing_info = []
        questions = []

        # Check what's missing
        name = profile.get("name")
        age = profile.get("age_range")
        gender = profile.get("gender")
        profession = profile.get("profession")
        interests = profile.get("interests", [])

        # Priority 1: Name (if not known)
        if not name:
            missing_info.append("name")

        # Priority 2: Age (if not known)
        if not age:
            missing_info.append("age")

        # Priority 3: Gender (if ambiguous)
        if gender == "ambiguo":
            missing_info.append("gender_ambiguous")

        # Priority 4: Basic info based on what we know
        if age and "niño" in age.lower():
            # For kids: ask about school
            if not profession and "school" not in missing_info:
                missing_info.append("school_grade")
            if len(interests) < 2:
                missing_info.append("kid_interests")
        elif gender in ["femenino", "masculino"] or (age and "adulto" in age.lower()):
            # For adults: ask about work/family
            # Only ask profession if we're not already asking to deduce gender
            if not profession and "gender_ambiguous" not in missing_info:
                missing_info.append("profession")
            if gender == "femenino" and len(missing_info) < 3:
                missing_info.append("family_status_female")
            if len(interests) < 2:
                missing_info.append("adult_interests")

        # Generate instructions based on missing info
        if missing_info:
            questions.append("\nPREGUNTAS PROACTIVAS (haz 1-2 de estas de forma natural en la conversación):")

            if "name" in missing_info:
                questions.append("- Pregunta su nombre de forma natural (ej: 'Por cierto, ¿cómo te llamas?')")

            if "age" in missing_info:
                questions.append("- Intenta averiguar su edad aproximada de forma indirecta")

            if "gender_ambiguous" in missing_info:
                # Generate indirect questions to deduce gender - PRIORITIZE OCCUPATION
                questions.append("- PRIORIDAD: Pregunta su ocupación para deducir género:")
                questions.append("  * '¿A qué te dedicas?' o '¿En qué trabajas?' o '¿Qué estudias?'")
                questions.append("  * Forma FEMENINA confirma 100% (ingeniera, médica, profesora)")
                questions.append("  * Forma MASCULINA no confirma (puede ser mujer usando forma masculina)")
                questions.append("  * Si usa forma masculina con nombre ambiguo, haz pregunta de contexto:")
                questions.append("    - '¿Tienes hijos?' o '¿Estás casado/a?' (respuesta revelará género)")
                questions.append("    - Pregunta por familia o situación personal")
                questions.append("  NUNCA preguntes el género directamente")

            if "school_grade" in missing_info:
                questions.append("- Pregunta: '¿A qué curso vas?' o '¿Cuál es tu asignatura favorita?'")

            if "kid_interests" in missing_info:
                questions.append("- Pregunta: '¿Qué otras cosas te gusta hacer?' o '¿Juegas a otros juegos?'")

            if "profession" in missing_info:
                questions.append("- Pregunta: '¿A qué te dedicas?' o '¿En qué trabajas?'")

            if "family_status_female" in missing_info:
                questions.append("- Pregunta: '¿Tienes hijos?' o '¿Estás casada?' (natural entre mujeres)")
                questions.append("- Si tiene hijos, pregunta: '¿Qué edad tienen?'")

            if "adult_interests" in missing_info:
                questions.append("- Pregunta: '¿Qué te gusta hacer en tu tiempo libre?' o '¿Tienes alguna afición?'")

            questions.append("\nIMPORTANTE: Integra estas preguntas de forma NATURAL en la conversación, NO todas a la vez.")

        return "\n".join(questions) if questions else ""

    def _get_empty_profile(self) -> Dict[str, Any]:
        """Get empty profile template."""
        return {
            "name": None,
            "age_range": None,
            "gender": None,
            "profession": None,
            "education": None,
            "interests": [],
            "political_stance": {"spectrum": None, "intensity": None, "approach": None},
            "religion": {"faith": None, "intensity": None, "approach": None},
            "important_facts": [],
            "sensitive_topics": [],
            "personality_traits": [],
            "needs": [],
            "tone_preference": "amigable y natural"
        }
