from .exception import http_exception_handler,integrity_error_handler,sqlalchemy_error_handler,general_exception_handler
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError,SQLAlchemyError


def register_exception_handlers(app):
    app.add_exception_handler(HTTPException, http_exception_handler) #业务
    app.add_exception_handler(IntegrityError, integrity_error_handler) #数据完整性约束
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler) #数据库相关的其他错误
    app.add_exception_handler(Exception, general_exception_handler) #兜底异常处理，捕获所有未处理的异常，防止泄露敏感信息