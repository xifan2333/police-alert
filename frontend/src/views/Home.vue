<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Toast from '@/components/Toast.vue'

const router = useRouter()

// 应用配置
const appConfig = {
  title: '沈西所警务智管助手',
  primaryColor: '#2c2772',
  backgroundImage: '/main-bg-003.jpg',
  navItems: [
    {
      text: "警力动态监测",
      icon: "i-ri-map-pin-user-line",
      to: "/police-location"
    },
    {
      text: "警情态势追踪",
      icon: "i-ri-dashboard-line",
      to: "/situation"
    },
    {
      text: "执法问题盯办",
      icon: "i-ri-file-list-3-line",
      to: "/cases"
    },
    {
      text: "矛盾纠纷管理",
      icon: "i-ri-user-voice-line",
      to: "/disputes"
    }
  ]
}

const appTitle = ref(appConfig.title)
const navItems = ref(appConfig.navItems)

// 导航按钮展开状态
const isNavExpanded = ref(false)

const handleNavClick = () => {
  isNavExpanded.value = !isNavExpanded.value
}

// 计算圆弧上的位置
const getArcPosition = (index, total) => {
  const radius = 300 // 圆弧半径
  const startAngle = 180 // 起始角度（从左边开始）
  const endAngle = 270 // 结束角度（到上边）
  const angleStep = (endAngle - startAngle) / (total - 1)
  const angle = startAngle + angleStep * index
  const radian = (angle * Math.PI) / 180

  return {
    x: Math.cos(radian) * radius,
    y: Math.sin(radian) * radius
  }
}

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
  <div
    class="home-container"
    :style="{ backgroundImage: `url(${appConfig.backgroundImage})` }"
  >
    <!-- 中心标题区域 -->
    <header class="title-section">
      <h1
        class="main-title"
        :style="{
          fontFamily: '-apple-system, BlinkMacSystemFont, \'PingFang SC\', \'Microsoft YaHei\', \'SimHei\', \'黑体\', sans-serif',
          fontWeight: '900',
          WebkitTextStroke: '1px rgba(255, 255, 255, 0.3)',
          textShadow: `
            0 0 10px ${appConfig.primaryColor},
            0 0 20px ${appConfig.primaryColor},
            0 0 30px ${appConfig.primaryColor},
            0 0 40px ${appConfig.primaryColor}80,
            0 0 70px ${appConfig.primaryColor}60,
            0 0 80px ${appConfig.primaryColor}40,
            0 2px 8px rgba(0,0,0,0.5)
          `
        }"
      >
        {{ appTitle }}
      </h1>
    </header>

    <!-- 右下角导航按钮 -->
    <nav
      class="nav-container-corner"
      :class="{ 'is-expanded': isNavExpanded }"
    >
      <div
        class="nav-center-btn"
        @click="handleNavClick"
      >
        <!-- 科技感背景层 -->
        <div class="tech-bg-layer"></div>
        <div class="tech-pulse-layer"></div>
        <div class="tech-scan-layer"></div>

        <!-- 图标 -->
        <div class="i-ri-apps-2-line nav-icon"></div>
      </div>

      <div class="nav-items">
        <a
          v-for="(item, index) in navItems"
          :key="index"
          class="nav-item"
          :style="{
            '--delay': `${(index + 1) * 50}ms`,
            '--arc-x': `${getArcPosition(index, navItems.length).x}px`,
            '--arc-y': `${getArcPosition(index, navItems.length).y}px`
          }"
          @click="router.push(item.to)"
        >
          <div class="nav-item-circle">
            <div :class="item.icon" class="nav-item-icon"></div>
          </div>
          <span class="nav-item-label">{{ item.text }}</span>
        </a>
      </div>
    </nav>

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
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* 中心标题区域 */
.title-section {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
  text-align: center;
  pointer-events: none;
}

.main-title {
  font-size: 3.5rem;
  font-weight: 900;
  letter-spacing: 0.3em;
  color: white;
  white-space: nowrap;
}

/* 导航容器 - 右下角 */
.nav-container-corner {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 5rem;
  height: 5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: auto;
  z-index: 100;
}

/* 中心按钮 */
.nav-center-btn {
  position: relative;
  width: 5rem;
  height: 5rem;
  background: linear-gradient(135deg, #2c2772 0%, #3b3799 50%, #4a46b8 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    0 0 20px rgba(44, 39, 114, 0.6),
    0 0 40px rgba(44, 39, 114, 0.4),
    0 8px 32px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  cursor: pointer;
  z-index: 50;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.27, 1.55);
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.15);
}

