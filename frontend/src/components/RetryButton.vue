<template>
  <button class="retry-btn" @click="$emit('click')" :disabled="disabled">
    <svg class="retry-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <polyline points="23 4 23 10 17 10" />
      <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10" />
    </svg>
    <span class="retry-text">重试</span>
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
.retry-btn {
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

.retry-btn::before {
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

.retry-btn:hover::before {
  left: 100%;
}

.retry-btn:hover {
  filter: brightness(1.1);
  box-shadow: 0 4px 16px rgba(240, 147, 251, 0.5);
}

.retry-btn:active {
  filter: brightness(0.95);
  box-shadow: 0 2px 6px rgba(240, 147, 251, 0.35);
}

.retry-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
}

.retry-icon {
  width: 12px;
  height: 12px;
  transition: transform 0.3s ease;
}

.retry-btn:hover .retry-icon {
  transform: rotate(-30deg);
}

.retry-text {
  position: relative;
  z-index: 1;
}
</style>
