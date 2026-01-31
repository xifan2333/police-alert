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
      background: index % 2 === 0 ? 'rgba(30, 58, 138, 0.3)' : 'rgba(30, 58, 138, 0.2)',
      color: item.style?.font_color || '#e5e7eb'
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
const currentIndex = ref(0)

// 自动轮播（横向）
const startAutoScroll = () => {
  if (!props.autoScroll) return

  if (scrollTimer.value) {
    clearInterval(scrollTimer.value)
  }

  scrollTimer.value = setInterval(() => {
    if (!isPaused.value && scrollContainer.value) {
      const container = scrollContainer.value
      const columns = container.querySelectorAll('.table-column')

      if (columns.length === 0) return

      // 计算下一个索引
      currentIndex.value = (currentIndex.value + 1) % columns.length

      // 获取目标列的位置
      const targetColumn = columns[currentIndex.value]
      const targetLeft = targetColumn.offsetLeft

      // 平滑滚动到目标位置
      container.scrollTo({
        left: targetLeft,
        behavior: 'smooth'
      })
    }
  }, props.scrollSpeed * 50) // 调整轮播间隔（原来是30ms，现在是1500ms）
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
    <!-- 表头（纵向） -->
    <div class="table-header-vertical">
      <div
        v-for="(header, index) in headers"
        :key="index"
        class="header-cell-vertical"
        :style="{
          height: header.height || '60px',
          textAlign: header.align || 'center'
        }"
      >
        {{ header.label }}
      </div>
    </div>

    <!-- 表体（横向滚动） -->
    <div
      ref="scrollContainer"
      class="table-body-horizontal"
      @mouseenter="handleMouseEnter"
      @mouseleave="handleMouseLeave"
    >
      <div
        v-for="(item, colIndex) in data"
        :key="colIndex"
        class="table-column"
        :style="getRowStyle(item, colIndex)"
      >
        <div
          v-for="(header, rowIndex) in headers"
          :key="rowIndex"
          class="table-cell-horizontal"
          :class="{ 'content-cell': header.wrap }"
          :style="{
            height: header.height || '60px',
            textAlign: header.align || 'center',
            justifyContent: header.align === 'left' ? 'flex-start' : header.align === 'right' ? 'flex-end' : 'center'
          }"
        >
          {{ getCellValue(item, rowIndex) }}
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
  flex-direction: row;
  overflow: hidden;
  background: linear-gradient(135deg, rgba(30, 58, 138, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%);
  border-radius: 8px;
  border: 1px solid rgba(59, 130, 246, 0.2);
}

/* 纵向表头 */
.table-header-vertical {
  display: flex;
  flex-direction: column;
  background: linear-gradient(180deg, rgba(30, 58, 138, 0.8) 0%, rgba(30, 58, 138, 0.6) 100%);
  backdrop-filter: blur(10px);
  border-right: 2px solid rgba(59, 130, 246, 0.3);
  flex-shrink: 0;
  min-width: 120px;
}

.header-cell-vertical {
  padding: 0 16px;
  font-weight: 600;
  font-size: 15px;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid rgba(59, 130, 246, 0.2);
  background: rgba(255, 255, 255, 0.05);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.header-cell-vertical:hover {
  background: rgba(59, 130, 246, 0.2);
}

.header-cell-vertical:last-child {
  border-bottom: none;
}

/* 横向表体 */
.table-body-horizontal {
  flex: 1;
  display: flex;
  overflow-x: auto;
  overflow-y: hidden;
  scrollbar-width: thin;
  scrollbar-color: rgba(59, 130, 246, 0.5) rgba(0, 0, 0, 0.2);
  scroll-behavior: smooth;
}

.table-body-horizontal::-webkit-scrollbar {
  height: 6px;
}

.table-body-horizontal::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.table-body-horizontal::-webkit-scrollbar-thumb {
  background: rgba(59, 130, 246, 0.5);
  border-radius: 3px;
}

.table-body-horizontal::-webkit-scrollbar-thumb:hover {
  background: rgba(59, 130, 246, 0.7);
}

/* 表格列 */
.table-column {
  display: flex;
  flex-direction: column;
  min-width: 200px;
  flex-shrink: 0;
  border-right: 1px solid rgba(59, 130, 246, 0.15);
  transition: all 0.3s ease;
}

.table-column:hover {
  background: rgba(59, 130, 246, 0.1) !important;
}

.table-column:last-child {
  border-right: none;
}

/* 横向单元格 */
.table-cell-horizontal {
  padding: 0 16px;
  font-size: 14px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgba(59, 130, 246, 0.1);
  word-break: break-word;
  color: #e5e7eb;
  transition: all 0.2s ease;
}

.table-cell-horizontal:last-child {
  border-bottom: none;
}

/* 内容单元格（支持换行） */
.content-cell {
  text-align: left;
  justify-content: flex-start;
  line-height: 1.6;
  white-space: normal;
  padding: 12px 16px;
}
</style>
