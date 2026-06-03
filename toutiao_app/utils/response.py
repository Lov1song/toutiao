from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(message:str = "success",data=None):
    content = {
        "code":200,
        "message":message,
        "data":data
    }
    #将任意的对象 都正常响应
    return JSONResponse(
        content=jsonable_encoder(content,by_alias=True)
    )