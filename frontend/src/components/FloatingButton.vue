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
  position: absolute;
  bottom: 32px;
  right: 32px;
  z-index: 1000;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(var(--c-primary-rgb), 0.9);
  border: 2px solid rgba(var(--c-primary-rgb), 0.6);
  box-shadow: 0 0 20px rgba(var(--c-primary-rgb), 0.5);
  color: var(--c-text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.floating-home-button:hover {
  transform: scale(1.1);
  background: var(--c-primary-light);
  box-shadow: 0 0 30px rgba(var(--c-primary-rgb), 0.7);
}

.floating-home-button:active {
  transform: scale(0.95);
}
</style>
