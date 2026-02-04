<script setup>
import { ref, computed, onMounted } from 'vue'
import PageHeader from '@/components/PageHeader.vue'
import ScrollTable from '@/components/ScrollTable.vue'
import FloatingButton from '@/components/FloatingButton.vue'
import { formatDateTime } from '@/utils/datetime'

// 响应式数据
const rawData = ref([])
const loading = ref(true)
const error = ref(null)
const filterStatus = ref(null) // null 表示显示所有数据
const scrollTableRef = ref(null)

// 表头配置
const headers = [
  { label: '事件名称', width: '180px', align: 'left' },
  { label: '事件类型', width: '100px', align: 'center' },
  { label: '事件内容', width: '400px', align: 'left', wrap: true },
  { label: '事发时间', width: '150px', align: 'center' },
  { label: '风险等级', width: '100px', align: 'center' },
  { label: '责任民警', width: '100px', align: 'center' },
  { label: '处置进度', width: '100px', align: 'center' }
]

// 获取单元格值
const getCellValue = (item, columnIndex) => {
  switch (columnIndex) {
    case 0: return item.event_name
    case 1: return item.event_type
    case 2: return item.content
    case 3: return formatDateTime(item.event_time)
    case 4: return item.risk_level
    case 5: return item.officer_name
    case 6: return item.status
    default: return ''
  }
}

// 获取行样式
const getRowStyle = (item, index) => ({
  background: index % 2 === 0 ? 'rgba(var(--c-primary-rgb), 0.2)' : 'rgba(var(--c-primary-rgb), 0.1)',
  color: item.style?.font_color || 'var(--c-text-primary)'
})

// 加载数据
const fetchData = async () => {
  loading.value = true
  error.value = null

  try {
    let url = '/api/v1/data/dispute-management?page=1&page_size=50&include_rules=true'
    if (filterStatus.value) {
      url += `&status=${filterStatus.value}`
    }

    const response = await fetch(url)
    const result = await response.json()

    if (result.code === 200 && result.data) {
      rawData.value = result.data.items || []
      // 数据加载完成后重启滚动
      setTimeout(() => {
        scrollTableRef.value?.restartScroll()
      }, 500)
    } else {
      throw new Error('数据格式错误')
    }
  } catch (err) {
    console.error('加载数据失败:', err)
    error.value = '数据加载失败，请稍后重试'
    rawData.value = []
  } finally {
    loading.value = false
  }
}

// 筛选按钮点击
const handleFilter = (status) => {
  filterStatus.value = status
  fetchData()
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="disputes-page">
    <PageHeader title="矛盾纠纷管理" />

    <div class="content-wrapper">
      <div class="list-wrapper">
        <div class="list-container">
          <!-- 加载状态 -->
          <div v-if="loading" class="h-full flex items-center justify-center">
            <div class="text-xl text-white">数据加载中...</div>
          </div>

          <!-- 错误状态 -->
          <div v-else-if="error" class="h-full flex items-center justify-center">
            <div class="text-xl text-red-400">{{ error }}</div>
          </div>

          <!-- 滚动表格 -->
          <ScrollTable
            v-else-if="rawData.length > 0"
            ref="scrollTableRef"
            :headers="headers"
            :data="rawData"
            :getCellValue="getCellValue"
            :getRowStyle="getRowStyle"
            :autoScroll="true"
            :scrollSpeed="30"
          />

          <!-- 无数据 -->
          <div v-else class="h-full flex items-center justify-center">
            <div class="text-xl text-gray-400">暂无数据</div>
          </div>
        </div>

        <!-- 筛选按钮（底部） -->
        <div class="filter-controls">
          <div class="control-group">
            <div class="control-label">状态筛选</div>
            <div class="control-buttons">
              <button
                @click="handleFilter(null)"
                :class="['control-btn', { active: filterStatus === null }]"
              >
                默认
              </button>
              <button
                @click="handleFilter('未调解')"
                :class="['control-btn', { active: filterStatus === '未调解' }]"
              >
                未调解
              </button>
              <button
                @click="handleFilter('待盯办')"
                :class="['control-btn', { active: filterStatus === '待盯办' }]"
              >
                待盯办
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 悬浮返回按钮 -->
    <FloatingButton />
  </div>
</template>

<style scoped>
.disputes-page {
  height: 100%;
  width: 100%;
  background: url(/main-bg.png) center/cover no-repeat;
  font-family: var(--font-sans);
  color: var(--c-text-primary);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.content-wrapper {
  flex: 1;
  padding: 0 12px 12px 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.list-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--c-bg-panel);
  border: 1px solid var(--c-border);
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 4px 12px var(--c-shadow);
  overflow: hidden;
}

.list-container {
  flex: 1;
  overflow: visible;
  margin-bottom: 12px;
  min-height: 0;
}

/* 底部筛选控制栏 */
.filter-controls {
  flex-shrink: 0;
  display: flex;
  gap: 16px;
  padding: 12px;
  background: rgba(var(--c-primary-rgb), 0.1);
  border-radius: 8px;
  border: 1px solid var(--c-border);
}

.control-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.control-label {
  font-size: 16px;
  font-weight: 600;
  color: var(--c-accent);
  white-space: nowrap;
  margin-right: 4px;
}

.control-buttons {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.control-btn {
  padding: 6px 14px;
  font-size: 15px;
  color: var(--c-text-secondary);
  background: rgba(var(--c-primary-rgb), 0.15);
  border: 2px solid rgba(var(--c-primary-rgb), 0.3);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.control-btn:hover {
  background: rgba(var(--c-primary-rgb), 0.3);
  border-color: rgba(var(--c-primary-rgb), 0.5);
}

.control-btn.active {
  color: var(--c-text-primary);
  background: var(--c-primary);
  border-color: var(--c-primary);
  box-shadow: 0 0 10px var(--c-primary);
}
</style>
