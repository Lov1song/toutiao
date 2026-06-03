from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column
from sqlalchemy import Column, Index, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint

from models.users import User
from models.news import News   

from datetime import datetime

class Base(DeclarativeBase):
    pass

class History(Base):

    __tablename__ = "history"

    __table_args__ = (
        
    )

    id:Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    user_id:Mapped[int] = mapped_column(Integer,ForeignKey(User.id),nullable=False)
    news_id:Mapped[int] = mapped_column(Integer,ForeignKey(News.id),nullable=False)
    view_time:Mapped[datetime] = mapped_column(DateTime,default=datetime.now)
    