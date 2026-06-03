import redis.asyncio as redis
import json
from typing import Any

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 0

#创建 Redis 连接对象
redis_client = redis.Redis(
    host = REDIS_HOST,
    port = REDIS_PORT,
    db = REDIS_DB,
    decode_responses = True
)

#设置和读取 (字符串，列表或者字典) "[{}]"

#读取 字符串
async def get_cahce(key:str):
    # data = await redis_client.get(key)
    try:
        data = await redis_client.get(key)
        return data
    except Exception as e:
        print(f"获取缓存失败，{e}")
        return None
    
#读取 列表或者 字典
async def get_json_cache(key:str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"获取缓存失败，{e}")
        return None

#设置缓存
async def set_cache(
    key:str,
    value:Any,
    expire:int = 3600      
):
    try:
        if isinstance(value,(dict,list)):
            value = json.dumps(value,ensure_ascii=False)
        await redis_client.set(key, value, ex = expire)
        return True
    except Exception as e:
        print(f"设置缓存失败，{e}")
        return False