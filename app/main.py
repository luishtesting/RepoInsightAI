from fastapi import FastAPI, HTTPException
import httpx
from app.services.ai_service import get_repo_analysis  # <--- Importación clave
import json
from app.schemas.project_schema import AnalysisResponse

app = FastAPI(title="RepoInsight AI")

@app.get("/analyze/{user}/{repo}", response_model=AnalysisResponse)
async def analyze_repo(user: str, repo: str):
    github_url = f"https://api.github.com/repos/{user}/{repo}"
    
    async with httpx.AsyncClient() as client:
        # 1. Obtener datos de GitHub
        res = await client.get(github_url)
        if res.status_code != 200:
            raise HTTPException(status_code=404, detail="Repo no encontrado en GitHub")
        
        repo_info = res.json()
        data_to_analyze = {
            "name": repo_info["name"],
            "stars": repo_info["stargazers_count"],
            "language": repo_info.get("language", "Unknown"),
            "description": repo_info.get("description", "Sin descripción")
        }

        # 2. Llamar al servicio de IA (aquí es donde se usa la lógica de ai_service.py)
        try:
            ai_review_raw = await get_repo_analysis(data_to_analyze)
            ai_review = json.loads(ai_review_raw) # Convertimos el string de la IA a diccionario
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la IA: {str(e)}")
        
        return {
            "github_stats": data_to_analyze,
            "ai_insight": ai_review
        }