.nav-center-btn:hover {
  transform: scale(1.1);
  box-shadow:
    0 0 30px rgba(44, 39, 114, 0.8),
    0 0 60px rgba(44, 39, 114, 0.6),
    0 12px 48px rgba(0, 0, 0, 0.4);
  border-color: rgba(255, 255, 255, 0.25);
}

/* 科技感背景层 */
.tech-bg-layer {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.3) 0%, transparent 60%);
  opacity: 0.5;
}

/* 脉冲层 */
.tech-pulse-layer {
  position: absolute;
  inset: -10px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(44, 39, 114, 0.4) 0%, transparent 70%);
  opacity: 0.6;
}

/* 扫描线层 */
.tech-scan-layer {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: linear-gradient(
    180deg,
    transparent 0%,
    rgba(255, 255, 255, 0.1) 50%,
    transparent 100%
  );
}

.nav-icon {
  width: 2rem;
  height: 2rem;
  transition: transform 0.5s ease-in-out;
  position: relative;
  z-index: 10;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

.nav-container-corner.is-expanded .nav-icon {
  transform: rotate(180deg);
}

.nav-center-btn:hover .nav-icon {
  transform: scale(1.1);
}

/* 导航项容器 */
.nav-items {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

/* 导航项 */
.nav-item {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0;
  transition: opacity 0.5s cubic-bezier(0.68, -0.55, 0.27, 1.55), transform 0.5s cubic-bezier(0.68, -0.55, 0.27, 1.55);
  transition-delay: var(--delay);
  cursor: pointer;
  pointer-events: none;
  z-index: 10;
}

.nav-item:hover {
  z-index: 9998;
}

.nav-container-corner.is-expanded .nav-item {
  opacity: 1;
  pointer-events: auto;
  transform: translate(calc(-50% + var(--arc-x)), calc(-50% + var(--arc-y)));
}

/* 导航项圆圈 */
.nav-item-circle {
  width: 3.5rem;
  height: 3.5rem;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.85) 100%);
  backdrop-filter: blur(10px);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    0 4px 16px rgba(0, 0, 0, 0.1),
    0 0 20px rgba(44, 39, 114, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
  border: 2px solid rgba(44, 39, 114, 0.2);
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.nav-item-circle::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.6) 0%, transparent 60%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.nav-item:hover .nav-item-circle {
  transform: scale(1.15);
  background: linear-gradient(135deg, rgba(255, 255, 255, 1) 0%, rgba(255, 255, 255, 0.95) 100%);
  box-shadow:
    0 8px 24px rgba(0, 0, 0, 0.15),
    0 0 30px rgba(44, 39, 114, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 1);
  border-color: rgba(44, 39, 114, 0.4);
}

.nav-item:hover .nav-item-circle::before {
  opacity: 1;
}

/* 导航项图标 */
.nav-item-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: #6b7280;
  transition: all 0.3s ease;
  position: relative;
  z-index: 10;
}

.nav-item:hover .nav-item-icon {
  color: #2c2772;
  transform: scale(1.1);
  filter: drop-shadow(0 2px 4px rgba(44, 39, 114, 0.3));
}

/* 导航项标签 - Tooltip 样式 */
.nav-item-label {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) translateY(-4.5rem);
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(12px);
  border-radius: 0.375rem;
  box-shadow:
    0 0 0 1px rgba(44, 39, 114, 0.5),
    0 0 20px rgba(44, 39, 114, 0.3),
    0 4px 12px rgba(0, 0, 0, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  opacity: 0;
  pointer-events: none;
  transition: all 0.3s ease;
  white-space: nowrap;
  letter-spacing: 0.05em;
  z-index: 9999;
}

/* Tooltip 箭头 - 底部 */
.nav-item-label::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 5px solid transparent;
  border-top-color: rgba(15, 23, 42, 0.95);
}

/* Tooltip 发光边框 */
.nav-item-label::before {
  content: '';
  position: absolute;
  inset: -1px;
  border-radius: 0.375rem;
  background: linear-gradient(135deg, rgba(44, 39, 114, 0.6), rgba(74, 70, 184, 0.6));
  z-index: -1;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.nav-item:hover .nav-item-label {
  opacity: 1;
  transform: translate(-50%, -50%) translateY(-5rem);
}

.nav-item:hover .nav-item-label::before {
  opacity: 1;
}

/* 右下角隐藏点击区域 */
.corner-click-area {
  position: fixed;
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
