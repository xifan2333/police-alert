<script setup>
import PageHeader from '../components/PageHeader.vue'
import FloatingButton from '@/components/FloatingButton.vue'

const iframeUrl = 'https://www.azliot.com/home/siteMap'
</script>

<template>
  <div class="police-location-page relative flex flex-col w-full h-full bg-#111827">
    <!-- 顶部导航栏 -->
    <PageHeader title="警力动态监测" />

    <!-- iframe 内容区域 -->
    <div class="flex-1 relative min-h-0">
      <iframe
        :src="iframeUrl"
        class="w-full h-full border-0"
        title="警力效能动态监测"
        allow="geolocation"
      ></iframe>
    </div>

    <!-- 悬浮返回按钮 -->
    <FloatingButton />
  </div>
</template>
