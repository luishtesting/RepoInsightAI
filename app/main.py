from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="RepoInsight AI")

@app.get("/")
def read_root():
    return {"message": "RepoInsight AI API is running"}

@app.get("/analyze/{user}/{repo}")
async def analyze_repo(user: str, repo: str):
    github_url = f"https://api.github.com/repos/{user}/{repo}"
    
    # Usamos httpx para peticiones asíncronas (moderno y eficiente)
    async with httpx.AsyncClient() as client:
        response = await client.get(github_url)
        
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Repositorio no encontrado")
            
        data = response.json()
        
        # De momento, devolvemos datos básicos para probar
        return {
            "name": data["name"],
            "stars": data["stargazers_count"],
            "language": data["language"],
            "description": data["description"]
        }