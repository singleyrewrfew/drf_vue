<template>
  <button type="button" class="search-btn" @click.stop="$emit('click')" :disabled="disabled">
    <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <circle cx="11" cy="11" r="8" />
      <line x1="21" y1="21" x2="16.65" y2="16.65" />
    </svg>
    <span class="search-text">{{ text }}</span>
  </button>
</template>

<script setup>
defineEmits(['click'])
defineProps({
  text: {
    type: String,
    default: '搜索'
  },
  disabled: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.search-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.35);
  position: relative;
  overflow: hidden;
  user-select: none;
}

.search-btn::before {
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

.search-btn:hover::before {
  left: 100%;
}

.search-btn:hover {
  filter: brightness(1.1);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.45);
}

.search-btn:active {
  filter: brightness(0.95);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.35);
}

.search-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
}

.search-icon {
  width: 14px;
  height: 14px;
  transition: transform 0.3s ease;
}

.search-btn:hover .search-icon {
  transform: scale(1.1);
}

.search-text {
  position: relative;
  z-index: 1;
}
</style>
