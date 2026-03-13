<template>
  <div class="search-page">
    <div class="container">
      <div class="page-header">
        <h1>搜索结果：{{ keyword }}</h1>
        <p>共找到 {{ total }} 篇相关文章</p>
      </div>

      <div class="article-list">
        <div
            v-for="article in articles"
            :key="article.id"
            class="article-item"
            @click="$router.push(getArticleUrl(article))"
          >
          <div v-if="article.cover_image" class="article-cover">
            <img :src="getCoverUrl(article.cover_image)" :alt="article.title" />
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

const route = useRoute()

const loading = ref(false)
const articles = ref([])
const total = ref(0)

const keyword = ref('')

const getCoverUrl = (coverImage) => {
  if (!coverImage) return ''
  if (coverImage.startsWith('http')) return coverImage
  return `http://localhost:8001${coverImage}`
}

const getArticleUrl = (article) => {
  return `/article/${article.slug || article.id}`
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

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
  color: #303133;
  margin-bottom: 8px;
}

.page-header p {
  color: #909399;
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.article-item {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  gap: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.article-item:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.article-cover {
  width: 200px;
  height: 120px;
  flex-shrink: 0;
  border-radius: 4px;
  overflow: hidden;
}

.article-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-content {
  flex: 1;
}

.article-content h2 {
  font-size: 18px;
  color: #303133;
  margin-bottom: 8px;
}

.article-content h2 :deep(mark) {
  background: #fef0f0;
  color: #f56c6c;
  padding: 0 2px;
}

.article-summary {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  margin-bottom: 12px;
}

.article-summary :deep(mark) {
  background: #fef0f0;
  color: #f56c6c;
  padding: 0 2px;
}

.article-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #909399;
}

.article-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}
</style>
