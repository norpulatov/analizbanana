from sqlalchemy import BigInteger, String, Integer, DateTime, Boolean, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from src.db import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    phone: Mapped[str | None] = mapped_column(String(32))
    name: Mapped[str | None] = mapped_column(String(128))
    lang: Mapped[str] = mapped_column(String(2), default="uz")
    premium_until: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    entries: Mapped[list["Entry"]] = relationship(back_populates="user")

class Entry(Base):
    __tablename__ = "entries"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    type: Mapped[str] = mapped_column(String(16))  # income|expense|debt_out|debt_in
    category: Mapped[str | None] = mapped_column(String(64))
    amount: Mapped[float] = mapped_column(Numeric(14,2))
    currency: Mapped[str] = mapped_column(String(8), default="UZS")
    note: Mapped[str | None] = mapped_column(Text)
    ts: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="entries")

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    plan: Mapped[str] = mapped_column(String(8))  # 1m | 3m
    amount: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(16), default="pending")  # pending|approved|rejected
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Limit(Base):
    __tablename__ = "limits"
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), primary_key=True)
    monthly_limit: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
