from pydantic import BaseModel, Field
from bson import ObjectId


class JobDocument(BaseModel):
    id: str = Field(alias="_id")
    title: str
    company: str
    location: str
    description: str
    required_skills: list[str] = []
    score: float = 0.0          # filled in by recommendation engine

    model_config = {"populate_by_name": True}