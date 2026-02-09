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
const filterStatus = ref(null) // null 表示显示所有数据
const scrollTableRef = ref(null)
const rulesDescription = ref('')

// 分页相关
const currentPage = ref(1)
const pageSize = 10
const total = ref(0)

// 表头配置
const headers = [
  { label: '事件名称', width: '280px', align: 'left' },
  { label: '事件类型', width: '120px', align: 'center' },
  { label: '事件内容', flex: 1, align: 'left', wrap: true },
  { label: '事发时间', width: '180px', align: 'center' },
  { label: '风险等级', width: '120px', align: 'center' },
  { label: '责任民警', width: '120px', align: 'center' },
  { label: '处置进度', width: '120px', align: 'center' }
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
  background: index % 2 === 0 ? 'var(--c-table-even-bg)' : 'var(--c-table-odd-bg)',
  color: item.style?.font_color || 'var(--c-text-primary)'
})

// 加载数据
const fetchData = async (page = 1) => {
  loading.value = true
  error.value = null

  try {
    const includeRules = page === 1 ? '&include_rules=true' : ''
    let url = `/api/v1/data/dispute-management?page=${page}&page_size=${pageSize}${includeRules}`
    if (filterStatus.value) {
      url += `&status=${filterStatus.value}`
    }

    const response = await fetch(url)
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

// 筛选按钮点击
const handleFilter = (status) => {
  filterStatus.value = status
  currentPage.value = 1
  total.value = 0
  fetchData(1)
}

onMounted(() => {
  fetchData(1)
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

        <!-- 底部控制栏 -->
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
          <!-- 规则描述 -->
          <div v-if="rulesDescription" class="control-group rules-group">
            <div class="control-label">显示规则</div>
            <div class="rules-text">{{ rulesDescription }}</div>
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
  background: var(--bg-sub) center/cover no-repeat;
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
  background: var(--c-panel-bg);
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
  background: rgba(var(--c-table-rgb), 0.15);
  border-radius: 8px;
  border: 1px solid var(--c-border);
}

.control-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.control-label {
  font-size: 18px;
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
  background: var(--c-control-bg);
  border: 2px solid var(--c-control-border);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.control-btn:hover {
  background: var(--c-control-hover-bg);
  border-color: var(--c-control-hover-border);
}

.control-btn.active {
  color: var(--c-text-primary);
  background: var(--c-primary);
  border-color: var(--c-primary);
  box-shadow: 0 0 10px var(--c-primary);
}

.rules-group {
  margin-left: auto;
  margin-right: 80px;
}

.rules-text {
  color: var(--c-text-secondary);
  font-size: 18px;
}
</style>
