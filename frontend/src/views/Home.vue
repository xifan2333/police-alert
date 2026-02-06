<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Toast from '@/components/Toast.vue'
import ArcNavButton from '@/components/ArcNavButton.vue'

const router = useRouter()

// 应用配置
const appConfig = {
  title: '沈西所警务智管助手',
  navItems: [
    {
      text: "警力动态监测",
      iconType: "police-car",
      to: "/police-location"
    },
    {
      text: "警情态势追踪",
      iconType: "dashboard",
      to: "/situation"
    },
    {
      text: "执法问题盯办",
      iconType: "file-list",
      to: "/cases"
    },
    {
      text: "矛盾纠纷管理",
      iconType: "balance",
      to: "/disputes"
    }
  ]
}

const appTitle = ref(appConfig.title)
const navItems = ref(appConfig.navItems)

// Toast 相关
const toastRef = ref(null)
const toastMessage = ref('')
const toastType = ref('info')

const showToast = (message, type = 'info') => {
  toastMessage.value = message
  toastType.value = type
  toastRef.value?.show()
}

// 右下角点击计数器（隐藏后台入口）
const cornerClickCount = ref(0)
let cornerClickTimer = null

const handleCornerClick = () => {
  cornerClickCount.value++
  if (cornerClickTimer) clearTimeout(cornerClickTimer)

  showToast(`再点击 ${5 - cornerClickCount.value} 次进入管理页面`, 'info')

  if (cornerClickCount.value >= 5) {
    cornerClickCount.value = 0
    showToast('正在进入管理页面...', 'success')
    setTimeout(() => router.push('/admin'), 500)
    return
  }

  cornerClickTimer = setTimeout(() => {
    cornerClickCount.value = 0
  }, 3000)
}
</script>

<template>
  <div class="home-container">
    <!-- 标题区域 -->
    <header class="title-section">
      <h1 class="main-title">
        {{ appTitle }}
      </h1>
    </header>

    <!-- 警徽 -->
    <img src="/logo-gold.png" alt="警徽" class="police-badge" />

    <!-- 右下角导航按钮 -->
    <ArcNavButton :nav-items="navItems" />

    <!-- Toast 提示 -->
    <Toast
      ref="toastRef"
      :message="toastMessage"
      :type="toastType"
    />

    <!-- 右下角隐藏点击区域 -->
    <div
      class="corner-click-area"
      @click="handleCornerClick"
    ></div>
  </div>
</template>

<style scoped>
/* 根容器 */
.home-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: var(--bg-main) center/cover no-repeat;
}

/* 警徽 - 上方 */
.police-badge {
  position: absolute;
  top: 8%;
  left: 50%;
  transform: translateX(-50%);
  width: 280px;
  height: auto;
  z-index: 10;
  filter: drop-shadow(0 0 20px rgba(var(--c-primary-rgb), 0.5));
}

/* 标题区域 - 下方 */
.title-section {
  position: absolute;
  top: 42%;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  text-align: center;
  pointer-events: none;
}

.main-title {
  font-size: 3.5rem;
  font-weight: 900;
  letter-spacing: 0.3em;
  color: var(--c-text-primary);
  white-space: nowrap;
  font-family: var(--font-sans);
  -webkit-text-stroke: 1px rgba(var(--c-text-primary-rgb), 0.3);
  text-shadow:
    0 0 10px var(--c-primary),
    0 0 20px var(--c-primary),
    0 0 30px var(--c-primary),
    0 0 40px rgba(var(--c-primary-rgb), 0.5),
    0 0 70px rgba(var(--c-primary-rgb), 0.4),
    0 0 80px rgba(var(--c-primary-rgb), 0.25),
    0 2px 8px rgba(0, 0, 0, 0.5);
}

/* 右下角隐藏点击区域 */
.corner-click-area {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 128px;
  height: 128px;
  cursor: pointer;
  z-index: 90;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .main-title {
    font-size: 2.5rem;
  }
}

@media (max-width: 768px) {
  .main-title {
    font-size: 2rem;
  }
}
</style>
