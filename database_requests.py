from database_models import async_session
from database_models import User
from sqlalchemy import select


async def add_user(tg_id: int):
    async with async_session() as session:
        session.add(User(tg_id=tg_id, referrers_count=0, token_balance=0, last_drop_date=0, wallet='Не указан'))
        await session.commit()


async def is_new_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return False
        return True


async def increment_referrers_count(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.referrers_count += 1
        await session.commit()


async def get_referrers_count(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user.referrers_count


async def get_token_balance(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user.token_balance


async def increment_token_balance(tg_id: int, count: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.token_balance += count
        await session.commit()


async def get_last_drop_date(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user.last_drop_date


async def set_last_drop_date(tg_id: int, date: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.last_drop_date = date
        await session.commit()


async def get_wallet(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user.wallet


async def set_wallet(tg_id: int, wallet: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.wallet = wallet
        await session.commit()
