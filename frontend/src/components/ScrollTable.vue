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
  }
})

const currentPage = ref(0)
const carouselTimer = ref(null)
const isPaused = ref(false)
const isSliding = ref(false)

// 计算总页数
const totalPages = computed(() => {
  if (!props.data || props.data.length === 0) return 0
  return Math.ceil(props.data.length / props.pageSize)
})

// 获取当前页数据
const currentPageData = computed(() => {
  if (!props.data || props.data.length === 0) return []
  const start = currentPage.value * props.pageSize
  const end = start + props.pageSize
  return props.data.slice(start, end)
})

// 切换到下一页
const goToNextPage = () => {
  if (totalPages.value <= 1 || isSliding.value) return

  isSliding.value = true

  // 等待滑出动画完成后切换数据
  setTimeout(() => {
    currentPage.value = (currentPage.value + 1) % totalPages.value
    isSliding.value = false
  }, 400)
}

// 切换到指定页
const goToPage = (page) => {
  if (page === currentPage.value || isSliding.value) return

  isSliding.value = true

  setTimeout(() => {
    currentPage.value = page
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
  currentPage.value = 0
  isSliding.value = false
  stopAutoScroll()
  setTimeout(() => {
    startAutoScroll()
  }, 500)
}

// 监听数据变化
watch(() => props.data, () => {
  currentPage.value = 0
  isSliding.value = false
  if (props.autoScroll) {
    restartScroll()
  }
}, { deep: true })

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
        :style="{
          width: header.width,
          textAlign: header.align || 'center'
        }"
      >
        {{ header.label }}
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
        :style="getRowStyle(item, currentPage * pageSize + rowIndex)"
      >
        <div
          v-for="(header, colIndex) in headers"
          :key="colIndex"
          class="table-cell"
          :class="{ 'content-cell': header.wrap }"
          :style="{
            width: header.width,
            textAlign: header.align || 'center',
            justifyContent: header.align === 'left' ? 'flex-start' : header.align === 'right' ? 'flex-end' : 'center'
          }"
        >
          <span class="cell-content" :class="{ 'fade-out': isSliding }">
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
  height: 50px;
  align-items: center;
  flex-shrink: 0;
  border-bottom: 2px solid var(--c-border);
}

.header-cell {
  padding: 0 8px;
  font-weight: 600;
  font-size: 16px;
  color: var(--c-text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
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
  min-height: 80px;
  flex-shrink: 0;
}

.table-row:hover {
  background: rgba(var(--c-table-rgb), 0.35) !important;
}

/* 表格单元格 */
.table-cell {
  padding: 0 8px;
  font-size: 14px;
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
