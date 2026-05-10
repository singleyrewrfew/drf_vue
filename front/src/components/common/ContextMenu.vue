<template>
  <Teleport to="body">
    <div
      v-show="visible"
      ref="menuRef"
      class="context-menu"
      :style="{ top: position.y + 'px', left: position.x + 'px' }"
      @contextmenu.prevent
      @click.stop
    >
      <div class="context-menu-inner">
        <div
          v-for="(item, index) in items"
          :key="index"
          class="context-menu-item"
          :class="{ 'is-divider': item.divider, 'is-disabled': item.disabled }"
          @click="handleItemClick(item, $event)"
        >
          <template v-if="!item.divider">
            <span v-if="item.icon" class="menu-icon">{{ item.icon }}</span>
            <span class="menu-label">{{ item.label }}</span>
            <span v-if="item.shortcut" class="menu-shortcut">{{ item.shortcut }}</span>
            <span v-if="item.children" class="menu-arrow">▸</span>
          </template>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  items: {
    type: Array,
    default: () => []
  },
  position: {
    type: Object,
    default: () => ({ x: 0, y: 0 })
  }
})

const emit = defineEmits(['select', 'close'])

const menuRef = ref(null)

const handleItemClick = (item, event) => {
  if (item.disabled || item.divider) return
  
  emit('select', item)
}

// 点击外部或按 ESC 关闭
const closeMenu = () => {
  emit('close')
}

// 监听 visible 变化来添加/移除事件监听
watch(() => props.visible, (val) => {
  if (val) {
    nextTick(() => adjustPosition())
    document.addEventListener('click', closeMenu)
    document.addEventListener('keydown', handleKeydown)
    document.addEventListener('contextmenu', closeMenu)
  } else {
    document.removeEventListener('click', closeMenu)
    document.removeEventListener('keydown', handleKeydown)
    document.removeEventListener('contextmenu', closeMenu)
  }
})

const handleKeydown = (e) => {
  if (e.key === 'Escape') {
    closeMenu()
  }
}

const adjustPosition = () => {
  if (!menuRef.value) return
  
  const menu = menuRef.value
  const rect = menu.getBoundingClientRect()
  
  // 右边界检测
  if (rect.right > window.innerWidth) {
    const newX = props.position.x - rect.width - 8
    menu.style.left = Math.max(8, newX) + 'px'
  }
  
  // 下边界检测
  if (rect.bottom > window.innerHeight) {
    const newY = props.position.y - rect.height - 8
    menu.style.top = Math.max(8, newY) + 'px'
  }
}
</script>

<style scoped>
.context-menu {
  position: fixed;
  z-index: 9999;
  min-width: 180px;
  padding: 4px;
}

.context-menu-inner {
  background: var(--paper-cream, #ede8dc);
  border: 1.5px solid var(--paper-aged, #ddd6c8);
  border-radius: var(--radius-sm, 4px);
  box-shadow:
    0 4px 16px rgba(26, 26, 26, 0.15),
    inset 0 0 0 1px rgba(255, 255, 255, 0.3);
  padding: 4px;
  font-family: "KaiTi", "STKaiti", serif;
}

.context-menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  cursor: pointer;
  border-radius: var(--radius-xs, 2px);
  transition: all 0.2s ease;
  color: var(--ink-dark, #1a1a1a);
  font-size: 14px;
  letter-spacing: 0.03em;
}

.context-menu-item:hover:not(.is-disabled):not(.is-divider) {
  background: rgba(197, 61, 67, 0.08);
  color: var(--vermilion-color, #c53d43);
}

.context-menu-item.is-disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.context-menu-item.is-divider {
  height: 1px;
  padding: 0;
  margin: 4px 8px;
  background: var(--paper-aged, #ddd6c8);
  cursor: default;
}

.menu-icon {
  width: 16px;
  text-align: center;
  flex-shrink: 0;
}

.menu-label {
  flex: 1;
}

.menu-shortcut {
  color: var(--ink-light, #8c8c8c);
  font-size: 12px;
  margin-left: auto;
}

.menu-arrow {
  color: var(--ink-light, #8c8c8c);
  font-size: 12px;
}

/* 暗色模式 */
[data-theme='dark'] .context-menu-inner {
  background: #27272a;
  border-color: #3f3f46;
  box-shadow:
    0 4px 20px rgba(0, 0, 0, 0.4),
    inset 0 0 0 1px rgba(255, 255, 255, 0.05);
}

[data-theme='dark'] .context-menu-item {
  color: #e4e4e7;
}

[data-theme='dark'] .context-menu-item:hover:not(.is-disabled):not(.is-divider) {
  background: rgba(220, 38, 38, 0.12);
  color: #ef4444;
}

[data-theme='dark'] .context-menu-item.is-divider {
  background: #3f3f46;
}
</style>
