<script setup>
import { ref, computed, onMounted } from 'vue'
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
const filterRiskLevel = ref(null) // 风险等级筛选
const filterOfficer = ref(null) // 警员筛选
const sortField = ref('event_time')
const sortOrder = ref('desc')
const scrollTableRef = ref(null)
const rulesDescription = ref('')

// 警员选项
const officerOptions = ref([])

// Dropdown 状态
const dropdowns = ref({
  riskLevel: false,
  status: false,
  officer: false
})

// 分页相关
const currentPage = ref(1)
const pageSize = 6
const total = ref(0)

// 表头配置
const headers = computed(() => [
  { label: '事件名称', width: '280px', align: 'center' },
  { label: `事件类型 ${getSortIcon('event_type')}`, width: '150px', align: 'center', sortable: true, field: 'event_type' },
  { label: '事件内容', flex: 1, align: 'left', wrap: true },
  { label: `事发时间 ${getSortIcon('event_time')}`, width: '180px', align: 'center', sortable: true, field: 'event_time' },
  { label: '风险等级', width: '120px', align: 'center' },
  { label: '责任民警', width: '120px', align: 'center' },
  { label: '处置进度', width: '120px', align: 'center' }
])

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

// 获取行样式（不再应用规则颜色到整行）
const getRowStyle = (item, index) => ({
  background: index % 2 === 0 ? 'var(--c-table-even-bg)' : 'var(--c-table-odd-bg)',
  color: 'var(--c-text-primary)'
})

// 字段名到列索引的映射
const fieldColumnMap = {
  risk_level: 4
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
    let url = `/api/v1/data/dispute-management?page=${page}&page_size=${pageSize}${includeRules}`
    if (filterStatus.value) {
      url += `&status=${filterStatus.value}`
    }
    if (filterRiskLevel.value) {
      url += `&risk_level=${filterRiskLevel.value}`
    }
    if (filterOfficer.value) {
      url += `&officer_name=${filterOfficer.value}`
    }
    url += `&sort_field=${sortField.value}&sort_order=${sortOrder.value}`

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
const handleFilter = (type, value) => {
  if (type === 'status') filterStatus.value = value
  else if (type === 'risk_level') filterRiskLevel.value = value
  else if (type === 'officer') filterOfficer.value = value
  currentPage.value = 1
  total.value = 0
  fetchData(1)
  // 关闭所有 dropdown
  Object.keys(dropdowns.value).forEach(key => dropdowns.value[key] = false)
}

// 切换 dropdown
const toggleDropdown = (name) => {
  dropdowns.value[name] = !dropdowns.value[name]
  // 关闭其他 dropdown
  Object.keys(dropdowns.value).forEach(key => {
    if (key !== name) dropdowns.value[key] = false
  })
}

// 获取筛选选项
const fetchFilterOptions = async () => {
  try {
    const response = await fetch('/api/v1/data/dispute-management/filter-options')
    const result = await response.json()
    if (result.code === 200) {
      officerOptions.value = result.data.officers || []
    }
  } catch (err) {
    console.error('获取筛选选项失败:', err)
  }
}

// 排序处理
const handleSort = (field) => {
  if (sortField.value === field) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortOrder.value = 'asc'
  }
  currentPage.value = 1
  fetchData(1)
}

// 获取排序图标
const getSortIcon = (field) => {
  if (sortField.value === field) {
    const directionClass = sortOrder.value === 'asc' ? 'asc' : 'desc'
    return `<span class="sort-icon ${directionClass}"></span>`
  } else {
    return `<span class="sort-icon default"></span>`
  }
}

onMounted(() => {
  fetchFilterOptions()
  fetchData(1)
})
</script>

