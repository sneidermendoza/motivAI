import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama3-8b-8192')
GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions'

EXTRACTION_PROMPT = '''
Eres un asistente experto en fitness. Extrae y valida los siguientes datos del mensaje del usuario. Si falta algún dato, indícalo en el campo "missing_fields". Devuelve SOLO un JSON válido con esta estructura:
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
  "missing_fields": [str]
}
Ejemplo de mensaje del usuario:
"Tengo 32 años, peso 80kg, mido 175cm, soy hombre, quiero perder grasa, entreno 3 veces por semana en casa, no tengo lesiones."
'''

def extract_fitness_data_with_groq(message):
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json',
    }
    prompt = EXTRACTION_PROMPT + f"\nMensaje del usuario:\n{message}\n"
    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "Eres un asistente de fitness que responde solo con JSON válido."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 512
    }
    try:
        response = requests.post(GROQ_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        # Extraer solo el JSON (por si la IA agrega texto extra)
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        json_str = content[json_start:json_end]
        result = json.loads(json_str)
        return result
    except Exception as e:
        return {"error": str(e)} 