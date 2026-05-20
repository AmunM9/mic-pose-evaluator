from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app.config import settings

# NullPool en producción (Vercel serverless): sin conexiones persistentes entre invocaciones
# Default pool en desarrollo (Docker): reutiliza conexiones del pool
_pool_kwargs = {"poolclass": NullPool} if settings.ENVIRONMENT == "production" else {}

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",
    **_pool_kwargs,
)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
