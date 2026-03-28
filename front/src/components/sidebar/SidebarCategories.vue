<template>
  <SidebarContainer title="分类导航" :icon="FolderOpened">
    <div class="category-list">
      <div
        v-for="cat in categories"
        :key="cat.id"
        class="category-item"
        :class="{ active: activeId === cat.id }"
        @click="handleClick(cat)"
      >
        <div class="category-left">
          <el-icon class="category-icon">
            <FolderOpened />
          </el-icon>
          <span>{{ cat.name }}</span>
        </div>
        <el-tag size="small" type="primary" round>{{ cat.content_count || 0 }}</el-tag>
      </div>
    </div>
  </SidebarContainer>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { FolderOpened } from '@element-plus/icons-vue'
import SidebarContainer from './SidebarContainer.vue'

const props = defineProps({
  categories: {
    type: Array,
    default: () => []
  },
  activeId: {
    type: [Number, String],
    default: null
  },
  selectable: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['select'])
const router = useRouter()

const handleClick = (cat) => {
  if (props.selectable) {
    emit('select', cat)
  } else {
    router.push(`/category/${cat.slug || cat.id}`)
  }
}
</script>

<style scoped>
.category-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: 14px;
  color: var(--text-secondary);
}

.category-item:hover {
  background: var(--primary-bg);
  color: var(--primary-color);
}

.category-item.active {
  background: var(--primary-color);
  color: #fff;
}

.category-item.active .el-tag {
  background: rgba(255, 255, 255, 0.2) !important;
  color: #fff !important;
  border-color: transparent !important;
}

.category-item:hover .el-tag {
  background: var(--primary-color) !important;
  color: #fff !important;
  border-color: transparent !important;
}

.category-item .el-tag {
  font-weight: 600;
  background: var(--primary-color);
  color: #fff !important;
  border: none;
  min-width: 24px;
  text-align: center;
}

.category-item .el-tag .el-tag__content {
  color: #fff !important;
}

.category-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.category-icon {
  font-size: 18px;
  opacity: 0.6;
  transition: all var(--transition-fast);
}

.category-item:hover .category-icon {
  opacity: 1;
  color: var(--primary-color);
}

.category-item.active .category-icon {
  opacity: 1;
  color: #fff;
}
</style>
