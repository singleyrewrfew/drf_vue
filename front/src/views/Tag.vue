<template>
  <div class="tag-page">
    <div class="container">
      <PageHeader :title="`标签：${tag.name || ''}`" :count="total" />

      <ArticleList
        :articles="articles"
        :loading="loading"
        mode="horizontal"
        :page-size="pageSize"
        :empty-text="该标签下暂无文章"
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
import { getTag, getContents } from '@/api/content'
import { PageHeader, ArticleList } from '@/components/common'

const route = useRoute()

const loading = ref(false)
const tag = ref({})
const articles = ref([])
const page = ref(1)
const pageSize = ref(4)
const total = ref(0)

const fetchData = async () => {
  loading.value = true
  try {
    const offset = (page.value - 1) * pageSize.value
    const tagId = route.params.id_or_slug
    const [tagRes, contentRes] = await Promise.all([
      getTag(tagId),
      getContents({
        status: 'published',
        tag: tagId,
        offset: offset,
        limit: pageSize.value,
      }),
    ])
    tag.value = tagRes.data
    articles.value = contentRes.data.results || contentRes.data
    total.value = contentRes.data.count || articles.value.length
  } catch (e) {
    console.error(e)
    if (e.response?.status !== 401) {
      ElMessage.error('加载标签失败')
    }
  } finally {
    loading.value = false
  }
}

watch(() => route.params.id_or_slug, fetchData, { immediate: true })
</script>

<style scoped>
.tag-page {
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
  .tag-page {
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
