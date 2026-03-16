<template>
  <div class="win-dropdown">
    <div class="win-dropdown-trigger" ref="triggerRef" @click="toggleDropdown">
      <slot name="trigger">
        <span class="win-dropdown-default-trigger">
          {{ label }}
          <svg class="win-dropdown-arrow" :class="{ 'is-open': isOpen }" viewBox="0 0 1024 1024" width="12" height="12">
            <path fill="currentColor" d="M512 714.667c-17.067 0-32-6.4-44.8-19.2L147.2 375.467c-25.6-25.6-25.6-64 0-89.6s64-25.6 89.6 0L512 561.067l275.2-275.2c25.6-25.6 64-25.6 89.6 0s25.6 64 0 89.6L556.8 695.467c-12.8 12.8-27.733 19.2-44.8 19.2z"/>
          </svg>
        </span>
      </slot>
    </div>
    <Teleport to="body">
      <Transition name="win-dropdown-fade">
        <div 
          v-if="isOpen" 
          class="win-dropdown-menu"
          :style="menuStyle"
          ref="menuRef"
        >
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
          <div v-if="!items.length" class="win-dropdown-empty">
            暂无数据
          </div>
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

const handleSelect = (item) => {
  if (item.disabled) return
  emit('update:modelValue', item.value)
  emit('select', item)
  emit('change', item)
  isOpen.value = false
}

const updatePosition = () => {
  if (!triggerRef.value || !isOpen.value) return
  
  const rect = triggerRef.value.getBoundingClientRect()
  const viewportHeight = window.innerHeight
  const menuHeight = 200
  
  let top = rect.bottom + 4
  
  if (rect.bottom + menuHeight > viewportHeight) {
    top = rect.top - menuHeight - 4
  }
  
  menuStyle.value = {
    position: 'fixed',
    left: `${rect.left}px`,
    top: `${top}px`,
    minWidth: `${Math.max(rect.width, 160)}px`,
    zIndex: 2000
  }
}

const handleClickOutside = (e) => {
  if (triggerRef.value && !triggerRef.value.contains(e.target)) {
    if (menuRef.value && !menuRef.value.contains(e.target)) {
      isOpen.value = false
    }
  }
}

watch(isOpen, (val) => {
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
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 14px;
  color: var(--text-primary);
  transition: all var(--transition-fast);
}

.win-dropdown-default-trigger:hover {
  background: var(--primary-bg);
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.win-dropdown-arrow {
  transition: transform var(--transition-fast);
}

.win-dropdown-arrow.is-open {
  transform: rotate(180deg);
}

.win-dropdown-menu {
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-md);
  padding: 4px;
  max-height: 280px;
  overflow-y: auto;
}

.win-dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: var(--radius-xs);
  font-size: 14px;
  color: var(--text-primary);
  cursor: pointer;
  transition: all var(--transition-fast);
  position: relative;
}

.win-dropdown-item:hover {
  background: var(--primary-bg);
  color: var(--primary-color);
}

.win-dropdown-item.is-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.win-dropdown-item.is-disabled:hover {
  background: transparent;
  color: var(--text-primary);
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
  padding: 16px;
  text-align: center;
  color: var(--text-tertiary);
  font-size: 14px;
}

.win-dropdown-fade-enter-active,
.win-dropdown-fade-leave-active {
  transition: all 0.15s ease;
}

.win-dropdown-fade-enter-from,
.win-dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>

<style>
.win-dropdown-menu {
  position: fixed;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-md);
  padding: 4px;
  max-height: 280px;
  overflow-y: auto;
  z-index: 2000;
}

.win-dropdown-menu .win-dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: var(--radius-xs);
  font-size: 14px;
  color: var(--text-primary);
  cursor: pointer;
  transition: all var(--transition-fast);
  position: relative;
}

.win-dropdown-menu .win-dropdown-item:hover {
  background: var(--primary-bg);
  color: var(--primary-color);
}

.win-dropdown-menu .win-dropdown-item.is-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.win-dropdown-menu .win-dropdown-item.is-disabled:hover {
  background: transparent;
  color: var(--text-primary);
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
  padding: 16px;
  text-align: center;
  color: var(--text-tertiary);
  font-size: 14px;
}
</style>
