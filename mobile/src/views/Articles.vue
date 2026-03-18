<template>
  <div class="page articles-page">
    <header class="page-header">
      <h1 class="page-title">文章</h1>
      <div class="header-actions">
        <button class="btn-icon" @click="$router.push('/search')">
          <el-icon><Search /></el-icon>
        </button>
      </div>
    </header>
    
    <div class="page-content">
      <div v-if="loading && !articles.length" class="skeleton-list">
        <div v-for="i in 5" :key="i" class="skeleton-card">
          <div class="skeleton skeleton-cover"></div>
          <div class="skeleton skeleton-title"></div>
          <div class="skeleton skeleton-text"></div>
        </div>
      </div>
      
      <div v-else-if="articles.length" class="article-list">
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
            <p class="article-excerpt">{{ truncateText(article.summary || article.content, 100) }}</p>
            <div class="article-meta">
              <span class="article-date">{{ formatRelativeTime(article.created_at) }}</span>
              <span v-if="article.category_name" class="article-category">{{ article.category_name }}</span>
            </div>
          </div>
        </router-link>
        
        <div v-if="hasMore" class="load-more">
          <button v-if="!loadingMore" class="btn btn-secondary btn-block" @click="loadMore">
            加载更多
          </button>
          <div v-else class="loading-indicator">
            <el-icon class="loading-icon"><Loading /></el-icon>
            <span>加载中...</span>
          </div>
        </div>
      </div>
      
      <div v-else class="empty-state">
        <el-icon class="empty-state-icon"><Document /></el-icon>
        <p class="empty-state-text">暂无文章</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, Document, Loading } from '@element-plus/icons-vue'
import { getContents } from '@/api/content'
import { getCoverUrl, truncateText, formatRelativeTime } from '@/utils'

const loading = ref(true)
const loadingMore = ref(false)
const articles = ref([])
const page = ref(1)
const hasMore = ref(true)

const fetchArticles = async (isLoadMore = false) => {
  if (isLoadMore) {
    loadingMore.value = true
  } else {
    loading.value = true
  }
  
  try {
    const { data } = await getContents({ 
      page: page.value,
      page_size: 10 
    })
    const results = data.results || data
    
    if (isLoadMore) {
      articles.value = [...articles.value, ...results]
    } else {
      articles.value = results
    }
    
    hasMore.value = data.next || results.length >= 10
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

const loadMore = () => {
  page.value++
  fetchArticles(true)
}

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.articles-page {
  background: var(--bg-color);
}

.header-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  width: 36px;
  height: 36px;
  border: none;
  background: var(--bg-secondary);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  transition: all var(--transition-fast);
}

.btn-icon:active {
  background: var(--bg-tertiary);
  transform: scale(0.95);
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
  height: 140px;
}

.skeleton-title {
  height: 18px;
  margin: 12px 12px 8px;
  border-radius: var(--radius-sm);
}

.skeleton-text {
  height: 14px;
  margin: 0 12px 12px;
  width: 60%;
  border-radius: var(--radius-sm);
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.article-card {
  display: flex;
  flex-direction: column;
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
  width: 100%;
  height: 140px;
  object-fit: cover;
}

.article-content {
  padding: 12px;
}

.article-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
  margin: 0 0 6px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-excerpt {
  font-size: 13px;
  color: var(--text-tertiary);
  line-height: 1.5;
  margin: 0 0 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-tertiary);
}

.article-category {
  color: var(--primary-color);
}

.load-more {
  padding: 16px 0;
}

.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: var(--text-tertiary);
  font-size: 14px;
}

.loading-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
