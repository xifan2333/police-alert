<script setup>
import { ref } from 'vue'
import PageHeader from '@/components/PageHeader.vue'
import FloatingButton from '@/components/FloatingButton.vue'

const activeTab = ref('data-import')
const uploadFile = ref(null)
const uploading = ref(false)
const uploadResult = ref(null)

// 下载模板
const downloadTemplate = async () => {
  try {
    const response = await fetch('/api/v1/admin/template')
    if (!response.ok) throw new Error('下载失败')

    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = '数据导入模板.xlsx'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('下载模板失败:', error)
    alert('下载模板失败，请稍后重试')
  }
}

// 文件选择
const handleFileChange = (event) => {
  uploadFile.value = event.target.files[0]
  uploadResult.value = null
}

// 上传文件
const uploadExcel = async () => {
  if (!uploadFile.value) {
    alert('请先选择文件')
    return
  }

  uploading.value = true
  uploadResult.value = null

  try {
    const formData = new FormData()
    formData.append('file', uploadFile.value)

    const response = await fetch('/api/v1/admin/import', {
      method: 'POST',
      body: formData
    })

    const result = await response.json()

    if (result.code === 200) {
      let message = '导入成功！\n'
      message += `执法问题盯办: ${result.data.执法问题盯办} 条\n`
      message += `矛盾纠纷管理: ${result.data.矛盾纠纷管理} 条\n`
      message += `警情态势追踪: ${result.data.警情态势追踪} 条\n`
      message += `重复报警记录: ${result.data.重复报警记录} 条\n`
      message += `总计: ${result.data.总计} 条`

      uploadResult.value = {
        success: true,
        message: message
      }
      uploadFile.value = null
      // 清空文件选择
      const fileInput = document.querySelector('input[type="file"]')
      if (fileInput) fileInput.value = ''
    } else {
      throw new Error(result.message || '导入失败')
    }
  } catch (error) {
    console.error('上传失败:', error)
    uploadResult.value = {
      success: false,
      message: error.message || '上传失败，请检查文件格式'
    }
  } finally {
    uploading.value = false
  }
}

// 规则管理相关
const rules = ref([])
const loadingRules = ref(false)
const editingRule = ref(null)
const showRuleDialog = ref(false)

// 规则表单
const ruleForm = ref({
  page_code: '',
  table_code: '',
  rule_name: '',
  description: '',
  priority: 1,
  is_enabled: 1,
  field: '',
  conditions: []
})

// 页面选项
const pageOptions = [
  { value: 'risk_supervision', label: '执法问题盯办' },
  { value: 'dispute_management', label: '矛盾纠纷管理' },
  { value: 'situation', label: '警情态势追踪' }
]

// 表格选项（仅 situation 页面需要）
const tableOptions = {
  situation: [
    { value: 'policeClassification', label: '警情分类总览' },
    { value: 'theftTraditional', label: '偷盗地点分布' },
    { value: 'telecomFraud', label: '诈骗小区分布' },
    { value: 'viceCases', label: '涉黄小区分布' },
    { value: 'disputeCases', label: '纠纷社区分布' },
    { value: 'fightCases', label: '人身伤害区域分布' },
    { value: 'gamblingCases', label: '涉赌地点分布' },
    { value: 'repeatAlarms', label: '重复报警记录' }
  ]
}

// 字段选项（根据页面动态变化）
const fieldOptions = {
  risk_supervision: [
    { value: 'days_remaining', label: '剩余天数' },
    { value: 'case_type', label: '案件类型' }
  ],
  dispute_management: [
    { value: 'risk_level', label: '风险等级' },
    { value: 'status', label: '处置进度' }
  ],
  situation: [
    { value: '名称', label: '名称' },
    { value: '数量', label: '数量' },
    { value: '同比', label: '同比' },
    { value: '环比', label: '环比' },
    { value: '地点', label: '地点' },
    { value: '小区', label: '小区' },
    { value: '社区', label: '社区' },
    { value: '区域', label: '区域' },
    { value: '报警次数', label: '报警次数' }
  ]
}

// 操作符选项
const operatorOptions = [
  { value: 'eq', label: '等于 (==)' },
  { value: '<=', label: '小于等于 (<=)' },
  { value: '>=', label: '大于等于 (>=)' },
  { value: 'in', label: '包含于 (in)' }
]

