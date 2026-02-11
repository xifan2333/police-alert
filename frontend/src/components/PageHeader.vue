<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  }
})

const currentTime = ref('')

// 更新时间
const updateTime = () => {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  currentTime.value = `${year}-${month}-${day} ${hours}:${minutes}`
}

let timer = null

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<template>
    <header class="page-header">
    <!-- 左侧：警徽和派出所名称 -->
    <div class="header-left">
      <img src="/logo-gold.png" alt="警徽" class="header-logo" />
      <div class="header-police-info">
        <div class="police-name">沈西派出所</div>
        <div class="police-name-en">SHENXI POLICE</div>
      </div>
    </div>

    <!-- 中间：标题（绝对居中） -->
    <div class="header-center">
      <dv-decoration-8 class="title-decoration" :reverse="true" />
      <h1 class="header-title">{{ title }}</h1>
      <dv-decoration-8 class="title-decoration" />
    </div>

    <!-- 右侧：时间 -->
    <div class="header-right">
      <div class="current-time">{{ currentTime }}</div>
    </div>
    </header>
</template>

<style scoped>


.page-header {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 80px;
  background: var(--bg-header) center 0/cover no-repeat;
  backdrop-filter: blur(8px);
  overflow: hidden;
  gap: 24px;
}

/* 左侧 */
.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 1;
}

.header-logo {
  width: 56px;
  height: 56px;
  opacity: 0.95;
  filter: drop-shadow(0 0 8px rgba(var(--c-primary-rgb), 0.5))
          drop-shadow(0 2px 4px var(--c-shadow));
}

.header-police-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 180px;
}

.police-name {
  font-family: var(--font-serif);
  font-size: 24px;
  font-weight: bold;
  color: var(--c-text-primary);
  text-shadow: 0 0 10px rgba(var(--c-primary-rgb), 0.6),
               0 2px 4px var(--c-shadow);
  letter-spacing: 2px;
}

.police-name-en {
  font-size: 14px;
  color: var(--c-text-secondary);
  letter-spacing: 1px;
  margin-top: 2px;
  text-shadow: 0 1px 2px var(--c-shadow);
}

/* 中间 */
.header-center {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 16px;
  z-index: 1;
  padding: 8px 48px;
}

.title-decoration {
  width: 150px;
  height: 30px;
  --color: var(--c-accent);
}

.header-title {
  font-family: var(--font-serif);
  font-size: 56px;
  font-weight: bold;
  color: var(--c-text-primary);
  letter-spacing: 6px;
  text-shadow: 0 0 12px rgba(var(--c-accent-rgb), 0.8),
               0 0 24px rgba(var(--c-primary-rgb), 0.6),
               0 0 40px rgba(var(--c-primary-rgb), 0.3),
               0 2px 4px var(--c-shadow);
  white-space: nowrap;
}

/* 右侧 */
.header-right {
  display: flex;
  align-items: center;
  z-index: 1;
}

.current-time {
  font-family: var(--font-mono);
  font-size: 22px;
  font-weight: 600;
  color: var(--c-text-primary);
  letter-spacing: 1px;
  text-shadow: 0 0 10px rgba(var(--c-accent-rgb), 0.7),
               0 0 20px rgba(var(--c-primary-rgb), 0.4),
               0 2px 4px var(--c-shadow);
  white-space: nowrap;
  min-width: 150px;
  text-align: right;
}

/* 响应式 */
@media (max-width: 1280px) {
  .header-title {
    font-size: 24px;
    letter-spacing: 3px;
  }

  .title-decoration {
    width: 120px;
  }

  .current-time {
    font-size: 16px;
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 8px 16px;
    height: 60px;
  }

  .header-logo {
    width: 36px;
    height: 36px;
  }

  .police-name {
    font-size: 14px;
  }

  .police-name-en {
    font-size: 10px;
  }

  .header-title {
    font-size: 18px;
    letter-spacing: 2px;
  }

  .title-decoration {
    width: 80px;
    height: 20px;
  }

  .time-decoration {
    width: 60px;
    height: 20px;
  }

  .current-time {
    font-size: 14px;
    min-width: 120px;
  }
}
</style>
