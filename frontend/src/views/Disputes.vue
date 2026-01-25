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
const filterStatus = ref(null) // null 表示默认筛选（未调解、待盯办）
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
  background: index % 2 === 0 ? 'rgba(30, 58, 138, 0.3)' : 'rgba(30, 58, 138, 0.2)',
  color: item.style?.font_color || '#e5e7eb'
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
      <!-- 筛选按钮 -->
      <div class="filter-bar">
        <button
          @click="handleFilter(null)"
          :class="[
            'filter-btn',
            filterStatus === null ? 'active' : ''
          ]"
        >
          默认筛选
        </button>
        <button
          @click="handleFilter('未调解')"
          :class="[
            'filter-btn',
            filterStatus === '未调解' ? 'active' : ''
          ]"
        >
          未调解
        </button>
        <button
          @click="handleFilter('待盯办')"
          :class="[
            'filter-btn',
            filterStatus === '待盯办' ? 'active' : ''
          ]"
        >
          待盯办
        </button>
      </div>

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
    </div>

    <!-- 悬浮返回按钮 -->
    <FloatingButton />
  </div>
</template>

<style scoped>
.disputes-page {
  height: 100%;
  width: 100%;
  background: url(/main-bg-003.jpg) center/cover no-repeat;
  font-family: sans-serif;
  color: #e5e7eb;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.content-wrapper {
  flex: 1;
  padding: 0.75rem;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.filter-bar {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.filter-btn {
  padding: 0.5rem 1rem;
  background: rgba(14, 165, 233, 0.2);
  border: 1px solid rgba(14, 165, 233, 0.3);
  border-radius: 0.5rem;
  color: #e5e7eb;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.875rem;
}

.filter-btn:hover {
  background: rgba(14, 165, 233, 0.3);
}

.filter-btn.active {
  background: rgba(14, 165, 233, 0.5);
  border-color: rgba(14, 165, 233, 0.6);
  font-weight: 600;
}

.list-container {
  flex: 1;
  background: rgba(6, 24, 70, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(14, 165, 233, 0.3);
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}
</style>
