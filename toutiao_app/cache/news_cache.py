"""
新闻相关的缓存方法 新闻的读取和写入
"""
CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX = "news_list:"


from config.cache_conf import get_json_cache,set_cache

from typing import List,Dict,Any,Optional

#获取新闻分类的缓存方法
async def get_cached_categories():
    return await get_json_cache(CATEGORIES_KEY)

#写入新闻分类的缓存方法
async def set_cached_categories(data:List[Dict[str,Any]],expire:int = 7200):
    return await set_cache(CATEGORIES_KEY,data,expire)

#写入缓存 新闻列表 key:news_list:分类id:页码:每页数量
async def set_cached_news_list(categroy_id:Optional[int],page:int,page_size:int,news_list:List[Dict[str,Any]],expire:int = 1800):
    category_part = categroy_id if categroy_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}:{category_part}:{page}:{page_size}"

    return await set_cache(key,news_list,expire)


#读取新闻列表
async def get_cached_news_list(categroy_id:Optional[int],page:int,page_size:int):
    category_part = categroy_id if categroy_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}:{category_part}:{page}:{page_size}"

    return await get_json_cache(key)