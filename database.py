import asyncio
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username_tg = Column(String(50), unique=True, index=True)
    full_name = Column(String(100))
    balance = Column(DECIMAL(10, 2), default=0.00)
    elite_status = Column(Boolean, default=False)
    learned_words_count = Column(Integer, default=0)
    referral_code = Column(String(20))
    referred_by = Column(Integer, ForeignKey('users.id'))
    elite_start_date = Column(TIMESTAMP)

DATABASE_URL = "postgresql+asyncpg://postgres:121212@localhost:5432/english_miniapp"

# Создаем асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем фабрику для асинхронных сессий
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        return session