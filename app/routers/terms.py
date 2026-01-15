from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud
from ..schemas import TermCreate, TermUpdate, TermOut

router = APIRouter(prefix="/terms", tags=["Термины"])

@router.get("", response_model=list[TermOut], summary="Получить список всех терминов")
def get_terms(db: Session = Depends(get_db)):
    return crud.list_terms(db)

@router.get("/{key}", response_model=TermOut, summary="Получить термин по ключу")
def get_term(key: str, db: Session = Depends(get_db)):
    term = crud.get_term_by_key(db, key)
    if not term:
        raise HTTPException(status_code=404, detail="Термин не найден")
    return term

@router.post("", response_model=TermOut, status_code=status.HTTP_201_CREATED, summary="Добавить новый термин")
def add_term(payload: TermCreate, db: Session = Depends(get_db)):
    existing = crud.get_term_by_key(db, payload.key)
    if existing:
        raise HTTPException(status_code=409, detail="Термин с таким ключом уже существует")
    return crud.create_term(db, payload)

@router.put("/{key}", response_model=TermOut, summary="Обновить существующий термин")
def edit_term(key: str, payload: TermUpdate, db: Session = Depends(get_db)):
    term = crud.get_term_by_key(db, key)
    if not term:
        raise HTTPException(status_code=404, detail="Термин не найден")
    return crud.update_term(db, term, payload)

@router.delete("/{key}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить термин")
def remove_term(key: str, db: Session = Depends(get_db)):
    term = crud.get_term_by_key(db, key)
    if not term:
        raise HTTPException(status_code=404, detail="Термин не найден")
    crud.delete_term(db, term)
    return None
