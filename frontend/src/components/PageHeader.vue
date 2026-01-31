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
      <img src="/logo-blue.png" alt="警徽" class="header-logo" />
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
      <dv-decoration-3 class="time-decoration" />
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
  padding: 12px 24px;
  height: 80px;
  background: transparent;
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
  width: 48px;
  height: 48px;
  opacity: 0.95;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

.header-police-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 180px;
}

.police-name {
  font-family: KaiTi, STKaiti, '楷体', serif;
  font-size: 18px;
  font-weight: bold;
  color: #fff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  letter-spacing: 2px;
}

.police-name-en {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.85);
  letter-spacing: 1px;
  margin-top: 2px;
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
  padding: 12px 48px;
  background: linear-gradient(135deg, rgba(0, 106, 206, 0.9) 0%, rgba(0, 82, 158, 0.8) 100%);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(59, 130, 246, 0.4);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
  clip-path: polygon(0% 0%, 100% 0%, 92% 100%, 8% 100%);
}

.title-decoration {
  width: 150px;
  height: 30px;
}

.header-title {
  font-family: KaiTi, STKaiti, '楷体', serif;
  font-size: 28px;
  font-weight: bold;
  color: #fff;
  letter-spacing: 4px;
  text-shadow: 0 0 10px rgba(59, 130, 246, 0.8),
               0 0 20px rgba(59, 130, 246, 0.6),
               0 2px 4px rgba(0, 0, 0, 0.5);
  white-space: nowrap;
}

/* 右侧 */
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 1;
}

.time-decoration {
  width: 100px;
  height: 30px;
}

.current-time {
  font-family: 'Courier New', monospace;
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  letter-spacing: 1px;
  text-shadow: 0 0 8px rgba(59, 130, 246, 0.8),
               0 2px 4px rgba(0, 0, 0, 0.5);
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
