<template>
  <button class="delete-btn" @click="$emit('click')" :disabled="disabled">
    <svg class="delete-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <polyline points="3 6 5 6 21 6" />
      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
      <line x1="10" y1="11" x2="10" y2="17" />
      <line x1="14" y1="11" x2="14" y2="17" />
    </svg>
    <span class="delete-text">删除</span>
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
.delete-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border: none;
  border-radius: 6px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
  color: #fff;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 6px rgba(255, 107, 107, 0.35);
  position: relative;
  overflow: hidden;
  vertical-align: middle;
}

.delete-btn::before {
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

.delete-btn:hover::before {
  left: 100%;
}

.delete-btn:hover {
  filter: brightness(1.1);
  box-shadow: 0 4px 16px rgba(255, 107, 107, 0.5);
}

.delete-btn:active {
  filter: brightness(0.95);
  box-shadow: 0 2px 6px rgba(255, 107, 107, 0.35);
}

.delete-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
}

.delete-icon {
  width: 12px;
  height: 12px;
  transition: transform 0.3s ease;
}

.delete-btn:hover .delete-icon {
  transform: scale(1.1);
}

.delete-text {
  position: relative;
  z-index: 1;
}
</style>
