<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  message: {
    type: String,
    default: ''
  },
  duration: {
    type: Number,
    default: 2000
  },
  type: {
    type: String,
    default: 'info', // info, success, warning, error
    validator: (value) => ['info', 'success', 'warning', 'error'].includes(value)
  }
})

const emit = defineEmits(['close'])

const visible = ref(false)
let timer = null

const show = () => {
  visible.value = true

  if (timer) {
    clearTimeout(timer)
  }

  timer = setTimeout(() => {
    hide()
  }, props.duration)
}

const hide = () => {
  visible.value = false
  emit('close')
}

watch(() => props.message, (newVal) => {
  if (newVal) {
    show()
  }
})

defineExpose({ show, hide })
</script>

<template>
  <transition name="toast">
    <div
      v-if="visible"
      class="toast"
      :class="`toast-${type}`"
    >
      <div class="toast-content">
        <div class="toast-icon">
          <div v-if="type === 'success'" class="i-ri-checkbox-circle-fill text-2xl" />
          <div v-else-if="type === 'error'" class="i-ri-close-circle-fill text-2xl" />
          <div v-else-if="type === 'warning'" class="i-ri-error-warning-fill text-2xl" />
          <div v-else class="i-ri-information-fill text-2xl" />
        </div>
        <div class="toast-message">{{ message }}</div>
      </div>
    </div>
  </transition>
</template>

<style scoped>
.toast {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
  padding: 16px 24px;
  border-radius: 8px;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  min-width: 200px;
  max-width: 400px;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.toast-icon {
  flex-shrink: 0;
}

.toast-message {
  font-size: 16px;
  font-weight: 500;
  color: #fff;
}

.toast-info {
  background: rgba(59, 130, 246, 0.9);
  border: 1px solid rgba(59, 130, 246, 0.5);
}

.toast-success {
  background: rgba(34, 197, 94, 0.9);
  border: 1px solid rgba(34, 197, 94, 0.5);
}

.toast-warning {
  background: rgba(251, 146, 60, 0.9);
  border: 1px solid rgba(251, 146, 60, 0.5);
}

.toast-error {
  background: rgba(239, 68, 68, 0.9);
  border: 1px solid rgba(239, 68, 68, 0.5);
}

/* 动画 */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.8);
}

.toast-leave-to {
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.8);
}
</style>
