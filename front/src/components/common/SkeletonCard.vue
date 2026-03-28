<template>
  <div :class="['skeleton-card', `skeleton-card--${mode}`]">
    <div v-if="showImage" class="skeleton-cover">
      <el-skeleton-item variant="image" style="width: 100%; height: 100%;" />
    </div>
    <div class="skeleton-info">
      <el-skeleton animated>
        <template #template>
          <el-skeleton-item variant="h3" :style="{ width: titleWidth }" />
          <el-skeleton-item v-if="showExcerpt" variant="text" style="width: 100%; margin-top: 12px;" />
          <el-skeleton-item v-if="showExcerpt" variant="text" style="width: 60%; margin-top: 8px;" />
          <div v-if="showFooter" class="skeleton-footer">
            <el-skeleton-item variant="text" style="width: 30%;" />
            <el-skeleton-item variant="text" style="width: 40%;" />
          </div>
        </template>
      </el-skeleton>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  mode: {
    type: String,
    default: 'grid',
    validator: (v) => ['grid', 'horizontal', 'list'].includes(v)
  },
  showImage: {
    type: Boolean,
    default: true
  },
  showExcerpt: {
    type: Boolean,
    default: true
  },
  showFooter: {
    type: Boolean,
    default: true
  },
  titleWidth: {
    type: String,
    default: '80%'
  }
})
</script>

<style scoped>
.skeleton-card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 1px solid var(--border-light);
}

.skeleton-card--grid {
  display: block;
}

.skeleton-card--horizontal {
  display: flex;
  gap: 24px;
  padding: 24px;
}

.skeleton-card--list {
  display: flex;
  flex-direction: column;
}

.skeleton-cover {
  overflow: hidden;
}

.skeleton-card--grid .skeleton-cover {
  height: 200px;
}

.skeleton-card--horizontal .skeleton-cover {
  width: 220px;
  height: 140px;
  flex-shrink: 0;
  border-radius: var(--radius-md);
}

.skeleton-card--list .skeleton-cover {
  height: 180px;
}

.skeleton-info {
  flex: 1;
}

.skeleton-card--grid .skeleton-info {
  padding: 20px;
}

.skeleton-card--horizontal .skeleton-info {
  padding: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.skeleton-card--list .skeleton-info {
  padding: 16px;
}

.skeleton-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid var(--border-light);
}

.skeleton-card--horizontal .skeleton-footer {
  border-top: none;
  padding-top: 0;
  margin-top: 12px;
  gap: 16px;
}

@media (max-width: 768px) {
  .skeleton-card--horizontal {
    flex-direction: column;
    padding: 16px;
    gap: 16px;
  }

  .skeleton-card--horizontal .skeleton-cover {
    width: 100%;
    height: 180px;
  }
}

@media (max-width: 576px) {
  .skeleton-card--grid .skeleton-cover {
    height: 140px;
  }

  .skeleton-card--horizontal .skeleton-cover {
    height: 160px;
  }

  .skeleton-info {
    padding: 12px;
  }
}
</style>
