<template>
  <div class="articles-page">
    <div class="container">
      <div class="page-header">
        <h1>
          <el-icon><Document /></el-icon>
          文章列表
        </h1>
        <p>共 <span class="count">{{ total }}</span> 篇文章</p>
      </div>

      <el-row :gutter="24">
        <el-col :span="18">
          <div class="article-list">
            <template v-if="loading">
              <div v-for="i in pageSize" :key="'skeleton-' + i" class="article-item skeleton">
                <div class="article-cover">
                  <el-skeleton-item variant="image" style="width: 100%; height: 100%;" />
                </div>
                <div class="article-content">
                  <el-skeleton-item variant="h3" style="width: 60%; margin-bottom: 12px;" />
                  <el-skeleton :rows="2" animated />
                  <div style="display: flex; gap: 16px; margin-top: 12px;">
                    <el-skeleton-item variant="text" style="width: 80px;" />
                    <el-skeleton-item variant="text" style="width: 80px;" />
                    <el-skeleton-item variant="text" style="width: 60px;" />
                  </div>
                </div>
              </div>
            </template>
            <template v-else>
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
                  <div class="article-header">
                    <h2>{{ article.title }}</h2>
                    <el-tag v-if="article.is_top" type="danger" size="small" effect="dark" class="top-tag">
                      <el-icon><Top /></el-icon>
                      置顶
                    </el-tag>
                  </div>
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
            </template>
          </div>

          <el-empty v-if="!loading && articles.length === 0" description="暂无文章">
            <el-button type="primary" @click="clearFilters">清除筛选</el-button>
          </el-empty>

          <div class="pagination-container" v-if="!loading && total > pageSize">
            <el-pagination
              v-model:current-page="page"
              :page-size="pageSize"
              :total="total"
              :pager-count="5"
              layout="prev, pager, next"
              background
              @current-change="fetchArticles"
            />
          </div>
        </el-col>

        <el-col :span="6">
          <div class="sidebar">
            <div class="sidebar-card">
              <h3>
                <el-icon><FolderOpened /></el-icon>
                分类
              </h3>
              <div class="category-list">
                <div
                  v-for="cat in categories"
                  :key="cat.id"
                  class="category-item"
                  :class="{ active: currentCategory === cat.id }"
                  @click="filterByCategory(cat.id)"
                >
                  <span>{{ cat.name }}</span>
                  <el-tag size="small" type="primary" round>{{ cat.content_count || 0 }}</el-tag>
                </div>
              </div>
            </div>

            <div class="sidebar-card">
              <h3>
                <el-icon><PriceTag /></el-icon>
                热门标签
              </h3>
              <div class="tag-cloud">
                <el-tag
                  v-for="tag in tags"
                  :key="tag.id"
                  class="tag-item"
                  type="info"
                  effect="plain"
                  @click="$router.push(`/tag/${tag.slug || tag.id}`)"
                >
                  #{{ tag.name }}
                </el-tag>
              </div>
            </div>

            <div class="sidebar-card">
              <h3>
                <el-icon><UserFilled /></el-icon>
                热门作者
              </h3>
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
                    <span v-else>{{ author.username?.charAt(0)?.toUpperCase() }}</span>
                  </div>
                  <div class="author-info">
                    <span class="author-name">{{ author.username }}</span>
                    <span class="article-count">{{ author.article_count || 0 }} 篇文章</span>
                  </div>
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
import { User, Folder, View, Calendar, Document, FolderOpened, PriceTag, UserFilled, Top } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getContents, getCategories, getTags } from '@/api/content'
import { getPopularAuthors } from '@/api/user'
import { getCoverUrl, getArticleUrl, formatDate } from '@/utils'

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

