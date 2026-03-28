<template>
  <div class="search-page">
    <div class="container">
      <PageHeader :title="`搜索结果：${keyword}`" :count="total" count-label="篇相关文章" />

      <ArticleList
        :articles="articles"
        :loading="loading"
        mode="horizontal"
        :page-size="pageSize"
        :empty-text="未找到相关文章"
        :highlight-keyword="keyword"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { searchContents } from '@/api/content'
import { PageHeader, ArticleList } from '@/components/common'

const route = useRoute()

const loading = ref(false)
const articles = ref([])
const total = ref(0)
const pageSize = ref(10)
const keyword = ref('')

const fetchArticles = async () => {
  keyword.value = route.query.q || ''
  if (!keyword.value) {
    articles.value = []
    total.value = 0
    return
  }

  loading.value = true
  try {
    const { data } = await searchContents(keyword.value)
    articles.value = data.results || data
    total.value = data.count || articles.value.length
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

watch(() => route.query.q, fetchArticles, { immediate: true })
</script>

<style scoped>
.search-page {
  padding: 32px 0;
  background: var(--bg-color);
  min-height: calc(100vh - var(--header-height) - 200px);
}

.container {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 24px;
}

@media (max-width: 768px) {
  .search-page {
    padding: 16px 0;
  }

  .container {
    padding: 0 16px;
  }
}
</style>
