import traceback
from fastapi import HTTPException,Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from starlette import status

#开发模式 ：抛出异常，显示详细的错误信息
#生产模式：捕获异常，记录日志，返回友好的错误提示

DEBUG_MODE = True #开发模式

async def http_exception_handler(request:Request,exc:HTTPException):
    """处理HTTPException异常，返回统一的错误响应格式"""

    #HTTPException 一般是业务主动抛出，data保持None
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code":exc.status_code,
            "message":exc.detail,
            "data":None
        }
    )

async def integrity_error_handler(request:Request,exc:IntegrityError):
    """处理数据库完整性错误，返回统一的错误响应格式"""
    error_msg = str(exc.orig)

    #判断具体的约束类型错误
    if "username_UNIQUE" in error_msg or "Duplicate entry" in error_msg:
        detail = "用户名已存在"
    elif "FOREIGN KEY" in error_msg:
        detail = "外键约束错误，相关数据不存在"
    else:
        detail = "数据库完整性错误"

    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error": error_msg,
            "error_detail":error_msg,
            "path":str(request.url),
        }

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code":status.HTTP_400_BAD_REQUEST,
            "message":detail,
            "data":error_data
        }
    )

async def sqlalchemy_error_handler(request:Request,exc:SQLAlchemyError):
    """处理SQLAlchemyError异常，返回统一的错误响应格式"""
    

    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error":type(exc).__name__,
            "error_detail":str(exc),
            #格式化异常信息
            "traceback":traceback.format_exc(),
            "path":str(request.url),
        }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code":status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message":"数据库操作错误",
            "data":error_data
        }
    )

async def general_exception_handler(request:Request,exc:Exception):
    """处理其他未捕获的异常，返回统一的错误响应格式"""

    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error":type(exc).__name__,
            "error_detail":str(exc),
            "traceback":traceback.format_exc(),
            "path":str(request.url),
        }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code":status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message":"服务器内部错误",
            "data":error_data
        }
    )