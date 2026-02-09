<script setup>
import { ref, onMounted } from 'vue'
import request from '@/api/request'

const props = defineProps({
  // 页面代码，用于获取对应页面的显示规则
  pageCode: {
    type: String,
    required: true
  }
})

const displayRules = ref('')
const loading = ref(true)

// 从后端获取显示规则
const fetchDisplayRules = async () => {
  try {
    loading.value = true
    const response = await request.get('/api/data/display-rules', {
      params: {
        page_code: props.pageCode
      }
    })
    displayRules.value = response.data?.display_rules || '暂无显示规则'
  } catch (error) {
    console.error('获取显示规则失败:', error)
    displayRules.value = '暂无显示规则'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchDisplayRules()
})
</script>

<template>
  <div class="display-rules">
    <dv-border-box-13>
      <div class="rules-container">
        <!-- 标题 -->
        <div class="rules-header">
          <dv-decoration-5 class="header-decoration" />
          <h3 class="rules-title">显示规则</h3>
          <dv-decoration-5 class="header-decoration" :reverse="true" />
        </div>

        <!-- 规则内容 -->
        <div class="rules-content">
          <div v-if="loading" class="loading-text">加载中...</div>
          <div v-else class="rules-text">{{ displayRules }}</div>
        </div>
      </div>
    </dv-border-box-13>
  </div>
</template>

<style scoped>
.display-rules {
  width: 100%;
  padding: 16px;
}

.rules-container {
  padding: 16px 24px;
  min-height: 80px;
}

/* 标题区域 */
.rules-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 16px;
}

.header-decoration {
  width: 100px;
  height: 20px;
}

.rules-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--c-primary-light);
  letter-spacing: 2px;
  text-shadow: 0 0 8px rgba(var(--c-primary-rgb), 0.6);
}

/* 规则内容 */
.rules-content {
  text-align: center;
}

.loading-text {
  font-size: 14px;
  color: var(--c-text-secondary);
}

.rules-text {
  font-size: 18px;
  line-height: 1.8;
  color: var(--c-text-primary);
  white-space: pre-wrap;
}

/* 响应式 */
@media (max-width: 768px) {
  .rules-text {
    font-size: 13px;
  }
}
</style>
