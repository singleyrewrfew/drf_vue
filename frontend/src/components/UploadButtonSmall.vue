<template>
  <button class="upload-btn" @click="$emit('click')" :disabled="disabled">
    <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <polyline points="17 8 12 3 7 8" />
      <line x1="12" y1="3" x2="12" y2="15" />
    </svg>
    <span class="upload-text"><slot>{{ text }}</slot></span>
  </button>
</template>

<script setup>
defineEmits(['click'])
defineProps({
  text: {
    type: String,
    default: '上传'
  },
  disabled: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.upload-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid #667eea;
  border-radius: 8px;
  background: transparent;
  color: #667eea;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.upload-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.upload-btn:hover::before {
  opacity: 0.1;
}

.upload-btn:hover {
  color: #fff;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.upload-btn:active {
  transform: scale(0.98);
}

.upload-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.upload-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

.upload-btn:hover .upload-icon {
  transform: translateY(-2px);
}

.upload-text {
  position: relative;
  z-index: 1;
}
</style>
