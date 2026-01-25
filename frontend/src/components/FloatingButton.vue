<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}
</script>

<template>
  <button
    class="floating-home-button"
    @click="goHome"
    title="返回主页"
  >
    <div class="i-ri-home-4-line text-1xl" />
  </button>
</template>

<style scoped>
.floating-home-button {
  position: fixed;
  bottom: 32px;
  right: 32px;
  z-index: 1000;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(44, 39, 114, 0.9);
  border: 2px solid rgba(59, 130, 246, 0.6);
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.floating-home-button:hover {
  transform: scale(1.1);
  background: rgba(59, 130, 246, 0.9);
  box-shadow: 0 0 30px rgba(59, 130, 246, 0.7);
}

.floating-home-button:active {
  transform: scale(0.95);
}
</style>
