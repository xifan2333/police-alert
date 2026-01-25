# 全局 UI 元素放大实施计划（方案 C）

> **方案**: 全局根字体混合方案
> **目标**: 将所有 UI 元素放大 2 倍，适配 3840x2160 显示器
> **实施日期**: 2026-01-24

---

## 📋 核心策略

通过调整根 `<html>` 的 `font-size` 从 16px 改为 32px，使所有使用 rem 单位的工具类自动翻倍。

---

## 🎯 文件修改清单

### 需要修改的文件

1. **`frontend/src/main.js`** - 引入全局样式文件
2. **`frontend/src/assets/global.css`** - 新建，设置根字体大小
3. **`frontend/src/views/Situation.vue`** - 手动调整 ECharts 配置中的 px 值
4. **其他 `.vue` 文件** - 审查并修正边框和其他 px 值

---

## 🔧 实施步骤

### 步骤 1：建立代码基线
```bash
git checkout -b feature/ui-scaling-4k
```

### 步骤 2：调整 rem 基准（核心改动）

#### 2.1 创建全局样式文件
- 创建 `frontend/src/assets/global.css`
- 内容：
```css
/*
 * 全局 UI 缩放基准
 * ----------------------------------------
 * 默认浏览器根字体大小为 16px，UnoCSS/Tailwind 的 rem 单位基于此计算。
 * 将根字体大小调整为 32px，使得 1rem = 32px。
 * 所有使用 rem 的工具类（text-*, w-*, p-* 等）的渲染尺寸将自动放大两倍。
 */
html {
  font-size: 32px;
}
```

#### 2.2 引入全局样式
- 修改 `frontend/src/main.js`
- 在顶部添加：
```javascript
import './assets/global.css'
```

### 步骤 3：手动调整 ECharts 图表尺寸

**文件**: `frontend/src/views/Situation.vue`

**操作**:
1. 定位到 ECharts 的 `option` 配置对象
2. 全局搜索 `fontSize:`、`symbolSize:`、`itemWidth:`、`itemHeight:` 等属性
3. 将所有数值**乘以 2**

**示例**:
```javascript
// 修改前
const option = {
  textStyle: {
    fontSize: 10,
  },
  legend: {
    itemWidth: 12,
    itemHeight: 12,
  },
};

// 修改后
const option = {
  textStyle: {
    fontSize: 20, // 10 * 2
  },
  legend: {
    itemWidth: 24,  // 12 * 2
    itemHeight: 24, // 12 * 2
  },
};
```

### 步骤 4：审查并修正 1px 边框问题

**操作**:
1. 全局搜索包含 ` border ` 但不包含 `border-` 的类
2. 对于需要加粗的边框，将 `border` 替换为 `border-2`

**示例**:
```html
<!-- 修改前 -->
<div class="border border-blue-500 rounded">...</div>

<!-- 修改后 -->
<div class="border-2 border-blue-500 rounded">...</div>
```

---

## ✅ 测试验证要点

### 1. 全局观感
- [ ] 整体 UI 是否按预期放大了约两倍？
- [ ] 布局是否和谐，没有元素重叠或溢出？

### 2. 字体和文本
- [ ] **首页 (`Home.vue`)**: 标题字号是否显著增大？
- [ ] **页头 (`PageHeader.vue`)**: 标题和返回按钮文本是否清晰可读？
- [ ] **表格 (`ScrollTable.vue`)**: 表格内的文字是否已放大，行高是否合适？

### 3. 图标和图片
- [ ] **首页 (`Home.vue`)**: 警徽图标是否清晰，没有模糊？
- [ ] **页头 (`PageHeader.vue`)**: 左上角的小警徽是否也已同步放大且清晰？

### 4. 图表（关键）
- [ ] **警情态势页 (`Situation.vue`)**:
  - [ ] X/Y 轴的标签字体是否已放大？
  - [ ] 图例 (legend) 的文字和色块是否已放大？
  - [ ] 鼠标悬浮时的提示框 (tooltip) 内容是否清晰、尺寸合适？
  - [ ] 图表内的其他文本标签是否也已缩放？

### 5. 交互元素
- [ ] 按钮、输入框、下拉菜单等，尺寸是否合适，易于点击？
- [ ] 鼠标悬浮 (`hover`) 效果是否正常？

---

## ⚠️ 潜在风险和注意事项

### 1. 位图资源模糊
- **风险**: `.png`, `.jpg` 等位图在拉伸后可能会变得模糊
- **缓解措施**: 建议提供 `@2x` 或更高分辨率的图片资源，SVG 格式无此问题

### 2. 未覆盖的 `px` 单位
- **风险**: 第三方组件或自定义 JS 逻辑中可能存在未被发现的 `px` 单位
- **缓解措施**: 在测试阶段特别留意"格格不入"的小元素，全局搜索 `px` 关键字排查

### 3. 开发环境体验
- **注意**: 在 1080p 开发显示器上，UI 将会显得非常巨大（根字体是 `32px`）
- **说明**: 这是预期行为，不影响最终在 4K 目标屏幕上的效果

### 4. `vh`/`vw` 单位
- **注意**: `vh` 或 `vw` 单位不受 `rem` 影响，继续相对于视口尺寸计算
- **操作**: 检查使用了这些单位的元素在缩放后是否表现正常

---

## 📊 预期效果对比

| 元素 | 当前尺寸 | 修改后尺寸 | 变化 |
|------|----------|------------|------|
| 标题 `text-4xl` | 36px | 72px | ✅ 自动 2x |
| 页面标题 `text-lg` | 18px | 36px | ✅ 自动 2x |
| 警徽图标 `w-16 h-16` | 64px | 128px | ✅ 自动 2x |
| 按钮 `w-16 h-16` | 64px | 128px | ✅ 自动 2x |
| 间距 `p-4` | 16px | 32px | ✅ 自动 2x |
| ECharts `fontSize: 10` | 10px | 20px | ⚠️ 手动修改 |
| 边框 `border` | 1px | 1px | ⚠️ 可选改为 `border-2` |

---

## 🎯 实施优先级

1. **P0 - 核心改动**: 创建 `global.css` 并引入到 `main.js`
2. **P1 - 图表修正**: 修改 `Situation.vue` 中的 ECharts 配置
3. **P2 - 边框优化**: 审查并修正 `1px` 边框问题
4. **P3 - 全面测试**: 按测试验证要点逐项检查

---

## 📝 回滚方案

如果出现问题，可以快速回滚：
```bash
git checkout main
git branch -D feature/ui-scaling-4k
```

或者只回滚 `global.css` 的修改：
```css
html {
  font-size: 16px; /* 恢复默认值 */
}
```
