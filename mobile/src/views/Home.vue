<template>
  <div class="page home-page">
    <header class="page-header">
      <h1 class="page-title">CMS</h1>
      <div class="header-actions">
        <button class="btn-icon" @click="$router.push('/search')">
          <el-icon><Search /></el-icon>
        </button>
      </div>
    </header>
    
    <div class="page-content">
      <div class="section">
        <div class="section-header">
          <h2 class="section-title">最新文章</h2>
          <router-link to="/articles" class="section-more">
            更多 <el-icon><ArrowRight /></el-icon>
          </router-link>
        </div>
        
        <div v-if="loading" class="skeleton-list">
          <div v-for="i in 3" :key="i" class="skeleton-card">
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
              <p class="article-excerpt">{{ truncateText(article.summary || article.content, 80) }}</p>
              <div class="article-meta">
                <span class="article-date">{{ formatRelativeTime(article.created_at) }}</span>
                <span v-if="article.category" class="article-category">{{ article.category_name }}</span>
              </div>
            </div>
          </router-link>
        </div>
        
        <div v-else class="empty-state">
          <el-icon class="empty-state-icon"><Document /></el-icon>
          <p class="empty-state-text">暂无文章</p>
        </div>
      </div>
      
      <div v-if="categories.length" class="section">
        <div class="section-header">
          <h2 class="section-title">分类</h2>
        </div>
        <div class="category-grid">
          <router-link 
            v-for="cat in categories" 
            :key="cat.id" 
            :to="`/category/${cat.slug || cat.id}`"
            class="category-card"
          >
            <el-icon class="category-icon"><Folder /></el-icon>
            <span class="category-name">{{ cat.name }}</span>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, ArrowRight, Document, Folder } from '@element-plus/icons-vue'
import { getContents, getCategories } from '@/api/content'
import { getCoverUrl, truncateText, formatRelativeTime } from '@/utils'

const loading = ref(true)
const articles = ref([])
const categories = ref([])

const fetchData = async () => {
  loading.value = true
  try {
    const [articlesRes, categoriesRes] = await Promise.all([
      getContents({ page_size: 5 }),
      getCategories({ page_size: 8 })
    ])
    articles.value = articlesRes.data.results || articlesRes.data
    categories.value = categoriesRes.data.results || categoriesRes.data
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
.home-page {
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

.section {
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.section-more {
  display: flex;
  align-items: center;
  gap: 2px;
  font-size: 13px;
  color: var(--text-tertiary);
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

.article-category {
  color: var(--primary-color);
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.category-card {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  text-decoration: none;
  transition: all var(--transition-fast);
}

.category-card:active {
  transform: scale(0.98);
  background: var(--card-bg-hover);
}

.category-icon {
  font-size: 20px;
  color: var(--primary-color);
}

.category-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}
</style>
