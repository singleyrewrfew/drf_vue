<template>
  <el-button
    type="primary"
    :loading="loading"
    :disabled="disabled"
    class="auth-submit-btn"
    size="default"
    @click="$emit('click')"
  >
    <span v-if="!loading">{{ text }}</span>
    <span v-else>{{ loadingText }}</span>
  </el-button>
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
  border-radius: var(--radius-sm);
  letter-spacing: 1px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.auth-submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(var(--primary-rgb), 0.35);
}

.auth-submit-btn:active:not(:disabled) {
  transform: translateY(0) scale(0.98);
}

.auth-submit-btn.is-disabled {
  opacity: 0.6;
}
</style>
