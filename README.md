# 🚀 RepoInsight AI

Analizador inteligente de repositorios de GitHub utilizando **FastAPI** y **LLMs (Llama 3.1)**. 

Este proyecto demuestra el uso de arquitecturas asíncronas en Python para coordinar múltiples APIs externas y procesar datos estructurados con IA.

## 🌟 Características Principales

* **Análisis Híbrido:** Mezcla métricas reales (conteo de clases/funciones) con interpretación semántica por IA.
* **Navegación Recursiva:** Utiliza la *GitHub Trees API* para localizar archivos fuente profundos, superando las limitaciones de búsqueda en la raíz del repositorio.
* **Motor de Análisis Estático:** Implementación del módulo `ast` de Python para inspeccionar código sin ejecución (Seguridad por diseño).
* **Arquitectura Non-Blocking:** Flujo 100% asíncrono con `FastAPI` y `httpx` para optimizar la concurrencia y reducir latencias.

## 🛠️ Tecnologías utilizadas

* **Lenguaje:** Python 3.12+ (con Type Hinting estricto).
* **Framework:** FastAPI + Uvicorn (ASGI).
* **Validación:** Pydantic v2 (Garantía de contratos de datos).
* **IA:** Groq Cloud API (Inferencia de baja latencia con Llama 3.1).
* **Cliente HTTP:** Httpx (Peticiones asíncronas concurrentes).

## 🏗️ Arquitectura

El proyecto implementa una separación clara de responsabilidades (**Separation of Concerns**):

* **Rutas (`app/main.py`):** Gestión de endpoints, validación de entrada y coordinación del flujo de datos.
* **Servicios (`app/services/`):** Lógica de integración con servicios de IA y gestión de prompts.
* **Utils (`app/utils/`):** Lógica computacional y análisis de Árboles de Sintaxis Abstracta (AST).
* **Schemas (`app/schemas/`):** Modelos de Pydantic para la serialización y validación de respuestas.

## 🚀 Cómo ejecutarlo
1. Clona el repositorio.
2. Crea un entorno virtual: `python -m venv venv`.
3. Instala dependencias: `pip install -r requirements.txt`.
4. Configura tu `.env` con `GROQ_API_KEY`.
5. Ejecuta: `uvicorn app.main:app --reload`.
Luego visita http://127.0.0.1:8000/docs para probar la API interactivamente.
¡Listo! Con esto tu repositorio se verá impecable. No olvides reemplazar `tu-usuario` en el enlace de clonación por tu nombre de usuario real de GitHub.

## 📊 Ejemplo de salida
Accediendo a `/analyze/user/repo`, obtendrás una auditoría técnica generada por IA sobre la salud y utilidad del proyecto.