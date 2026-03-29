<template>
  <div class="articles-page">
    <div class="container">
      <PageHeader :icon="Document" title="文章列表" :count="total" />

      <el-row :gutter="24">
        <el-col :span="18">
          <ArticleList
            :articles="articles"
            :loading="loading"
            mode="horizontal"
            :page-size="pageSize"
            empty-text="暂无文章"
          >
            <template #empty-action>
              <el-button type="primary" @click="clearFilters">清除筛选</el-button>
            </template>
          </ArticleList>

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
            <SidebarCategories
              :categories="categories"
              :active-id="currentCategory"
              :selectable="true"
              @select="filterByCategory"
            />
            <SidebarTags :tags="tags" />
            <SidebarAuthors
              :authors="authors"
              :active-id="currentAuthor"
              @select="filterByAuthor"
            />
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Document } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getContents, getCategories, getTags } from '@/api/content'
import { getPopularAuthors } from '@/api/user'
import { PageHeader, ArticleList } from '@/components/common'
import { SidebarCategories, SidebarTags, SidebarAuthors } from '@/components/sidebar'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const userStore = useUserStore()

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
  // 只有已登录用户才获取热门作者
  if (!userStore.isLoggedIn) {
    authors.value = []
    return
  }
  
  try {
    const { data } = await getPopularAuthors()
    authors.value = data.results || data
  } catch (e) {
    // 401 错误表示用户未登录，这是正常情况，不打印错误
    if (e.response?.status !== 401) {
      console.error('Failed to fetch authors:', e)
    }
  }
}

const filterByCategory = (cat) => {
  currentCategory.value = currentCategory.value === cat.id ? null : cat.id
  page.value = 1
  fetchArticles()
}

const filterByAuthor = (author) => {
  currentAuthor.value = currentAuthor.value === author.id ? null : author.id
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

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: sticky;
  top: 96px;
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

@media (max-width: 992px) {
  .el-col-18 {
    max-width: 100%;
    flex: 0 0 100%;
  }

  .el-col-6 {
    display: none;
  }
}

@media (max-width: 768px) {
  .articles-page {
    padding: 16px 0;
  }

  .container {
    padding: 0 16px;
  }

  .pagination-container {
    margin-top: 24px;
  }

  .pagination-container :deep(.el-pagination) {
    flex-wrap: wrap;
    gap: 8px;
  }
}
</style>
