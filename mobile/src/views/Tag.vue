<template>
  <div class="page">
    <PageHeader :title="tag?.name || '标签'" />
    
    <div class="page-content">
      <div v-if="loading" class="feed-list">
        <Skeleton v-for="i in 5" :key="i" type="card-image" />
      </div>
      
      <template v-else-if="articles.length">
        <div class="feed-list">
          <ArticleCard 
            v-for="article in articles" 
            :key="article.id" 
            :article="article"
          />
        </div>
      </template>
      
      <EmptyState v-else />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getTag, getContents } from '@/api/content'
import Skeleton from '@/components/Skeleton.vue'
import ArticleCard from '@/components/ArticleCard.vue'
import EmptyState from '@/components/EmptyState.vue'
import PageHeader from '@/components/PageHeader.vue'

const route = useRoute()
const loading = ref(true)
const tag = ref(null)
const articles = ref([])

const fetchData = async () => {
  loading.value = true
  try {
    const id = route.params.id_or_slug
    const [tagRes, articlesRes] = await Promise.all([
      getTag(id),
      getContents({ tag: id, page_size: 20 })
    ])
    tag.value = tagRes.data
    articles.value = articlesRes.data.results || articlesRes.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

watch(() => route.params.id_or_slug, fetchData)
onMounted(fetchData)
</script>

<style scoped>
.feed-list {
  background: var(--bg-color);
}
</style>
