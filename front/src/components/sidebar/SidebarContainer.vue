<template>
  <div class="sidebar-container">
    <div class="sidebar-title">
      <span class="title-seal"></span>
      <span class="title-text">{{ title }}</span>
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
  background: var(--paper-cream, #ede8dc);
  border-radius: var(--radius-sm);
  padding: 20px;
  border: 1px solid var(--paper-aged, #ddd6c8);
  transition: all var(--transition-normal);
  position: relative;
  box-shadow:
    0 2px 4px rgba(26, 26, 26, 0.04),
    0 4px 8px rgba(26, 26, 26, 0.02);
}

.sidebar-container:hover {
  border-color: var(--ink-medium, #595959);
  box-shadow:
    0 4px 8px rgba(26, 26, 26, 0.08),
    0 8px 16px rgba(26, 26, 26, 0.04);
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 700;
  color: var(--ink-black, #1a1a1a);
  margin-bottom: 18px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--paper-aged, #ddd6c8);
  position: relative;
  font-family: "Noto Serif SC", "Source Han Serif SC", "SimSun", "Georgia", serif;
  letter-spacing: var(--tracking-wide, 0.1em);
}

.title-seal {
  width: 14px;
  height: 14px;
  background: var(--vermilion-color, #c53d43);
  border-radius: 2px;
  flex-shrink: 0;
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.25),
    1px 1px 3px rgba(197, 61, 67, 0.3);
}

.title-text {
  flex: 1;
}

.sidebar-content {
  min-height: 0;
}

[data-theme='dark'] .sidebar-container {
  background: var(--card-bg, #1a1814);
  border-color: var(--border-color, #3d3830);
}

[data-theme='dark'] .sidebar-container:hover {
  border-color: #5c5649;
}

[data-theme='dark'] .sidebar-title {
  color: var(--text-primary, #e8e4d9);
  border-bottom-color: var(--border-color, #3d3830);
}

@media (max-width: 768px) {
  .sidebar-container {
    padding: 16px;
  }

  .sidebar-title {
    font-size: 15px;
    margin-bottom: 14px;
    padding-bottom: 10px;
  }
}
</style>
