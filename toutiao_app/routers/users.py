from fastapi import APIRouter,Depends, HTTPException,Query
from config.db_config import get_db
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserRequest, UserAuthResponse,UserInfoResponse,UserUpdateRequest,UserChangePasswordRequest
from models.users import User
from crud.users import authenticate_user, get_user_by_username, create_user, create_token,update_user_info,update_user_password
from starlette import status
from utils.response import success_response
from utils.auth import get_current_user

router = APIRouter(prefix="/api/user",tags=["user"])

@router.post("/register")
async def register(user_data:UserRequest,db:AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_username(user_data.username, db)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    try:
        user = await create_user(user_data, db)
        token = await create_token(user.id, db)
        await db.commit() #提交事务，保存用户和token到数据库
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="注册失败")

    select().where(user_data.username == User.username)

    response_data = UserAuthResponse(token=token.token, user_info=UserInfoResponse.model_validate(user))
    return success_response(
        message="注册成功",
        data = response_data
    )
    # return {
    #     "code":200, 
    #     "message":"注册成功",
    #     "data":{
    #         "token":token,
    #         "userInfo":{
    #             "id":user.id,
    #             "username":user.username,
    #             "bio":user.bio,
    #             "avatar":user.avatar
    #         }
    #     }
    # }

@router.post("/login")
async def login(user_data:UserRequest,db:AsyncSession = Depends(get_db)):
    user = await authenticate_user(user_data.username, user_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = await create_token(user.id, db)
    await db.commit() #提交事务，保存token到数据库

    response_data = UserAuthResponse(token = token.token,user_info = UserInfoResponse.model_validate(user))

    return success_response(
        message="登录成功",
        data = response_data
    )

#登陆后才能获取用户信息，所以需要在请求头中携带token进行身份验证
#前端里的请求头 Authorization:Bearer <token> 后端解析这个token 检查有效性，获取用户信息
@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    res_data = UserInfoResponse.model_validate(user)
    return success_response(
        message = "获取用户信息成功",
        data = res_data
    )

@router.put("/update")
async def update_current_user_info(
    user_data:UserUpdateRequest,
    user:User = Depends(get_current_user),
    db:AsyncSession = Depends(get_db)
):
    
    user = await update_user_info(user.username,user_data,db)
    res_data = UserInfoResponse.model_validate(user)
    return success_response(
        message="修改成功",
        data = res_data
    )


#更新密码
@router.put("/password")
async def update_current_user_password(
    password_data:UserChangePasswordRequest,
    user:User = Depends(get_current_user),
    db:AsyncSession = Depends(get_db)
):
    old = password_data.old_password
    new = password_data.new_password
    
    res = await update_user_password(old,new,user,db)
    if not res:
        raise HTTPException(status_code=500,detail="修改密码失败，请稍后再试")
    

    return success_response(
        message="修改密码成功",
        data=""
    )