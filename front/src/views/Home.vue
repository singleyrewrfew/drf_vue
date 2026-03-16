<template>
  <div class="home-page">
    <section class="hero-section" v-if="featuredContents.length">
      <el-carousel height="500px" :interval="6000">
        <el-carousel-item v-for="item in featuredContents" :key="item.id">
          <div class="hero-item" @click="$router.push(getArticleUrl(item))">
            <img :src="getCoverUrl(item.cover_image)" :alt="item.title" />
            <div class="hero-overlay"></div>
            <div class="hero-content">
              <el-tag type="primary" effect="dark" size="small" class="recommend-tag">
                <el-icon><Star /></el-icon>
                推荐
              </el-tag>
              <h2>{{ item.title }}</h2>
              <p>{{ item.summary || '暂无摘要' }}</p>
              <div class="hero-meta">
                <span><el-icon><User /></el-icon> {{ item.author_name }}</span>
                <span><el-icon><View /></el-icon> {{ item.view_count }} 阅读</span>
                <span><el-icon><Calendar /></el-icon> {{ formatDate(item.created_at) }}</span>
              </div>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </section>

    <div class="main-content">
      <div class="container">
        <el-row :gutter="24">
          <el-col :span="17">
            <section class="section">
              <div class="section-header">
                <h2>
                  <el-icon><Document /></el-icon>
                  最新文章
                </h2>
                <el-button type="primary" link @click="$router.push('/articles')">
                  查看更多 <el-icon><ArrowRight /></el-icon>
                </el-button>
              </div>
              <div class="article-grid" v-loading="loading">
                <template v-if="loading">
                  <div v-for="i in 4" :key="i" class="article-card skeleton-card">
                    <div class="article-cover">
                      <el-skeleton animated>
                        <template #template>
                          <el-skeleton-item variant="image" style="width: 100%; height: 200px;" />
                        </template>
                      </el-skeleton>
                    </div>
                    <div class="article-info">
                      <el-skeleton animated>
                        <template #template>
                          <el-skeleton-item variant="h3" style="width: 80%; margin-bottom: 12px;" />
                          <el-skeleton-item variant="text" style="width: 100%; margin-bottom: 8px;" />
                          <el-skeleton-item variant="text" style="width: 60%; margin-bottom: 16px;" />
                          <div style="display: flex; justify-content: space-between; align-items: center;">
                            <el-skeleton-item variant="text" style="width: 30%;" />
                            <el-skeleton-item variant="text" style="width: 40%;" />
                          </div>
                        </template>
                      </el-skeleton>
                    </div>
                  </div>
                </template>
                <template v-else>
                  <div
                    v-for="article in latestArticles"
                    :key="article.id"
                    class="article-card"
                    @click="$router.push(getArticleUrl(article))"
                  >
                    <div class="article-cover">
                      <img :src="getCoverUrl(article.cover_image)" :alt="article.title" />
                      <div class="article-badges">
                        <el-tag v-if="article.is_top" type="danger" size="small" effect="dark" class="top-tag">
                          <el-icon><Top /></el-icon>
                          置顶
                        </el-tag>
                        <div class="article-category" v-if="article.category_name">
                          {{ article.category_name }}
                        </div>
                      </div>
                      <div class="cover-overlay"></div>
                    </div>
                    <div class="article-info">
                      <h3>{{ article.title }}</h3>
                      <p class="article-summary">{{ article.summary || '暂无摘要' }}</p>
                      <div class="article-footer">
                        <div class="article-author">
                          <el-avatar :size="28" :src="getAvatarUrl(article.author_avatar)">{{ article.author_name?.charAt(0)?.toUpperCase() }}</el-avatar>
                          <span>{{ article.author_name }}</span>
                        </div>
                        <div class="article-stats">
                          <span><el-icon><View /></el-icon> {{ article.view_count }}</span>
                          <span><el-icon><Clock /></el-icon> {{ formatDate(article.created_at) }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </template>
              </div>
              <div class="pagination-container">
                <el-pagination
                  v-model:current-page="currentPage"
                  v-model:page-size="pageSize"
                  :page-sizes="[4, 8, 12, 16]"
                  :total="total"
                  :pager-count="5"
                  layout="total, sizes, prev, pager, next, jumper"
                  @size-change="handleSizeChange"
                  @current-change="handleCurrentChange"
                />
              </div>
            </section>
          </el-col>

          <el-col :span="7">
            <div class="sidebar">
              <div class="sidebar-card hot-card">
                <div class="sidebar-title">
                  <el-icon><TrendCharts /></el-icon>
                  <span>热门文章</span>
                </div>
                <div class="hot-list">
                  <div
                    v-for="(article, index) in hotArticles"
                    :key="article.id"
                    class="hot-item"
                    @click="$router.push(getArticleUrl(article))"
                  >
                    <span class="hot-rank" :class="{ top: index < 3 }">{{ index + 1 }}</span>
                    <div class="hot-info">
                      <h4>{{ article.title }}</h4>
                      <div class="hot-meta">
                        <span><el-icon><View /></el-icon> {{ article.view_count }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="sidebar-card category-card">
                <div class="sidebar-title">
                  <el-icon><Folder /></el-icon>
                  <span>分类导航</span>
                </div>
                <div class="category-list">
                  <div
                    v-for="cat in categories"
                    :key="cat.id"
                    class="category-item"
                    @click="$router.push(`/category/${cat.id}`)"
                  >
                    <div class="category-left">
                      <el-icon class="category-icon"><FolderOpened /></el-icon>
                      <span>{{ cat.name }}</span>
                    </div>
                    <el-tag size="small" type="primary" round>{{ cat.content_count || 0 }}</el-tag>
                  </div>
                </div>
              </div>

              <div class="sidebar-card tag-card">
                <div class="sidebar-title">
                  <el-icon><PriceTag /></el-icon>
                  <span>热门标签</span>
                </div>
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
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { User, View, Calendar, Clock, Document, ArrowRight, TrendCharts, Folder, FolderOpened, PriceTag, Star, Top } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getContents, getCategories, getTags } from '@/api/content'

const featuredContents = ref([])
const latestArticles = ref([])
const hotArticles = ref([])
const categories = ref([])
const tags = ref([])
const currentPage = ref(1)
const pageSize = ref(4)
const total = ref(0)
const loading = ref(true)

const getCoverUrl = (coverImage) => {
  if (!coverImage) return 'https://picsum.photos/800/400?random=' + Math.random()
  if (coverImage.startsWith('http')) return coverImage
  return `http://localhost:8001${coverImage}`
}

const getArticleUrl = (article) => {
  return `/article/${article.slug || article.id}`
}

const getAvatarUrl = (avatar) => {
  if (!avatar) return ''
  if (avatar.startsWith('http')) return avatar
  return `http://localhost:8001${avatar}`
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

const fetchData = async () => {
  loading.value = true
  try {
    const offset = (currentPage.value - 1) * pageSize.value
    const [featuredRes, latestRes, hotRes, catRes, tagRes] = await Promise.all([
      getContents({ status: 'published', is_top: true, limit: 5 }),
      getContents({ status: 'published', offset: offset, limit: pageSize.value }),
      getContents({ status: 'published', ordering: '-view_count', limit: 8 }),
      getCategories(),
      getTags(),
    ])

    featuredContents.value = featuredRes.data.results || featuredRes.data
    latestArticles.value = latestRes.data.results || latestRes.data
    total.value = latestRes.data.count || 0
    hotArticles.value = hotRes.data.results || hotRes.data
    categories.value = catRes.data.results || catRes.data
    tags.value = tagRes.data.results || tagRes.data
  } catch (e) {
    console.error('Failed to fetch data:', e)
    if (e.response?.status !== 401) {
      ElMessage.error('加载数据失败，请刷新页面重试')
    }
  } finally {
    loading.value = false
  }
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchData()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchData()
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
}

.hero-section {
  background: #fff;
  margin-bottom: 32px;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.hero-section :deep(.el-carousel__indicators) {
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
}

.hero-section :deep(.el-carousel__indicator--horizontal .el-carousel__button) {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  transition: all var(--transition-normal);
  border: 2px solid transparent;
}

.hero-section :deep(.el-carousel__indicator--horizontal.is-active .el-carousel__button) {
  width: 32px;
  border-radius: 5px;
  background: #fff;
  border-color: rgba(255, 255, 255, 0.3);
}

.hero-item {
  height: 100%;
  position: relative;
  cursor: pointer;
}

.hero-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 8s ease;
}

.hero-item:hover img {
  transform: scale(1.05);
}

.hero-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 70%;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
}

.hero-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 48px 80px;
  color: #fff;
  animation: fadeInUp 0.6s ease-out;
}

