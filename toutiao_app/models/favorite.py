
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Index, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from models.users import User
from models.news import News
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Favorite(Base):
    """
    收藏表ORM模型
    """
    __tablename__ = "favorite"

    #UniqueConstraint 唯一约束 当前用户当前新闻 只能收藏一次
    __table_args__ = (
        UniqueConstraint('user_id', 'news_id',name = "user_news_unique"),
        Index('fk_favorite_user_idx','user_id'),
        Index('fk_favorite_news_idx','news_id')
    )

    id:Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True) # 收藏id
    user_id:Mapped[int] = mapped_column(Integer,ForeignKey(User.id),nullable=False)
    news_id:Mapped[int] = mapped_column(Integer,ForeignKey(News.id),nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime,default=datetime.now)

    def __repr__(self):
        return f"<Favorite(id={self.id},user_id={self.user_id},news_id={self.news_id},created_at={self.created_at})>"