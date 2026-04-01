import httpx
import os
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

async def get_repo_analysis(repo_data: dict):
    """
    Envía los metadatos del repo a la IA para obtener un veredicto profesional.
    """
    
    # IMPORTANTE: Cuando usas response_format JSON, el prompt DEBE pedir JSON
    prompt = f"""
    Eres un experto en auditoría de código. Analiza este repositorio:
    Nombre: {repo_data['name']}
    Lenguaje: {repo_data['language']}
    Estrellas: {repo_data['stars']}
    Descripción: {repo_data['description']}
    
    Responde exclusivamente en formato JSON con esta estructura:
    {{
        "resumen": "Tu análisis en 2 frases",
        "puntuacion_mantenimiento": 8
    }}
    """

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Usamos llama-3.1-8b-instant que es el modelo más estable y gratuito actualmente
    payload = {
        "model": "llama-3.1-8b-instant", 
        "messages": [
            {
                "role": "system", 
                "content": "Eres un asistente que solo responde en formato JSON."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.5
    }

    async with httpx.AsyncClient() as client:
        try:
            # Timeout de 10 segundos por si la IA tarda en pensar
            response = await client.post(GROQ_URL, headers=headers, json=payload, timeout=10.0)
            
            # Verificamos si la API de Groq devolvió un error (401, 404, 429...)
            if response.status_code != 200:
                error_msg = response.text
                print(f"Error de Groq: {error_msg}")
                return json.dumps({
                    "error": f"Error de API Groq (Status: {response.status_code})",
                    "details": error_msg
                })

            data = response.json()
            
            # Verificación de seguridad para evitar el KeyError 'choices'
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            else:
                return json.dumps({
                    "error": "Respuesta inesperada de la IA",
                    "raw_response": data
                })

        except httpx.ConnectError:
            return json.dumps({"error": "No se pudo conectar con el servidor de Groq"})
        except Exception as e:
            return json.dumps({"error": f"Error inesperado: {str(e)}"})