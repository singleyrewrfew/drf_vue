<template>
  <button class="preview-btn" @click="$emit('click')" :disabled="disabled">
    <svg class="preview-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
      <circle cx="8.5" cy="8.5" r="1.5" />
      <polyline points="21 15 16 10 5 21" />
    </svg>
    <span class="preview-text">预览</span>
  </button>
</template>

<script setup>
defineEmits(['click'])
defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.preview-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border: none;
  border-radius: var(--radius-xs);
  background: var(--info-color);
  color: #fff;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
  vertical-align: middle;
  position: relative;
  z-index: 1;
}

.preview-btn:hover {
  filter: brightness(1.1);
}

.preview-btn:active {
  filter: brightness(0.95);
}

.preview-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.preview-icon {
  width: 12px;
  height: 12px;
}
</style>
