<template>
  <div class="home-page">
    <section class="hero-section" v-if="featuredContents.length">
      <el-carousel height="480px" :interval="6000">
        <el-carousel-item v-for="item in featuredContents" :key="item.id">
          <div class="hero-item" @click="$router.push(`/article/${item.id}`)">
            <img :src="getCoverUrl(item.cover_image)" :alt="item.title" />
            <div class="hero-overlay"></div>
            <div class="hero-content">
              <el-tag type="primary" effect="dark" size="small">推荐</el-tag>
              <h2>{{ item.title }}</h2>
              <p>{{ item.summary || '暂无摘要' }}</p>
              <div class="hero-meta">
                <span><el-icon><User /></el-icon> {{ item.author_name }}</span>
                <span><el-icon><View /></el-icon> {{ item.view_count }} 阅读</span>
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
              <div class="article-grid">
                <div
                  v-for="article in latestArticles"
                  :key="article.id"
                  class="article-card"
                  @click="$router.push(`/article/${article.id}`)"
                >
                  <div class="article-cover">
                    <img :src="getCoverUrl(article.cover_image)" :alt="article.title" />
                    <div class="article-badges">
                      <el-tag v-if="article.is_top" type="danger" size="small" effect="dark">置顶</el-tag>
                      <div class="article-category" v-if="article.category_name">
                        {{ article.category_name }}
                      </div>
                    </div>
                  </div>
                  <div class="article-info">
                    <h3>{{ article.title }}</h3>
                    <p class="article-summary">{{ article.summary || '暂无摘要' }}</p>
                    <div class="article-footer">
                      <div class="article-author">
                        <el-avatar :size="24" :src="getAvatarUrl(article.author_avatar)">{{ article.author_name?.charAt(0)?.toUpperCase() }}</el-avatar>
                        <span>{{ article.author_name }}</span>
                      </div>
                      <div class="article-stats">
                        <span><el-icon><View /></el-icon> {{ article.view_count }}</span>
                        <span><el-icon><Calendar /></el-icon> {{ formatDate(article.created_at) }}</span>
                      </div>
                    </div>
                  </div>
                </div>
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
              <div class="sidebar-card">
                <div class="sidebar-title">
                  <el-icon><TrendCharts /></el-icon>
                  <span>热门文章</span>
                </div>
                <div class="hot-list">
                  <div
                    v-for="(article, index) in hotArticles"
                    :key="article.id"
                    class="hot-item"
                    @click="$router.push(`/article/${article.id}`)"
                  >
                    <span class="hot-rank" :class="{ top: index < 3 }">{{ index + 1 }}</span>
                    <div class="hot-info">
                      <h4>{{ article.title }}</h4>
                      <div class="hot-meta">
                        <span>{{ article.view_count }} 阅读</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="sidebar-card">
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
                    <span>{{ cat.name }}</span>
                    <el-tag size="small" type="success" round>{{ cat.content_count || 0 }}</el-tag>
                  </div>
                </div>
              </div>

              <div class="sidebar-card">
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
                    @click="$router.push(`/tag/${tag.id}`)"
                  >
                    {{ tag.name }}
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
import { User, View, Calendar, Document, ArrowRight, TrendCharts, Folder, PriceTag } from '@element-plus/icons-vue'
import { getContents, getCategories, getTags } from '@/api/content'

const featuredContents = ref([])
const latestArticles = ref([])
const hotArticles = ref([])
const categories = ref([])
const tags = ref([])
const currentPage = ref(1)
const pageSize = ref(4)
const total = ref(0)

const getCoverUrl = (coverImage) => {
  if (!coverImage) return 'https://picsum.photos/800/400?random=' + Math.random()
  if (coverImage.startsWith('http')) return coverImage
  return `http://localhost:8001${coverImage}`
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
  try {
    const offset = (currentPage.value - 1) * pageSize.value
    const [featuredRes, latestRes, hotRes, catRes, tagRes] = await Promise.all([
      getContents({ status: 'published', is_top: true, limit: 5 }),
      getContents({ status: 'published', ordering: '-created_at', offset: offset, limit: pageSize.value }),
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
    console.error(e)
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
  margin-bottom: 24px;
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
}

.hero-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60%;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
}

.hero-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px 60px;
  color: #fff;
}

.hero-content h2 {
  font-size: 32px;
  font-weight: 600;
  margin: 16px 0 12px;
  line-height: 1.3;
}

.hero-content p {
  font-size: 15px;
  opacity: 0.9;
  line-height: 1.6;
  max-width: 600px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.hero-meta {
  display: flex;
  gap: 20px;
  margin-top: 16px;
  font-size: 14px;
  opacity: 0.8;
}

.hero-meta span {
  display: flex;
  align-items: center;
  gap: 6px;
}

.main-content {
  padding: 0 0 40px;
}

.container {
  max-width: 1400px;
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
}

.section-header h2 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.section-header h2 .el-icon {
  color: #409eff;
}

.article-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.article-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.article-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.article-cover {
  height: 180px;
  position: relative;
  overflow: hidden;
}

.article-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.article-card:hover .article-cover img {
  transform: scale(1.05);
}

.article-badges {
  position: absolute;
  top: 12px;
  left: 12px;
  display: flex;
  flex-direction: row;
  gap: 8px;
  z-index: 1;
}

.article-category {
  padding: 4px 12px;
  background: rgba(64, 158, 255, 0.9);
  color: #fff;
  font-size: 12px;
  border-radius: 4px;
  align-self: flex-start;
  font-weight: 500;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}

.el-tag.el-tag--danger.el-tag--small.el-tag--dark {
  font-size: 12px;
  font-weight: 500;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}

.article-info {
  padding: 20px;
}

.article-info h3 {
  font-size: 17px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 10px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-summary {
  font-size: 14px;
  color: #909399;
  line-height: 1.6;
  height: 44px;
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
}

.article-author {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #606266;
}

.article-stats {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #909399;
}

.article-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #ebeef5;
}

.sidebar-title .el-icon {
  color: #409eff;
}

.hot-list {
  display: flex;
  flex-direction: column;
}

.hot-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f5f7fa;
  cursor: pointer;
  transition: all 0.3s;
}

.hot-item:last-child {
  border-bottom: none;
}

.hot-item:hover {
  background: #f5f7fa;
  margin: 0 -20px;
  padding-left: 20px;
  padding-right: 20px;
}

.hot-rank {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  background: #e4e7ed;
  color: #909399;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.hot-rank.top {
  background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);
  color: #fff;
}

.hot-info {
  flex: 1;
  min-width: 0;
}

.hot-info h4 {
  font-size: 14px;
  color: #303133;
  line-height: 1.4;
  margin-bottom: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.hot-meta {
  font-size: 12px;
  color: #909399;
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
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
  color: #606266;
}

.category-item:hover {
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

@media (max-width: 1200px) {
  .article-grid {
    grid-template-columns: 1fr;
  }
}

.pagination-container {
  margin-top: 32px;
  display: flex;
  justify-content: center;
}

@media (max-width: 768px) {
  .hero-content {
    padding: 24px;
  }
  
  .hero-content h2 {
    font-size: 22px;
  }
}
</style>
