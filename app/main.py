from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.workflows import router as workflow_router
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Workflow Replay API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(workflow_router, prefix="/api/workflows", tags=["Workflows"])

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
