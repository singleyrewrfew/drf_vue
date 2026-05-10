<template>
  <div class="win-dropdown">
    <div class="win-dropdown-trigger" ref="triggerRef" @click="toggleDropdown">
      <slot name="trigger">
        <span class="win-dropdown-default-trigger">
          {{ label }}
          <svg
            class="win-dropdown-arrow"
            :class="{ 'is-open': isOpen }"
            viewBox="0 0 1024 1024"
            width="12"
            height="12"
          >
            <path
              fill="currentColor"
              d="M512 714.667c-17.067 0-32-6.4-44.8-19.2L147.2 375.467c-25.6-25.6-25.6-64 0-89.6s64-25.6 89.6 0L512 561.067l275.2-275.2c25.6-25.6 64-25.6 89.6 0s25.6 64 0 89.6L556.8 695.467c-12.8 12.8-27.733 19.2-44.8 19.2z"
            />
          </svg>
        </span>
      </slot>
    </div>
    <Teleport to="body">
      <Transition name="win-dropdown-fade">
        <div v-if="isOpen" class="win-dropdown-menu" :style="menuStyle" ref="menuRef">
          <div
            v-for="item in items"
            :key="item.value"
            class="win-dropdown-item"
            :class="{ 'is-disabled': item.disabled }"
            @click="handleSelect(item)"
          >
            <span v-if="item.icon" class="win-dropdown-item-icon">
              <component :is="item.icon" />
            </span>
            <span class="win-dropdown-item-text">{{ item.label }}</span>
          </div>
          <div v-if="!items.length" class="win-dropdown-empty">暂无数据</div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  label: {
    type: String,
    default: '下拉菜单'
  },
  items: {
    type: Array,
    default: () => []
  },
  modelValue: {
    type: [String, Number],
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'select', 'change'])

const triggerRef = ref(null)
const menuRef = ref(null)
const isOpen = ref(false)
const menuStyle = ref({})

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const handleSelect = item => {
  if (item.disabled) return
  emit('update:modelValue', item.value)
  emit('select', item)
  emit('change', item)
  isOpen.value = false
}

const updatePosition = () => {
  if (!triggerRef.value || !isOpen.value) return

  const rect = triggerRef.value.getBoundingClientRect()
  const viewportWidth = window.innerWidth
  const viewportHeight = window.innerHeight
  const menuHeight = 200
  const menuWidth = Math.max(rect.width, 160)

  let top = rect.bottom + 4
  let left = rect.left

  // 垂直方向：如果下方空间不足，向上弹出
  if (rect.bottom + menuHeight > viewportHeight) {
    top = rect.top - menuHeight - 4
  }

  // 水平方向：如果右侧空间不足，向左调整
  if (left + menuWidth > viewportWidth) {
    left = viewportWidth - menuWidth - 8
  }

  // 确保不超出左边界
  if (left < 8) {
    left = 8
  }

  menuStyle.value = {
    position: 'fixed',
    left: `${left}px`,
    top: `${top}px`,
    minWidth: `${menuWidth}px`,
    zIndex: 2000
  }
}

const handleClickOutside = e => {
  if (triggerRef.value && !triggerRef.value.contains(e.target)) {
    if (menuRef.value && !menuRef.value.contains(e.target)) {
      isOpen.value = false
    }
  }
}

watch(isOpen, val => {
  if (val) {
    updatePosition()
  }
})

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('scroll', updatePosition, true)
  window.addEventListener('resize', updatePosition)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('scroll', updatePosition, true)
  window.removeEventListener('resize', updatePosition)
})
</script>

<style scoped>
.win-dropdown {
  display: inline-block;
  position: relative;
}

.win-dropdown-trigger {
  cursor: pointer;
  user-select: none;
}

