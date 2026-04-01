from pydantic import BaseModel

class AnalysisResponse(BaseModel):
    github_stats: dict
    ai_insight: dict