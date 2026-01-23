@echo off
REM 警情态势演示系统 - Windows 本地打包脚本

echo ==========================================
echo   警情态势演示系统 - 本地打包
echo ==========================================

REM 1. 检查依赖
echo.
echo [1/5] 检查依赖...
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到 Node.js，请先安装
    exit /b 1
)
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到 Python，请先安装
    exit /b 1
)
echo √ 依赖检查通过

REM 2. 构建前端
echo.
echo [2/5] 构建前端...
cd frontend
if not exist "node_modules" (
    echo 安装前端依赖...
    call npm install
)
echo 打包前端...
call npm run build
cd ..
echo √ 前端构建完成

REM 3. 复制前端产物到后端
echo.
echo [3/5] 复制前端到后端...
if exist "backend\static" rmdir /s /q backend\static
mkdir backend\static
xcopy /s /e /y frontend\dist\* backend\static\
echo √ 前端文件已复制到 backend\static\

REM 4. 安装后端依赖
echo.
echo [4/5] 安装后端依赖...
cd backend
if not exist ".venv" (
    echo 创建虚拟环境...
    python -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>nul
pip install -e . >nul 2>nul
pip install pyinstaller >nul 2>nul
echo √ 后端依赖安装完成

REM 5. 打包后端
echo.
echo [5/5] 打包后端可执行文件...
pyinstaller --clean --noconfirm ^
    --name police-alert ^
    --onefile ^
    --add-data "static;static" ^
    --hidden-import uvicorn.logging ^
    --hidden-import uvicorn.loops ^
    --hidden-import uvicorn.loops.auto ^
    --hidden-import uvicorn.protocols ^
    --hidden-import uvicorn.protocols.http ^
    --hidden-import uvicorn.protocols.http.auto ^
    --hidden-import uvicorn.protocols.websockets ^
    --hidden-import uvicorn.protocols.websockets.auto ^
    --hidden-import uvicorn.lifespan ^
    --hidden-import uvicorn.lifespan.on ^
    main.py

cd ..
echo √ 打包完成

REM 6. 输出结果
echo.
echo ==========================================
echo √ 打包成功！
echo ==========================================
echo 可执行文件位置: backend\dist\police-alert.exe
echo.
echo 运行方法:
echo   cd backend\dist
echo   police-alert.exe
echo.
echo 访问地址: http://localhost:8000
echo ==========================================
pause
