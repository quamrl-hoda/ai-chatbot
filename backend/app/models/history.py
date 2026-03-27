"""
app/models/history.py – SQLAlchemy ORM models for persistent conversation history.

Requires the DB layer (app.db.session) to be fully configured.
"""
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Conversation(Base):
    __tablename__ = "conversations"

    id       = Column(String(36), primary_key=True)   # UUID
    title    = Column(String(200), nullable=False, default="New chat")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Message(Base):
    __tablename__ = "messages"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String(36), nullable=False, index=True)
    role            = Column(String(20), nullable=False)   # "user" | "assistant"
    content         = Column(Text, nullable=False)
    created_at      = Column(DateTime, default=datetime.utcnow)
