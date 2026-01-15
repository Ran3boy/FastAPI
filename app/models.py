from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, func, UniqueConstraint

class Base(DeclarativeBase):
    pass

class Term(Base):
    __tablename__ = "terms"
    __table_args__ = (UniqueConstraint("key", name="uq_terms_key"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    key: Mapped[str] = mapped_column(String(80), index=True)
    title: Mapped[str] = mapped_column(String(200))
    definition: Mapped[str] = mapped_column(Text)
    source: Mapped[str | None] = mapped_column(String(500), nullable=True)

    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
