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
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: #fff;
  color: #606266;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  user-select: none;
}

.reset-btn:hover {
  color: #667eea;
  border-color: #667eea;
  background: #f5f7ff;
}

.reset-btn:active {
  background: #eef0ff;
}

.reset-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.reset-icon {
  width: 14px;
  height: 14px;
  transition: transform 0.3s ease;
}

.reset-btn:hover .reset-icon {
  transform: rotate(-30deg);
}

.reset-text {
  position: relative;
  z-index: 1;
}
</style>
