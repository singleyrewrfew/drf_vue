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
  border-radius: 10px;
  background: var(--card-bg, #fff);
  border: 1px solid var(--border-light, #e5e7eb);
  color: var(--text-secondary, #6b7280);
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.08),
    0 1px 2px rgba(0, 0, 0, 0.04);
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

.action-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: radial-gradient(circle, currentColor 0%, transparent 70%);
  transform: translate(-50%, -50%);
  transition: width 0.4s ease, height 0.4s ease;
  border-radius: 50%;
  opacity: 0;
}

.action-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, rgba(var(--primary-rgb), 0.08), rgba(var(--primary-rgb), 0.04));
  color: var(--primary-color);
  box-shadow:
    0 6px 20px rgba(var(--primary-rgb), 0.15),
    0 2px 8px rgba(var(--primary-rgb), 0.08);
  transform: translateY(-2px);
}

.action-btn:hover:not(:disabled)::before {
  width: 60px;
  height: 60px;
  opacity: 0.15;
}

.action-btn:active:not(:disabled) {
  transform: scale(0.94) translateY(0);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
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
  background: var(--card-bg, #fff);
  color: var(--text-secondary, #6b7280);
  border: none;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.08),
    0 1px 2px rgba(0, 0, 0, 0.04);
}

.immersive-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, rgba(var(--primary-rgb), 0.12), rgba(var(--primary-rgb), 0.06));
  color: var(--primary-color);
  box-shadow:
    0 8px 24px rgba(var(--primary-rgb), 0.2),
    0 4px 12px rgba(var(--primary-rgb), 0.1);
}

.immersive-btn::before {
  background: radial-gradient(circle, currentColor 0%, transparent 70%);
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
  background: var(--card-bg);
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  opacity: 0;
  visibility: hidden;
  transform: translateX(10px);
  transition: all 0.25s ease;
  pointer-events: none;
}

.action-btn:hover:not(:disabled) .btn-label {
  opacity: 1;
  visibility: visible;
  transform: translateX(0);
}

/* ====== 深色模式适配 ====== */
[data-theme='dark'] .action-btn:not(.immersive-btn) {
  background: rgba(39, 39, 42, 0.95);
  border-color: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
  box-shadow:
    0 2px 12px rgba(0, 0, 0, 0.4),
    0 1px 4px rgba(0, 0, 0, 0.2);
}

[data-theme='dark'] .action-btn:not(.immersive-btn):hover:not(:disabled) {
  background: rgba(var(--primary-rgb), 0.15);
  border-color: rgba(var(--primary-rgb), 0.4);
  box-shadow:
    0 8px 24px rgba(var(--primary-rgb), 0.2),
    0 2px 8px rgba(var(--primary-rgb), 0.1);
}

[data-theme='dark'] .btn-label {
  background: rgba(39, 39, 42, 0.98);
  color: rgba(255, 255, 255, 0.9);
}

/* ====== 响应式设计 ====== */
@media (max-width: 768px) {
  .action-btn {
    width: 38px;
    height: 38px;
    border-radius: 9px;
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
