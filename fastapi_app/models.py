from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date

# データベースの接続URLを設定
DATABASE_URL = "sqlite:///./app.db"

# SQLAlchemyのエンジンを作成
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# セッションを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Baseクラスを定義
Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id: int = Column(Integer, primary_key=True) # type: ignore
    title: str = Column(String(255), nullable=False) # type: ignore
    description: Optional[str] = Column(Text, nullable=True) # type: ignore
    deadline: Optional[date] = Column(Date, nullable=True) # type: ignore
    completed: bool = Column(Boolean, default=False) # type: ignore