.recommend-tag {
  border-radius: var(--radius-full) !important;
  background: var(--primary-gradient) !important;
  border: none !important;
  font-weight: 600;
  font-size: 13px;
  letter-spacing: 0.5px;
  padding: 6px 14px !important;
  height: auto !important;
}

.recommend-tag :deep(.el-tag__content) {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.recommend-tag :deep(.el-icon) {
  font-size: 14px;
  margin: 0;
  line-height: 1;
  vertical-align: middle;
}

.hero-content h2 {
  font-size: 42px;
  font-weight: 800;
  margin: 16px 0 12px;
  line-height: 1.2;
  text-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  letter-spacing: 1px;
  color: #fff;
}

.hero-content p {
  font-size: 16px;
  opacity: 0.9;
  line-height: 1.7;
  max-width: 600px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.hero-meta {
  display: flex;
  gap: 24px;
  margin-top: 20px;
  font-size: 14px;
  opacity: 0.85;
}

.hero-meta span {
  display: flex;
  align-items: center;
  gap: 6px;
}

.main-content {
  padding: 0 0 48px;
}

.container {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 24px;
}

.section {
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid var(--border-light);
}

.section-header h2 {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
}

.section-header h2 .el-icon {
  color: var(--primary-color);
  font-size: 24px;
}

.section-header .el-button {
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 20px;
  border-radius: var(--radius-full);
  background: var(--primary-gradient);
  border: none;
  color: #fff;
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-primary);
}

.section-header .el-button:hover {
  transform: translateX(4px);
  box-shadow: var(--shadow-primary-lg);
}

.section-header .el-button .el-icon {
  transition: transform var(--transition-fast);
}

.section-header .el-button:hover .el-icon {
  transform: translateX(4px);
}

.article-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.article-card {
  background: #fff;
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-sm);
  position: relative;
}

