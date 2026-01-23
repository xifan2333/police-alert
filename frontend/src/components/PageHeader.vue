<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  title: {
    type: String,
    required: true
  }
})

const router = useRouter()

const goBack = () => {
  router.push('/')
}
</script>

<template>
  <header class="relative flex items-center px-4 py-2 bg-[#2c2772] shadow-lg">
    <!-- 左侧：警徽 -->
    <div class="flex items-center">
      <img src="/logo.svg" alt="警徽" class="w-8 h-8 md:w-10 md:h-10 opacity-90" />
    </div>

    <!-- 中间：标题（绝对居中） -->
    <h1 class="absolute left-1/2 -translate-x-1/2 text-lg md:text-xl font-bold text-white tracking-wider">
      {{ title }}
    </h1>

    <!-- 右侧：返回按钮 -->
    <button
      @click="goBack"
      class="ml-auto flex items-center gap-2 px-3 py-1.5 bg-white/10 hover:bg-white/20 rounded-lg transition-all duration-300 text-white font-semibold backdrop-blur-sm text-sm"
    >
      <i class="i-ri-arrow-left-line text-lg"></i>
      <span class="hidden md:inline">返回首页</span>
    </button>
  </header>
</template>
