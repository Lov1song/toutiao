from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select,delete

from models.history import History
from models.news import News
from datetime import datetime

async def add_current_history(
    user_id:int,
    news_id:int,
    db:AsyncSession
):
    history = History(user_id=user_id,news_id=news_id,view_time=datetime.now())
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history

async def get_current_history_count(
    user_id:int,
    db:AsyncSession
):
    query = select(func.count()).where(History.user_id == user_id)
    result = await db.execute(query)
    return result.scalar() or 0

async def get_current_history_list(
    user_id:int,
    db:AsyncSession,
    page:int = 1,
    page_size:int = 10,
):
    offset = (page - 1) * page_size
    query = select(News,History.id.label("history_id"),History.view_time.label("view_time")).join(History).where(History.user_id == user_id).order_by(History.view_time.desc()).offset(offset).limit(page_size)

    result = await db.execute(query)

    total = await get_current_history_count(user_id, db)

    return result.all(), total


async def delete_current_history(
    user_id:int,
    history_id:int,
    db:AsyncSession
):
    query = delete(History).where(History.id == history_id,History.user_id == user_id)
    result = await db.execute(query)
    await db.commit()

    return result.rowcount > 0

async def clear_current_history(
    user_id:int,
    db:AsyncSession
):
    query = delete(History).where(History.user_id == user_id)
    result = await db.execute(query)
    await db.commit()

    return result.rowcount > 0