<template>
  <div class="category-page">
    <div class="container">
      <div class="page-header">
        <h1>{{ category.name }}</h1>
        <p>{{ category.description }}</p>
      </div>

      <div class="article-list">
        <div
          v-for="article in articles"
          :key="article.id"
          class="article-item"
          @click="$router.push(`/article/${article.id}`)"
        >
          <div v-if="article.cover_image" class="article-cover">
            <img :src="getCoverUrl(article.cover_image)" :alt="article.title" />
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
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { User, View, Calendar } from '@element-plus/icons-vue'
import { getCategory } from '@/api/content'
import { getContents } from '@/api/content'

const route = useRoute()

const loading = ref(false)
const category = ref({})
const articles = ref([])

const getCoverUrl = (coverImage) => {
  if (!coverImage) return ''
  if (coverImage.startsWith('http')) return coverImage
  return `http://localhost:8001${coverImage}`
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const fetchData = async () => {
  loading.value = true
  try {
    const [catRes, contentRes] = await Promise.all([
      getCategory(route.params.id),
      getContents({ status: 'published', category: route.params.id }),
    ])
    category.value = catRes.data
    articles.value = contentRes.data.results || contentRes.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

watch(() => route.params.id, fetchData, { immediate: true })
</script>

<style scoped>
.category-page {
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

.article-summary {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  margin-bottom: 12px;
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
