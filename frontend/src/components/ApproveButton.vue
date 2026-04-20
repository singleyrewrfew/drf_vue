<template>
  <button class="approve-btn" @click="$emit('click')" :disabled="disabled">
    <svg class="approve-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <polyline points="20 6 9 17 4"/>
    </svg>
    <span class="approve-text">审核</span>
  </button>
</template>

<script setup>
// 接收父组件传过来的方法
defineEmits(['click'])
// 接收父组件传过来的数据
defineProps({
  // 我要接收一个叫 disabled 的属性
  disabled: {
    type: Boolean,   // 类型：必须是布尔值（true 或 false）
    default: false  // 默认值：如果父组件没传，就是 false
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
  border-radius: var(--radius-xs);
  background: var(--success-color);
  color: #fff;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
  vertical-align: middle;
  position: relative;
  z-index: 1;
}

.approve-btn:hover {
  background: var(--success-hover);
}

.approve-btn:active {
  filter: brightness(0.95);
}

.approve-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.approve-icon {
  width: 12px;
  height: 12px;
}
</style>
