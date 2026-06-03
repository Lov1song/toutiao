from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.news import Category,News
from schemas.news import NewsResponse
from cache.news_cache import get_cached_categories,set_cached_categories,set_cached_news_list,get_cached_news_list

async def get_category(db:AsyncSession,skip:int=0,limit:int=100):
    # 缓存
    categories = await get_cached_categories()
    if categories:
        return categories

    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()

    if categories:
        categories = jsonable_encoder(categories)
        await set_cached_categories(categories,expire=7200)

    return categories

async def get_news_lists(db:AsyncSession,category_id:int=0,skip:int=0,limit:int=10):
    #缓存
    page = skip // limit + 1
    news_list = await get_cached_news_list(category_id,page,limit)
    if news_list:
        return [News(**item) for item in news_list]
    

    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = result.scalars().all()
    #写入缓存
    if news_list:
        #ORM 转字典
        news_list = [NewsResponse.model_validate(item).model_dump(mode="json",by_alias=False) for item in news_list]
        await set_cached_news_list(category_id,page,limit,news_list)

    return result.scalars().all()

async def get_news_count(db:AsyncSession,category_id:int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()

async def get_news_details(db:AsyncSession,news_id:int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def increase_news_views(db:AsyncSession,news_id:int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    #数据库更新 -> 检查数据库是否命中数据
    return result.rowcount > 0 

async def get_related_news(db:AsyncSession,news_id:int,category_id,limit:int=5):
    stmt = select(News).where(
        News.id != news_id,
        News.category_id == category_id
        ).order_by(
            News.views.desc(),
            News.publish_time.desc()
            ).limit(limit)
    result = await db.execute(stmt)
    # return result.scalars().all()
    #列表推导式
    related_news = result.scalars().all()
    return [{
        "id":news.id,
        "title":news.title,
        "image":news.image,
        "author":news.author,
        "publishTime":news.publish_time,
        "categoryId":news.category_id,
        "views":news.views
    } for news in related_news]