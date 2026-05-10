<template>
  <div class="page-header">
    <h1>
      <el-icon v-if="icon">
        <component :is="icon" />
      </el-icon>
      <span v-html="title"></span>
    </h1>
    <p v-if="subtitle || showCount">
      {{ subtitle }}
      <template v-if="showCount">
        共 <span class="count">{{ count }}</span> {{ countLabel }}
      </template>
    </p>
    <slot></slot>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
  count: {
    type: Number,
    default: 0
  },
  countLabel: {
    type: String,
    default: '篇文章'
  },
  showCount: {
    type: Boolean,
    default: true
  },
  icon: {
    type: [String, Object],
    default: null
  }
})
</script>

<style scoped>
.page-header {
  margin-bottom: 32px;
  padding: 24px 28px;
  background: var(--paper-cream, #ede8dc);
  border-radius: var(--radius-sm, 4px);
  border: 1.5px solid var(--paper-aged, #ddd6c8);
}

.page-header h1 {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 26px;
  color: var(--ink-dark, #1a1a1a);
  margin-bottom: 10px;
  font-weight: 700;
  font-family: "Noto Serif SC", "SimSun", serif;
  letter-spacing: 0.05em;
}

.page-header h1 .el-icon {
  color: var(--vermilion-color, #c53d43);
  font-size: 28px;
}

.page-header p {
  color: var(--ink-medium, #595959);
  font-size: 14px;
  font-family: "KaiTi", "STKaiti", serif;
  letter-spacing: 0.03em;
}

.page-header .count {
  color: var(--vermilion-color, #c53d43);
  font-weight: 600;
  font-size: 16px;
}

@media (max-width: 768px) {
  .page-header {
    padding: 20px;
    margin-bottom: 20px;
  }

  .page-header h1 {
    font-size: 22px;
  }
}

@media (max-width: 576px) {
  .page-header {
    padding: 16px;
  }

  .page-header h1 {
    font-size: 20px;
  }
}

/* ====== 暗色模式适配 ====== */

[data-theme='dark'] .page-header {
  background: #27272a;
  border-color: #3f3f46;
}

[data-theme='dark'] .page-header h1 {
  color: #e4e4e7;
}

[data-theme='dark'] .page-header h1 .el-icon {
  color: #ef4444;
}

[data-theme='dark'] .page-header p {
  color: #a1a1aa;
}

[data-theme='dark'] .page-header .count {
  color: #ef4444;
}
</style>
