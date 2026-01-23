<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}
</script>

<template>
  <div class="back-section">
    <button @click="goHome" class="back-btn">
      <div class="i-ri-arrow-left-line"></div>
      <span>返回主页</span>
    </button>
    <div class="divider"></div>
  </div>
</template>

<style scoped>
.back-section {
  margin-bottom: 12px;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: rgba(14, 165, 233, 0.15);
  border: 1px solid rgba(14, 165, 233, 0.6);
  border-radius: 4px;
  color: #06B6D4;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 12px;
}

.back-btn:hover {
  background: rgba(14, 165, 233, 0.25);
  border-color: rgba(14, 165, 233, 0.8);
  color: #22D3EE;
  transform: translateX(-4px);
}

.divider {
  width: 100%;
  height: 1px;
  background: linear-gradient(
    90deg,
    rgba(14, 165, 233, 0.8) 0%,
    rgba(14, 165, 233, 0.4) 50%,
    rgba(14, 165, 233, 0) 100%
  );
}
</style>
