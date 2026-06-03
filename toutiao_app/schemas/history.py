from pydantic import BaseModel,Field,ConfigDict
from datetime import datetime

from schemas.news import NewsResponse

class HistoryAddRequest(BaseModel):
    news_id: int = Field(...,alias="newsId")
    
    model_config = ConfigDict(populate_by_name=True)

class HistoryAddResponse(BaseModel):
    id : int
    user_id:int = Field(...,alias="userId")
    news_id:int = Field(...,alias="newsId")
    view_time:datetime = Field(...,alias="viewTime")

    model_config = ConfigDict(from_attributes=True,populate_by_name=True)

class HistoryResponse(NewsResponse):
    history_id:int = Field(...,alias="historyId")
    view_time:datetime = Field(...,alias="viewTime")

    model_config = ConfigDict(from_attributes=True,populate_by_name=True)

class HistoryListResponse(BaseModel):
    list:list[HistoryResponse]
    total:int
    hasMore:bool = False

    model_config = ConfigDict(from_attributes=True,populate_by_name=True)