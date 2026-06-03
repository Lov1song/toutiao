from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession,create_async_engine

ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@mysql:3306/news_app?charset=utf8mb4"

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
    )

AsyncSessionLocal = async_sessionmaker(
    bind = async_engine,
    class_ = AsyncSession,
    expire_on_commit = False
)

#依赖注入，获取数据库会话

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        