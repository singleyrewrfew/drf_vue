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

.publish-btn::before {
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

.publish-btn:hover::before {
  left: 100%;
}

.publish-btn:hover {
  filter: brightness(1.1);
  box-shadow: 0 4px 16px rgba(86, 171, 47, 0.5);
}

.publish-btn:active {
  filter: brightness(0.95);
  box-shadow: 0 2px 6px rgba(86, 171, 47, 0.35);
}

.publish-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
}

.publish-icon {
  width: 12px;
  height: 12px;
  transition: transform 0.3s ease;
}

.publish-btn:hover .publish-icon {
  transform: translateX(2px);
}

.publish-text {
  position: relative;
  z-index: 1;
}
</style>
