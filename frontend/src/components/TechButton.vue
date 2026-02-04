<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  borderColor: {
    type: String,
    default: '#00cfff'
  },
  glowColor: {
    type: String,
    default: '#00cfff'
  },
  gradientFrom: {
    type: String,
    default: 'rgba(0, 40, 80, 0.9)'
  },
  gradientTo: {
    type: String,
    default: 'rgba(0, 20, 50, 0.95)'
  },
  cornerSize: {
    type: Number,
    default: 7 // 6-8px 切角深度
  },
  cornerExtend: {
    type: Number,
    default: 12 // 护角向两端延伸的长度
  }
})

const containerRef = ref(null)
const width = ref(0)
const height = ref(0)

const updateSize = () => {
  if (containerRef.value) {
    width.value = containerRef.value.offsetWidth
    height.value = containerRef.value.offsetHeight
  }
}

onMounted(() => {
  updateSize()
  window.addEventListener('resize', updateSize)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateSize)
})

// 四角 45 度切角的 SVG path
const shapePath = computed(() => {
  const w = width.value
  const h = height.value
  const c = props.cornerSize
  // 顺时针：左上切角 -> 右上切角 -> 右下切角 -> 左下切角
  return `M ${c},0 L ${w - c},0 L ${w},${c} L ${w},${h - c} L ${w - c},${h} L ${c},${h} L 0,${h - c} L 0,${c} Z`
})

// 四个护角路径（斜边 + 两端延伸）
// 形成 "┘" "└" "┐" "┌" 形状的护角
const cornerPaths = computed(() => {
  const w = width.value
  const h = height.value
  const c = props.cornerSize
  const ext = props.cornerExtend

  return [
    // 左上角 ┌ : 垂直延伸 -> 斜边 -> 水平延伸
    `M 0,${c + ext} L 0,${c} L ${c},0 L ${c + ext},0`,
    // 右上角 ┐ : 水平延伸 -> 斜边 -> 垂直延伸
    `M ${w - c - ext},0 L ${w - c},0 L ${w},${c} L ${w},${c + ext}`,
    // 右下角 ┘ : 垂直延伸 -> 斜边 -> 水平延伸
    `M ${w},${h - c - ext} L ${w},${h - c} L ${w - c},${h} L ${w - c - ext},${h}`,
    // 左下角 └ : 水平延伸 -> 斜边 -> 垂直延伸
    `M ${c + ext},${h} L ${c},${h} L 0,${h - c} L 0,${h - c - ext}`
  ]
})

const uid = ref(`tech-btn-${Math.random().toString(36).substr(2, 9)}`)
</script>

<template>
  <div ref="containerRef" class="tech-button">
    <svg class="border-svg" :width="width" :height="height">
      <defs>
        <!-- 渐变填充 -->
        <linearGradient :id="`${uid}-gradient`" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :stop-color="gradientFrom" />
          <stop offset="100%" :stop-color="gradientTo" />
        </linearGradient>

        <!-- 内发光渐变（边缘向内） -->
        <radialGradient :id="`${uid}-inner-glow`" cx="50%" cy="50%" r="70%" fx="50%" fy="50%">
          <stop offset="60%" stop-color="transparent" />
          <stop offset="100%" :stop-color="glowColor" stop-opacity="0.15" />
        </radialGradient>

        <!-- 基础边框发光 -->
        <filter :id="`${uid}-glow`" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur in="SourceGraphic" stdDeviation="1.5" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>

        <!-- 切角强发光 -->
        <filter :id="`${uid}-corner-glow`" x="-100%" y="-100%" width="300%" height="300%">
          <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur1" />
          <feGaussianBlur in="SourceGraphic" stdDeviation="1" result="blur2" />
          <feMerge>
            <feMergeNode in="blur1" />
            <feMergeNode in="blur2" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>

        <!-- 内发光滤镜 -->
        <filter :id="`${uid}-inner-glow-filter`" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur in="SourceAlpha" stdDeviation="4" result="blur" />
          <feOffset in="blur" dx="0" dy="0" result="offsetBlur" />
          <feFlood :flood-color="glowColor" flood-opacity="0.3" result="color" />
          <feComposite in="color" in2="offsetBlur" operator="in" result="shadow" />
          <feComposite in="shadow" in2="SourceAlpha" operator="in" result="innerShadow" />
          <feMerge>
            <feMergeNode in="SourceGraphic" />
            <feMergeNode in="innerShadow" />
          </feMerge>
        </filter>

        <!-- clip path 用于内发光层 -->
        <clipPath :id="`${uid}-clip`">
          <path :d="shapePath" />
        </clipPath>
      </defs>

      <!-- 背景填充 -->
      <path
        :d="shapePath"
        :fill="`url(#${uid}-gradient)`"
      />

      <!-- 内发光层 -->
      <g :clip-path="`url(#${uid}-clip)`">
        <!-- 边缘内发光（模拟内阴影） -->
        <path
          :d="shapePath"
          fill="none"
          :stroke="glowColor"
          :stroke-width="16"
          stroke-opacity="0.08"
        />
        <path
          :d="shapePath"
          fill="none"
          :stroke="glowColor"
          :stroke-width="8"
          stroke-opacity="0.12"
        />
        <path
          :d="shapePath"
          fill="none"
          :stroke="glowColor"
          :stroke-width="4"
          stroke-opacity="0.15"
        />
      </g>

      <!-- 基础边框 1px -->
      <path
        :d="shapePath"
        fill="none"
        :stroke="borderColor"
        stroke-width="1"
        stroke-opacity="0.8"
        :filter="`url(#${uid}-glow)`"
      />

      <!-- 四个护角：斜边 + 两端延伸，加粗 + 强发光 -->
      <path
        v-for="(d, index) in cornerPaths"
        :key="index"
        :d="d"
        fill="none"
        :stroke="glowColor"
        stroke-width="2"
        stroke-linecap="square"
        stroke-linejoin="miter"
        :filter="`url(#${uid}-corner-glow)`"
      />
    </svg>
    <div class="button-content">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.tech-button {
  position: relative;
  width: 100%;
  height: 100%;
}

.border-svg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: visible;
}

.button-content {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}

.button-content :deep(*),
.button-content {
  font-size: 24px !important;
  font-weight: 600 !important;
  letter-spacing: 0.08em !important;
}
</style>
