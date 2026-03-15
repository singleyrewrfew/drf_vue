<template>
  <button class="edit-btn" @click="$emit('click')" :disabled="disabled">
    <svg class="edit-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
    </svg>
    <span class="edit-text">编辑</span>
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
.edit-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border: none;
  border-radius: 6px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 6px rgba(102, 126, 234, 0.35);
  position: relative;
  overflow: hidden;
  vertical-align: middle;
}

.edit-btn::before {
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

.edit-btn:hover::before {
  left: 100%;
}

.edit-btn:hover {
  filter: brightness(1.1);
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.5);
}

.edit-btn:active {
  filter: brightness(0.95);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.35);
}

.edit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.edit-icon {
  width: 12px;
  height: 12px;
  transition: transform 0.3s ease;
}

.edit-btn:hover .edit-icon {
  transform: rotate(-15deg) scale(1.1);
}

.edit-text {
  position: relative;
  z-index: 1;
}
</style>
