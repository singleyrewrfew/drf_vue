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
                  查看更多
                  <el-icon><ArrowRight /></el-icon>
                </el-button>
              </div>

              <ArticleList
                :articles="latestArticles"
                :loading="loading && isInitialLoad"
                mode="grid"
                :page-size="pageSize"
                empty-text="暂无文章"
              />

              <div class="pagination-container">
                <WinPagination
                  v-model:current-page="currentPage"
                  v-model:page-size="pageSize"
                  :page-sizes="[4, 8, 12, 16]"
                  :total="total"
                  :pager-count="5"
                  @size-change="handleSizeChange"
                  @current-change="handleCurrentChange"
                />
              </div>
            </section>
          </el-col>

          <el-col :span="7">
            <div class="sidebar">
              <SidebarHotArticles :articles="hotArticles" />
              <SidebarCategories :categories="categories" />
              <SidebarTags :tags="tags" />
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { User, View, Calendar, Document, ArrowRight, Star } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getContents, getCategories, getTags } from '@/api/content'
import { ArticleList } from '@/components/common'
import { SidebarHotArticles, SidebarCategories, SidebarTags } from '@/components/sidebar'
import WinPagination from '@/components/WinPagination.vue'
import { getCoverUrl, getArticleUrl, formatDate } from '@/utils'

const router = useRouter()

const featuredContents = ref([])
const latestArticles = ref([])
const hotArticles = ref([])
const categories = ref([])
const tags = ref([])
const currentPage = ref(1)
const pageSize = ref(4)
const total = ref(0)
const loading = ref(true)
const isInitialLoad = ref(true)

const fetchData = async () => {
  loading.value = true
  try {
    const offset = (currentPage.value - 1) * pageSize.value
    const [featuredRes, latestRes, hotRes, catRes, tagRes] = await Promise.all([
      getContents({ status: 'published', limit: 5 }),
      getContents({ status: 'published', offset: offset, limit: pageSize.value }),
      getContents({ status: 'published', ordering: '-view_count', limit: 8 }),
      getCategories(),
      getTags(),
    ])

    // 统一处理分页数据和非分页数据
    const extractData = (response) => {
      if (response.results) {
        return response.results
      } else if (Array.isArray(response)) {
        return response
      }
      console.warn('Unexpected data format:', response)
      return []
    }

    featuredContents.value = extractData(featuredRes.data)
    latestArticles.value = extractData(latestRes.data)
    total.value = latestRes.data.count || 0
    hotArticles.value = extractData(hotRes.data)
    categories.value = extractData(catRes.data)
    tags.value = extractData(tagRes.data)
  } catch (e) {
    console.error('Failed to fetch data:', e)
    if (e.response?.status !== 401) {
      ElMessage.error('加载数据失败，请刷新页面重试')
    }
    // 重置状态以便下次加载
    featuredContents.value = []
    latestArticles.value = []
    hotArticles.value = []
    categories.value = []
    tags.value = []
  } finally {
    loading.value = false
    isInitialLoad.value = false
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

// 监听路由变化，确保从其他页面返回时重新加载数据
router.afterEach((to, from) => {
  if (to.path === '/' && from.path !== '/') {
    // 从其他页面跳转到首页时重置状态
    currentPage.value = 1
    pageSize.value = 4
    total.value = 0
    featuredContents.value = []
    latestArticles.value = []
    hotArticles.value = []
    categories.value = []
    tags.value = []
    isInitialLoad.value = true
    fetchData()
  }
})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: var(--bg-color);
}

.hero-section {
  background: var(--card-bg);
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
  border-radius: var(--radius-sm) !important;
  background: var(--primary-color) !important;
  color: #fff !important;
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
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  background: var(--primary-color);
  border: none;
  color: #fff;
  transition: all var(--transition-fast);
}

.section-header .el-button:hover {
  background: var(--primary-hover);
}

.section-header .el-button .el-icon {
  transition: transform var(--transition-fast);
}

.section-header .el-button:hover .el-icon {
  transform: translateX(4px);
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.pagination-container {
  margin-top: 40px;
  display: flex;
  justify-content: center;
}

@media (max-width: 992px) {
  .el-col-17 {
    max-width: 100%;
    flex: 0 0 100%;
  }

  .el-col-7 {
    display: none;
  }
}

@media (max-width: 768px) {
  .hero-section {
    margin-bottom: 20px;
  }

  .hero-section :deep(.el-carousel) {
    height: 300px !important;
  }

  .hero-content {
    padding: 24px 20px;
  }

  .hero-content h2 {
    font-size: 22px;
    margin: 12px 0 8px;
  }

  .hero-content p {
    font-size: 14px;
    -webkit-line-clamp: 2;
  }

  .hero-meta {
    gap: 16px;
    font-size: 12px;
    margin-top: 12px;
  }

  .recommend-tag {
    font-size: 12px;
    padding: 4px 10px !important;
  }

  .main-content {
    padding: 0 0 32px;
  }

  .container {
    padding: 0 16px;
  }

  .section-header {
    margin-bottom: 16px;
    padding-bottom: 12px;
  }

  .section-header h2 {
    font-size: 18px;
  }

  .section-header .el-button {
    font-size: 13px;
    padding: 6px 12px;
  }

  .pagination-container {
    margin-top: 24px;
  }
}

@media (max-width: 576px) {
  .hero-section :deep(.el-carousel) {
    height: 240px !important;
  }

  .hero-content {
    padding: 20px 16px;
  }

  .hero-content h2 {
    font-size: 18px;
  }

  .hero-content p {
    display: none;
  }

  .hero-meta {
    gap: 12px;
  }

  .hero-meta span:nth-child(n+3) {
    display: none;
  }
}
</style>
