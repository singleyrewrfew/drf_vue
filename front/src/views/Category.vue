<template>
  <div class="category-page">
    <div class="container">
      <div class="page-header">
        <h1>{{ category.name }}</h1>
        <p>共 <span class="count">{{ total }}</span> 篇文章</p>
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
            <h2>{{ article.title }}</h2>
            <p class="article-summary">{{ article.summary || '暂无摘要' }}</p>
            <div class="article-meta">
              <span><el-icon><User /></el-icon> {{ article.author_name }}</span>
              <span><el-icon><View /></el-icon> {{ article.view_count }}</span>
              <span><el-icon><Calendar /></el-icon> {{ formatDate(article.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>

      <el-empty v-if="!loading && articles.length === 0" description="该分类下暂无文章" />

      <div v-if="total > pageSize" class="pagination-container">
        <el-pagination
          v-model:current-page="page"
          :page-size="pageSize"
          :total="total"
          :pager-count="5"
          layout="prev, pager, next"
          background
          @current-change="fetchData"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { User, View, Calendar } from '@element-plus/icons-vue'
import { getCategory, getContents } from '@/api/content'

const route = useRoute()

const loading = ref(false)
const category = ref({})
const articles = ref([])
const page = ref(1)
const pageSize = ref(4)
const total = ref(0)

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

const fetchData = async () => {
  loading.value = true
  try {
    const offset = (page.value - 1) * pageSize.value
    const categoryId = route.params.id_or_slug
    const [catRes, contentRes] = await Promise.all([
      getCategory(categoryId),
      getContents({ 
        status: 'published', 
        category: categoryId,
        offset: offset,
        limit: pageSize.value,
      }),
    ])
    category.value = catRes.data
    articles.value = contentRes.data.results || contentRes.data
    total.value = contentRes.data.count || articles.value.length
  } catch (e) {
    console.error(e)
    if (e.response?.status !== 401) {
      ElMessage.error('加载分类失败')
    }
  } finally {
    loading.value = false
  }
}

watch(() => route.params.id_or_slug, fetchData, { immediate: true })
</script>

<style scoped>
.category-page {
  padding: 20px 0;
  background: var(--bg-color);
  min-height: calc(100vh - var(--header-height));
}

.container {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 24px;
}

.page-header {
  margin-bottom: 32px;
  padding: 24px 28px;
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
}

.page-header h1 {
  font-size: 24px;
  color: var(--text-primary);
  margin-bottom: 8px;
  font-weight: 700;
}

.page-header p {
  color: var(--text-secondary);
  font-size: 14px;
}

.page-header .count {
  color: var(--primary-color);
  font-weight: 600;
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

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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

.article-summary {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 12px;
  flex: 1;
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

.pagination-container {
  margin-top: 32px;
  display: flex;
  justify-content: center;
}

.pagination-container :deep(.el-pager li.is-active) {
  background: var(--primary-color) !important;
  color: #fff !important;
  border: none !important;
}

.pagination-container :deep(.el-pager li:hover) {
  color: var(--primary-color) !important;
}
</style>
