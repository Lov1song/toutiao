from fastapi import FastAPI
from routers import news,users,favorite,history
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handlers import register_exception_handlers
app = FastAPI()

register_exception_handlers(app)

app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)

#跨域配置
origins = [
    "http://localhost:3000",
    "http://localhost",
    "https://your-frontend-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#源
    allow_credentials=True,#是否允许携带cookie
    allow_methods=["*"],#允许的HTTP方法
    allow_headers=["*"],#允许的HTTP头
)

@app.get("/")
async def root():
    return {"msg": "Hello World"}



