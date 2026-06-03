from crud.users import get_user_by_token
from config.db_config import get_db
from fastapi import Depends, HTTPException,Header
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


async def get_current_user(
    authorization:str = Header(...),
    db:AsyncSession = Depends(get_db)
):
    #Authorization: bearer <Token>
    parts = authorization.split(" ")
    token = parts[1] if len(parts) == 2 else parts[0]
    user = await get_user_by_token(token,db)
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail="无效的令牌或者已经过期的令牌")
    return user

