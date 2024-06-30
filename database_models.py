from sqlalchemy import BigInteger, Boolean, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///database.db')
async_session = async_sessionmaker(engine)


class Database(AsyncAttrs, DeclarativeBase):
    pass


class User(Database):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    referrers_count: Mapped[int] = mapped_column(BigInteger)
    token_balance: Mapped[int] = mapped_column(BigInteger)
    last_drop_date: Mapped[int] = mapped_column(BigInteger)
    wallet: Mapped[int] = mapped_column(String)


async def async_setup():
    async with engine.begin() as connection:
        await connection.run_sync(Database.metadata.create_all)
