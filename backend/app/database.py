import ssl as _ssl_module
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app.config import settings


def _strip_ssl_params(url: str) -> str:
    """asyncpg 0.30+ requiere SSLContext, no string — strip ssl/sslmode del URL y manejar via connect_args."""
    parsed = urlparse(url)
    params = {k: v for k, v in parse_qs(parsed.query).items() if k not in ("ssl", "sslmode")}
    return urlunparse(parsed._replace(query=urlencode({k: v[0] for k, v in params.items()})))


# NullPool en producción (Vercel serverless): sin conexiones persistentes entre invocaciones
# Default pool en desarrollo (Docker): reutiliza conexiones del pool
_pool_kwargs = {"poolclass": NullPool} if settings.ENVIRONMENT == "production" else {}

# asyncpg 0.30+ deprecó ssl como string — pasar SSLContext explícito en producción
_connect_args: dict = {}
if settings.ENVIRONMENT == "production":
    _ssl_ctx = _ssl_module.create_default_context()
    _connect_args = {"ssl": _ssl_ctx}

engine = create_async_engine(
    _strip_ssl_params(settings.DATABASE_URL),
    echo=settings.ENVIRONMENT == "development",
    connect_args=_connect_args,
    **_pool_kwargs,
)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
