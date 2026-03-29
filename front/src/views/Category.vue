<template>
  <div class="category-page">
    <div class="container">
      <PageHeader :title="category.name || '分类'" :count="total" />

      <ArticleList
        :articles="articles"
        :loading="loading"
        mode="horizontal"
        :page-size="pageSize"
        empty-text="该分类下暂无文章"
      />

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
import { ElMessage } from 'element-plus'
import { getCategory, getContents } from '@/api/content'
import { PageHeader, ArticleList } from '@/components/common'

const route = useRoute()

const loading = ref(false)
const category = ref({})
const articles = ref([])
const page = ref(1)
const pageSize = ref(4)
const total = ref(0)

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
  padding: 32px 0;
  background: var(--bg-color);
  min-height: calc(100vh - var(--header-height) - 200px);
}

.container {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 24px;
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

@media (max-width: 768px) {
  .category-page {
    padding: 16px 0;
  }

  .container {
    padding: 0 16px;
  }

  .pagination-container {
    margin-top: 24px;
  }
}
</style>
