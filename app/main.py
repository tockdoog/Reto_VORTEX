from fastapi import FastAPI
from app.api.predict import router as predict_router
from app.api.model_info import router as info_router
from app.api.train import router as train_router

app = FastAPI(
    title="MS-Classification-Service",
    description="Microservicio responsable de clasificar tickets (Correctivo vs Evolutivo)",
    version="1.0.0"
)

# Endpoints
app.include_router(predict_router, prefix="/api/classification")
app.include_router(info_router, prefix="/api/classification")
app.include_router(train_router, prefix="/api/classification")

@app.get("/health")
def health_check():
    return {"status": "ok"}