.article-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--primary-gradient);
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.article-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-lg);
}

.article-card:hover::before {
  opacity: 1;
}

.article-cover {
  height: 200px;
  position: relative;
  overflow: hidden;
}

.article-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
}

.article-card:hover .article-cover img {
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

.article-card:hover .cover-overlay {
  opacity: 1;
}

.article-badges {
  position: absolute;
  top: 12px;
  left: 12px;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 8px;
  z-index: 1;
  align-items: center;
}

.top-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-weight: 500;
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

.article-category {
  padding: 4px 14px;
  background: var(--primary-gradient);
  color: #fff;
  font-size: 12px;
  border-radius: var(--radius-full);
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-primary);
}

.article-info {
  padding: 20px;
}

.article-info h3 {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 10px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color var(--transition-fast);
}

.article-card:hover .article-info h3 {
  color: var(--primary-color);
}

.article-summary {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
  height: 48px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  margin-bottom: 16px;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--border-light);
}

.article-author {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: var(--text-secondary);
}

.article-author .el-avatar {
  border-radius: var(--radius-sm) !important;
  border: 2px solid var(--border-light);
}

.article-stats {
  display: flex;
  gap: 14px;
  font-size: 12px;
  color: var(--text-tertiary);
}

.article-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.sidebar-card {
  background: #fff;
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-normal);
}

.sidebar-card:hover {
  box-shadow: var(--shadow-md);
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 20px;
  padding-bottom: 14px;
  border-bottom: 2px solid var(--border-light);
}

.sidebar-title .el-icon {
  color: var(--primary-color);
  font-size: 20px;
}

.hot-list {
  display: flex;
  flex-direction: column;
}

.hot-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 14px 0;
  border-bottom: 1px solid var(--border-light);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.hot-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.hot-item:first-child {
  padding-top: 0;
}

.hot-item:hover {
  transform: translateX(4px);
}

.hot-rank {
  width: 26px;
  height: 26px;
  border-radius: var(--radius-sm);
  background: var(--bg-tertiary);
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
  transition: all var(--transition-fast);
}

.hot-rank.top {
  background: var(--primary-gradient);
  color: #fff;
  box-shadow: var(--shadow-primary);
}

.hot-item:hover .hot-rank {
  transform: scale(1.1);
}

.hot-info {
  flex: 1;
  min-width: 0;
}

.hot-info h4 {
  font-size: 14px;
  color: var(--text-primary);
  line-height: 1.5;
  margin-bottom: 6px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color var(--transition-fast);
}

.hot-item:hover .hot-info h4 {
  color: var(--primary-color);
}

.hot-meta {
  font-size: 12px;
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  gap: 4px;
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
  padding: 12px 14px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: 14px;
  color: var(--text-secondary);
}

.category-item:hover {
  background: var(--primary-bg);
  color: var(--primary-color);
  transform: translateX(4px);
}

.category-item:hover .el-tag {
  background: var(--primary-gradient) !important;
  color: #fff !important;
  border-color: transparent !important;
}

.category-item .el-tag {
  font-weight: 600;
  background: var(--primary-gradient);
  color: #fff !important;
  border: none;
  min-width: 24px;
  text-align: center;
}

.category-item .el-tag .el-tag__content {
  color: #fff !important;
}

.category-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.category-icon {
  font-size: 18px;
  opacity: 0.6;
  transition: all var(--transition-fast);
}

.category-item:hover .category-icon {
  opacity: 1;
  color: var(--primary-color);
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-item {
  cursor: pointer;
  transition: all var(--transition-fast);
  border-radius: var(--radius-full);
  padding: 6px 14px;
}

.tag-item:hover {
  background: var(--primary-gradient) !important;
  color: #fff !important;
  border-color: transparent !important;
  transform: translateY(-2px);
  box-shadow: var(--shadow-primary);
}

.pagination-container {
  margin-top: 40px;
  display: flex;
  justify-content: center;
}

.pagination-container :deep(.el-pager li.is-active) {
  color: #fff;
}

.pagination-container :deep(.el-pager li:hover) {
  color: var(--primary-color);
}

@media (max-width: 1200px) {
  .article-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .hero-content {
    padding: 32px 24px;
  }
  
  .hero-content h2 {
    font-size: 24px;
  }
  
  .hero-section {
    margin-bottom: 24px;
  }
  
  .container {
    padding: 0 16px;
  }
}
</style>
