from fastapi import APIRouter, HTTPException

from app.modules.gliner.schemas import (
    GLiNERConfiguredRequest,
    GLiNERConfiguredResponse,
    GLiNERRequest,
    GLiNERResponse,
    GLiNERUseCaseListResponse,
)
from app.modules.gliner.service import extract_entities, extract_entities_configured, list_use_cases

router = APIRouter(prefix="/extract", tags=["GLiNER"])


@router.post("/gliner", response_model=GLiNERResponse)
def run_gliner(request: GLiNERRequest) -> GLiNERResponse:
    """Backward-compatible endpoint that accepts explicit labels."""

    entities = extract_entities(request.text, request.labels)
    return GLiNERResponse(entities=entities)


@router.get("/gliner/use-cases", response_model=GLiNERUseCaseListResponse)
def get_gliner_use_cases() -> GLiNERUseCaseListResponse:
    return GLiNERUseCaseListResponse(use_cases=list_use_cases())


@router.post("/gliner/configured", response_model=GLiNERConfiguredResponse)
def run_gliner_configured(request: GLiNERConfiguredRequest) -> GLiNERConfiguredResponse:
    try:
        return extract_entities_configured(
            text=request.text,
            use_case=request.use_case,
            labels=request.labels,
            processing_overrides=request.processing_overrides,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