// 加载规则列表
const loadRules = async () => {
  loadingRules.value = true
  try {
    const response = await fetch('/api/v1/admin/rules')
    const result = await response.json()
    if (result.code === 200) {
      rules.value = result.data || []
    }
  } catch (error) {
    console.error('加载规则失败:', error)
  } finally {
    loadingRules.value = false
  }
}

// 新建规则
const createRule = () => {
  editingRule.value = null
  ruleForm.value = {
    page_code: 'risk_supervision',
    table_code: '',
    rule_name: '',
    description: '',
    priority: 1,
    is_enabled: 1,
    field: '',
    conditions: []
  }
  showRuleDialog.value = true
}

// 编辑规则
const editRule = (rule) => {
  editingRule.value = rule
  const config = rule.rule_config
  ruleForm.value = {
    page_code: rule.page_code,
    table_code: rule.table_code || '',
    rule_name: rule.rule_name,
    description: rule.description,
    priority: rule.priority,
    is_enabled: rule.is_enabled,
    field: config.field || '',
    conditions: config.conditions || []
  }
  showRuleDialog.value = true
}

// 添加条件
const addCondition = () => {
  ruleForm.value.conditions.push({
    operator: 'eq',
    value: '',
    font_color: '#f5222d'
  })
}

// 删除条件
const removeCondition = (index) => {
  ruleForm.value.conditions.splice(index, 1)
}

// 保存规则
const saveRule = async () => {
  // 验证
  if (!ruleForm.value.rule_name) {
    alert('请输入规则名称')
    return
  }
  if (!ruleForm.value.field) {
    alert('请选择字段')
    return
  }
  if (ruleForm.value.conditions.length === 0) {
    alert('请至少添加一个条件')
    return
  }

  try {
    const ruleConfig = {
      field: ruleForm.value.field,
      conditions: ruleForm.value.conditions
    }

    const payload = {
      page_code: ruleForm.value.page_code,
      table_code: ruleForm.value.table_code || null,
      rule_type: 'color',
      rule_name: ruleForm.value.rule_name,
      description: ruleForm.value.description,
      priority: ruleForm.value.priority,
      is_enabled: ruleForm.value.is_enabled,
      rule_config: ruleConfig
    }

    let response
    if (editingRule.value) {
      // 更新
      response = await fetch(`/api/v1/admin/rules/${editingRule.value.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
    } else {
      // 新建
      response = await fetch('/api/v1/admin/rules', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
    }

    const result = await response.json()
    if (result.code === 200) {
      alert('保存成功')
      showRuleDialog.value = false
      loadRules()
    } else {
      alert(result.message || '保存失败')
    }
  } catch (error) {
    console.error('保存失败:', error)
    alert('保存失败')
  }
}

// 取消编辑
const cancelEdit = () => {
  showRuleDialog.value = false
  editingRule.value = null
}

// 删除规则
const deleteRule = async (ruleId) => {
  if (!confirm('确定要删除这条规则吗？')) return

  try {
    const response = await fetch(`/api/v1/admin/rules/${ruleId}`, {
      method: 'DELETE'
    })
    const result = await response.json()
    if (result.code === 200) {
      alert('删除成功')
      loadRules()
    }
  } catch (error) {
    console.error('删除失败:', error)
    alert('删除失败')
  }
}

// 切换规则启用状态
const toggleRule = async (rule) => {
  try {
    const response = await fetch(`/api/v1/admin/rules/${rule.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...rule,
        is_enabled: rule.is_enabled === 1 ? 0 : 1
      })
    })
    const result = await response.json()
    if (result.code === 200) {
      loadRules()
    }
  } catch (error) {
    console.error('更新失败:', error)
  }
}

// 监听标签切换
const handleTabChange = (tab) => {
  activeTab.value = tab
  if (tab === 'rule-management') {
    loadRules()
  }
}
</script>

