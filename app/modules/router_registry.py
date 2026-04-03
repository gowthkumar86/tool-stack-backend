from fastapi import APIRouter

from app.modules.gliner.api import router as gliner_router
from app.modules.html_parser.api import router as html_parser_router

# Central place to register feature routers.
FEATURE_ROUTERS: tuple[APIRouter, ...] = (
    gliner_router,
    html_parser_router,
)
