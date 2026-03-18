<template>
  <div class="search-page">
    <div class="container">
      <div class="page-header">
        <h1>搜索结果：{{ keyword }}</h1>
        <p>共找到 {{ total }} 篇相关文章</p>
      </div>

      <div class="article-list">
        <div
            v-for="(article, index) in articles"
            :key="article.id"
            class="article-item"
            :style="{ animationDelay: `${index * 0.1}s` }"
            @click="$router.push(getArticleUrl(article))"
          >
          <div v-if="article.cover_image" class="article-cover">
            <img :src="getCoverUrl(article.cover_image)" :alt="article.title" />
            <div class="cover-overlay"></div>
          </div>
          <div class="article-content">
            <h2 v-html="highlightKeyword(article.title)"></h2>
            <p class="article-summary" v-html="highlightKeyword(article.summary)"></p>
            <div class="article-meta">
              <span><el-icon><User /></el-icon> {{ article.author_name }}</span>
              <span><el-icon><View /></el-icon> {{ article.view_count }}</span>
              <span><el-icon><Calendar /></el-icon> {{ formatDate(article.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>

      <el-empty v-if="!loading && articles.length === 0" description="未找到相关文章" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { User, View, Calendar } from '@element-plus/icons-vue'
import { searchContents } from '@/api/content'
import { getCoverUrl, getArticleUrl, formatDate } from '@/utils'

const route = useRoute()

const loading = ref(false)
const articles = ref([])
const total = ref(0)

const keyword = ref('')

const highlightKeyword = (text) => {
  if (!text || !keyword.value) return text
  const regex = new RegExp(`(${keyword.value})`, 'gi')
  return text.replace(regex, '<mark>$1</mark>')
}

const fetchArticles = async () => {
  keyword.value = route.query.q || ''
  if (!keyword.value) {
    articles.value = []
    total.value = 0
    return
  }

  loading.value = true
  try {
    const { data } = await searchContents(keyword.value)
    articles.value = data.results || data
    total.value = data.count || articles.value.length
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

watch(() => route.query.q, fetchArticles, { immediate: true })
</script>

<style scoped>
.search-page {
  padding: 20px 0;
  background: var(--bg-color);
  min-height: calc(100vh - var(--header-height));
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 24px;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.page-header p {
  color: var(--text-secondary);
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.article-item {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 24px;
  display: flex;
  gap: 24px;
  cursor: pointer;
  transition: all var(--transition-fast);
  border: 1px solid var(--border-light);
  position: relative;
  overflow: hidden;
  animation: fadeInUp 0.15s ease-out backwards;
}

.article-item:hover {
  border-color: var(--primary-color);
  box-shadow: var(--shadow-md);
}

.article-cover {
  width: 220px;
  height: 140px;
  flex-shrink: 0;
  border-radius: var(--radius-md);
  overflow: hidden;
  position: relative;
}

.article-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-slow);
}

.article-item:hover .article-cover img {
  transform: scale(1.08);
}

.cover-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.3));
  opacity: 0;
  transition: opacity var(--transition-normal);
}

.article-item:hover .cover-overlay {
  opacity: 1;
}

.article-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.article-content h2 {
  font-size: 18px;
  color: var(--text-primary);
  margin-bottom: 8px;
  font-weight: 600;
}

.article-content h2 :deep(mark) {
  background: var(--danger-bg);
  color: var(--danger-color);
  padding: 0 2px;
}

.article-summary {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 12px;
  flex: 1;
}

.article-summary :deep(mark) {
  background: var(--danger-bg);
  color: var(--danger-color);
  padding: 0 2px;
}

.article-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: var(--text-tertiary);
}

.article-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
}

.article-meta span:hover {
  background: var(--primary-bg);
  color: var(--primary-color);
}

[data-theme="dark"] .article-meta span {
  background: var(--bg-tertiary);
}

@media (max-width: 768px) {
  .search-page {
    padding: 16px 0;
  }
  
  .container {
    padding: 0 16px;
  }
  
  .page-header {
    margin-bottom: 20px;
  }
  
  .page-header h1 {
    font-size: 18px;
  }
  
  .article-item {
    flex-direction: column;
    padding: 16px;
    gap: 16px;
  }
  
  .article-cover {
    width: 100%;
    height: 180px;
  }
  
  .article-content h2 {
    font-size: 16px;
  }
  
  .article-summary {
    font-size: 13px;
  }
  
  .article-meta {
    flex-wrap: wrap;
    gap: 8px;
    font-size: 12px;
  }
  
  .article-meta span {
    padding: 3px 8px;
  }
}

@media (max-width: 576px) {
  .page-header h1 {
    font-size: 16px;
  }
  
  .article-cover {
    height: 160px;
  }
  
  .article-meta span:nth-child(n+3) {
    display: none;
  }
}
</style>
