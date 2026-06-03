from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.favorite import IsFavoriteResponse,FavoriteAddRequest,FavoriteResponse,FavoriteListResponse,FavoriteNewsItemResponse
from config.db_config import get_db
from models.users import User
from utils.auth import get_current_user
from utils.response import success_response
from models.favorite import Favorite
from crud.favorite import clear_current_favorite, is_news_favorite,add_current_favorite,remove_current_favorite,get_current_favorite_list
from starlette import status
router = APIRouter(prefix="/api/favorite",tags=["favorite"])

@router.get("/check")
async def check_favorite(
    news_id:int = Query(...,alias="newsId"),
    user:User = Depends(get_current_user),
    db:AsyncSession = Depends(get_db)    
):
    is_favorite = await is_news_favorite(user.id,news_id,db)
    res_data = IsFavoriteResponse(is_favorite = is_favorite)
    return success_response(
        message="success",
        data = res_data
    )

@router.post("/add")
async def add_favorite(
    news_id:FavoriteAddRequest,
    user:User = Depends(get_current_user),
    db:AsyncSession = Depends(get_db)    
):
    is_favorite = await is_news_favorite(user.id,news_id.news_id,db)
    if is_favorite:
        raise HTTPException(status_code=400,detail="已收藏")

    favorite = await add_current_favorite(user.id,news_id.news_id,db)
    res_data = FavoriteResponse.model_validate(favorite)
    return success_response(
        message="success",
        data = res_data
    )

@router.delete("/remove")
async def remove_favorite(
    news_id:int = Query(...,alias="newsId"),
    user:User = Depends(get_current_user),
    db:AsyncSession = Depends(get_db)    
):
    is_removed = await remove_current_favorite(user.id,news_id,db)
    if not is_removed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="未收藏")

    return success_response(
        message="success",
    )

@router.get("/list")
async def get_favorite_list(
    page:int = Query(1,ge = 1),
    page_size:int = Query(10,ge = 1,le = 100),
    user:User = Depends(get_current_user),
    db:AsyncSession = Depends(get_db)    
):

    total,rows = await get_current_favorite_list(user.id,db,page,page_size)

    favorite_list = [{
        **news.__dict__,
        "favorite_time":favorite_time,
        "favorite_id":favorite_id
        }for news,favorite_time,favorite_id in rows]
    has_more = total > page * page_size

    res_data = FavoriteListResponse(
        list = favorite_list,
        total = total,
        hasMore = has_more
    )
    return success_response(
        message="success",
        data = res_data
    )

@router.delete("/clear")
async def clear_favorite(
    user:User = Depends(get_current_user),
    db:AsyncSession = Depends(get_db)
):
    clear_count = await clear_current_favorite(user.id,db)
    
    return success_response(
        message="成功删除{clear_count}条收藏",
    )