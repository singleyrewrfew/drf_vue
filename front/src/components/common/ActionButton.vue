<template>
  <button
    class="action-btn"
    :class="[variantClass, { 'dynamic-icon-btn': isDynamicIcon }]"
    :title="title"
    :disabled="disabled"
    @click="$emit('click', $event)"
  >
    <component v-if="iconComponent" :is="iconComponent" />
    <svg
      v-else-if="icon"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      :stroke-width="strokeWidth"
      :class="{ 'dynamic-icon': isDynamicIcon }"
    >
      <g v-if="isDynamicIcon" v-html="icon"></g>
      <path v-else :d="icon"/>
    </svg>
    <span v-if="label" class="btn-label">{{ label }}</span>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'default'
  },
  title: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  icon: {
    type: String,
    default: ''
  },
  iconComponent: {
    type: [Object, Function],
    default: null
  },
  disabled: {
    type: Boolean,
    default: false
  },
  strokeWidth: {
    type: [String, Number],
    default: 2.5
  }
})

defineEmits(['click'])

const variantClass = computed(() => {
  const map = {
    default: '',
    scrollTop: 'scroll-top',
    scrollBottom: 'scroll-bottom',
    immersive: 'immersive-btn',
    toc: 'action-toc'
  }
  return map[props.variant] || props.variant
})

const isDynamicIcon = computed(() => {
  return props.icon && (props.icon.includes('<') || props.icon.includes('line') || props.icon.includes('path'))
})
</script>

<style scoped>
.action-btn {
  width: 42px;
  height: 42px;
  padding: 0;
  margin: 0;
  border-radius: var(--radius-xs, 2px);
  background: var(--paper-cream, #ede8dc);
  border: 1.5px solid var(--paper-aged, #ddd6c8);
  color: var(--ink-medium, #595959);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.5),
    1px 1px 4px rgba(26, 26, 26, 0.08);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn:hover:not(:disabled) {
  background: var(--vermilion-color, #c53d43);
  color: #fff;
  border-color: var(--vermilion-color, #c53d43);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.2),
    0 4px 12px rgba(197, 61, 67, 0.3);
  transform: translateY(-2px);
}

.action-btn:active:not(:disabled) {
  transform: scale(0.96) translateY(0);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.15),
    1px 1px 4px rgba(197, 61, 67, 0.25);
}

.action-btn svg {
  width: 20px;
  height: 20px;
  position: relative;
  z-index: 1;
  transition: transform 0.3s ease;
}

/* ====== 变体样式 ====== */

/* 滚动到顶部 - hover 时图标上移 */
.scroll-top:hover svg {
  transform: translateY(-2px);
}

/* 滚动到底部 - hover 时图标下移 */
.scroll-bottom:hover svg {
  transform: translateY(2px);
}

/* 沉浸式按钮 - 统一透明风格 */
.immersive-btn {
  background: var(--paper-cream, #ede8dc);
  color: var(--ink-medium, #595959);
  border: 1.5px solid var(--paper-aged, #ddd6c8);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.5),
    1px 1px 4px rgba(26, 26, 26, 0.08);
}

.immersive-btn:hover:not(:disabled) {
  background: var(--vermilion-color, #c53d43);
  color: #fff;
  border-color: var(--vermilion-color, #c53d43);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.2),
    0 4px 12px rgba(197, 61, 67, 0.3);
}

/* 目录按钮 - 图标微调居中 */
.action-toc .dynamic-icon {
  transform: translateX(-2.5px);
}

/* 标签悬浮提示 */
.btn-label {
  position: absolute;
  right: calc(100% + 12px);
  padding: 6px 12px;
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
  background: var(--paper-cream, #ede8dc);
  border: 1.5px solid var(--paper-aged, #ddd6c8);
  border-radius: var(--radius-xs, 2px);
  box-shadow: 1px 1px 6px rgba(26, 26, 26, 0.1);
  opacity: 0;
  visibility: hidden;
  transform: translateX(10px);
  transition: all 0.25s ease;
  pointer-events: none;
  color: var(--ink-dark, #1a1a1a);
}

.action-btn:hover:not(:disabled) .btn-label {
  opacity: 1;
  visibility: visible;
  transform: translateX(0);
}

/* ====== 暗色模式适配 ====== */
[data-theme='dark'] .action-btn {
  background: #27272a;
  border-color: #3f3f46;
  color: #a1a1aa;
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.05),
    1px 1px 4px rgba(0, 0, 0, 0.3);
}

[data-theme='dark'] .action-btn:hover:not(:disabled) {
  background: #dc2626;
  color: #fff;
  border-color: #dc2626;
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.15),
    0 4px 12px rgba(220, 38, 38, 0.4);
}

[data-theme='dark'] .immersive-btn {
  background: #27272a;
  border-color: #3f3f46;
  color: #a1a1aa;
}

[data-theme='dark'] .immersive-btn:hover:not(:disabled) {
  background: #dc2626;
  border-color: #dc2626;
}

[data-theme='dark'] .btn-label {
  background: #27272a;
  border-color: #3f3f46;
  color: #e4e4e7;
}

/* ====== 响应式设计 ====== */
@media (max-width: 768px) {
  .action-btn {
    width: 38px;
    height: 38px;
    border-radius: var(--radius-xs, 2px);
  }

  .action-btn svg {
    width: 18px;
    height: 18px;
  }

  .btn-label {
    display: none;
  }
}
</style>
