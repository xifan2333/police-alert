<script setup>
import PageHeader from '../components/PageHeader.vue'

const iframeUrl = 'https://www.azliot.com/home/siteMap'
</script>

<template>
  <div class="h-screen w-screen flex flex-col bg-gray-900">
    <!-- 顶部导航栏 -->
    <PageHeader title="警力效能动态监测" />

    <!-- iframe 内容区域 -->
    <div class="flex-1 relative">
      <iframe
        :src="iframeUrl"
        class="w-full h-full border-0"
        title="警力效能动态监测"
        allow="geolocation"
      ></iframe>
    </div>
  </div>
</template>