<template>
  <div class="disputes-page">
    <PageHeader title="矛盾纠纷管理" />

    <div class="content-wrapper">
      <div class="list-wrapper">
        <div class="list-container">
          <!-- 表格工具栏：筛选器 -->
          <div class="table-toolbar">
            <!-- 风险等级 -->
            <div class="dropdown-wrapper">
              <button class="dropdown-btn" @click="toggleDropdown('riskLevel')">
                风险等级: {{ filterRiskLevel || '全部' }}
                <span class="arrow"></span>
              </button>
              <div v-show="dropdowns.riskLevel" class="dropdown-menu">
                <div @click="handleFilter('risk_level', null)" :class="['dropdown-item', { active: filterRiskLevel === null }]">全部</div>
                <div @click="handleFilter('risk_level', '高')" :class="['dropdown-item', { active: filterRiskLevel === '高' }]">高</div>
                <div @click="handleFilter('risk_level', '中')" :class="['dropdown-item', { active: filterRiskLevel === '中' }]">中</div>
                <div @click="handleFilter('risk_level', '低')" :class="['dropdown-item', { active: filterRiskLevel === '低' }]">低</div>
              </div>
            </div>

            <!-- 责任民警 -->
            <div class="dropdown-wrapper">
              <button class="dropdown-btn" @click="toggleDropdown('officer')">
                责任民警: {{ filterOfficer || '全部' }}
                <span class="arrow"></span>
              </button>
              <div v-show="dropdowns.officer" class="dropdown-menu">
                <div @click="handleFilter('officer', null)" :class="['dropdown-item', { active: filterOfficer === null }]">全部</div>
                <div
                  v-for="officer in officerOptions"
                  :key="officer"
                  @click="handleFilter('officer', officer)"
                  :class="['dropdown-item', { active: filterOfficer === officer }]"
                >
                  {{ officer }}
                </div>
              </div>
            </div>

            <!-- 处置进度 -->
            <div class="dropdown-wrapper">
              <button class="dropdown-btn" @click="toggleDropdown('status')">
                处置进度: {{ filterStatus || '全部' }}
                <span class="arrow"></span>
              </button>
              <div v-show="dropdowns.status" class="dropdown-menu">
                <div @click="handleFilter('status', null)" :class="['dropdown-item', { active: filterStatus === null }]">全部</div>
                <div @click="handleFilter('status', '待化解')" :class="['dropdown-item', { active: filterStatus === '待化解' }]">待化解</div>
                <div @click="handleFilter('status', '待关注')" :class="['dropdown-item', { active: filterStatus === '待关注' }]">待关注</div>
              </div>
            </div>
          </div>

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
            @header-click="handleSort"
          />

          <!-- 无数据 -->
          <div v-else class="h-full flex items-center justify-center">
            <div class="text-xl text-gray-400">暂无数据</div>
          </div>
        </div>

        <!-- 底部规则显示 -->
        <div v-if="rulesDescription" class="rules-display">
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
  display: flex;
  flex-direction: column;
}

.table-toolbar {
  flex-shrink: 0;
  padding-bottom: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.rules-display {
  flex-shrink: 0;
  padding: 10px 16px;
  background: rgba(var(--c-table-rgb), 0.15);
  border-radius: 6px;
  border: 1px solid var(--c-border);
  display: flex;
  align-items: center;
  gap: 8px;
}

.rules-label {
  font-size: 22px;
  font-weight: 600;
  color: var(--c-accent);
  white-space: nowrap;
}

.rules-text {
  font-size: 22px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.rules-text :deep(span) {
  color: inherit;
}

.dropdown-wrapper {
  position: relative;
}

.dropdown-btn {
  padding: 6px 14px;
  font-size: 22px;
  color: var(--c-text-secondary);
  background: var(--c-control-bg);
  border: 2px solid var(--c-control-border);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 6px;
}

.dropdown-btn:hover {
  background: var(--c-control-hover-bg);
  border-color: var(--c-control-hover-border);
}

.dropdown-btn .arrow {
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 7px solid currentColor;
  transition: transform 0.2s ease-out;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 4px;
  background: rgba(30, 58, 138, 0.95);
  backdrop-filter: blur(10px);
  border: 2px solid var(--c-control-border);
  border-radius: 6px;
  overflow: hidden;
  z-index: 1000;
  min-width: 100%;
  max-height: 300px;
  overflow-y: auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.dropdown-item {
  padding: 8px 14px;
  font-size: 22px;
  color: var(--c-text-secondary);
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.dropdown-item:hover {
  background: var(--c-control-hover-bg);
  color: var(--c-primary);
}

.dropdown-item.active {
  color: var(--c-text-primary);
  background: var(--c-primary);
  border-color: var(--c-primary);
  box-shadow: 0 0 10px var(--c-primary);
  font-weight: bold;
}
</style>
