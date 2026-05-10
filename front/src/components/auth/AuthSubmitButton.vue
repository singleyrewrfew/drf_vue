<template>
  <button
    type="button"
    class="auth-submit-btn"
    :class="{ 'is-disabled': disabled, 'is-loading': loading }"
    :disabled="disabled"
    @click="$emit('click')"
  >
    <span v-if="!loading">{{ text }}</span>
    <span v-else>{{ loadingText }}</span>
  </button>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    default: '提交'
  },
  loadingText: {
    type: String,
    default: '提交中...'
  },
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

defineEmits(['click'])
</script>

<style scoped>
.auth-submit-btn {
  width: 100%;
  height: 40px;
  font-size: 14px;
  font-weight: 600;
  border-radius: var(--radius-xs);
  letter-spacing: var(--tracking-wide, 0.1em);
  background: var(--vermilion-color, #c53d43);
  border: none;
  color: #fff;
  font-family: "KaiTi", "STKaiti", "楷体", serif;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.15),
    1px 1px 6px rgba(197, 61, 67, 0.3);
}

.auth-submit-btn:hover:not(:disabled) {
  background: var(--vermilion-hover, #a02f33);
  transform: translateY(-1px);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.2),
    0 4px 12px rgba(197, 61, 67, 0.35);
}

.auth-submit-btn:active:not(:disabled) {
  transform: translateY(0) scale(0.98);
}

.auth-submit-btn.is-disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background: var(--ink-light, #8c8c8c) !important;
  box-shadow: none !important;
}

.auth-submit-btn.is-loading {
  cursor: wait;
}

/* 暗色模式适配 */
[data-theme='dark'] .auth-submit-btn {
  background: var(--dark-vermilion, #dc2626);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.1),
    1px 1px 6px rgba(220, 38, 38, 0.3);
}

[data-theme='dark'] .auth-submit-btn:hover:not(:disabled) {
  background: #b91c1c;
}

[data-theme='dark'] .auth-submit-btn.is-disabled {
  background: #3f3f46 !important;
}
</style>