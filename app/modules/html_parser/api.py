from fastapi import APIRouter, Body, File, HTTPException, UploadFile

from app.modules.html_parser.schemas import HTMLParseRequest, HTMLParseResponse
from app.modules.html_parser.service import parse_html

router = APIRouter(prefix="/extract", tags=["HTML Parser"])


@router.post("/html", response_model=HTMLParseResponse)
def run_html_parser(request: HTMLParseRequest) -> HTMLParseResponse:
    return parse_html(request.html)


@router.post("/html/raw", response_model=HTMLParseResponse)
def run_html_parser_raw(
    html: str = Body(..., media_type="text/plain", description="Paste raw HTML source directly."),
) -> HTMLParseResponse:
    if not html.strip():
        raise HTTPException(status_code=400, detail="HTML content is empty.")
    return parse_html(html)


@router.post("/html/file", response_model=HTMLParseResponse)
async def run_html_parser_file(file: UploadFile = File(...)) -> HTMLParseResponse:
    raw_bytes = await file.read()
    if not raw_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    html = raw_bytes.decode("utf-8", errors="ignore").strip()
    if not html:
        raise HTTPException(status_code=400, detail="Unable to read HTML text from uploaded file.")

    return parse_html(html)
