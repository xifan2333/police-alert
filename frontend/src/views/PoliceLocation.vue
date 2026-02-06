<script setup>
import PageHeader from '../components/PageHeader.vue'
import FloatingButton from '@/components/FloatingButton.vue'

const iframeUrl = 'https://www.azliot.com/home/siteMap'
</script>

<template>
  <div class="police-location-page">
    <!-- 顶部导航栏 -->
    <PageHeader title="警力动态监测" />

    <!-- iframe 内容区域 -->
    <div class="iframe-wrapper">
      <iframe
        :src="iframeUrl"
        class="iframe-content"
        title="警力效能动态监测"
        allow="geolocation"
      ></iframe>
    </div>

    <!-- 悬浮返回按钮 -->
    <FloatingButton />
  </div>
</template>

<style scoped>
.police-location-page {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  background: var(--bg-sub) center/cover no-repeat;
}

.iframe-wrapper {
  flex: 1;
  position: relative;
  min-height: 0;
}

.iframe-content {
  width: 100%;
  height: 100%;
  border: 0;
}
</style>
