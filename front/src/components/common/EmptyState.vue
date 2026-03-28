<template>
  <div class="empty-state">
    <div class="empty-icon">
      <el-icon :size="64">
        <component :is="iconComponent" />
      </el-icon>
    </div>
    <p class="empty-text">{{ text }}</p>
    <p v-if="hint" class="empty-hint">{{ hint }}</p>
    <slot></slot>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Document, Folder, Search, ChatDotSquare, User } from '@element-plus/icons-vue'

const props = defineProps({
  icon: {
    type: [String, Object],
    default: 'document'
  },
  text: {
    type: String,
    default: '暂无数据'
  },
  hint: {
    type: String,
    default: ''
  }
})

const iconMap = {
  document: Document,
  folder: Folder,
  search: Search,
  comment: ChatDotSquare,
  user: User
}

const iconComponent = computed(() => {
  if (typeof props.icon === 'string') {
    return iconMap[props.icon] || Document
  }
  return props.icon
})
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  color: var(--text-tertiary);
  opacity: 0.5;
  margin-bottom: 20px;
}

.empty-text {
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.empty-hint {
  font-size: 13px;
  color: var(--text-tertiary);
}

@media (max-width: 768px) {
  .empty-state {
    padding: 40px 16px;
  }

  .empty-icon :deep(.el-icon) {
    font-size: 48px !important;
  }

  .empty-text {
    font-size: 14px;
  }
}
</style>
