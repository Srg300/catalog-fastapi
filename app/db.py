from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import settings


DATABASE_URL = settings.SQLALCHEMY_DATABASES_URI

Base = declarative_base()

engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=False,
    # pool_size=settings.POSTGRES_MAX_CONNECTIONS,
    # max_overflow=settings.POSTGRES_CONNECTIONS_OVERFLOW,
    # pool_pre_ping=True,
    # pool_recycle=300,
    # connect_args={"server_settings": {"application_name": f"{settings.APP_NAME.lower()}[{settings.ENVIRONMENT.lower()}]"}},
)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session() as session, session.begin():
        yield session
