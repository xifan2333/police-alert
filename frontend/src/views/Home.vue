<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Toast from '@/components/Toast.vue'

const router = useRouter()

// 应用配置（硬编码）
const appConfig = {
  title: '沈西所警务智管助手',
  primaryColor: '#2c2772',
  backgroundImage: '/main-bg-003.jpg',
  navItems: [
    {
      "text": "警力动态监测",
      "icon": "i-ri-map-pin-user-line",
      "iconEnabled": false,
      "to": "/police-location",
      "external": false
    },
    {
      "text": "警情态势追踪",
      "icon": "i-ri-dashboard-line",
      "iconEnabled": false,
      "to": "/situation",
      "external": false
    },
    {
      "text": "执法问题盯办",
      "icon": "i-ri-file-list-3-line",
      "iconEnabled": false,
      "to": "/cases",
      "external": false
    },
    {
      "text": "矛盾纠纷管理",
      "icon": "i-ri-user-voice-line",
      "iconEnabled": false,
      "to": "/disputes",
      "external": false
    }
  ]
}

// 响应式引用（保持数据驱动视图）
const appTitle = ref(appConfig.title)
const backgroundImage = ref(appConfig.backgroundImage)
const navItems = ref(appConfig.navItems)

// 浮动按钮展开状态
const isMenuExpanded = ref(false)

// 切换菜单展开/收起
const toggleMenu = () => {
  isMenuExpanded.value = !isMenuExpanded.value
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

  // 清除之前的定时器
  if (cornerClickTimer) {
    clearTimeout(cornerClickTimer)
  }

  // 显示提示
  showToast(`再点击 ${5 - cornerClickCount.value} 次进入管理页面`, 'info')

  // 如果点击 5 次，进入后台
  if (cornerClickCount.value >= 5) {
    cornerClickCount.value = 0
    showToast('正在进入管理页面...', 'success')
    setTimeout(() => {
      router.push('/admin')
    }, 500)
    return
  }

  // 3 秒后重置计数器
  cornerClickTimer = setTimeout(() => {
    cornerClickCount.value = 0
  }, 3000)
}

</script>

<template>
  <!-- 根容器 -->
  <div
    class="h-full w-full of-hidden font-sans text-gray-200 relative
           bg-cover bg-center bg-no-repeat"
    :style="{ backgroundImage: `url(${backgroundImage})` }"
  >
    <!-- 模糊遮罩层 -->
    <div class="absolute inset-0 backdrop-blur-sm bg-black/20"></div>

    <!-- 主内容 - 绝对定位布局 -->
    <main class="relative h-full w-full z-10">

      <!-- 左上角警徽图标 -->
      <div class="absolute top-6 left-6 md:top-8 md:left-8">
        <img
          src="/logo-gold.png"
          alt="警徽"
          class="w-16 h-16 md:w-20 md:h-20 opacity-90 transition-transform hover:scale-110"
        />
      </div>

      <!-- 右下角隐藏点击区域 -->
      <div
        class="fixed bottom-0 right-0 w-32 h-32 cursor-pointer z-40"
        @click="handleCornerClick"
      ></div>

      <!-- 标题区域 - 页面中央 -->
      <header class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-5xl px-8">
        <div class="flex items-center justify-center px-8 py-6">
          <!-- 主标题 -->
          <h1
            class="text-3xl sm:text-5xl md:text-5xl lg:text-5xl font-bold
                   tracking-[0.3em] text-center text-white"
            :style="{
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
        </div>
      </header>

      <!-- 右下角浮动菜单 -->
      <div class="fixed right-8 bottom-8 z-50">
        <!-- 展开的菜单项容器 -->
        <div class="absolute bottom-20 right-0 flex flex-col items-end gap-4">
          <transition-group name="menu-item">
            <router-link
              v-for="(item, index) in navItems"
              v-show="isMenuExpanded"
              :key="index"
              :to="item.to"
              class="no-underline"
              :style="{
                transitionDelay: `${index * 50}ms`
              }"
            >
              <div
                class="w-64 transition-all duration-300 hover:-translate-y-1 hover:scale-105 relative"
                :style="{
                  backgroundColor: appConfig.primaryColor,
                  clipPath: 'polygon(0 0, 100% 0, 100% calc(100% - 12px), calc(100% - 12px) 100%, 0 100%)',
                  border: '1px solid rgba(59, 130, 246, 0.5)',
                  boxShadow: '0 0 15px rgba(59, 130, 246, 0.4)'
                }"
              >
                <div class="flex items-center justify-center gap-3 px-4 py-3">
                  <div v-if="item.iconEnabled && item.icon" :class="[item.icon, 'text-xl text-cyan-400 flex-shrink-0']" />
                  <span class="text-base tracking-wider text-white font-semibold" style="font-family: KaiTi, STKaiti, '楷体', serif;">{{ item.text }}</span>
                </div>
              </div>
            </router-link>
          </transition-group>
        </div>

        <!-- 主浮动按钮 -->
        <button
          @click="toggleMenu"
          class="w-16 h-16 rounded-full flex items-center justify-center transition-all duration-300 shadow-lg hover:scale-110"
          :style="{
            backgroundColor: appConfig.primaryColor,
            border: '2px solid rgba(59, 130, 246, 0.6)',
            boxShadow: '0 0 20px rgba(59, 130, 246, 0.5)'
          }"
        >
          <div class="text-3xl text-white transition-all duration-300">
            <div v-if="!isMenuExpanded" class="i-ri-police-badge-line" />
            <div v-else class="i-ri-close-line" />
          </div>
        </button>
      </div>

    </main>

    <!-- Toast 提示 -->
    <Toast
      ref="toastRef"
      :message="toastMessage"
      :type="toastType"
    />
  </div>
</template>

<style scoped>
/* 菜单项展开动画 */
.menu-item-enter-active,
.menu-item-leave-active {
  transition: all 0.3s ease;
}

.menu-item-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.8);
}

.menu-item-leave-to {
  opacity: 0;
  transform: translateY(30px) scale(0.8);
}

.menu-item-enter-to,
.menu-item-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}
</style>
