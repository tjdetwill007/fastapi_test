from sqlmodel import create_engine, text, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from src.config import conf

engine = AsyncEngine(create_engine(url=conf.DATABASE_URL, echo=True))

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))  # Test the connection
            print("✅ Database connection is working.")

            from src.routers.books.models import (
                Book,
            )  # Import models here to avoid circular import issues and ensure they are registered with SQLModel metadata

            await conn.run_sync(SQLModel.metadata.create_all)  # Create all tables
            print("✅ Database tables created.")
    except Exception as e:
        print(f"❌ Connection failed: {e}")


async def close_db():
    try:
        await engine.dispose()
        print("✅ Database connection closed.")
    except Exception as e:
        print(f"❌ Failed to close connection: {e}")

async def get_session():
    """Get a new session."""
    async with async_session() as session:
        yield session