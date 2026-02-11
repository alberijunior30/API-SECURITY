from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker

from core.settings import settings


engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)


