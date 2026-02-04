<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { DESIGN_WIDTH, DESIGN_HEIGHT } from '@/config/design.js'
import TechButton from '@/components/TechButton.vue'

const props = defineProps({
  navItems: {
    type: Array,
    required: true,
    default: () => []
  }
})

const router = useRouter()

// 状态
const isMenuOpen = ref(false)
const isDragging = ref(false)
const hoverIndex = ref(-1)

// 位置状态
const position = ref({ x: 0, y: 0 })
const dragStart = ref({ x: 0, y: 0 })
const hasMoved = ref(false)

// 初始化位置（基于设计稿尺寸，右下角）
onMounted(() => {
  position.value = {
    x: DESIGN_WIDTH - 170,
    y: DESIGN_HEIGHT - 200
  }
})

// 菜单列表的垂直偏移，使其中心在屏幕中心线
const menuOffsetY = computed(() => {
  return DESIGN_HEIGHT / 2 - position.value.y
})

// 切换菜单
const toggleMenu = () => {
  if (hasMoved.value) {
    hasMoved.value = false
    return
  }
  isMenuOpen.value = !isMenuOpen.value
}

// 处理菜单项点击
const handleItemClick = (item) => {
  router.push(item.to)
  isMenuOpen.value = false
  hoverIndex.value = -1
}

// 拖拽开始
const startDrag = (e) => {
  isDragging.value = true
  hasMoved.value = false
  const clientX = e.touches ? e.touches[0].clientX : e.clientX
  const clientY = e.touches ? e.touches[0].clientY : e.clientY
  dragStart.value = {
    x: clientX - position.value.x,
    y: clientY - position.value.y
  }
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
  document.addEventListener('touchmove', onDrag, { passive: false })
  document.addEventListener('touchend', stopDrag)
}

// 拖拽中
const onDrag = (e) => {
  if (!isDragging.value) return
  e.preventDefault()
  const clientX = e.touches ? e.touches[0].clientX : e.clientX
  const clientY = e.touches ? e.touches[0].clientY : e.clientY

  const newX = clientX - dragStart.value.x
  const newY = clientY - dragStart.value.y

  if (Math.abs(newX - position.value.x) > 3 || Math.abs(newY - position.value.y) > 3) {
    hasMoved.value = true
  }

  // 限制在设计稿尺寸范围内
  position.value = {
    x: Math.max(60, Math.min(DESIGN_WIDTH - 60, newX)),
    y: Math.max(60, Math.min(DESIGN_HEIGHT - 60, newY))
  }
}

// 拖拽结束
const stopDrag = () => {
  isDragging.value = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
  document.removeEventListener('touchmove', onDrag)
  document.removeEventListener('touchend', stopDrag)
}

onUnmounted(() => {
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
  document.removeEventListener('touchmove', onDrag)
  document.removeEventListener('touchend', stopDrag)
})
</script>

<template>
  <nav
    class="nav-container"
    :style="{
      left: position.x + 'px',
      top: position.y + 'px'
    }"
  >
    <!-- 菜单列表 -->
    <div
      class="menu-list"
      :class="{ show: isMenuOpen }"
      :style="{ transform: `translate(-50%, -50%) translateY(${menuOffsetY}px)` }"
    >
      <TechButton
        v-for="(item, index) in navItems"
        :key="index"
        class="menu-item"
        border-color="#00cfff"
        background-color="rgba(5, 20, 45, 0.9)"
        @click="handleItemClick(item)"
      >
        <div class="item-content">
          {{ item.text }}
        </div>
      </TechButton>
    </div>

    <!-- 中心按钮 -->
    <div
      class="nav-center-btn"
      :class="{ active: isMenuOpen, dragging: isDragging }"
      @mousedown="startDrag"
      @touchstart="startDrag"
      @click="toggleMenu"
    >
      <img src="/button.png" alt="菜单" class="btn-image" />
    </div>
  </nav>
</template>

<style scoped>
.nav-container {
  position: absolute;
  z-index: 1000;
  transform: translate(-50%, -50%);
}

.menu-list {
  position: absolute;
  left: 50%;
  top: 50%;
  display: flex;
  flex-direction: column;
  gap: 32px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.menu-list.show {
  opacity: 1;
  pointer-events: auto;
}

.menu-item {
  width: 280px;
  height: 64px;
  cursor: pointer;
  transition: transform 0.2s ease, filter 0.2s ease;
}

.menu-item:hover {
  transform: scale(1.02);
  filter: brightness(1.2);
}

.item-content {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  font-weight: bold;
  color: #fff;
  letter-spacing: 6px;
}

.nav-center-btn {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 160px;
  height: 160px;
  cursor: grab;
  z-index: 50;
  transition: transform 0.3s ease;
}

.btn-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.nav-center-btn:hover .btn-image {
  transform: scale(1.08);
}

.nav-center-btn.dragging {
  cursor: grabbing;
}

.nav-center-btn.dragging .btn-image {
  transform: scale(1.05);
}
</style>
