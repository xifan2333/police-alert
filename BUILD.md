# 打包和发布指南

## 📦 本地打包

### Linux / macOS

```bash
# 执行打包脚本
./build.sh

# 运行可执行文件
cd backend/dist
./police-alert
```

### Windows

```cmd
# 执行打包脚本
build.bat

# 运行可执行文件
cd backend\dist
police-alert.exe
```

打包完成后，访问 http://localhost:8000 即可使用。

---

## 🚀 GitHub Actions 自动打包

### 触发方式

#### 方式一：推送标签（推荐）

```bash
# 创建标签
git tag v1.0.0

# 推送标签到远程
git push origin v1.0.0
```

#### 方式二：手动触发

1. 进入 GitHub 仓库
2. 点击 `Actions` 标签
3. 选择 `Build and Release` 工作流
4. 点击 `Run workflow` 按钮
5. 选择分支并运行

### 构建产物

GitHub Actions 会自动构建以下平台的可执行文件：

- **Linux x64**: `police-alert-linux-x64.tar.gz`
- **Windows x64**: `police-alert-windows-x64.exe`
- **macOS x64**: `police-alert-macos-x64.tar.gz`

### 下载构建产物

#### 从 Artifacts 下载（所有构建）

1. 进入 `Actions` 标签
2. 点击对应的工作流运行记录
3. 在 `Artifacts` 部分下载对应平台的文件

#### 从 Releases 下载（标签触发）

1. 进入 `Releases` 标签
2. 找到对应版本
3. 下载 `Assets` 中的文件

---

## 📋 打包流程说明

### 1. 前端构建
```bash
cd frontend
npm ci
npm run build
```
产物位置: `frontend/dist/`

### 2. 复制到后端
```bash
mkdir -p backend/static
cp -r frontend/dist/* backend/static/
```

### 3. 后端打包
```bash
cd backend
pip install -e .
pip install pyinstaller

pyinstaller --name police-alert \
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
```

产物位置: `backend/dist/police-alert` (或 `police-alert.exe`)

---

## 🔧 后端静态文件托管

后端已配置静态文件托管，前端打包产物会被自动托管：

```python
# backend/main.py
from fastapi.staticfiles import StaticFiles

# 挂载静态文件
app.mount("/", StaticFiles(directory="static", html=True), name="static")
```

### 路由说明

- `/` - 前端首页（index.html）
- `/api/*` - 后端 API 接口
- `/docs` - API 文档（Swagger UI）
- `/redoc` - API 文档（ReDoc）

---

## 📝 版本发布流程

### 1. 更新版本号

修改以下文件中的版本号：

- `backend/pyproject.toml`
- `frontend/package.json`

### 2. 提交更改

```bash
git add .
git commit -m "chore: bump version to v1.0.0"
git push
```

### 3. 创建标签

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### 4. 等待构建

GitHub Actions 会自动：
1. 构建前端
2. 打包后端（Windows/Linux/macOS）
3. 创建 Release
4. 上传构建产物

### 5. 发布 Release

构建完成后，Release 会自动创建，包含：
- 版本说明（自动生成）
- 构建产物（3个平台）

---

## 🐛 常见问题

### Q: PyInstaller 打包失败？

A: 确保安装了所有依赖：
```bash
pip install -e .
pip install pyinstaller
```

### Q: 静态文件找不到？

A: 检查 `backend/static/` 目录是否存在且包含前端文件。

### Q: GitHub Actions 构建失败？

A: 检查以下内容：
1. `package-lock.json` 是否存在
2. Python 版本是否为 3.11
3. 依赖是否正确安装

### Q: 可执行文件无法运行？

A:
- **Linux/macOS**: 确保有执行权限 `chmod +x police-alert`
- **Windows**: 检查是否被杀毒软件拦截

---

## 📚 相关文档

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [PyInstaller 文档](https://pyinstaller.org/)
- [FastAPI 静态文件](https://fastapi.tiangolo.com/tutorial/static-files/)
