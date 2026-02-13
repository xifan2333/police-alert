<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  // 表头配置
  headers: {
    type: Array,
    required: true,
    // 格式: [{ label: '列名', width: '100px', align: 'center' }]
  },
  // 数据数组
  data: {
    type: Array,
    required: true
  },
  // 获取单元格值的函数
  getCellValue: {
    type: Function,
    required: true
    // (item, columnIndex) => value
  },
  // 获取行样式的函数
  getRowStyle: {
    type: Function,
    default: (item, index) => ({
      background: index % 2 === 0 ? 'var(--c-table-even-bg)' : 'var(--c-table-odd-bg)',
      color: item.style?.font_color || 'var(--c-text-primary)'
    })
  },
  // 获取单元格样式的函数（用于列级别颜色规则）
  getCellStyle: {
    type: Function,
    default: null
    // (item, columnIndex) => { color: '#xxx' } | null
  },
  // 是否启用自动轮播
  autoScroll: {
    type: Boolean,
    default: true
  },
  // 轮播间隔（毫秒）
  interval: {
    type: Number,
    default: 5000
  },
  // 每页显示行数
  pageSize: {
    type: Number,
    default: 10
  },
  // 是否使用远程分页（后端翻页）
  remote: {
    type: Boolean,
    default: false
  },
  // 当前页码（远程分页时由父组件控制，1-indexed）
  page: {
    type: Number,
    default: 1
  },
  // 总记录数（远程分页时必须提供）
  total: {
    type: Number,
    default: 0
  },
  // 是否正在加载（远程分页时使用）
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['page-change', 'header-click'])

// 内部页码状态（仅用于本地分页模式，0-indexed）
const localPage = ref(0)
const carouselTimer = ref(null)
const isPaused = ref(false)
const isSliding = ref(false)

// 当前页码（0-indexed）
const currentPage = computed(() => {
  if (props.remote) {
    return props.page - 1 // 父组件传入1-indexed，转为0-indexed
  }
  return localPage.value
})

// 计算总页数
const totalPages = computed(() => {
  if (props.remote) {
    // 远程分页：根据 total 计算
    if (props.total <= 0) return 0
    return Math.ceil(props.total / props.pageSize)
  } else {
    // 本地分页：根据 data 长度计算
    if (!props.data || props.data.length === 0) return 0
    return Math.ceil(props.data.length / props.pageSize)
  }
})

// 获取当前页数据
const currentPageData = computed(() => {
  if (!props.data || props.data.length === 0) return []
  if (props.remote) {
    // 远程分页：data 就是当前页数据
    return props.data
  } else {
    // 本地分页：从 data 中切片
    const start = currentPage.value * props.pageSize
    const end = start + props.pageSize
    return props.data.slice(start, end)
  }
})

// 切换到下一页
const goToNextPage = () => {
  if (totalPages.value <= 1 || isSliding.value || props.loading) return

  isSliding.value = true
  const nextPage = (currentPage.value + 1) % totalPages.value

  // 等待滑出动画完成后切换数据
  setTimeout(() => {
    if (props.remote) {
      // 远程分页：通知父组件切换页码
      emit('page-change', nextPage + 1) // 转回1-indexed
    } else {
      // 本地分页：直接更新内部状态
      localPage.value = nextPage
    }
    isSliding.value = false
  }, 400)
}

// 切换到指定页
const goToPage = (page) => {
  if (page === currentPage.value || isSliding.value || props.loading) return

  isSliding.value = true

  setTimeout(() => {
    if (props.remote) {
      // 远程分页：通知父组件切换页码
      emit('page-change', page + 1) // 转回1-indexed
    } else {
      // 本地分页：直接更新内部状态
      localPage.value = page
    }
    isSliding.value = false
  }, 400)
}

// 开始自动轮播
const startAutoScroll = () => {
  if (!props.autoScroll || totalPages.value <= 1) return

  stopAutoScroll()

  carouselTimer.value = setInterval(() => {
    if (!isPaused.value) {
      goToNextPage()
    }
  }, props.interval)
}

// 停止自动轮播
const stopAutoScroll = () => {
  if (carouselTimer.value) {
    clearInterval(carouselTimer.value)
    carouselTimer.value = null
  }
}

// 鼠标悬停暂停
const handleMouseEnter = () => {
  isPaused.value = true
}

const handleMouseLeave = () => {
  isPaused.value = false
}

// 重新启动轮播（用于数据更新后）
const restartScroll = () => {
  if (!props.remote) {
    localPage.value = 0
  }
  isSliding.value = false
  stopAutoScroll()
  setTimeout(() => {
    startAutoScroll()
  }, 500)
}

// 监听数据变化（仅本地分页模式）
watch(() => props.data, () => {
  if (!props.remote) {
    // 本地分页：数据变化时重置页码
    localPage.value = 0
    isSliding.value = false
    if (props.autoScroll) {
      restartScroll()
    }
  }
}, { deep: true })

// 监听 total 变化（远程分页模式）
watch(() => props.total, (newTotal, oldTotal) => {
  if (props.remote && props.autoScroll) {
    const newTotalPages = newTotal > 0 ? Math.ceil(newTotal / props.pageSize) : 0
    // 当 totalPages 从 0 或 1 变为 > 1 时启动轮播
    if (newTotalPages > 1 && !carouselTimer.value) {
      startAutoScroll()
    }
  }
})

