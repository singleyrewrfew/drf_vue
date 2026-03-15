<template>
  <button class="approve-btn" @click="$emit('click')" :disabled="disabled">
    <svg class="approve-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <polyline points="20 6 9 17 6" />
      <line x1="9" y1="12" x2="15" y2="12" />
      <line x1="9" y1="16" x2="15" y2="16" />
      <line x1="12" y1="9" x2="12" y2="15" />
    </svg>
    <span class="approve-text">审核</span>
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
.approve-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border: none;
  border-radius: 6px;
  background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
  color: #fff;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 6px rgba(86, 171, 47, 0.35);
  position: relative;
  overflow: hidden;
  vertical-align: middle;
}

.approve-btn::before {
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

.approve-btn:hover::before {
  left: 100%;
}

.approve-btn:hover {
  filter: brightness(1.1);
  box-shadow: 0 4px 16px rgba(86, 171, 47, 0.5);
}

.approve-btn:active {
  filter: brightness(0.95);
  box-shadow: 0 2px 6px rgba(86, 171, 47, 0.35);
}

.approve-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
}

.approve-icon {
  width: 12px;
  height: 12px;
  transition: transform 0.3s ease;
}

.approve-btn:hover .approve-icon {
  transform: scale(1.1);
}

.approve-text {
  position: relative;
  z-index: 1;
}
</style>
