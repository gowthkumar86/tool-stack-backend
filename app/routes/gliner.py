from fastapi import APIRouter
from pydantic import BaseModel
from app.services.gliner_service import extract_entities

router = APIRouter()

class GLiNERRequest(BaseModel):
    text: str
    labels: list[str]

@router.post("/gliner")
def run_gliner(request: GLiNERRequest):
    result = extract_entities(request.text, request.labels)
    return {"entities": result}