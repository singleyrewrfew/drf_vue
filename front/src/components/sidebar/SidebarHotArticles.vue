<template>
  <SidebarContainer title="热门文章" :icon="TrendCharts">
    <div class="hot-list">
      <div
        v-for="(article, index) in displayArticles"
        :key="article.id"
        class="hot-item"
        @click="handleClick(article)"
      >
        <span class="hot-rank" :class="{ top: index < 3 }">{{ index + 1 }}</span>
        <div class="hot-info">
          <h4>{{ article.title }}</h4>
          <div class="hot-meta">
            <span><el-icon><View /></el-icon> {{ article.view_count }}</span>
          </div>
        </div>
      </div>
    </div>
  </SidebarContainer>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { TrendCharts, View } from '@element-plus/icons-vue'
import SidebarContainer from './SidebarContainer.vue'
import { getArticleUrl } from '@/utils'

const props = defineProps({
  articles: {
    type: Array,
    default: () => []
  },
  maxItems: {
    type: Number,
    default: 8
  }
})

const router = useRouter()

const displayArticles = computed(() => {
  return props.articles.slice(0, props.maxItems)
})

const handleClick = (article) => {
  router.push(getArticleUrl(article))
}
</script>

<style scoped>
.hot-list {
  display: flex;
  flex-direction: column;
}

.hot-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 14px 0;
  border-bottom: 1px solid var(--border-light);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.hot-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.hot-item:first-child {
  padding-top: 0;
}

.hot-item:hover {
  transform: translateX(4px);
}

.hot-rank {
  width: 26px;
  height: 26px;
  border-radius: var(--radius-sm);
  background: var(--bg-tertiary);
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
  transition: all var(--transition-fast);
}

.hot-rank.top {
  background: var(--primary-color);
  color: #fff;
}

.hot-item:hover .hot-rank {
  transform: scale(1.1);
}

.hot-info {
  flex: 1;
  min-width: 0;
}

.hot-info h4 {
  font-size: 14px;
  color: var(--text-primary);
  line-height: 1.5;
  margin-bottom: 6px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color var(--transition-fast);
}

.hot-item:hover .hot-info h4 {
  color: var(--primary-color);
}

.hot-meta {
  font-size: 12px;
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  gap: 4px;
}
</style>
