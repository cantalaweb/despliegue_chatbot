"""
LLM Service module for interacting with OpenAI API.
Handles chat completions, emotional analysis, and profile extraction.
"""

import os
import json
from typing import List, Dict, Any, Optional
from openai import OpenAI


class LLMService:
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the LLM service.

        Args:
            api_key: OpenAI API key. If None, will try to get from environment.
            model: The OpenAI model to use.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided and not found in environment")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.system_prompt = """Eres un asistente conversacional inteligente y amigable.
Tienes acceso al historial completo de la conversación con cada usuario, lo que te permite:
- Recordar información mencionada anteriormente
- Mantener el contexto de conversaciones previas
- Hacer referencias a temas discutidos en el pasado
- Proporcionar respuestas coherentes y personalizadas

Sé natural, útil y demuestra que recuerdas la conversación."""

    def chat(self, messages: List[Dict[str, str]], max_tokens: int = 500) -> Dict[str, Any]:
        """
        Generate a chat completion.

        Args:
            messages: List of message dicts with 'role' and 'content' keys.
            max_tokens: Maximum tokens in the response.

        Returns:
            Dict with 'content' (response text) and 'usage' (token usage info).
        """
        # Build messages array with system prompt
        chat_messages = [{"role": "system", "content": self.system_prompt}]

        # Add conversation history
        for msg in messages:
            chat_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=chat_messages,
                max_tokens=max_tokens,
                temperature=0.7
            )

            return {
                "content": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "model": response.model
            }

        except Exception as e:
            return {
                "content": f"Error al generar respuesta: {str(e)}",
                "error": True
            }

    def chat_with_memory(self, current_message: str, history: List[Dict[str, str]],
                        max_history: int = 10) -> Dict[str, Any]:
        """
        Generate a chat completion using conversation history.

        Args:
            current_message: The current user message.
            history: Previous messages from the database.
            max_history: Maximum number of historical messages to include.

        Returns:
            Dict with response content and metadata.
        """
        # Limit history to prevent token overflow
        recent_history = history[-max_history:] if len(history) > max_history else history

        # Add current message
        messages = recent_history + [{"role": "user", "content": current_message}]

        return self.chat(messages)

    def chat_with_custom_system(self, messages: List[Dict[str, str]],
                               system_prompt: str, max_tokens: int = 500) -> Dict[str, Any]:
        """
        Generate chat completion with custom system prompt.

        Args:
            messages: List of message dicts
            system_prompt: Custom system prompt to use
            max_tokens: Maximum tokens in response

        Returns:
            Dict with response content and metadata
        """
        chat_messages = [{"role": "system", "content": system_prompt}]

        for msg in messages:
            chat_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=chat_messages,
                max_tokens=max_tokens,
                temperature=0.7
            )

            return {
                "content": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "model": response.model
            }

        except Exception as e:
            return {
                "content": f"Error: {str(e)}",
                "error": True
            }

    def analyze_emotional_state(self, conversation: List[Dict[str, str]]) -> Optional[Dict[str, Any]]:
        """
        Analyze user's emotional state using LLM as expert psychologist.

        Args:
            conversation: Recent conversation history

        Returns:
            Dict with emotional analysis or None if error
        """
        if len(conversation) < 3:
            return {"insufficient_data": True}

        # Format conversation for analysis
        conv_text = "\n".join([
            f"{'Usuario' if msg['role'] == 'user' else 'Asistente'}: {msg['content']}"
            for msg in conversation
        ])

        analysis_prompt = f"""Actúa como un PSICÓLOGO CLÍNICO EXPERTO analizando esta conversación.

IMPORTANTE:
- Basa tu análisis en EVIDENCIA observable en el texto
- Sé objetivo y profesional
- No exageres ni minimices señales
- Si la información es insuficiente, indica baja confianza

CONVERSACIÓN A ANALIZAR:
━━━━━━━━━━━━━━━━━━━━━━━━━━━
{conv_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━

EVALÚA:
1. Probabilidad de depresión (0.0-1.0)
   - Busca: desesperanza, anhedonia, fatiga, ideación suicida

2. Nivel de ansiedad (none/low/moderate/high/severe)
   - Busca: preocupación excesiva, nerviosismo, pánico

3. Nivel de soledad (none/low/moderate/high/severe)
   - Busca: aislamiento, falta de conexión, vacío emocional

4. Necesidad de apoyo (none/low/moderate/high/urgent)
   - Considera gravedad y urgencia de la situación

5. Modo recomendado:
   - normal: conversación estándar
   - friendly: amigable y cálido
   - empathetic: empático y comprensivo
   - supportive: apoyo emocional activo
   - crisis: situación de riesgo, intervención necesaria

Responde SOLO con este JSON (sin texto adicional):
{{
  "depression_probability": 0.0,
  "anxiety_level": "none",
  "loneliness_level": "none",
  "support_needed": "none",
  "recommended_mode": "normal",
  "detected_concerns": [],
  "positive_indicators": [],
  "confidence": 0.0,
  "professional_help_suggested": false,
  "notes": ""
}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": analysis_prompt}],
                max_tokens=400,
                temperature=0.3  # Lower temperature for more consistent analysis
            )

            analysis = json.loads(response.choices[0].message.content)
            return analysis

        except Exception as e:
            print(f"Error in emotional analysis: {str(e)}")
            return None

    def generate_proactive_question(self, user_interests: List[str],
                                   news_articles: List[Dict[str, Any]],
                                   user_profile: Dict[str, Any]) -> Optional[str]:
        """
        Generate proactive conversation starter based on news.

        Args:
            user_interests: List of user's interests
            news_articles: Recent news articles
            user_profile: User's profile for tone adaptation

        Returns:
            Proactive question/greeting or None
        """
        if not news_articles or not user_interests:
            return None

        age_info = user_profile.get("age_range", "adulto")
        tone = user_profile.get("tone_preference", "amigable")

        news_text = "\n".join([
            f"- {article['title']}\n  {article['description'][:150]}..."
            for article in news_articles[:2]
        ])

        prompt = f"""Basándote en estas noticias recientes sobre {user_interests[0]}:

{news_text}

Genera UNA pregunta corta y entusiasta para iniciar conversación.

CONTEXTO DEL USUARIO:
- Edad: {age_info}
- Interés: {user_interests[0]}
- Tono preferido: {tone}

INSTRUCCIONES:
- Menciona la noticia más interesante
- Sé apropiado para la edad del usuario
- Invita a conversar
- Sé natural y {tone}
- Máximo 2 líneas

Ejemplo: "¡Ey! ¿Viste que sacaron la nueva Nintendo Switch 2? ¿Te gustaría tenerla? 😊"

Genera SOLO la pregunta (sin explicaciones):"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.8
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error generating proactive question: {str(e)}")
            return None
