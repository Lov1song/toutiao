from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from schemas.news import NewsResponse
class IsFavoriteResponse(BaseModel):
    is_favorite: bool = Field(...,alias="isFavorite")

    model_config = ConfigDict(populate_by_name=True)

class FavoriteAddRequest(BaseModel):
    news_id: int = Field(...,alias="newsId")

    model_config = ConfigDict(populate_by_name=True)
    
class FavoriteResponse(BaseModel):
    id: int
    user_id: int = Field(...,alias="userId")
    news_id: int = Field(...,alias="newsId")
    created_at: datetime = Field(...,alias="createTime")

    model_config = ConfigDict(populate_by_name=True,from_attributes=True)


class FavoriteNewsItemResponse(NewsResponse):
    favorite_id:int = Field(...,alias="favoriteId")
    favorite_time:datetime = Field(...,alias="favoriteTime")     # 收藏时间，使用别名映射favoriteTime
    # 模型配置，启用属性转换和名称映射功能
    model_config = ConfigDict(from_attributes=True,populate_by_name=True)

class FavoriteListResponse(BaseModel):
    list:list[FavoriteNewsItemResponse]
    total:int
    hasMore:bool = Field(alias="hasMore")

    model_config = ConfigDict(populate_by_name=True,from_attributes=True)