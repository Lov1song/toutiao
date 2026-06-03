from fastapi import APIRouter,Depends,Query,HTTPException

from models.users import User

from schemas.history import HistoryAddRequest,HistoryAddResponse, HistoryListResponse
from config.db_config import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from crud.history import add_current_history,get_current_history_list,delete_current_history,clear_current_history

from utils.response import success_response
from utils.auth import get_current_user

router = APIRouter(prefix="/api/history",tags=["history"])

@router.post("/add")
async def add_history(
    data:HistoryAddRequest,
    user:User = Depends(get_current_user),
    db:AsyncSession = Depends(get_db)
):
    history = await add_current_history(user.id,data.news_id,db)
    res_data = HistoryAddResponse.model_validate(history)

    return success_response(
        message="success",
        data = res_data
    )

@router.get("/list")
async def get_history_list(
    page:int = Query(1,ge = 1),
    page_size:int = Query(10,ge = 1,le = 100),
    user:User = Depends(get_current_user),
    db:AsyncSession = Depends(get_db)    
):
    rows,total = await get_current_history_list(user.id,db,page,page_size)

    history_list = [{
        **news.__dict__,
        "historyId":history_id,
        "viewTime":view_time
    }for news,history_id,view_time in rows]

    has_more = total > page * page_size

    res_data = HistoryListResponse(
        list = history_list,
        total = total,
        hasMore = has_more
    )

    print("res_data:", res_data)
    print("res_data dict:", res_data.model_dump())
    return success_response(
        message="success",
        #data = res_data
        data=res_data.model_dump(by_alias=True)
    )

@router.delete("/delete/{history_id}")
async def delete_history(
    history_id:int,
    user:User = Depends(get_current_user),
    db:AsyncSession = Depends(get_db)
):
    res = await delete_current_history(
        user_id = user.id,
        history_id = history_id,
        db = db
    )
    if not res:
        raise HTTPException(status_code=404,detail="history not found")

    return success_response(
        message="success"
    )

@router.delete("/clear")
async def clear_history(
    user:User = Depends(get_current_user),
    db:AsyncSession = Depends(get_db)
):
    res = clear_current_history(user.id,db)
    if not res:
        raise HTTPException(status_code=404,detail="history not found")
    
    
    return success_response(
        message="success",
    )