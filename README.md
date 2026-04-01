# 🚀 RepoInsight AI

Analizador inteligente de repositorios de GitHub utilizando **FastAPI** y **LLMs (Llama 3.1)**. 

Este proyecto demuestra el uso de arquitecturas asíncronas en Python para coordinar múltiples APIs externas y procesar datos estructurados con IA.

## 🛠️ Tecnologías utilizadas
* **Python 3.12+**
* **FastAPI**: Framework web de alto rendimiento.
* **Httpx**: Cliente HTTP asíncrono para llamadas a APIs.
* **Pydantic v2**: Validación de datos y esquemas.
* **Groq Cloud API**: Inferencia de modelos de lenguaje (Llama 3.1).
* **GitHub REST API**: Extracción de metadatos de repositorios.

## 🏗️ Arquitectura
El proyecto sigue principios de **Clean Architecture**, separando la lógica de negocio (Servicios) de los puntos de entrada (Rutas).



## 🚀 Cómo ejecutarlo
1. Clona el repositorio.
2. Crea un entorno virtual: `python -m venv venv`.
3. Instala dependencias: `pip install -r requirements.txt`.
4. Configura tu `.env` con `GROQ_API_KEY`.
5. Ejecuta: `uvicorn app.main:app --reload`.

## 📊 Ejemplo de salida
Accediendo a `/analyze/user/repo`, obtendrás una auditoría técnica generada por IA sobre la salud y utilidad del proyecto.