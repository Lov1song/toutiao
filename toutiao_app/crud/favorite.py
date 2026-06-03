from fastapi import Query
from sqlalchemy import func, select,delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from models.news import News
from models.favorite import Favorite

#输出布尔值
async def is_news_favorite(user_id:int,news_id:int,db:AsyncSession):
    query = select(Favorite).where(Favorite.news_id == news_id,Favorite.user_id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None

async def add_current_favorite(
    user_id:int,
    news_id:int,
    db:AsyncSession      
):
    favorite = Favorite(user_id=user_id,news_id=news_id)
    db.add(favorite)  
    await db.commit()  
    await db.refresh(favorite)

    return favorite


async def remove_current_favorite(
    user_id:int,
    news_id:int,
    db:AsyncSession      
):
    query = delete(Favorite).where(Favorite.news_id == news_id,Favorite.user_id == user_id)
    result = await db.execute(query)
    await db.commit()

    return result.rowcount > 0


async def get_current_favorite_count(
    user_id:int,
    db:AsyncSession,
):
    query = select(func.count()).where(Favorite.user_id == user_id)
    count = await db.execute(query)
    return count.scalar_one()

#联表查询
async def get_current_favorite_list(
    user_id:int,
    db:AsyncSession,
    page:int = 1,
    page_size:int = 10,
):
    total = await get_current_favorite_count(user_id,db)
    #select(查询主体，字段别名).join(联合查询，联合查询的条件)
    offset = (page - 1) * page_size
    query = select(News,Favorite.created_at.label("favorite_time"),Favorite.id.label("favorite_id")).join(Favorite,Favorite.news_id == News.id).where(Favorite.user_id == user_id).order_by(Favorite.created_at.desc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    rows = result.all()
    return total,rows

async def clear_current_favorite(
    user_id:int,
    db:AsyncSession,
):
    query = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount or 0