from fastapi import APIRouter,Depends, HTTPException,Query
from crud.news import get_news_count,get_news_details,increase_news_views,get_related_news
from crud.news_cache import get_category,get_news_lists

from config.db_config import get_db 
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/news",tags=["news"])

@router.get("/categories")
async def get_categories(skip:int=0,limit:int=100,db:AsyncSession=Depends(get_db)):
    categories = await get_category(db,skip,limit)
    return {
        "code":200,
        "message":"success",
        "data":categories
    }


@router.get("/list")
async def get_news_list(
    categoryId:int = Query(0,description="分类ID，0表示全部"),
    page:int = 1,
    page_size:int = Query(10,le = 100,alias = "pageSize"),
    db:AsyncSession = Depends(get_db)
):
    #思路 ：处理分页，查询列表，计算总量，计算是否还有更多

    offset = (page-1)*page_size
    news_list = await get_news_lists(db,categoryId,skip=offset,limit=page_size)
    total = await get_news_count(db,categoryId)
    #跳过的 + 当前列表的数量 是否小于 总量
    has_more = (offset + len(news_list)) < total
    return {
        "code":200,
        "message":"success",
        "data":{
            "list":news_list,
            "total":total,
            "hasMore":has_more
        }
    }

#获取新闻详情，响应结果 当前的新闻详情 + 增加一次浏览量 + 相关新闻
@router.get("/detail")
async def get_news_detail(news_id:int = Query(...,alias="id"),db:AsyncSession = Depends(get_db)):
    news_detail = await get_news_details(db,news_id)
    if not news_detail:
        return HTTPException(status_code=404,detail="新闻未找到")
    views_res = await increase_news_views(db,news_detail.id)
    if not views_res:
        raise HTTPException(status_code=404,detail="新闻未找到")
    related_news = await get_related_news(db,news_detail.id,news_detail.category_id,limit=5)    
    return {
        "code":200,
        "message":"success",
        "data":{
            "id":news_detail.id,
            "title":news_detail.title,
            "content":news_detail.content,
            "image":news_detail.image,
            "author":news_detail.author,
            "pubishTime":news_detail.publish_time,
            "categoryId":news_detail.category_id,
            "views":news_detail.views,
            "relatedNews":related_news
        }
    }