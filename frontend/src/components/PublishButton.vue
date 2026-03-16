<template>
  <button class="publish-btn" @click="$emit('click')" :disabled="disabled">
    <svg class="publish-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M22 2L11 13" />
      <path d="M22 2L15 22L11 13L2 9L22 2Z" />
    </svg>
    <span class="publish-text">发布</span>
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
.publish-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border: none;
  border-radius: var(--radius-xs);
  background: var(--success-color);
  color: #fff;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
  vertical-align: middle;
  position: relative;
  z-index: 1;
}

.publish-btn:hover {
  background: var(--success-hover);
}

.publish-btn:active {
  filter: brightness(0.95);
}

.publish-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.publish-icon {
  width: 12px;
  height: 12px;
}
</style>
