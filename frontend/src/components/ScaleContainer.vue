<template>
  <div class="viewport" ref="viewportRef">
    <div class="scale-container" :style="containerStyle">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { DESIGN_WIDTH, DESIGN_HEIGHT } from '@/config/design.js'

// 定义组件的 props，允许外部传入设计稿尺寸，并设置默认值
const props = defineProps({
  width: {
    type: Number,
    default: DESIGN_WIDTH
  },
  height: {
    type: Number,
    default: DESIGN_HEIGHT
  }
})

const viewportRef = ref(null)
const containerStyle = ref({})

const updateScale = () => {
  if (!viewportRef.value) return

  const { clientWidth, clientHeight } = viewportRef.value
  const designWidth = props.width
  const designHeight = props.height

  // 计算缩放比例，优先保证内容完整显示
  const scale = Math.min(
    clientWidth / designWidth,
    clientHeight / designHeight
  )

  // 计算缩放后的实际尺寸
  const scaledWidth = designWidth * scale
  const scaledHeight = designHeight * scale

  // 计算居中偏移量
  const offsetX = (clientWidth - scaledWidth) / 2
  const offsetY = (clientHeight - scaledHeight) / 2

  containerStyle.value = {
    position: 'absolute',
    left: `${offsetX}px`,
    top: `${offsetY}px`,
    transform: `scale(${scale})`,
    transformOrigin: '0 0',
    width: `${designWidth}px`,
    height: `${designHeight}px`
  }
}

onMounted(() => {
  // 使用防抖优化 resize 事件
  let debounceTimer
  const debouncedUpdateScale = () => {
    clearTimeout(debounceTimer)
    debounceTimer = setTimeout(updateScale, 100)
  }

  updateScale()
  window.addEventListener('resize', debouncedUpdateScale)

  onUnmounted(() => {
    window.removeEventListener('resize', debouncedUpdateScale)
    clearTimeout(debounceTimer)
  })
})
</script>

<style scoped>
.viewport {
  width: 100vw;
  height: 100vh;
  position: relative;
  overflow: hidden;
  background-color: #0c1029; /* 深蓝背景色，与警务主题匹配 */
}

.scale-container {
  backface-visibility: hidden; /* 优化渲染性能 */
}
</style>
