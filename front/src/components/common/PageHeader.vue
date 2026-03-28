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
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
}

.page-header h1 {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 26px;
  color: var(--text-primary);
  margin-bottom: 8px;
  font-weight: 700;
}

.page-header h1 .el-icon {
  color: var(--primary-color);
  font-size: 28px;
}

.page-header p {
  color: var(--text-secondary);
  font-size: 14px;
}

.page-header .count {
  color: var(--primary-color);
  font-weight: 600;
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
</style>
