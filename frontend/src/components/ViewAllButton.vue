<template>
  <button type="button" class="view-all-btn" @click.stop="$emit('click')" :disabled="disabled">
    <span class="view-all-text">{{ text }}</span>
    <svg class="view-all-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>
  </button>
</template>

<script setup>
defineEmits(['click'])
defineProps({
  text: {
    type: String,
    default: '查看全部'
  },
  disabled: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.view-all-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border: none;
  border-radius: 6px;
  background: linear-gradient(135deg, #00c6fb 0%, #005bea 100%);
  color: #fff;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 6px rgba(0, 198, 251, 0.35);
  position: relative;
  overflow: hidden;
  vertical-align: middle;
}

.view-all-btn::before {
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

.view-all-btn:hover::before {
  left: 100%;
}

.view-all-btn:hover {
  filter: brightness(1.1);
  box-shadow: 0 4px 16px rgba(0, 198, 251, 0.5);
}

.view-all-btn:active {
  filter: brightness(0.95);
  box-shadow: 0 2px 6px rgba(0, 198, 251, 0.35);
}

.view-all-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
}

.view-all-icon {
  width: 12px;
  height: 12px;
  transition: transform 0.3s ease;
}

.view-all-btn:hover .view-all-icon {
  transform: translateX(3px);
}

.view-all-text {
  position: relative;
  z-index: 1;
}
</style>
