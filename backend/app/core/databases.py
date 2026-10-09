from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine,async_sessionmaker
from base import Base

database_url = "sqlite:///workspaces.db"

engine = create_async_engine(database_url, connect_args={"check_same_thread": False})

AsyncSessionLocal = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)


async def get_db():
   async with AsyncSessionLocal() as session:
        yield session