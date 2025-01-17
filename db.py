from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, unique=True, nullable=False)  # Telegram ID пользователя
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(String, nullable=False, default="не указан")  # Пол пользователя
    goal = Column(String, nullable=False)
    level = Column(String, nullable=False, default="Новичок")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Ilya2005@localhost:5432/bot_db"

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def init_db():
    Base.metadata.create_all(bind=engine)
