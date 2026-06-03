from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from typing import Optional
class NewsResponse(BaseModel):
    id:int                    # 收藏列表的唯一标识符ID
    title:str                 # 收藏项目的标题
    description:Optional[str] = None    # 收藏项目的描述信息
    image:Optional[str] = None    
    author:Optional[str] = None             # 收藏项目的图片链接或路径
    publish_time:Optional[datetime] = Field(...,alias="publishTime")  # 发布时间，使用别名映射publistTime
    category_id:int = Field(...,alias="categoryId")          # 分类ID，使用别名映射categoryId
    views:int

    model_config = ConfigDict(
        populate_by_name=True, #允许使用别名来填充数据
        from_attributes=True #允许从 ORM 模型属性中填充数据
    )