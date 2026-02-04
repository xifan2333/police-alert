<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

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
      background: index % 2 === 0 ? 'rgba(var(--c-primary-light-rgb), 0.2)' : 'rgba(var(--c-primary-light-rgb), 0.1)',
      color: item.style?.font_color || 'var(--c-text-primary)'
    })
  },
  // 是否启用自动滚动
  autoScroll: {
    type: Boolean,
    default: true
  },
  // 滚动速度（毫秒）
  scrollSpeed: {
    type: Number,
    default: 30
  }
})

const scrollContainer = ref(null)
const scrollTimer = ref(null)
const isPaused = ref(false)

// 自动滚动
const startAutoScroll = () => {
  if (!props.autoScroll) return

  if (scrollTimer.value) {
    clearInterval(scrollTimer.value)
  }

  scrollTimer.value = setInterval(() => {
    if (!isPaused.value && scrollContainer.value) {
      const container = scrollContainer.value
      const scrollStep = 1

      if (container.scrollTop + container.clientHeight >= container.scrollHeight) {
        // 滚动到底部，回到顶部
        container.scrollTop = 0
      } else {
        container.scrollTop += scrollStep
      }
    }
  }, props.scrollSpeed)
}

// 停止滚动
const stopAutoScroll = () => {
  if (scrollTimer.value) {
    clearInterval(scrollTimer.value)
    scrollTimer.value = null
  }
}

// 鼠标悬停暂停
const handleMouseEnter = () => {
  isPaused.value = true
}

const handleMouseLeave = () => {
  isPaused.value = false
}

// 重新启动滚动（用于数据更新后）
const restartScroll = () => {
  stopAutoScroll()
  setTimeout(() => {
    startAutoScroll()
  }, 500)
}

// 暴露方法给父组件
defineExpose({
  restartScroll,
  stopAutoScroll,
  startAutoScroll
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

    <!-- 表体 -->
    <div
      ref="scrollContainer"
      class="table-body"
      @mouseenter="handleMouseEnter"
      @mouseleave="handleMouseLeave"
    >
      <div
        v-for="(item, rowIndex) in data"
        :key="rowIndex"
        class="table-row"
        :style="getRowStyle(item, rowIndex)"
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
          {{ getCellValue(item, colIndex) }}
        </div>
      </div>
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
  background: linear-gradient(180deg, rgba(var(--c-primary-light-rgb), 0.6) 0%, rgba(var(--c-primary-light-rgb), 0.4) 100%);
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
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  scrollbar-color: rgba(var(--c-primary-light-rgb), 0.5) rgba(0, 0, 0, 0.2);
  background: transparent;
}

.table-body::-webkit-scrollbar {
  width: 6px;
}

.table-body::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.table-body::-webkit-scrollbar-thumb {
  background: rgba(var(--c-primary-light-rgb), 0.5);
  border-radius: 3px;
}

.table-body::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--c-primary-light-rgb), 0.7);
}

/* 表格行 */
.table-row {
  display: flex;
  padding: 16px 8px;
  border-bottom: 1px solid var(--c-border-light);
  transition: background 0.2s;
  min-height: 80px;
}

.table-row:hover {
  background: rgba(var(--c-primary-light-rgb), 0.15) !important;
}

/* 表格单元格 */
.table-cell {
  padding: 0 8px;
  font-size: 14px;
  display: flex;
  align-items: center;
  text-align: center;
  word-break: break-word;
  color: var(--c-text-primary);
}

/* 内容单元格（支持换行） */
.content-cell {
  text-align: left;
  justify-content: flex-start;
  line-height: 1.6;
  white-space: normal;
}
</style>
