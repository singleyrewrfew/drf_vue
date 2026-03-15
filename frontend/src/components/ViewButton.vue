<template>
  <button class="view-btn" @click="$emit('click')" :disabled="disabled">
    <svg class="view-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
      <circle cx="12" cy="12" r="3" />
    </svg>
    <span class="view-text">查看</span>
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
.view-btn {
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

.view-btn::before {
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

.view-btn:hover::before {
  left: 100%;
}

.view-btn:hover {
  filter: brightness(1.1);
  box-shadow: 0 4px 16px rgba(0, 198, 251, 0.5);
}

.view-btn:active {
  filter: brightness(0.95);
  box-shadow: 0 2px 8px rgba(0, 198, 251, 0.35);
}

.view-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.view-icon {
  width: 12px;
  height: 12px;
  transition: transform 0.3s ease;
}

.view-btn:hover .view-icon {
  transform: scale(1.15);
}

.view-text {
  position: relative;
  z-index: 1;
}
</style>
