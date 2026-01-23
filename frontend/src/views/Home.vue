<script setup>
import { ref } from 'vue'

// 应用配置（硬编码）
const appConfig = {
  title: '沈西所警务工作管家',
  primaryColor: '#2c2772',
  backgroundImage: '/main-bg-003.jpg',
  navItems: [
    {
      "text": "警力效能动态监测",
      "icon": "i-ri-map-pin-user-line",
      "iconEnabled": false,
      "to": "/police-location",
      "external": false
    },
    {
      "text": "警情态势监控追踪",
      "icon": "i-ri-dashboard-line",
      "iconEnabled": false,
      "to": "/situation",
      "external": false
    },
    {
      "text": "执法问题风险盯办",
      "icon": "i-ri-file-list-3-line",
      "iconEnabled": false,
      "to": "/cases",
      "external": false
    },
    {
      "text": "未矛盾纠纷闭环管理",
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
</script>

<template>
  <!-- 根容器 -->
  <div
    class="h-screen w-screen of-hidden font-sans text-gray-200 relative
           bg-cover bg-center bg-no-repeat"
    :style="{ backgroundImage: `url(${backgroundImage})` }"
  >
    <!-- 主内容 - 绝对定位布局 -->
    <main class="relative h-full w-full">

      <!-- 左上角警徽图标 -->
      <div class="absolute top-6 left-6 md:top-8 md:left-8">
        <img src="/logo.svg" alt="警徽" class="w-16 h-16 md:w-20 md:h-20 opacity-90" />
      </div>

      <!-- 标题区域 - 页面中央偏上 -->
      <header class="absolute top-[40%] left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-4xl px-8">
        <div class="flex items-center justify-center px-8 py-6">
          <!-- 主标题 -->
          <h1
            class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold
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

      <!-- 导航区域 - 底部往上 -->
      <nav class="absolute bottom-16 md:bottom-20 left-1/2 -translate-x-1/2 w-full max-w-7xl px-4">
        <div class="flex flex-wrap justify-center items-center gap-3 md:gap-4">
          <!-- 遍历所有导航按钮 -->
          <router-link
            v-for="(item, index) in navItems"
            :key="index"
            :to="item.to"
            class="no-underline"
          >
            <div
              class="w-56 md:w-64 lg:w-72 transition-all duration-300 hover:-translate-y-1.5 hover:scale-105 relative"
              :style="{
                backgroundColor: appConfig.primaryColor,
                clipPath: 'polygon(0 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%)',
                border: '1px solid rgba(59, 130, 246, 0.5)',
                boxShadow: '0 0 10px rgba(59, 130, 246, 0.3)'
              }"
            >
              <div class="flex items-center justify-center gap-3 px-3 py-3">
                <div v-if="item.iconEnabled && item.icon" :class="[item.icon, 'text-xl md:text-2xl text-cyan-400 flex-shrink-0']" />
                <span class="text-sm md:text-base lg:text-lg tracking-wider text-white font-semibold">{{ item.text }}</span>
              </div>
            </div>
          </router-link>
        </div>
      </nav>

    </main>
  </div>
</template>
