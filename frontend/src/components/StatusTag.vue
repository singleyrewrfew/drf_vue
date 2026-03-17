<template>
  <span class="status-tag" :class="[`status-tag--${type}`, { 'status-tag--dot': showDot }]">
    <span v-if="showDot" class="status-dot"></span>
    <slot>{{ text }}</slot>
  </span>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'primary', 'success', 'warning', 'danger', 'info'].includes(value)
  },
  text: {
    type: String,
    default: ''
  },
  showDot: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.status-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  line-height: 1.5;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-tag--default {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}

.status-tag--default .status-dot {
  background: var(--text-tertiary);
}

.status-tag--primary {
  background: var(--primary-bg);
  color: var(--primary-color);
}

.status-tag--primary .status-dot {
  background: var(--primary-color);
}

.status-tag--success {
  background: var(--success-bg);
  color: var(--success-color);
}

.status-tag--success .status-dot {
  background: var(--success-color);
}

.status-tag--warning {
  background: var(--warning-bg);
  color: var(--warning-color);
}

.status-tag--warning .status-dot {
  background: var(--warning-color);
}

.status-tag--danger {
  background: var(--danger-bg);
  color: var(--danger-color);
}

.status-tag--danger .status-dot {
  background: var(--danger-color);
}

.status-tag--info {
  background: var(--info-bg);
  color: var(--info-color);
}

.status-tag--info .status-dot {
  background: var(--info-color);
}
</style>