<template>
  <div class="admin-page">
    <PageHeader title="后台管理" />

    <div class="content-wrapper">
      <div class="admin-container">
        <!-- 标签页 -->
        <div class="tabs">
          <button
            :class="['tab-btn', activeTab === 'data-import' ? 'active' : '']"
            @click="handleTabChange('data-import')"
          >
            数据导入
          </button>
          <button
            :class="['tab-btn', activeTab === 'rule-management' ? 'active' : '']"
            @click="handleTabChange('rule-management')"
          >
            规则管理
          </button>
        </div>

        <!-- 数据导入面板 -->
        <div v-if="activeTab === 'data-import'" class="panel">
          <div class="panel-section">
            <h3 class="section-title">下载模板</h3>
            <p class="section-desc">下载多sheet Excel 模板，包含所有数据类型（执法问题盯办、矛盾纠纷管理、警情态势追踪、重复报警记录）</p>
            <button @click="downloadTemplate" class="btn btn-secondary">
              下载模板
            </button>
          </div>

          <div class="panel-section">
            <h3 class="section-title">上传数据</h3>
            <p class="section-desc">选择填写好的 Excel 文件进行导入，系统会自动识别并导入所有sheet的数据</p>
            <div class="upload-area">
              <input
                type="file"
                accept=".xlsx,.xls"
                @change="handleFileChange"
                class="file-input"
              />
              <div v-if="uploadFile" class="file-info">
                已选择: {{ uploadFile.name }}
              </div>
            </div>
            <button
              @click="uploadExcel"
              :disabled="!uploadFile || uploading"
              class="btn btn-primary"
            >
              {{ uploading ? '上传中...' : '上传并导入' }}
            </button>

            <!-- 上传结果 -->
            <div v-if="uploadResult" :class="['result-message', uploadResult.success ? 'success' : 'error']">
              <pre style="white-space: pre-wrap; margin: 0;">{{ uploadResult.message }}</pre>
            </div>
          </div>
        </div>

        <!-- 规则管理面板 -->
        <div v-if="activeTab === 'rule-management'" class="panel">
          <div class="panel-section">
            <div class="section-header">
              <h3 class="section-title">显示规则列表</h3>
              <button @click="createRule" class="btn btn-primary">新建规则</button>
            </div>

            <div v-if="loadingRules" class="text-center py-8">
              加载中...
            </div>

            <div v-else-if="rules.length === 0" class="text-center py-8 text-gray-400">
              暂无规则
            </div>

            <div v-else class="rules-list">
              <div v-for="rule in rules" :key="rule.id" class="rule-item">
                <div class="rule-info">
                  <div class="rule-name">{{ rule.rule_name }}</div>
                  <div class="rule-meta">
                    <span class="rule-page">{{ rule.page_code }}</span>
                    <span v-if="rule.table_code" class="rule-table">{{ rule.table_code }}</span>
                    <span class="rule-type">{{ rule.rule_type }}</span>
                    <span class="rule-priority">优先级: {{ rule.priority }}</span>
                  </div>
                  <div class="rule-desc">{{ rule.description }}</div>
                  <div class="rule-config">
                    字段: {{ rule.rule_config.field }} |
                    条件数: {{ rule.rule_config.conditions?.length || 0 }}
                  </div>
                </div>
                <div class="rule-actions">
                  <button
                    @click="toggleRule(rule)"
                    :class="['btn-toggle', rule.is_enabled === 1 ? 'enabled' : 'disabled']"
                  >
                    {{ rule.is_enabled === 1 ? '已启用' : '已禁用' }}
                  </button>
                  <button @click="editRule(rule)" class="btn-action">编辑</button>
                  <button @click="deleteRule(rule.id)" class="btn-action btn-danger">删除</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 编辑规则对话框 -->
      <div v-if="showRuleDialog" class="dialog-overlay" @click="cancelEdit">
        <div class="dialog dialog-large" @click.stop>
          <div class="dialog-header">
            <h3>{{ editingRule ? '编辑规则' : '新建规则' }}</h3>
            <button @click="cancelEdit" class="close-btn">&times;</button>
          </div>
          <div class="dialog-body">
            <div class="form-group">
              <label>应用页面 *</label>
              <select v-model="ruleForm.page_code" class="form-input">
                <option v-for="page in pageOptions" :key="page.value" :value="page.value">
                  {{ page.label }}
                </option>
              </select>
            </div>

            <div v-if="ruleForm.page_code === 'situation'" class="form-group">
              <label>应用表格（仅警情态势）</label>
              <select v-model="ruleForm.table_code" class="form-input">
                <option value="">全部表格</option>
                <option v-for="table in tableOptions.situation" :key="table.value" :value="table.value">
                  {{ table.label }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>规则名称 *</label>
              <input v-model="ruleForm.rule_name" type="text" class="form-input" placeholder="例如：风险等级颜色规则" />
            </div>

            <div class="form-group">
              <label>规则描述</label>
              <textarea v-model="ruleForm.description" class="form-textarea" rows="2" placeholder="描述规则的作用"></textarea>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>优先级</label>
                <input v-model.number="ruleForm.priority" type="number" class="form-input" min="1" />
              </div>

              <div class="form-group">
                <label>状态</label>
                <select v-model.number="ruleForm.is_enabled" class="form-input">
                  <option :value="1">启用</option>
                  <option :value="0">禁用</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label>判断字段 *</label>
              <select v-model="ruleForm.field" class="form-input">
                <option value="">请选择字段</option>
                <option
                  v-for="field in fieldOptions[ruleForm.page_code]"
                  :key="field.value"
                  :value="field.value"
                >
                  {{ field.label }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <div class="conditions-header">
                <label>条件配置 *</label>
                <button @click="addCondition" class="btn-small btn-primary">添加条件</button>
              </div>

              <div v-if="ruleForm.conditions.length === 0" class="empty-conditions">
                暂无条件，请点击"添加条件"按钮
              </div>

              <div v-else class="conditions-list">
                <div v-for="(condition, index) in ruleForm.conditions" :key="index" class="condition-item">
                  <div class="condition-row">
                    <div class="condition-field">
                      <label>操作符</label>
                      <select v-model="condition.operator" class="form-input-small">
                        <option v-for="op in operatorOptions" :key="op.value" :value="op.value">
                          {{ op.label }}
                        </option>
                      </select>
                    </div>

                    <div class="condition-field">
                      <label>值</label>
                      <input v-model="condition.value" type="text" class="form-input-small" placeholder="例如：高" />
                    </div>

                    <div class="condition-field">
                      <label>文字颜色</label>
                      <input v-model="condition.font_color" type="color" class="form-input-color" />
                      <span class="color-preview" :style="{ color: condition.font_color }">预览</span>
                    </div>

                    <div class="condition-actions">
                      <button @click="removeCondition(index)" class="btn-icon btn-danger">
                        删除
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="dialog-footer">
            <button @click="cancelEdit" class="btn btn-secondary">取消</button>
            <button @click="saveRule" class="btn btn-primary">保存</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 悬浮返回按钮 -->
    <FloatingButton />
  </div>
</template>

<style scoped>
.admin-page {
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
  padding: 1rem;
  overflow: auto;
}

.admin-container {
  max-width: 1200px;
  margin: 0 auto;
  background: var(--c-bg-dialog);
  border: 1px solid var(--c-border);
  border-radius: 8px;
  overflow: hidden;
}

/* 标签页 */
.tabs {
  display: flex;
  border-bottom: 1px solid var(--c-border);
}

.tab-btn {
  flex: 1;
  padding: 1rem;
  background: transparent;
  border: none;
  color: var(--c-text-primary);
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  border-bottom: 2px solid transparent;
}

.tab-btn:hover {
  background: rgba(var(--c-primary-rgb), 0.1);
}

.tab-btn.active {
  background: rgba(var(--c-primary-rgb), 0.2);
  border-bottom-color: var(--c-primary);
  font-weight: 600;
}

/* 面板 */
.panel {
  padding: 2rem;
}

.panel-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(var(--c-primary-rgb), 0.2);
}

.panel-section:last-child {
  border-bottom: none;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--c-text-primary);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header .section-title {
  margin-bottom: 0;
}

.section-desc {
  color: var(--c-text-secondary);
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

/* 表单元素 */
.select-input {
  width: 100%;
  max-width: 400px;
  padding: 0.75rem;
  background: rgba(var(--c-primary-rgb), 0.15);
  border: 1px solid var(--c-border);
  border-radius: 4px;
  color: var(--c-text-primary);
  font-size: 1rem;
}

.file-input {
  display: block;
  margin-bottom: 1rem;
  color: var(--c-text-primary);
}

.file-info {
  margin-bottom: 1rem;
  padding: 0.5rem;
  background: rgba(var(--c-primary-rgb), 0.15);
  border-radius: 4px;
  font-size: 0.875rem;
}

/* 按钮 */
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  margin-right: 0.5rem;
}

.btn-primary {
  background: var(--c-primary);
  color: #fff;
}

.btn-primary:hover:not(:disabled) {
  background: var(--c-primary-dark);
}

.btn-primary:disabled {
  background: var(--c-gray-500);
  cursor: not-allowed;
}

.btn-secondary {
  background: rgba(var(--c-primary-rgb), 0.3);
  color: var(--c-text-primary);
  border: 1px solid rgba(var(--c-primary-rgb), 0.5);
}

.btn-secondary:hover {
  background: rgba(var(--c-primary-rgb), 0.5);
}

/* 结果消息 */
.result-message {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

.result-message.success {
  background: rgba(var(--c-success-rgb), 0.2);
  border: 1px solid rgba(var(--c-success-rgb), 0.5);
  color: var(--c-success-light);
}

.result-message.error {
  background: rgba(var(--c-danger-rgb), 0.2);
  border: 1px solid rgba(var(--c-danger-rgb), 0.5);
  color: var(--c-danger-light);
}

/* 规则列表 */
.rules-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.rule-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(var(--c-primary-rgb), 0.15);
  border: 1px solid var(--c-border);
  border-radius: 4px;
}

.rule-info {
  flex: 1;
}

.rule-name {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.rule-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: var(--c-text-secondary);
}

.rule-page,
.rule-table,
.rule-type,
.rule-priority {
  padding: 0.25rem 0.5rem;
  background: rgba(var(--c-primary-rgb), 0.2);
  border-radius: 4px;
}

.rule-desc {
  font-size: 0.875rem;
  color: var(--c-text-secondary);
}

.rule-config {
  font-size: 0.875rem;
  color: var(--c-accent);
  margin-top: 0.5rem;
}

.rule-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-toggle {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-toggle.enabled {
  background: rgba(var(--c-success-rgb), 0.3);
  color: var(--c-success-light);
}

.btn-toggle.disabled {
  background: rgba(107, 114, 128, 0.3);
  color: var(--c-gray-400);
}

.btn-action {
  padding: 0.5rem 1rem;
  background: rgba(var(--c-primary-rgb), 0.3);
  border: 1px solid rgba(var(--c-primary-rgb), 0.5);
  border-radius: 4px;
  color: var(--c-text-primary);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-action:hover {
  background: rgba(var(--c-primary-rgb), 0.5);
}

.btn-action.btn-danger {
  background: rgba(var(--c-danger-rgb), 0.3);
  border-color: rgba(var(--c-danger-rgb), 0.5);
  color: var(--c-danger-light);
}

.btn-action.btn-danger:hover {
  background: rgba(var(--c-danger-rgb), 0.5);
}

/* 对话框 */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog {
  background: var(--c-bg-glass-dark);
  border: 1px solid rgba(var(--c-primary-rgb), 0.5);
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow: auto;
}

.dialog-large {
  max-width: 800px;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--c-border);
}

.dialog-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--c-text-primary);
}

