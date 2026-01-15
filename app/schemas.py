from pydantic import BaseModel, Field, HttpUrl, constr
from typing import Optional
from datetime import datetime

# key в формате kebab-case: fastapi, rest-api, openapi-spec
KeyStr = constr(
    min_length=2,
    max_length=80,
    pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
)

class TermBase(BaseModel):
    key: KeyStr = Field(..., description="Уникальный ключ термина (kebab-case)")
    title: str = Field(..., min_length=2, max_length=200, description="Короткое название термина")
    definition: str = Field(..., min_length=5, description="Определение термина")
    source: Optional[HttpUrl] = Field(None, description="Ссылка на источник (опционально)")

class TermCreate(TermBase):
    pass

class TermUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=200)
    definition: Optional[str] = Field(None, min_length=5)
    source: Optional[HttpUrl] = None

class TermOut(TermBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # разрешаем формировать ответ из ORM-моделей SQLAlchemy
