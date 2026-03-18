<template>
  <div class="page category-page">
    <header class="page-header">
      <button class="btn-back" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
      </button>
      <h1 class="page-title">{{ category?.name || '分类' }}</h1>
    </header>
    
    <div v-if="loading" class="page-content">
      <div class="skeleton-list">
        <div v-for="i in 3" :key="i" class="skeleton-card">
          <div class="skeleton skeleton-cover"></div>
          <div class="skeleton skeleton-title"></div>
        </div>
      </div>
    </div>
    
    <div v-else-if="articles.length" class="page-content">
      <div class="article-list">
        <router-link 
          v-for="article in articles" 
          :key="article.id" 
          :to="`/article/${article.slug || article.id}`"
          class="article-card"
        >
          <img 
            v-if="article.cover_image" 
            :src="getCoverUrl(article.cover_image)" 
            class="article-cover"
            loading="lazy"
          />
          <div class="article-content">
            <h3 class="article-title">{{ article.title }}</h3>
            <p class="article-excerpt">{{ truncateText(article.summary || article.content, 80) }}</p>
            <div class="article-meta">
              <span class="article-date">{{ formatRelativeTime(article.created_at) }}</span>
            </div>
          </div>
        </router-link>
      </div>
    </div>
    
    <div v-else class="page-content">
      <div class="empty-state">
        <el-icon class="empty-state-icon"><Folder /></el-icon>
        <p class="empty-state-text">该分类下暂无文章</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft, Folder } from '@element-plus/icons-vue'
import { getCategory } from '@/api/content'
import { getContents } from '@/api/content'
import { getCoverUrl, truncateText, formatRelativeTime } from '@/utils'

const route = useRoute()
const loading = ref(true)
const category = ref(null)
const articles = ref([])

const fetchData = async () => {
  loading.value = true
  try {
    const id = route.params.id_or_slug
    const [categoryRes, articlesRes] = await Promise.all([
      getCategory(id),
      getContents({ category: id, page_size: 20 })
    ])
    category.value = categoryRes.data
    articles.value = articlesRes.data.results || articlesRes.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.category-page {
  background: var(--bg-color);
}

.btn-back {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-primary);
  transition: all var(--transition-fast);
}

.btn-back:active {
  background: var(--bg-secondary);
}

.skeleton-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skeleton-card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.skeleton-cover {
  height: 120px;
}

.skeleton-title {
  height: 18px;
  margin: 12px;
  border-radius: var(--radius-sm);
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.article-card {
  display: flex;
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  overflow: hidden;
  text-decoration: none;
  transition: all var(--transition-fast);
}

.article-card:active {
  transform: scale(0.98);
}

.article-cover {
  width: 100px;
  height: 80px;
  object-fit: cover;
  flex-shrink: 0;
}

.article-content {
  flex: 1;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-width: 0;
}

.article-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
  margin: 0 0 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-excerpt {
  font-size: 12px;
  color: var(--text-tertiary);
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  color: var(--text-tertiary);
}
</style>
