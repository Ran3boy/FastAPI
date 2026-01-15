from fastapi import FastAPI
from .config import settings
from .routers.terms import router as terms_router

app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description="Web API для глоссария терминов ВКР: CRUD + OpenAPI/Swagger + SQLite.",
)

app.include_router(terms_router)

@app.get("/health", tags=["Система"], summary="Проверка работоспособности сервиса")
def health():
    return {"status": "ok"}
