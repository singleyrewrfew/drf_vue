<template>
  <div class="sidebar-card">
    <div class="sidebar-title">
      <el-icon>
        <Document />
      </el-icon>
      <span>相关文章</span>
    </div>
    <div class="related-list">
      <div
        v-for="item in articles"
        :key="item.id"
        class="related-item"
        @click="$router.push(getArticleUrl(item))"
      >
        <div class="related-cover" v-if="item.cover_image">
          <img :src="getCoverUrl(item.cover_image)" :alt="item.title" loading="lazy" />
        </div>
        <div class="related-info">
          <span class="related-title">{{ item.title }}</span>
          <span class="related-views" v-if="item.view_count">{{ item.view_count }} 阅读</span>
        </div>
      </div>
      <el-empty v-if="articles.length === 0" description="暂无相关文章" :image-size="60" />
    </div>
  </div>
</template>

<script setup>
import { Document } from '@element-plus/icons-vue'
import { getCoverUrl, getArticleUrl } from '@/utils'

defineProps({
  articles: {
    type: Array,
    default: () => []
  }
})
</script>

<style scoped>
.sidebar-card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 24px;
  border: 1px solid var(--border-light);
  transition: all var(--transition-fast);
}

.sidebar-card:hover {
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
  margin-bottom: 18px;
  padding-bottom: 14px;
  border-bottom: 2px solid var(--border-light);
}

.sidebar-title .el-icon {
  color: var(--primary-color);
  font-size: 20px;
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.related-item {
  display: flex;
  gap: 14px;
  padding: 14px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  border: 1px solid transparent;
}

.related-item:hover {
  background: var(--primary-bg);
  border-color: var(--primary-light);
  transform: translateX(4px);
}

.related-cover {
  width: 80px;
  height: 60px;
  border-radius: var(--radius-md);
  overflow: hidden;
  flex-shrink: 0;
}

.related-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-normal);
}

.related-item:hover .related-cover img {
  transform: scale(1.1);
}

.related-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
}

.related-title {
  font-size: 14px;
  color: var(--text-primary);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 6px;
  font-weight: 500;
  transition: color var(--transition-fast);
}

.related-item:hover .related-title {
  color: var(--primary-color);
}

.related-views {
  font-size: 12px;
  color: var(--text-tertiary);
}
</style>