.win-dropdown-default-trigger {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: var(--paper-cream, #ede8dc);
  border: 1.5px solid var(--paper-aged, #ddd6c8);
  border-radius: var(--radius-xs, 2px);
  font-size: 14px;
  color: var(--ink-medium, #595959);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: "KaiTi", "STKaiti", serif;
}

.win-dropdown-default-trigger:hover {
  background: var(--vermilion-color, #c53d43);
  border-color: var(--vermilion-color, #c53d43);
  color: #fff;
}

.win-dropdown-arrow {
  transition: transform var(--transition-fast);
}

.win-dropdown-arrow.is-open {
  transform: rotate(180deg);
}

.win-dropdown-menu {
  background: var(--paper-cream, #ede8dc);
  border: 1.5px solid var(--paper-aged, #ddd6c8);
  border-radius: var(--radius-xs, 2px);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.4),
    1px 1px 6px rgba(26, 26, 26, 0.08);
  padding: 6px;
  max-height: 280px;
  overflow-y: auto;
  scrollbar-width: none;
}

.win-dropdown-menu::-webkit-scrollbar {
  display: none;
}

.win-dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-radius: var(--radius-xs, 2px);
  font-size: 14px;
  color: var(--ink-dark, #1a1a1a);
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  font-family: "KaiTi", "STKaiti", serif;
  letter-spacing: 0.03em;
}

.win-dropdown-item:hover {
  background: rgba(197, 61, 67, 0.08);
  color: var(--vermilion-color, #c53d43);
}

.win-dropdown-item.is-disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.win-dropdown-item.is-disabled:hover {
  background: transparent;
  color: var(--ink-dark, #1a1a1a);
}

.win-dropdown-item-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
}

.win-dropdown-item-text {
  flex: 1;
}

.win-dropdown-empty {
  padding: 20px;
  text-align: center;
  color: var(--ink-light, #8c8c8c);
  font-size: 14px;
  font-family: "KaiTi", "STKaiti", serif;
}

.win-dropdown-fade-enter-active,
.win-dropdown-fade-leave-active {
  transition: all 0.18s ease;
}

.win-dropdown-fade-enter-from,
.win-dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-6px) scale(0.97);
}

/* ====== 暗色模式适配 ====== */

[data-theme='dark'] .win-dropdown-default-trigger {
  background: #27272a;
  border-color: #3f3f46;
  color: #a1a1aa;
}

[data-theme='dark'] .win-dropdown-default-trigger:hover {
  background: #dc2626;
  border-color: #dc2626;
  color: #fff;
}

[data-theme='dark'] .win-dropdown-menu {
  background: #27272a;
  border-color: #3f3f46;
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.05),
    1px 1px 8px rgba(0, 0, 0, 0.4);
}

[data-theme='dark'] .win-dropdown-item {
  color: #e4e4e7;
}

[data-theme='dark'] .win-dropdown-item:hover {
  background: rgba(220, 38, 38, 0.12);
  color: #ef4444;
}

[data-theme='dark'] .win-dropdown-item.is-disabled:hover {
  color: #e4e4e7;
}

[data-theme='dark'] .win-dropdown-empty {
  color: #71717a;
}
</style>

<style>
.win-dropdown-menu {
  position: fixed;
  background: var(--paper-cream, #ede8dc);
  border: 1.5px solid var(--paper-aged, #ddd6c8);
  border-radius: var(--radius-xs, 2px);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.4),
    1px 1px 6px rgba(26, 26, 26, 0.08);
  padding: 6px;
  max-height: 280px;
  overflow-y: auto;
  z-index: 2000;
  scrollbar-width: none;
}

.win-dropdown-menu::-webkit-scrollbar {
  display: none;
}

.win-dropdown-menu .win-dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-radius: var(--radius-xs, 2px);
  font-size: 14px;
  color: var(--ink-dark, #1a1a1a);
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  font-family: "KaiTi", "STKaiti", serif;
  letter-spacing: 0.03em;
}

.win-dropdown-menu .win-dropdown-item:hover {
  background: rgba(197, 61, 67, 0.08);
  color: var(--vermilion-color, #c53d43);
}

.win-dropdown-menu .win-dropdown-item.is-disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.win-dropdown-menu .win-dropdown-item.is-disabled:hover {
  background: transparent;
  color: var(--ink-dark, #1a1a1a);
}

.win-dropdown-menu .win-dropdown-item-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
}

.win-dropdown-menu .win-dropdown-item-text {
  flex: 1;
}

.win-dropdown-menu .win-dropdown-empty {
  padding: 20px;
  text-align: center;
  color: var(--ink-light, #8c8c8c);
  font-size: 14px;
  font-family: "KaiTi", "STKaiti", serif;
}

/* ====== 暗色模式适配（Teleport 到 body 的菜单） ====== */

[data-theme='dark'] .win-dropdown-menu {
  background: #27272a;
  border-color: #3f3f46;
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.05),
    1px 1px 8px rgba(0, 0, 0, 0.4);
}

[data-theme='dark'] .win-dropdown-menu .win-dropdown-item {
  color: #e4e4e7;
}

[data-theme='dark'] .win-dropdown-menu .win-dropdown-item:hover {
  background: rgba(220, 38, 38, 0.12);
  color: #ef4444;
}

[data-theme='dark'] .win-dropdown-menu .win-dropdown-item.is-disabled:hover {
  color: #e4e4e7;
}

[data-theme='dark'] .win-dropdown-menu .win-dropdown-empty {
  color: #71717a;
}
</style>
