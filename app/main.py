from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import store_hygiene, champion, chatbot
from app.models.schemas import HealthResponse

app = FastAPI(
    title="AI/ML Service — Scheduling Project",
    description="AI microservice for Store Hygiene and Champion Development audit modules",
    version="1.0.0"
)

# Allow all origins for development (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(store_hygiene.router)
app.include_router(champion.router)
app.include_router(chatbot.router)

@app.get("/api/v1/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    return HealthResponse(status="ok", service="ai_ml_service", version="1.0.0")