from datetime import datetime, timedelta

from models.users import User, UserToken
from sqlalchemy import select, update
from config.db_config import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from schemas.users import UserRequest, UserUpdateRequest,UserChangePasswordRequest
from utils.security import get_password_hash, verify_password
import uuid

async def get_user_by_username(username:str,db:AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create_user(user_data:UserRequest,db:AsyncSession = Depends(get_db)):
    #密码加密
    hashed_pwd = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        password=hashed_pwd
    )
    db.add(new_user)
    await db.flush()
    await db.refresh(new_user) #从数据库读回最新的user对象，包含自动生成的id和created_at等字段
    return new_user

async def create_token(user_id:int,db:AsyncSession = Depends(get_db)):
    #生成token,设置过期时间，查询用户是否有token 有->更新 没有->创建
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7) #设置过期时间为7天

    stmt = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(stmt)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        db.add(user_token)

    await db.flush()# flush 而不是 commit，让 id 生成但不提交
    await db.refresh(user_token)
    return user_token

async def authenticate_user(username:str,password:str,db:AsyncSession = Depends(get_db)):
    user = await get_user_by_username(username, db)
    if not user or not verify_password(password, user.password):
        return None
    return user

#根据token查询用户 验证 token -> 查询用户
async def get_user_by_token(token:UserToken,db:AsyncSession = Depends(get_db)):
    stmt = select(UserToken).where(UserToken.token == token)
    result = await db.execute(stmt)
    user_token = result.scalar_one_or_none()

    if not user_token or user_token.expires_at < datetime.now():
        return None

    stmt = select(User).where(User.id == user_token.user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

#更新信息 update更新 -> 检查是否命中 -> 返回更新后的用户信息
async def update_user_info(username:str,user_data:UserUpdateRequest,db:AsyncSession = Depends(get_db)):
    #user_data pydantic 类型 得到字典 -> 解包
    #没有设置值的不更新

    query = update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_unset = True,
        exclude_none = True
    ))
    result = await db.execute(query)
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code = 404,detail = "用户不存在")
    
    updated_user = await get_user_by_username(username,db)
    return updated_user

#更新密码
async def update_user_password(
    old_password:str,
    new_password:str,
    user:User,
    db:AsyncSession=Depends(get_db)
):
    if not verify_password(old_password,user.password):
        return False
    
    new_hash = get_password_hash(new_password)
    user.password = new_hash
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True


