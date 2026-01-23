#!/bin/bash

# 警情态势演示系统 - 本地打包脚本
# 用途: 在本地构建前端+后端的完整可执行文件

set -e  # 遇到错误立即退出

echo "=========================================="
echo "  警情态势演示系统 - 本地打包"
echo "=========================================="

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. 检查依赖
echo -e "\n${BLUE}[1/5] 检查依赖...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}错误: 未找到 Node.js，请先安装${NC}"
    exit 1
fi
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到 Python 3，请先安装${NC}"
    exit 1
fi
echo -e "${GREEN}✓ 依赖检查通过${NC}"

# 2. 构建前端
echo -e "\n${BLUE}[2/5] 构建前端...${NC}"
cd frontend
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi
echo "打包前端..."
npm run build
cd ..
echo -e "${GREEN}✓ 前端构建完成${NC}"

# 3. 复制前端产物到后端
echo -e "\n${BLUE}[3/5] 复制前端到后端...${NC}"
rm -rf backend/static
mkdir -p backend/static
cp -r frontend/dist/* backend/static/
echo -e "${GREEN}✓ 前端文件已复制到 backend/static/${NC}"

# 4. 安装后端依赖
echo -e "\n${BLUE}[4/5] 安装后端依赖...${NC}"
cd backend
if [ ! -d ".venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip > /dev/null
pip install -e . > /dev/null
pip install pyinstaller > /dev/null
echo -e "${GREEN}✓ 后端依赖安装完成${NC}"

# 5. 打包后端
echo -e "\n${BLUE}[5/5] 打包后端可执行文件...${NC}"
pyinstaller --clean --noconfirm \
    --name police-alert \
    --onefile \
    --add-data "static:static" \
    --hidden-import uvicorn.logging \
    --hidden-import uvicorn.loops \
    --hidden-import uvicorn.loops.auto \
    --hidden-import uvicorn.protocols \
    --hidden-import uvicorn.protocols.http \
    --hidden-import uvicorn.protocols.http.auto \
    --hidden-import uvicorn.protocols.websockets \
    --hidden-import uvicorn.protocols.websockets.auto \
    --hidden-import uvicorn.lifespan \
    --hidden-import uvicorn.lifespan.on \
    main.py

cd ..
echo -e "${GREEN}✓ 打包完成${NC}"

# 6. 输出结果
echo -e "\n=========================================="
echo -e "${GREEN}✓ 打包成功！${NC}"
echo "=========================================="
echo -e "可执行文件位置: ${BLUE}backend/dist/police-alert${NC}"
echo ""
echo "运行方法:"
echo "  cd backend/dist"
echo "  ./police-alert"
echo ""
echo "访问地址: http://localhost:8000"
echo "=========================================="
