<template>
  <SidebarContainer title="热门作者" :icon="UserFilled">
    <div class="author-list">
      <div
        v-for="author in authors"
        :key="author.id"
        class="author-item"
        :class="{ active: activeId === author.id }"
        @click="handleClick(author)"
      >
        <div class="author-avatar">
          <img v-if="author.avatar" :src="getAvatarUrl(author.avatar)" :alt="author.username" />
          <span v-else>{{ author.username?.charAt(0)?.toUpperCase() }}</span>
        </div>
        <div class="author-info">
          <span class="author-name">{{ author.username }}</span>
          <span class="article-count">{{ author.article_count || 0 }} 篇文章</span>
        </div>
      </div>
    </div>
  </SidebarContainer>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { UserFilled } from '@element-plus/icons-vue'
import SidebarContainer from './SidebarContainer.vue'
import { getAvatarUrl } from '@/utils'

const props = defineProps({
  authors: {
    type: Array,
    default: () => []
  },
  activeId: {
    type: [Number, String],
    default: null
  }
})

const emit = defineEmits(['select'])
const router = useRouter()

const handleClick = (author) => {
  emit('select', author)
}
</script>

<style scoped>
.author-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.author-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.author-item:hover {
  background: var(--primary-bg);
}

.author-item.active {
  background: var(--primary-bg);
}

.author-avatar {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  background: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 600;
  font-size: 16px;
}

.author-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.author-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.author-name {
  font-size: 14px;
  color: var(--text-primary);
  font-weight: 600;
}

.article-count {
  font-size: 12px;
  color: var(--text-tertiary);
}
</style>