const fetchArticles = async () => {
  loading.value = true
  try {
    const offset = (page.value - 1) * pageSize.value
    const params = {
      status: 'published',
      offset: offset,
      limit: pageSize.value,
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
    console.error('Failed to fetch articles:', e)
    if (e.response?.status !== 401) {
      ElMessage.error('加载文章失败')
    }
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const { data } = await getCategories()
    categories.value = data.results || data
  } catch (e) {
    console.error('Failed to fetch categories:', e)
  }
}

const fetchTags = async () => {
  try {
    const { data } = await getTags()
    tags.value = data.results || data
  } catch (e) {
    console.error('Failed to fetch tags:', e)
  }
}

const fetchAuthors = async () => {
  try {
    const { data } = await getPopularAuthors()
    authors.value = data.results || data
  } catch (e) {
    console.error('Failed to fetch authors:', e)
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

const clearFilters = () => {
  currentCategory.value = null
  currentAuthor.value = null
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
  padding: 32px 0;
  min-height: calc(100vh - var(--header-height) - 200px);
  background: var(--bg-color);
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
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 26px;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.page-header h1 .el-icon {
  color: var(--primary-color);
  font-size: 28px;
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

.article-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 10px;
}

.article-content h2 {
  font-size: 18px;
  color: var(--text-primary);
  font-weight: 600;
  line-height: 1.5;
  flex: 1;
  transition: color var(--transition-fast);
}

.article-item:hover .article-content h2 {
  color: var(--primary-color);
}

.top-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}

.top-tag :deep(.el-tag__content) {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.top-tag .el-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.article-summary {
  flex: 1;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  margin-bottom: 16px;
}

.article-meta {
  display: flex;
  gap: 20px;
  font-size: 13px;
  color: var(--text-tertiary);
}

.article-meta span {
  display: flex;
  align-items: center;
  gap: 6px;
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

.article-meta span .el-icon {
  font-size: 14px;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: sticky;
  top: 96px;
}

.sidebar-card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 24px;
  border: 1px solid var(--border-light);
}

.sidebar-card h3 {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 17px;
  color: var(--text-primary);
  margin-bottom: 18px;
  padding-bottom: 14px;
  border-bottom: 2px solid var(--border-light);
}

.sidebar-card h3 .el-icon {
  color: var(--primary-color);
  font-size: 20px;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: 14px;
  color: var(--text-secondary);
}

.category-item:hover {
  background: var(--primary-bg);
  color: var(--primary-color);
}

.category-item.active {
  background: var(--primary-color);
  color: #fff;
}

.category-item.active .el-tag {
  background: rgba(255, 255, 255, 0.2) !important;
  color: #fff !important;
  border-color: transparent !important;
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-item {
  cursor: pointer;
  transition: all var(--transition-fast);
  border-radius: var(--radius-sm);
  padding: 6px 12px;
}

.tag-item:hover {
  background: var(--primary-color) !important;
  color: #fff !important;
  border-color: transparent !important;
}

.author-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.author-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.author-item:hover {
  background: var(--primary-bg);
}

.author-item.active {
  background: var(--primary-bg);
}

.author-avatar {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  background: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 600;
  font-size: 16px;
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
  gap: 4px;
}

.author-name {
  font-size: 14px;
  color: var(--text-primary);
  font-weight: 600;
}

.article-count {
  font-size: 12px;
  color: var(--text-tertiary);
}

.pagination-container {
  margin-top: 32px;
  display: flex;
  justify-content: center;
}

.pagination-container :deep(.el-pagination) {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

.pagination-container :deep(.el-pager li.is-active) {
  background: var(--primary-color) !important;
  color: #fff !important;
  border: none !important;
}

.pagination-container :deep(.el-pager li:hover) {
  color: var(--primary-color) !important;
}

.pagination-container :deep(.btn-prev),
.pagination-container :deep(.btn-next) {
  border-radius: var(--radius-md) !important;
  transition: all var(--transition-fast) !important;
}

.pagination-container :deep(.btn-prev:hover),
.pagination-container :deep(.btn-next:hover) {
  color: var(--primary-color) !important;
  background: var(--primary-bg) !important;
}

@media (max-width: 768px) {
  .article-cover {
    width: 160px;
    height: 100px;
  }
  
  .article-meta {
    flex-wrap: wrap;
    gap: 10px;
  }
}
</style>
