from pydantic import BaseModel
import os

class Settings(BaseModel):
    # SQLite по умолчанию хранится в ./data/glossary.db
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/glossary.db")
    app_title: str = os.getenv("APP_TITLE", "Глоссарий ВКР (API)")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")

settings = Settings()
