<template>
  <div class="quick-action-card" @click="$emit('click')">
    <div class="action-icon-wrapper">
      <div class="action-icon-bg" :class="type"></div>
      <el-icon :size="24" class="action-icon">
        <slot></slot>
      </el-icon>
    </div>
    <div class="action-content">
      <span class="action-title">{{ title }}</span>
      <span class="action-desc" v-if="description">{{ description }}</span>
    </div>
    <div class="action-arrow">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="5" y1="12" x2="19" y2="12" />
        <polyline points="12 5 19 12 12 19" />
      </svg>
    </div>
  </div>
</template>

<script setup>
defineEmits(['click'])
defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'primary',
    validator: (v) => ['primary', 'success', 'warning', 'danger', 'info'].includes(v)
  }
})
</script>

<style scoped>
.quick-action-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #fff;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #f0f0f0;
  position: relative;
  overflow: hidden;
}

.quick-action-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, var(--hover-color) 0%, transparent 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.quick-action-card:hover::before {
  opacity: 0.05;
}

.quick-action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  border-color: var(--border-color);
}

.quick-action-card:active {
  transform: translateY(0);
}

.action-icon-wrapper {
  position: relative;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.action-icon-bg {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 12px;
  opacity: 0.15;
  transition: opacity 0.3s ease;
}

.quick-action-card:hover .action-icon-bg {
  opacity: 0.25;
}

.action-icon-bg.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.action-icon-bg.success {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.action-icon-bg.warning {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.action-icon-bg.danger {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
}

.action-icon-bg.info {
  background: linear-gradient(135deg, #00c6fb 0%, #005bea 100%);
}

.action-icon {
  position: relative;
  z-index: 1;
  color: var(--icon-color);
  transition: transform 0.3s ease;
}

.quick-action-card:hover .action-icon {
  transform: scale(1.1);
}

.action-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.action-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.action-desc {
  font-size: 12px;
  color: #909399;
}

.action-arrow {
  width: 24px;
  height: 24px;
  color: #c0c4cc;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.quick-action-card:hover .action-arrow {
  color: var(--icon-color);
  transform: translateX(4px);
}

.action-arrow svg {
  width: 100%;
  height: 100%;
}

/* 颜色变量 */
.quick-action-card {
  --icon-color: #667eea;
  --border-color: rgba(102, 126, 234, 0.3);
  --hover-color: #667eea;
}

.quick-action-card.success {
  --icon-color: #11998e;
  --border-color: rgba(17, 153, 142, 0.3);
  --hover-color: #11998e;
}

.quick-action-card.warning {
  --icon-color: #f5576c;
  --border-color: rgba(245, 87, 108, 0.3);
  --hover-color: #f5576c;
}

.quick-action-card.danger {
  --icon-color: #ff6b6b;
  --border-color: rgba(255, 107, 107, 0.3);
  --hover-color: #ff6b6b;
}

.quick-action-card.info {
  --icon-color: #005bea;
  --border-color: rgba(0, 91, 234, 0.3);
  --hover-color: #005bea;
}
</style>
