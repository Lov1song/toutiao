from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, Index, Text
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
            DateTime,
            default=datetime.now,
            comment = "创建时间"
        )
    
    
class User(Base):
    __tablename__ = "user"
    #创建索引
    __table_args__ = (
        Index('username_UNIQUE', 'username'),
        Index('phone_UNIQUE', 'phone')
    )


    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String,unique=True,nullable=False,comment="用户名")
    password: Mapped[str] = mapped_column(String,nullable=False,comment="密码")
    nickname:Mapped[Optional[str]] = mapped_column(String,comment="昵称")
    avatar:Mapped[Optional[str]] = mapped_column(String,comment="头像URL",default='https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg')
    gender:Mapped[Optional[str]] = mapped_column(String,comment="性别")
    bio: Mapped[Optional[str]] = mapped_column(String,comment="个人简介")
    phone: Mapped[Optional[str]] = mapped_column(String,comment="手机号")
    updated_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.now,onupdate=datetime.now,comment="更新时间")
    def __repr__(self) -> str:
        return f"Users(id={self.id}, username='{self.username}', bio='{self.bio}', avatar='{self.avatar}')"
    
class UserToken(Base):
    """
    用户令牌表
    """
    __tablename__ = "user_token"
    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey("user.id"),nullable=False,comment="用户ID")
    token: Mapped[str] = mapped_column(String,unique=True,nullable=False,comment="令牌")
    expires_at: Mapped[datetime] = mapped_column(DateTime,nullable=False,comment="过期时间")

    def __repr__(self) -> str:
        return f"UserToken(id={self.id}, user_id={self.user_id}, token='{self.token}', expires_at={self.expires_at})"