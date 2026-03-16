import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Add validation
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Optional: Fix common URL issues (like Heroku's postgres:// URLs)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

# Create an asynchronous engine with connection pooling for better performance under load.
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,       # Number of connections to keep open
    max_overflow=10    # Extra connections allowed during traffic spikes
)

# Factory for asynchronous sessions.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Declarative base class for ORM models.
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
