from pydantic import BaseModel
from typing import Optional, Any

class AnalysisResponse(BaseModel):
    github_stats: dict
    ai_insight: dict