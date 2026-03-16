<template>
  <button class="reset-btn" @click="$emit('click')" :disabled="disabled">
    <svg class="reset-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
      <path d="M3 3v5h5" />
    </svg>
    <span class="reset-text">{{ text }}</span>
  </button>
</template>

<script setup>
defineEmits(['click'])
defineProps({
  text: {
    type: String,
    default: '重置'
  },
  disabled: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.reset-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  background: var(--card-bg);
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
  user-select: none;
  position: relative;
  z-index: 1;
}

.reset-btn:hover {
  background: var(--bg-secondary);
  border-color: var(--border-dark);
}

.reset-btn:active {
  background: var(--bg-tertiary);
}

.reset-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.reset-icon {
  width: 14px;
  height: 14px;
}
</style>
