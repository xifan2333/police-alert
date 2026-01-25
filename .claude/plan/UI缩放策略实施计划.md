# UI 缩放策略实施计划

> **方案**: CSS Transform 等比缩放
> **目标**: 1920x1080 → 4096x2160 视觉效果一致
> **实施日期**: 2026-01-24

---

## 📋 核心文件变更

- **创建**: `src/components/ScaleContainer.vue` (核心缩放逻辑)
- **创建**: `src/config/design.js` (设计尺寸管理)
- **修改**: `src/App.vue` (集成 ScaleContainer 组件)
- **优化**: Logo 转 SVG，背景图 4K 版本

---

## 🎯 实施步骤

### 步骤 1: 创建配置文件
- 创建 `src/config/design.js`
- 定义 DESIGN_WIDTH = 1920, DESIGN_HEIGHT = 1080

### 步骤 2: 创建 ScaleContainer 组件
- 创建 `src/components/ScaleContainer.vue`
- 实现缩放逻辑和防抖优化

### 步骤 3: 集成到 App.vue
- 用 ScaleContainer 包裹 router-view

### 步骤 4: 资源优化
- Logo 转 SVG
- 背景图 4K 版本 + 媒体查询

---

## ✅ 验证清单

- [ ] 1920x1080 下视觉效果正常
- [ ] 4096x2160 下视觉效果与开发环境一致
- [ ] 非 16:9 比例下有黑边且居中
- [ ] 所有交互功能正常
- [ ] 资源加载正确（4K 背景图、SVG logo）
- [ ] 页面滚动正常

---

## 🔧 测试方法

使用 Chrome DevTools:
1. F12 打开开发者工具
2. Toggle device toolbar
3. 输入 4096x2160 测试
4. 验证缩放效果和交互
