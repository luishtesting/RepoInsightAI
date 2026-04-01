from fastapi import FastAPI, HTTPException
import httpx
from app.services.ai_service import get_repo_analysis  # <--- Importación clave
import json
from app.schemas.project_schema import AnalysisResponse
from app.utils.analyzer import analyze_python_code

app = FastAPI(title="RepoInsight AI")

@app.get("/analyze/{user}/{repo}", response_model=AnalysisResponse)
async def analyze_repo(user: str, repo: str):
    async with httpx.AsyncClient() as client:
        # 1. Metadatos básicos
        res = await client.get(f"https://api.github.com/repos/{user}/{repo}")
        if res.status_code != 200:
            raise HTTPException(status_code=404, detail="Repo no encontrado")
        repo_info = res.json()

        # 2. BÚSQUEDA RECURSIVA DE CÓDIGO (La mejora)
        # Usamos la API de "Trees" con recursive=1 para ver TODO el árbol
        default_branch = repo_info.get("default_branch", "main")
        tree_res = await client.get(
            f"https://api.github.com/repos/{user}/{repo}/git/trees/{default_branch}?recursive=1"
        )
        
        code_stats = {"note": "No se encontró código Python"}
        
        if tree_res.status_code == 200:
            tree_data = tree_res.json()
            # Buscamos el primer archivo .py, esté donde esté (evitando carpetas ocultas)
            py_files = [
                item for item in tree_data.get("tree", []) 
                if item["path"].endswith(".py") and "test" not in item["path"].lower()
            ]
            
            if py_files:
                # Tomamos el primero (o el que parezca más importante)
                target_file = py_files[0]
                # Para descargar el contenido crudo usamos la URL de "raw"
                raw_url = f"https://raw.githubusercontent.com/{user}/{repo}/{default_branch}/{target_file['path']}"
                file_res = await client.get(raw_url)
                
                if file_res.status_code == 200:
                    code_stats = analyze_python_code(file_res.text)
                    code_stats["file_analyzed"] = target_file["path"]

        # 3. Preparar datos para la IA (Asegúrate de incluir 'stars')
        data_to_analyze = {
            "name": repo_info["name"],
            "stars": repo_info.get("stargazers_count", 0), # <--- ESTO FALTABA
            "language": repo_info.get("language", "Unknown"),
            "description": repo_info.get("description", "Sin descripción"),
            "metrics": code_stats
        }

        ai_review_raw = await get_repo_analysis(data_to_analyze)
        
        return {
            "github_stats": data_to_analyze,
            "ai_insight": json.loads(ai_review_raw)
        }