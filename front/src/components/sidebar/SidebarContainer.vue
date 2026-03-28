<template>
  <div class="sidebar-container">
    <div class="sidebar-title">
      <el-icon v-if="icon">
        <component :is="icon" />
      </el-icon>
      <span>{{ title }}</span>
    </div>
    <div class="sidebar-content">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  icon: {
    type: [String, Object],
    default: null
  }
})
</script>

<style scoped>
.sidebar-container {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 24px;
  border: 1px solid var(--border-light);
  transition: all var(--transition-fast);
}

.sidebar-container:hover {
  border-color: rgba(0, 120, 212, 0.2);
  box-shadow: var(--shadow-sm);
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 20px;
  padding-bottom: 14px;
  border-bottom: 2px solid var(--border-light);
}

.sidebar-title .el-icon {
  color: var(--primary-color);
  font-size: 20px;
}

.sidebar-content {
  min-height: 0;
}

@media (max-width: 768px) {
  .sidebar-container {
    padding: 20px;
  }

  .sidebar-title {
    font-size: 15px;
    margin-bottom: 16px;
    padding-bottom: 12px;
  }
}
</style>
