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
  border-radius: 6px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: #fff;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 6px rgba(240, 147, 251, 0.35);
  position: relative;
  overflow: hidden;
  vertical-align: middle;
}

.preview-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: left 0.5s ease;
}

.preview-btn:hover::before {
  left: 100%;
}

.preview-btn:hover {
  filter: brightness(1.1);
  box-shadow: 0 4px 16px rgba(240, 147, 251, 0.5);
}

.preview-btn:active {
  filter: brightness(0.95);
  box-shadow: 0 2px 6px rgba(240, 147, 251, 0.35);
}

.preview-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
}

.preview-icon {
  width: 12px;
  height: 12px;
  transition: transform 0.3s ease;
}

.preview-btn:hover .preview-icon {
  transform: scale(1.1);
}

.preview-text {
  position: relative;
  z-index: 1;
}
</style>
