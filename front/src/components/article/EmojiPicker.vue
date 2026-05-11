<template>
  <div class="emoji-picker-wrapper" ref="pickerRef">
    <button
      type="button"
      class="emoji-trigger"
      :class="{ active: visible }"
      @click.stop="toggle"
    >
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
        <line x1="9" y1="9" x2="9.01" y2="9"/>
        <line x1="15" y1="9" x2="15.01" y2="9"/>
      </svg>
    </button>

    <Teleport to="body">
      <Transition name="emoji-fade">
        <div
          v-if="visible"
          class="emoji-dropdown"
          :style="dropdownStyle"
          ref="dropdownRef"
          @click.stop
        >
          <div class="emoji-grid">
            <span
              v-for="(emoji, index) in emojis"
              :key="index"
              class="emoji-cell"
              @click="select(emoji)"
            >
              {{ emoji }}
            </span>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  emojis: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['select'])

const pickerRef = ref(null)
const dropdownRef = ref(null)
const visible = ref(false)
const position = ref({ top: 0, left: 0 })

const dropdownStyle = computed(() => ({
  top: `${position.value.top}px`,
  left: `${position.value.left}px`
}))

const toggle = () => {
  if (visible.value) {
    close()
  } else {
    open()
  }
}

const open = () => {
  updatePosition()
  visible.value = true
  document.addEventListener('click', handleClickOutside)
}

const close = () => {
  visible.value = false
  document.removeEventListener('click', handleClickOutside)
}

const updatePosition = () => {
  if (!pickerRef.value) return
  const rect = pickerRef.value.getBoundingClientRect()
  position.value = {
    top: rect.bottom + window.scrollY + 6,
    left: rect.left + window.scrollX - 80
  }
}

const handleClickOutside = e => {
  if (
    pickerRef.value &&
    !pickerRef.value.contains(e.target) &&
    dropdownRef.value &&
    !dropdownRef.value.contains(e.target)
  ) {
    close()
  }
}

const select = emoji => {
  emit('select', emoji)
  close()
}

onBeforeUnmount(() => {
  close()
})
</script>

<style scoped>
.emoji-picker-wrapper {
  position: relative;
  display: inline-flex;
}

.emoji-trigger {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 28px;
  color: var(--text-placeholder);
  cursor: pointer;
  border: none;
  border-radius: var(--radius-sm);
  background: transparent;
  transition: all 0.15s ease;
}

.emoji-trigger:hover,
.emoji-trigger.active {
  color: var(--primary-color);
  background: var(--primary-bg, rgba(45, 90, 74, 0.08));
}

.emoji-dropdown {
  position: absolute;
  z-index: 2100;
  width: 200px;
  padding: 10px;
  background: var(--card-bg, #fff);
  border: 1px solid var(--border-color, rgba(0,0,0,0.08));
  border-radius: var(--radius-md);
  box-shadow: 0 10px 30px rgba(0,0,0,0.12), 0 3px 10px rgba(0,0,0,0.08);
}

.emoji-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  justify-content: center;
}

.emoji-cell {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  font-size: 20px;
  cursor: pointer;
  border-radius: var(--radius-sm);
  transition: all 0.12s ease;
}

.emoji-cell:hover {
  background: var(--primary-bg, rgba(45, 90, 74, 0.1));
  transform: scale(1.15);
}

/* 暗色模式 */
[data-theme='dark'] .emoji-dropdown {
  background: var(--bg-tertiary, #252219);
  border-color: var(--border-dark, #3d3830);
  box-shadow: 0 10px 30px rgba(0,0,0,0.4), 0 3px 10px rgba(0,0,0,0.25);
}

[data-theme='dark'] .emoji-trigger:hover,
[data-theme='dark'] .emoji-trigger.active {
  color: #5db396;
  background: rgba(93, 179, 150, 0.1);
}

[data-theme='dark'] .emoji-cell:hover {
  background: rgba(93, 179, 150, 0.12);
}

/* 过渡动画 */
.emoji-fade-enter-active {
  transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
}
.emoji-fade-leave-active {
  transition: all 0.12s ease-in;
}
.emoji-fade-enter-from {
  opacity: 0;
  transform: translateY(-6px) scale(0.96);
}
.emoji-fade-leave-to {
  opacity: 0;
  transform: translateY(-4px) scale(0.98);
}
</style>
