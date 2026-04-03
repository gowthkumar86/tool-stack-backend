from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.router_registry import FEATURE_ROUTERS

app = FastAPI()

# CORS (so React can call this)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Feature routes
for router in FEATURE_ROUTERS:
    app.include_router(router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Toolstack Backend Running"}
