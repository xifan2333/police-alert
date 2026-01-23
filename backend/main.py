"""警情态势演示系统后端API"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.init_db import init_database
import os
import sys




@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    print("正在初始化数据库...")
    init_database()
    print("数据库初始化完成")
    yield
    # 关闭时执行（如需要）


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="警情态势演示系统后端API",
    debug=settings.DEBUG,
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 注册路由
from app.api import data, admin

app.include_router(data.router, prefix="/api/v1/data", tags=["数据"])
app.include_router(admin.router, prefix="/api/v1", tags=["管理后台"])

# 挂载静态文件（前端）
# PyInstaller 打包后，静态文件在 _MEIPASS 目录下
if getattr(sys, 'frozen', False):
    # 打包后的路径
    base_path = sys._MEIPASS
else:
    # 开发环境路径
    base_path = os.path.dirname(__file__)

static_dir = os.path.join(base_path, "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")



# 根路径
@app.get("/api", tags=["根路径"])
def read_root():
    """API根路径"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


# 健康检查
@app.get("/api/health", tags=["健康检查"])
def health_check():
    """健康检查接口"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    # 打包后禁用 reload，避免一直重启
    is_packaged = getattr(sys, 'frozen', False)
    uvicorn.run(
        "main:app" if not is_packaged else app,
        host="0.0.0.0",
        port=8000,
        reload=False if is_packaged else settings.DEBUG
    )
