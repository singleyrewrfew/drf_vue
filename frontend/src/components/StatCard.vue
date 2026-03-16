<template>
  <div class="stat-card" :class="[`stat-card-${type}`]">
    <div class="stat-card-content">
      <div class="stat-icon">
        <slot name="icon"></slot>
      </div>
      <div class="stat-info">
        <span class="stat-value">{{ value }}</span>
        <span class="stat-label">{{ label }}</span>
      </div>
    </div>
    <div class="stat-footer" v-if="footer">
      <slot name="footer">{{ footer }}</slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  value: {
    type: [String, Number],
    required: true
  },
  label: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'primary',
    validator: (v) => ['primary', 'success', 'warning', 'danger', 'info'].includes(v)
  },
  footer: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.stat-card {
  position: relative;
  padding: 16px;
  border-radius: var(--radius-md);
  background: var(--card-bg);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.15s ease;
  border: 1px solid var(--border-color);
}

.stat-card:hover {
  border-color: var(--primary-color);
  box-shadow: var(--shadow-sm);
}

.stat-card-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--icon-bg);
  color: var(--icon-color);
  flex-shrink: 0;
}

.stat-icon :deep(.el-icon) {
  font-size: 22px;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.2;
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 400;
}

.stat-footer {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--border-light);
  font-size: 12px;
  color: var(--text-tertiary);
}

.stat-card-primary {
  --icon-bg: var(--primary-bg);
  --icon-color: var(--primary-color);
}

.stat-card-success {
  --icon-bg: var(--success-bg);
  --icon-color: var(--success-color);
}

.stat-card-warning {
  --icon-bg: var(--warning-bg);
  --icon-color: var(--warning-color);
}

.stat-card-danger {
  --icon-bg: var(--danger-bg);
  --icon-color: var(--danger-color);
}

.stat-card-info {
  --icon-bg: var(--info-bg);
  --icon-color: var(--info-color);
}
</style>
