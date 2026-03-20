<template>
  <button type="button" class="confirm-btn" @click.stop="$emit('click')" :disabled="disabled">
    <svg class="confirm-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <polyline points="20 6 9 17 4 12" />
    </svg>
    <span class="confirm-text">{{ text }}</span>
  </button>
</template>

<script setup>
defineEmits(['click'])
defineProps({
  text: {
    type: String,
    default: '确定'
  },
  disabled: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.confirm-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 16px;
  border: none;
  border-radius: var(--radius-sm);
  background: var(--primary-color);
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
  user-select: none;
  position: relative;
  z-index: 1;
}

.confirm-btn:hover {
  background: var(--primary-hover);
}

.confirm-btn:active {
  background: var(--primary-active);
}

.confirm-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.confirm-btn:disabled:hover {
  background: var(--primary-color);
}

.confirm-icon {
  width: 14px;
  height: 14px;
}
</style>
