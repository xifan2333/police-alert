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
const scrollTableRef = ref(null)
const rulesDescription = ref('')

// 筛选和排序
const filterCaseType = ref(null)
const filterProblemType = ref(null)
const filterOfficer = ref(null)
const sortField = ref('days_remaining')
const sortOrder = ref('asc')

// 警员选项
const officerOptions = ref([])
const caseTypeOptions = ref([])

// Dropdown 状态
const dropdowns = ref({
  caseType: false,
  problemType: false,
  officer: false
})

// 分页相关
const currentPage = ref(1)
const pageSize = 6
const total = ref(0)

// 表头配置
const headers = computed(() => [
  { label: `案件编号 ${getSortIcon('case_number')}`, width: '260px', align: 'center', sortable: true, field: 'case_number' },
  { label: '案件名称', width: '280px', align: 'center' },
  { label: `案发时间 ${getSortIcon('case_time')}`, width: '180px', align: 'center', sortable: true, field: 'case_time' },
  { label: '案件类型', width: '120px', align: 'center', filterable: true },
  { label: '问题类型', width: '150px', align: 'center', filterable: true },
  { label: '具体内容', flex: 1, align: 'left', wrap: true },
  { label: `整改期限 ${getSortIcon('deadline')}`, width: '180px', align: 'center', sortable: true, field: 'deadline' },
  { label: `剩余天数 ${getSortIcon('days_remaining')}`, width: '160px', align: 'center', sortable: true, field: 'days_remaining' },
  { label: '责任民警', width: '120px', align: 'center', filterable: true }
])

// 获取单元格值
const getCellValue = (item, columnIndex) => {
  switch (columnIndex) {
    case 0: return item.case_number
    case 1: return item.case_name
    case 2: return formatDateTime(item.case_time)
    case 3: return item.case_type
    case 4: return item.problem_type
    case 5: return Array.isArray(item.specific_content) ? item.specific_content.join(', ') : item.specific_content
    case 6: return formatDateTime(item.deadline)
    case 7: return `${item.days_remaining}天`
    case 8: return item.officer_name
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
  days_remaining: 7
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
    let url = `/api/v1/data/risk-supervision?page=${page}&page_size=${pageSize}${includeRules}`

    if (filterCaseType.value) url += `&case_type=${filterCaseType.value}`
    if (filterProblemType.value) url += `&problem_type=${filterProblemType.value}`
    if (filterOfficer.value) url += `&officer_name=${filterOfficer.value}`
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

// 筛选处理
const handleFilter = (type, value) => {
  if (type === 'case_type') filterCaseType.value = value
  else if (type === 'problem_type') filterProblemType.value = value
  else if (type === 'officer') filterOfficer.value = value
  currentPage.value = 1
  fetchData(1)
  Object.keys(dropdowns.value).forEach(key => dropdowns.value[key] = false)
}

// 排序处理
const handleSort = (field) => {
  console.log('handleSort called with field:', field)
  console.log('current sortField:', sortField.value, 'sortOrder:', sortOrder.value)

  if (sortField.value === field) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortOrder.value = 'asc'
  }

  console.log('new sortField:', sortField.value, 'sortOrder:', sortOrder.value)
  currentPage.value = 1
  fetchData(1)
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
    const response = await fetch('/api/v1/data/risk-supervision/filter-options')
    const result = await response.json()
    if (result.code === 200) {
      officerOptions.value = result.data.officers || []
      caseTypeOptions.value = result.data.case_types || []
    }
  } catch (err) {
    console.error('获取筛选选项失败:', err)
  }
}

// 获取排序图标
const getSortIcon = (field) => {
  if (sortField.value === field) {
    // 当前排序字段：显示高亮的上/下箭头
    const directionClass = sortOrder.value === 'asc' ? 'asc' : 'desc'
    return `<span class="sort-icon ${directionClass}"></span>`
  } else {
    // 其他可排序字段：显示默认的双向箭头
    return `<span class="sort-icon default"></span>`
  }
}

onMounted(() => {
  fetchFilterOptions()
  fetchData(1)
})
</script>

<template>
  <div class="cases-page">
    <PageHeader title="执法问题盯办" />

    <div class="content-wrapper">
      <div class="list-container">
        <!-- 表格工具栏：筛选器 -->
        <div class="table-toolbar">
          <!-- 案件类型 -->
          <div class="dropdown-wrapper">
            <button class="dropdown-btn" @click="toggleDropdown('caseType')">
              案件类型: {{ filterCaseType || '全部' }}
              <span class="arrow"></span>
            </button>
            <div v-show="dropdowns.caseType" class="dropdown-menu">
              <div @click="handleFilter('case_type', null)" :class="['dropdown-item', { active: filterCaseType === null }]">全部</div>
              <div
                v-for="caseType in caseTypeOptions"
                :key="caseType"
                @click="handleFilter('case_type', caseType)"
                :class="['dropdown-item', { active: filterCaseType === caseType }]"
              >
                {{ caseType }}
              </div>
            </div>
          </div>

          <!-- 问题类型 -->
          <div class="dropdown-wrapper">
            <button class="dropdown-btn" @click="toggleDropdown('problemType')">
              问题类型: {{ filterProblemType || '全部' }}
              <span class="arrow"></span>
            </button>
            <div v-show="dropdowns.problemType" class="dropdown-menu">
              <div @click="handleFilter('problem_type', null)" :class="['dropdown-item', { active: filterProblemType === null }]">全部</div>
              <div @click="handleFilter('problem_type', '文书开具')" :class="['dropdown-item', { active: filterProblemType === '文书开具' }]">文书开具</div>
              <div @click="handleFilter('problem_type', '笔录上传')" :class="['dropdown-item', { active: filterProblemType === '笔录上传' }]">笔录上传</div>
              <div @click="handleFilter('problem_type', '办案期限')" :class="['dropdown-item', { active: filterProblemType === '办案期限' }]">办案期限</div>
              <div @click="handleFilter('problem_type', '音视频上传')" :class="['dropdown-item', { active: filterProblemType === '音视频上传' }]">音视频上传</div>
              <div @click="handleFilter('problem_type', '调查取证')" :class="['dropdown-item', { active: filterProblemType === '调查取证' }]">调查取证</div>
              <div @click="handleFilter('problem_type', '涉案财物')" :class="['dropdown-item', { active: filterProblemType === '涉案财物' }]">涉案财物</div>
              <div @click="handleFilter('problem_type', '办案程序')" :class="['dropdown-item', { active: filterProblemType === '办案程序' }]">办案程序</div>
              <div @click="handleFilter('problem_type', '其它')" :class="['dropdown-item', { active: filterProblemType === '其它' }]">其它</div>
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
        </div>

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

.table-toolbar {
  flex-shrink: 0;
  padding-bottom: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.table-wrapper {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.rules-display {
  flex-shrink: 0;
  margin-top: 12px;
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
  color: var(--c-text-secondary);
  font-size: 22px;
  overflow: hidden;
  text-overflow: ellipsis;
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
  transition: all 0.3s;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 6px;
}

.dropdown-btn:hover {
  color: var(--c-primary);
  border-color: var(--c-primary);
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
  color: var(--c-primary);
  background: rgba(var(--c-primary-rgb), 0.15);
  font-weight: bold;
}
</style>
