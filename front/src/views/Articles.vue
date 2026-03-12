<template>
  <div class="articles-page">
    <div class="container">
      <div class="page-header">
        <h1>文章列表</h1>
        <p>共 {{ total }} 篇文章</p>
      </div>

      <el-row :gutter="20">
        <el-col :span="18">
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
                  <span class="author">
                    <el-icon><User /></el-icon>
                    {{ article.author_name }}
                  </span>
                  <span v-if="article.category_name" class="category">
                    <el-icon><Folder /></el-icon>
                    {{ article.category_name }}
                  </span>
                  <span class="views">
                    <el-icon><View /></el-icon>
                    {{ article.view_count }}
                  </span>
                  <span class="date">
                    <el-icon><Calendar /></el-icon>
                    {{ formatDate(article.created_at) }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <el-empty v-if="!loading && articles.length === 0" description="暂无文章" />

          <el-pagination
            v-model:current-page="page"
            :page-size="pageSize"
            :total="total"
            :pager-count="5"
            layout="prev, pager, next"
            background
            @current-change="fetchArticles"
          />
        </el-col>

        <el-col :span="6">
          <div class="sidebar-card">
            <h3>分类</h3>
            <div class="category-list">
              <div
                v-for="cat in categories"
                :key="cat.id"
                class="category-item"
                :class="{ active: currentCategory === cat.id }"
                @click="filterByCategory(cat.id)"
              >
                <span>{{ cat.name }}</span>
                <el-tag size="small" type="success">{{ cat.content_count || 0 }}</el-tag>
              </div>
            </div>
          </div>

          <div class="sidebar-card">
            <h3>热门标签</h3>
            <div class="tag-cloud">
              <el-tag
                v-for="tag in tags"
                :key="tag.id"
                class="tag-item"
                type="info"
                effect="plain"
                @click="$router.push(`/tag/${tag.id}`)"
              >
                {{ tag.name }}
              </el-tag>
            </div>
          </div>

          <div class="sidebar-card">
            <h3>热门作者</h3>
            <div class="author-list">
              <div
                v-for="author in authors"
                :key="author.id"
                class="author-item"
                :class="{ active: currentAuthor === author.id }"
                @click="filterByAuthor(author.id)"
              >
                <div class="author-avatar">
                  <img v-if="author.avatar" :src="getCoverUrl(author.avatar)" :alt="author.username" />
                  <el-icon v-else><User /></el-icon>
                </div>
                <div class="author-info">
                  <span class="author-name">{{ author.username }}</span>
                  <span class="article-count">{{ author.article_count || 0 }} 篇文章</span>
                </div>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { User, Folder, View, Calendar } from '@element-plus/icons-vue'
import { getContents, getCategories, getTags } from '@/api/content'
import { getPopularAuthors } from '@/api/user'

const route = useRoute()

const loading = ref(false)
const articles = ref([])
const categories = ref([])
const tags = ref([])
const authors = ref([])
const page = ref(1)
const pageSize = ref(4)
const total = ref(0)
const currentCategory = ref(null)
const currentAuthor = ref(null)

const getCoverUrl = (coverImage) => {
  if (!coverImage) return ''
  if (coverImage.startsWith('http')) return coverImage
  return `http://localhost:8001${coverImage}`
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

const fetchArticles = async () => {
  loading.value = true
  try {
    const offset = (page.value - 1) * pageSize.value
    const params = {
      status: 'published',
      offset: offset,
      limit: pageSize.value,
      ordering: '-created_at',
    }
    if (currentCategory.value) {
      params.category = currentCategory.value
    }
    if (currentAuthor.value) {
      params.author = currentAuthor.value
    }
    const { data } = await getContents(params)
    articles.value = data.results || data
    total.value = data.count || articles.value.length
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const { data } = await getCategories()
    categories.value = data.results || data
  } catch (e) {
    console.error(e)
  }
}

const fetchTags = async () => {
  try {
    const { data } = await getTags()
    tags.value = data.results || data
  } catch (e) {
    console.error(e)
  }
}

const fetchAuthors = async () => {
  try {
    const { data } = await getPopularAuthors()
    authors.value = data.results || data
  } catch (e) {
    console.error(e)
  }
}

const filterByCategory = (categoryId) => {
  currentCategory.value = currentCategory.value === categoryId ? null : categoryId
  page.value = 1
  fetchArticles()
}

const filterByAuthor = (authorId) => {
  currentAuthor.value = currentAuthor.value === authorId ? null : authorId
  page.value = 1
  fetchArticles()
}

watch(() => route.query, () => {
  if (route.query.category) {
    currentCategory.value = route.query.category
  }
  fetchArticles()
}, { immediate: true })

onMounted(() => {
  fetchCategories()
  fetchTags()
  fetchAuthors()
})
</script>

<style scoped>
.articles-page {
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
  font-size: 14px;
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
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
  display: flex;
  flex-direction: column;
}

.article-content h2 {
  font-size: 18px;
  color: #303133;
  margin-bottom: 8px;
}

.article-summary {
  flex: 1;
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.article-meta {
  display: flex;
  gap: 16px;
  margin-top: 12px;
  font-size: 13px;
  color: #909399;
}

.article-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.sidebar-card {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
}

.sidebar-card h3 {
  font-size: 16px;
  color: #303133;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #ebeef5;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.category-item:hover,
.category-item.active {
  background: #ecf5ff;
  color: #409eff;
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  cursor: pointer;
  transition: all 0.3s;
}

.tag-item:hover {
  background: #409eff;
  color: #fff;
  border-color: #409eff;
}

.author-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.author-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.author-item:hover,
.author-item.active {
  background: #ecf5ff;
}

.author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  background: #f0f2f5;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
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
  gap: 2px;
}

.author-name {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
}

.article-count {
  font-size: 12px;
  color: #909399;
}

.el-pagination {
  margin-top: 20px;
  justify-content: center;
}
</style>
