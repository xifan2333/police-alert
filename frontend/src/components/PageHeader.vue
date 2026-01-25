<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true
  }
})
</script>

<template>
  <header class="relative flex items-center px-4 py-2 bg-[#006ACE] shadow-lg">
    <!-- 左侧：警徽和派出所名称 -->
    <div class="flex items-center gap-3">
      <img src="/logo-blue.png" alt="警徽" class="w-10 h-10 md:w-12 md:h-12 opacity-90" />
      <div class="flex flex-col justify-center" style="width: 200px;">
        <div class="text-white text-sm md:text-base font-bold" style="font-family: KaiTi, STKaiti, '楷体', serif; text-align: justify; text-align-last: justify;">
          沈西派出所
        </div>
        <div class="text-white/80 text-xs" style="text-align: justify; text-align-last: justify;">
          SHENXI POLICE
        </div>
      </div>
    </div>

    <!-- 中间：标题（绝对居中） -->
    <h1 class="absolute left-1/2 -translate-x-1/2 text-lg md:text-xl font-bold text-white tracking-wider" style="font-family: KaiTi, STKaiti, '楷体', serif;">
      {{ title }}
    </h1>
  </header>
</template>
