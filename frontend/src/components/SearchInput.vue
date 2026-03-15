<template>
  <div class="search-input-wrapper">
    <div class="search-input-container" :class="{ focused: isFocused }">
      <div class="search-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
      </div>
      <input
        ref="inputRef"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        class="search-input"
        @input="$emit('update:modelValue', $event.target.value)"
        @focus="handleFocus"
        @blur="handleBlur"
        @keyup.enter="$emit('search')"
      />
      <div class="search-border"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineEmits(['update:modelValue', 'search'])
defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '搜索...'
  },
  type: {
    type: String,
    default: 'text'
  }
})

const inputRef = ref(null)
const isFocused = ref(false)

const handleFocus = () => {
  isFocused.value = true
}

const handleBlur = () => {
  isFocused.value = false
}
</script>

<style scoped>
.search-input-wrapper {
  position: relative;
}

.search-input-container {
  position: relative;
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #dcdfe6;
}

.search-input-container:hover {
  border-color: #c0c4cc;
}

.search-input-container.focused {
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.search-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.search-icon svg {
  width: 14px;
  height: 14px;
}

.search-input-container.focused .search-icon {
  color: #667eea;
}

.search-input {
  flex: 1;
  height: 32px;
  border: none;
  outline: none;
  font-size: 14px;
  color: #303133;
  background: transparent;
  padding-right: 12px;
}

.search-input::placeholder {
  color: #c0c4cc;
}

.search-border {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.search-input-container.focused .search-border {
  transform: scaleX(1);
}
</style>
