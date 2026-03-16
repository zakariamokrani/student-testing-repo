import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Ensure we're using an async driver
if "postgresql" in DATABASE_URL or "postgres" in DATABASE_URL:
    # Replace common sync drivers with asyncpg
    if "+psycopg2" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("+psycopg2", "+asyncpg")
    elif "://" in DATABASE_URL and "+" not in DATABASE_URL.split("://")[0]:
        # No driver specified, add asyncpg
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

print(f"Connecting with: {DATABASE_URL}")  # For debugging

try:
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_size=5,
        max_overflow=10
    )
except Exception as e:
    print(f"Error creating engine: {e}")
    raise

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
