<template>
  <button class="create-btn" @click="$emit('click')" :disabled="disabled">
    <svg class="create-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <line x1="12" y1="5" x2="12" y2="19" />
      <line x1="5" y1="12" x2="19" y2="12" />
    </svg>
    <span class="create-text">{{ text }}</span>
  </button>
</template>

<script setup>
defineEmits(['click'])
defineProps({
  text: {
    type: String,
    default: '新建'
  },
  disabled: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.create-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.35);
  position: relative;
  overflow: hidden;
  user-select: none;
}

.create-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transition: left 0.6s ease;
}

.create-btn:hover::before {
  left: 100%;
}

.create-btn:hover {
  filter: brightness(1.1);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.45);
}

.create-btn:active {
  filter: brightness(0.95);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.35);
}

.create-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
}

.create-icon {
  width: 14px;
  height: 14px;
  transition: transform 0.3s ease;
}

.create-btn:hover .create-icon {
  transform: rotate(90deg);
}

.create-text {
  position: relative;
  z-index: 1;
}
</style>
