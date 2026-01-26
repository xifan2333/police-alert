<script setup>
import { ref, onMounted } from 'vue'
import PageHeader from '@/components/PageHeader.vue'
import ScrollTable from '@/components/ScrollTable.vue'
import FloatingButton from '@/components/FloatingButton.vue'
import { formatDateTime } from '@/utils/datetime'
import { applyRowStyles } from '@/utils/styleApplicator'

// 响应式数据
const rawData = ref([])
const loading = ref(true)
const error = ref(null)
const scrollTableRef = ref(null)

// 表头配置
const headers = [
  { label: '案件编号', width: '180px', align: 'center' },
  { label: '案件名称', width: '200px', align: 'left' },
  { label: '案发时间', width: '150px', align: 'center' },
  { label: '案件类型', width: '100px', align: 'center' },
  { label: '风险问题', width: '250px', align: 'left', wrap: true },
  { label: '整改期限', width: '150px', align: 'center' },
  { label: '剩余天数', width: '100px', align: 'center' },
  { label: '责任民警', width: '100px', align: 'center' }
]

// 获取单元格值
const getCellValue = (item, columnIndex) => {
  switch (columnIndex) {
    case 0: return item.case_number
    case 1: return item.case_name
    case 2: return formatDateTime(item.case_time)
    case 3: return item.case_type
    case 4: return Array.isArray(item.risk_issues) ? item.risk_issues.join(', ') : item.risk_issues
    case 5: return formatDateTime(item.deadline)
    case 6: return `${item.days_remaining}天`
    case 7: return item.officer_name
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
    const response = await fetch('/api/v1/data/risk-supervision?page=1&page_size=50&include_rules=true')
    const result = await response.json()

    if (result.code === 200 && result.data) {
      const items = result.data.items || []
      const rules = result.data.rules || []

      // 使用统一的样式应用函数
      rawData.value = applyRowStyles(items, rules)

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

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="cases-page">
    <PageHeader title="执法问题盯办" />

    <div class="content-wrapper">
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
.cases-page {
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
}

.list-container {
  height: 100%;
  background: rgba(6, 24, 70, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(14, 165, 233, 0.3);
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}
</style>
