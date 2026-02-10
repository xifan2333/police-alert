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
const rulesDescription = ref('')

// 分页相关
const currentPage = ref(1)
const pageSize = 10
const total = ref(0)

// 表头配置
const headers = [
  { label: '案件编号', width: '200px', align: 'center' },
  { label: '案件名称', width: '280px', align: 'center' },
  { label: '案发时间', width: '180px', align: 'center' },
  { label: '案件类型', width: '120px', align: 'center' },
  { label: '风险问题', flex: 1, align: 'left', wrap: true },
  { label: '整改期限', width: '180px', align: 'center' },
  { label: '剩余天数', width: '120px', align: 'center' },
  { label: '责任民警', width: '120px', align: 'center' }
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

// 获取行样式（不再应用规则颜色到整行）
const getRowStyle = (item, index) => ({
  background: index % 2 === 0 ? 'var(--c-table-even-bg)' : 'var(--c-table-odd-bg)',
  color: 'var(--c-text-primary)'
})

// 字段名到列索引的映射
const fieldColumnMap = {
  days_remaining: 6
}

// 获取单元格样式（规则颜色只作用于判断标准列）
const getCellStyle = (item, columnIndex) => {
  const style = item.style
  if (!style?.font_color || !style?.field) return null
  if (fieldColumnMap[style.field] !== columnIndex) return null
  return { color: style.font_color, fontWeight: 'bold' }
}

// 加载数据
const fetchData = async (page = 1) => {
  loading.value = true
  error.value = null

  try {
    const includeRules = page === 1 ? '&include_rules=true' : ''
    const response = await fetch(`/api/v1/data/risk-supervision?page=${page}&page_size=${pageSize}${includeRules}`)
    const result = await response.json()

    if (result.code === 200 && result.data) {
      const items = result.data.items || []
      const rules = result.data.rules || []

      // 更新总数
      total.value = result.data.total || 0
      currentPage.value = page

      // 使用统一的样式应用函数
      rawData.value = applyRowStyles(items, rules)

      // 只在首次加载时提取规则描述
      if (page === 1 && rules.length > 0) {
        const descriptions = rules
          .filter(r => r.description)
          .map(r => r.description)
        rulesDescription.value = descriptions.join(' | ') || ''
      }
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

// 处理页码变化
const handlePageChange = (page) => {
  fetchData(page)
}

onMounted(() => {
  fetchData(1)
})
</script>

<template>
  <div class="cases-page">
    <PageHeader title="执法问题盯办" />

    <div class="content-wrapper">
      <div class="list-container">
        <div class="table-wrapper">
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
            :getCellStyle="getCellStyle"
            :autoScroll="true"
            :interval="10000"
            :pageSize="pageSize"
            :remote="true"
            :page="currentPage"
            :total="total"
            :loading="loading"
            @page-change="handlePageChange"
          />

          <!-- 无数据 -->
          <div v-else class="h-full flex items-center justify-center">
            <div class="text-xl text-gray-400">暂无数据</div>
          </div>
        </div>

        <!-- 规则描述 -->
        <div v-if="rulesDescription" class="rules-description">
          <span class="rules-label">显示规则：</span>
          <span class="rules-text" v-html="rulesDescription"></span>
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
  background: var(--bg-sub) center/cover no-repeat;
  font-family: var(--font-sans);
  color: var(--c-text-primary);
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
  background: var(--c-panel-bg);
  border: 1px solid var(--c-border);
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 4px 12px var(--c-shadow);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.table-wrapper {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.rules-description {
  flex-shrink: 0;
  margin-top: 12px;
  padding: 10px 16px;
  padding-right: 80px;
  background: rgba(var(--c-table-rgb), 0.15);
  border-radius: 6px;
  border: 1px solid var(--c-border);
  font-size: 18px;
}

.rules-label {
  color: var(--c-accent);
  font-weight: 600;
  margin-right: 8px;
}

.rules-text {
  color: var(--c-text-secondary);
}
</style>
