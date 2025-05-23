import requests
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama3-8b-8192')
GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions'

headers = {
    'Authorization': f'Bearer {GROQ_API_KEY}',
    'Content-Type': 'application/json'
}

payload = {
    "model": GROQ_MODEL,
    "messages": [
        {"role": "system", "content": "Eres una entrenadora personal experta en salud, fitness y motivación. Responde siempre en JSON."},
        {"role": "user", "content": "Crea un plan semanal de entrenamiento personalizado para un hombre de 28 años, 80kg, 175cm, principiante, que quiere bajar 5kg en 3 meses. Devuelve solo un JSON con el plan y recomendaciones."}
    ],
    "max_tokens": 512,
    "temperature": 0.7
}

response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=60)
print("Status code:", response.status_code)
try:
    print("Respuesta:", response.json())
except Exception as e:
    print("Error al parsear la respuesta:", e)
    print("Texto bruto:", response.text) 