.close-btn {
  background: none;
  border: none;
  color: var(--c-text-primary);
  font-size: 2rem;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: var(--c-text-primary);
}

.dialog-body {
  padding: 1.5rem;
}

.dialog-footer {
  padding: 1.5rem;
  border-top: 1px solid var(--c-border);
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

/* 表单 */
.form-group {
  margin-bottom: 1.5rem;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--c-text-primary);
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem;
  background: rgba(var(--c-primary-rgb), 0.15);
  border: 1px solid var(--c-border);
  border-radius: 4px;
  color: var(--c-text-primary);
  font-size: 1rem;
  font-family: inherit;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--c-border-strong);
}

.form-textarea {
  resize: vertical;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-input-small {
  width: 100%;
  padding: 0.5rem;
  background: rgba(var(--c-primary-rgb), 0.15);
  border: 1px solid var(--c-border);
  border-radius: 4px;
  color: var(--c-text-primary);
  font-size: 0.875rem;
}

.form-input-color {
  width: 60px;
  height: 36px;
  padding: 0.25rem;
  background: rgba(var(--c-primary-rgb), 0.15);
  border: 1px solid var(--c-border);
  border-radius: 4px;
  cursor: pointer;
}

.btn-small {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-icon {
  padding: 0.5rem;
  border: none;
  border-radius: 4px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.3s;
}

/* 条件配置 */
.conditions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.conditions-header label {
  margin-bottom: 0;
}

.empty-conditions {
  padding: 2rem;
  text-align: center;
  color: var(--c-text-secondary);
  background: rgba(var(--c-primary-rgb), 0.1);
  border: 1px dashed var(--c-border);
  border-radius: 4px;
}

.conditions-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.condition-item {
  padding: 1rem;
  background: rgba(var(--c-primary-rgb), 0.1);
  border: 1px solid var(--c-border);
  border-radius: 4px;
}

.condition-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1.5fr auto;
  gap: 1rem;
  align-items: end;
}

.condition-field label {
  display: block;
  margin-bottom: 0.25rem;
  font-size: 0.875rem;
  color: var(--c-text-secondary);
}

.condition-actions {
  display: flex;
  align-items: flex-end;
}

.color-preview {
  margin-left: 0.5rem;
  font-weight: 600;
}
</style>
