from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import Term
from .schemas import TermCreate, TermUpdate

def list_terms(db: Session) -> list[Term]:
    return list(db.scalars(select(Term).order_by(Term.key)))

def get_term_by_key(db: Session, key: str) -> Term | None:
    return db.scalar(select(Term).where(Term.key == key))

def create_term(db: Session, data: TermCreate) -> Term:
    term = Term(
        key=data.key,
        title=data.title,
        definition=data.definition,
        source=str(data.source) if data.source else None,
    )
    db.add(term)
    db.commit()
    db.refresh(term)
    return term

def update_term(db: Session, term: Term, data: TermUpdate) -> Term:
    if data.title is not None:
        term.title = data.title
    if data.definition is not None:
        term.definition = data.definition
    if data.source is not None:
        term.source = str(data.source)
    db.commit()
    db.refresh(term)
    return term

def delete_term(db: Session, term: Term) -> None:
    db.delete(term)
    db.commit()