// 暴露方法给父组件
defineExpose({
  restartScroll,
  stopAutoScroll,
  startAutoScroll,
  goToNextPage,
  goToPage
})

onMounted(() => {
  startAutoScroll()
})

onUnmounted(() => {
  stopAutoScroll()
})
</script>

<template>
  <div class="scroll-table">
    <!-- 表头 -->
    <div class="table-header">
      <div
        v-for="(header, index) in headers"
        :key="index"
        class="header-cell"
        :class="{ sortable: header.sortable, filterable: header.filterable }"
        :style="{
          width: header.flex ? 'auto' : header.width,
          flex: header.flex || 'none',
          textAlign: header.align || 'center'
        }"
        @click="header.sortable ? emit('header-click', header.field) : null"
      >
        <span v-html="header.label"></span>
      </div>
    </div>

    <!-- 表体轮播容器 -->
    <div
      class="table-body"
      @mouseenter="handleMouseEnter"
      @mouseleave="handleMouseLeave"
    >
      <div
        v-for="(item, rowIndex) in currentPageData"
        :key="rowIndex"
        class="table-row"
        :style="getRowStyle(item, props.remote ? rowIndex : currentPage * props.pageSize + rowIndex)"
      >
        <div
          v-for="(header, colIndex) in headers"
          :key="colIndex"
          class="table-cell"
          :class="{ 'content-cell': header.wrap }"
          :style="{
            width: header.flex ? 'auto' : header.width,
            flex: header.flex || 'none',
            textAlign: header.align || 'center',
            justifyContent: header.align === 'left' ? 'flex-start' : header.align === 'right' ? 'flex-end' : 'center'
          }"
        >
          <span class="cell-content" :class="{ 'fade-out': isSliding }" :style="getCellStyle ? getCellStyle(item, colIndex) : null">
            {{ getCellValue(item, colIndex) }}
          </span>
        </div>
      </div>
    </div>

    <!-- 分页指示器 -->
    <div class="pagination-dots" v-if="totalPages > 1">
      <button
        v-for="page in totalPages"
        :key="page"
        class="dot"
        :class="{ active: currentPage === page - 1 }"
        @click="goToPage(page - 1)"
      />
    </div>
  </div>
</template>

<style>
/* 非作用域样式：用于 v-html 注入的排序图标 */
.sort-icon {
  display: inline-block;
  vertical-align: middle;
  margin-left: 4px;
  transition: all 0.2s ease-out;
  position: relative;
  width: 12px;
  height: 14px;
}

/* 升序箭头：向上 */
.sort-icon.asc {
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-bottom: 8px solid currentColor;
}

/* 降序箭头：向下 */
.sort-icon.desc {
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-top: 8px solid currentColor;
}

/* 默认双向箭头 */
.sort-icon.default::before,
.sort-icon.default::after {
  content: '';
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
}

.sort-icon.default::before {
  top: 0;
  border-bottom: 6px solid rgba(255, 255, 255, 0.4);
}

.sort-icon.default::after {
  bottom: 0;
  border-top: 6px solid rgba(255, 255, 255, 0.4);
}
</style>

<style scoped>
/* 表格容器 */
.scroll-table {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 表头 */
.table-header {
  display: flex;
  background: var(--c-table-header-bg);
  border-radius: 4px 4px 0 0;
  padding: 0 8px;
  height: 60px;
  align-items: center;
  flex-shrink: 0;
  border-bottom: 2px solid var(--c-border);
}

.header-cell {
  padding: 0 8px;
  font-weight: 800;
  font-size: 26px;
  color: var(--c-text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.header-cell.sortable {
  cursor: pointer;
  user-select: none;
}

.header-cell.sortable:hover {
  color: var(--c-primary);
}

/* 表体 */
.table-body {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  background: transparent;
}

/* 表格行 */
.table-row {
  display: flex;
  padding: 16px 8px;
  border-bottom: 1px solid var(--c-border-light);
  transition: background 0.2s;
  flex: 1;
  flex-shrink: 0;
}

.table-row:hover {
  background: rgba(var(--c-table-rgb), 0.35) !important;
}

/* 表格单元格 */
.table-cell {
  padding: 0 8px;
  font-size: 22px;
  font-weight: 600;
  display: flex;
  align-items: center;
  text-align: center;
  word-break: break-word;
  color: inherit;
}

/* 内容单元格（支持换行） */
.content-cell {
  text-align: left;
  justify-content: flex-start;
  line-height: 1.6;
  white-space: normal;
}

/* 单元格内容 - 淡入淡出效果 */
.cell-content {
  opacity: 1;
  transition: opacity 0.3s ease;
  color: inherit;
}

.cell-content.fade-out {
  opacity: 0;
}

/* 分页指示器 */
.pagination-dots {
  display: flex;
  justify-content: center;
  gap: 8px;
  padding: 12px 0;
  flex-shrink: 0;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(var(--c-table-rgb), 0.3);
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
}

.dot:hover {
  background: rgba(var(--c-table-rgb), 0.5);
  transform: scale(1.2);
}

.dot.active {
  background: var(--c-primary);
  box-shadow: 0 0 8px var(--c-primary);
  transform: scale(1.2);
}
</style>
