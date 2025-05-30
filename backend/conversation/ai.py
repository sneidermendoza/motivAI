import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama3-70b-8192')
GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions'

EXTRACTION_PROMPT = '''
Eres un entrenador personal experto en fitness y motivación, con un tono cálido y empático. Tu objetivo es guiar una conversación natural para crear un plan de entrenamiento personalizado, haciendo que el usuario se sienta cómodo y motivado.

REGLAS FUNDAMENTALES:
1. SIEMPRE mantén un tono conversacional, amigable y motivador.
2. NUNCA listes campos faltantes ni uses frases técnicas.
3. Personaliza cada pregunta usando la información que ya tienes del usuario.
4. Haz una sola pregunta a la vez, enfocándote en el dato más relevante según el contexto.

EXTRACCIÓN DE DATOS:
Extrae y valida estos datos del mensaje del usuario:
- edad (número entero)
- sexo (masculino/femenino/otro)
- peso (número decimal en kg)
- altura (número decimal en cm)
- objetivo (texto)
- motivación (texto)
- nivel_actividad (texto)
- restricciones (texto)
- frecuencia_ejercicio (texto)
- nivel_experiencia (texto)
- dias_entrenar (número)
- lugar_entrenamiento (texto)

MANEJO DE RESPUESTAS:

1. Si la respuesta NO está relacionada con salud/ejercicio:
   Devuelve todos los campos como null y en "message" pon EXACTAMENTE:
   "Tu respuesta no está relacionada con salud, ejercicio o motivación. Por favor, cuéntame sobre tus objetivos o motivaciones para mejorar tu salud o condición física."

2. Si ya tienes TODOS los datos:
   En "message" pon:
   "¡Excelente! Ya tengo toda la información para crear tu plan personalizado. ¿Te gustaría que empecemos a diseñarlo?"

3. Si faltan datos:
   - Analiza qué datos ya tienes y cuáles son más relevantes según el contexto.
   - Formula una pregunta natural y personalizada usando la información que ya tienes.
   - Ejemplos de preguntas naturales:
     * Si ya sabes la motivación: "¡Me encanta tu motivación de sentirte más enérgico! Para personalizar tu plan, ¿podrías decirme tu edad y peso actual?"
     * Si ya sabes el objetivo: "¡Genial que quieras bajar de peso! ¿Con qué frecuencia podrías entrenar y dónde te gustaría hacerlo?"
     * Si ya sabes la frecuencia: "¡Perfecto que puedas entrenar 3 veces por semana! ¿Tienes experiencia previa con el ejercicio?"

4. Si la respuesta es ambigua o incompleta:
   - Pide aclaración de forma amable y específica.
   - Ejemplo: "Entiendo que quieres mejorar tu salud. ¿Podrías ser más específico sobre qué te gustaría lograr? Por ejemplo, ¿bajar de peso, ganar músculo, mejorar tu resistencia?"

ESTRUCTURA DE RESPUESTA:
Devuelve SOLO un JSON con esta estructura:
{
  "edad": int | null,
  "sexo": "masculino"|"femenino"|"otro"|null,
  "peso": float | null,
  "altura": float | null,
  "objetivo": str | null,
  "motivacion": str | null,
  "nivel_actividad": str | null,
  "restricciones": str | null,
  "frecuencia_ejercicio": str | null,
  "nivel_experiencia": str | null,
  "dias_entrenar": int | null,
  "lugar_entrenamiento": str | null,
  "otros": dict | null,
  "message": str
}

IMPORTANTE:
- El campo "message" DEBE ser una pregunta o comentario conversacional natural.
- NUNCA uses frases como "faltan los siguientes datos" o "por favor proporciona".
- SIEMPRE personaliza la pregunta usando la información que ya tienes del usuario.
- MANTÉN un tono motivador y empático en todo momento.
'''

def extract_fitness_data_with_groq(message, context=None):
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json',
    }
    
    # Construir el contexto de datos ya recolectados
    context_str = ""
    if context and 'collected_data' in context:
        collected = context['collected_data']
        context_str = "\nDatos ya recolectados:\n"
        for key, value in collected.items():
            if value and key != 'message':
                context_str += f"- {key}: {value}\n"
    
    prompt = EXTRACTION_PROMPT + f"\n{context_str}\nMensaje del usuario:\n{message}\n"
    
    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "Eres un asistente de fitness que responde SOLO con JSON válido. NO agregues texto adicional antes o después del JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 512
    }
    
    try:
        response = requests.post(GROQ_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        
        # Limpiar el contenido para asegurar que solo tenemos JSON
        content = content.strip()
        if not content.startswith('{'):
            content = content[content.find('{'):]
        if not content.endswith('}'):
            content = content[:content.rfind('}')+1]
            
        result = json.loads(content)
        
        # Validar que tenemos los campos requeridos
        required_fields = ['message']
        for field in required_fields:
            if field not in result:
                result[field] = None
                
        # Mantener los datos ya recolectados
        if context and 'collected_data' in context:
            for key, value in context['collected_data'].items():
                if value and key != 'message':
                    result[key] = value
                
        return result
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON inválido: {str(e)}")
        print(f"[DEBUG] Contenido recibido: {content}")
        return {
            "message": "Tu respuesta no está relacionada con salud, ejercicio o motivación. Por favor, cuéntame sobre tus objetivos o motivaciones para mejorar tu salud o condición física.",
            "edad": None,
            "sexo": None,
            "peso": None,
            "altura": None,
            "objetivo": None,
            "motivacion": None,
            "nivel_actividad": None,
            "restricciones": None,
            "frecuencia_ejercicio": None,
            "nivel_experiencia": None,
            "dias_entrenar": None,
            "lugar_entrenamiento": None,
            "otros": None
        }
    except Exception as e:
        print(f"[ERROR] Error en extract_fitness_data_with_groq: {str(e)}")
        return {
            "message": "Tu respuesta no está relacionada con salud, ejercicio o motivación. Por favor, cuéntame sobre tus objetivos o motivaciones para mejorar tu salud o condición física.",
            "edad": None,
            "sexo": None,
            "peso": None,
            "altura": None,
            "objetivo": None,
            "motivacion": None,
            "nivel_actividad": None,
            "restricciones": None,
            "frecuencia_ejercicio": None,
            "nivel_experiencia": None,
            "dias_entrenar": None,
            "lugar_entrenamiento": None,
            "otros": None
        }