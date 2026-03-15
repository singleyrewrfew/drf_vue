<template>
  <div class="stat-card" :class="[`stat-card-${type}`]">
    <div class="stat-card-glow"></div>
    <div class="stat-card-content">
      <div class="stat-icon-wrapper">
        <div class="stat-icon">
          <slot name="icon"></slot>
        </div>
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
  padding: 24px;
  border-radius: 16px;
  background: #fff;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--gradient);
  border-radius: 16px 16px 0 0;
}

.stat-card-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, var(--glow-color) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.stat-card:hover .stat-card-glow {
  opacity: 0.15;
}

.stat-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.stat-card-content {
  display: flex;
  align-items: center;
  gap: 20px;
  position: relative;
  z-index: 1;
}

.stat-icon-wrapper {
  position: relative;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient);
  color: #fff;
  font-size: 28px;
  transition: transform 0.3s ease;
  box-shadow: 0 8px 20px var(--shadow-color);
}

.stat-card:hover .stat-icon {
  transform: scale(1.1) rotate(5deg);
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #1a1a2e;
  line-height: 1;
  transition: color 0.3s ease;
}

.stat-card:hover .stat-value {
  color: var(--text-color);
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.stat-footer {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
  font-size: 13px;
  color: #9ca3af;
  position: relative;
  z-index: 1;
}

/* Primary - Blue */
.stat-card-primary {
  --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --glow-color: rgba(102, 126, 234, 0.4);
  --shadow-color: rgba(102, 126, 234, 0.35);
  --text-color: #667eea;
}

/* Success - Green */
.stat-card-success {
  --gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  --glow-color: rgba(17, 153, 142, 0.4);
  --shadow-color: rgba(17, 153, 142, 0.35);
  --text-color: #11998e;
}

/* Warning - Orange */
.stat-card-warning {
  --gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  --glow-color: rgba(240, 147, 251, 0.4);
  --shadow-color: rgba(240, 147, 251, 0.35);
  --text-color: #f5576c;
}

/* Danger - Red */
.stat-card-danger {
  --gradient: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
  --glow-color: rgba(255, 107, 107, 0.4);
  --shadow-color: rgba(255, 107, 107, 0.35);
  --text-color: #ff6b6b;
}

/* Info - Cyan */
.stat-card-info {
  --gradient: linear-gradient(135deg, #00c6fb 0%, #005bea 100%);
  --glow-color: rgba(0, 198, 251, 0.4);
  --shadow-color: rgba(0, 198, 251, 0.35);
  --text-color: #005bea;
}
</style>
