from typing import Optional

from pydantic import BaseModel,Field,ConfigDict

class UserRequest(BaseModel):
    username: str
    password: str

class UserInfoBase(BaseModel):
    """
    用户基本信息模型，包含用户的基本属性，如用户名、简介和头像等。
    """
    nickname:Optional[str] = Field(None, description="用户昵称")
    avatar:Optional[str] = Field(None, description="用户头像URL")
    gender:Optional[str] = Field(None, description="用户性别")
    bio:Optional[str] = Field(None, description="用户简介")


class UserInfoResponse(UserInfoBase):
    id: int
    username: str
    model_config = ConfigDict(
        from_attributes=True #允许从 ORM 对象属性中填充数据
    )


class UserAuthResponse(BaseModel):
    token: str
    user_info:UserInfoResponse = Field(...,alias="userInfo")

    model_config = ConfigDict(
        populate_by_name=True,#允许使用别名来填充数据
        from_attributes=True #允许从 ORM 对象属性中填充数据
    )

class UserUpdateRequest(BaseModel):
    nickname:str = None
    avatar:str = None
    gender:str = None
    bio:str = None
    phone:str = None


class UserChangePasswordRequest(BaseModel):
    old_password : str = Field(...,alias="oldPassword",descriptio="旧密码")
    new_password : str = Field(...,min_length=6,alias="newPassword",descriptio="新密码")

    model_config = ConfigDict(populate_by_name=True)