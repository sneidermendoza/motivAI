import os
import requests
from dotenv import load_dotenv
import json
import re

# Cargar variables de entorno
load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama3-70b-8192')
GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions'

print("[DEBUG] GROQ_API_KEY:", GROQ_API_KEY)  # Log temporal para depuración
print("[DEBUG] GROQ_MODEL:", repr(GROQ_MODEL))  # Log temporal para depuración

def build_training_plan_prompt(user_data):
    prompt = f"""
Eres una entrenadora personal experta en salud, fitness y motivación. Tu tarea es crear un plan de entrenamiento semanal completamente personalizado para el siguiente usuario, teniendo en cuenta todos sus datos, objetivos, contexto y cualquier información adicional que desee agregar.

Datos del usuario:
- Edad: {user_data.get('age', 'No especificado')}
- Sexo: {user_data.get('gender', 'No especificado')}
- Peso: {user_data.get('weight', 'No especificado')} kg
- Altura: {user_data.get('height', 'No especificado')} cm
- Motivación principal: {user_data.get('motivation', 'No especificado')}
- Condiciones médicas relevantes: {user_data.get('medical_conditions', 'Ninguna')}
- Lesiones o limitaciones físicas: {user_data.get('injuries', 'Ninguna')}
- Frecuencia de ejercicio actual: {user_data.get('exercise_frequency', 'No especificado')}
- Nivel de experiencia: {user_data.get('experience_level', 'No especificado')}
- Objetivo(s) específico(s): {user_data.get('specific_goals', 'No especificado')}
- Tiempo objetivo para lograrlo: {user_data.get('timeline', 'No especificado')}
- Información adicional proporcionada por el usuario: {user_data.get('additional_info', 'Ninguna')}

Por favor, diseña un plan semanal detallado y realista, adaptado a su nivel y objetivos, que incluya:
- Días de la semana y tipo de entrenamiento (cardio, fuerza, flexibilidad, descanso, etc.)
- Duración y descripción de cada sesión
- Notas o recomendaciones específicas para cada día
- Consejos generales de salud, motivación y recuperación
- Precauciones si hay condiciones médicas o lesiones

Formato de respuesta:
Devuelve SOLO un JSON estructurado así (no agregues texto fuera del JSON):

{{
  "plan": [
    {{
      "day": "Lunes",
      "workout": "Cardio moderado (caminata rápida 40 min)",
      "notes": "Mantener ritmo constante, hidratarse bien"
    }},
    {{
      "day": "Martes",
      "workout": "Fuerza: circuito de tren superior (30 min)",
      "notes": "Enfocarse en técnica, usar peso moderado"
    }}
    // ... resto de la semana
  ],
  "recommendations": [
    "Descansar al menos 7 horas por noche",
    "Mantenerse hidratado durante todo el día",
    "Consultar a un médico antes de iniciar cualquier rutina si tiene dudas"
  ]
}}
"""
    return prompt

def generate_training_plan_with_groq(user_data):
    """
    Llama a la API de Groq para generar un plan personalizado.
    user_data: dict con los datos del usuario y contexto.
    Devuelve el JSON del plan generado o un error claro.
    """
    prompt = build_training_plan_prompt(user_data)
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "Eres una entrenadora personal experta en salud, fitness y motivación. Responde siempre en JSON."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1024,
        "temperature": 0.7
    }
    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=60)
    except requests.exceptions.ReadTimeout:
        print("[GROQ TIMEOUT] La petición a la IA superó el tiempo de espera.")
        return {"error": "La petición a la IA superó el tiempo de espera (timeout). Intenta de nuevo en unos minutos o prueba con otro modelo.", "status_code": 504}
    except Exception as e:
        print("[GROQ REQUEST ERROR]", e)
        return {"error": f"Error inesperado al conectar con la IA: {str(e)}", "status_code": 500}
    print("[GROQ API STATUS]", response.status_code)
    try:
        data = response.json()
        print("[GROQ RAW RESPONSE]", data)
        if response.status_code == 200:
            content = data['choices'][0]['message']['content']
            # Extraer el JSON del string usando regex
            match = re.search(r'\{[\s\S]*\}', content)
            if match:
                try:
                    return json.loads(match.group(0))
                except Exception as e:
                    print("[GROQ JSON PARSE ERROR]", e)
                    return {"error": "La IA respondió pero el JSON no es válido.", "raw": content}
            else:
                return {"error": "No se encontró un JSON válido en la respuesta de la IA.", "raw": content}
        else:
            return {"error": data.get('error', {}).get('message', 'Error desconocido de la API de Groq.'), "status_code": response.status_code}
    except Exception as e:
        print("[GROQ RESPONSE ERROR]", e)
        return {"error": f"Error inesperado al procesar la respuesta de la IA: {str(e)}", "status_code": 500} 