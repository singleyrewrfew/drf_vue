<template>
  <div class="page">
    <header class="page-header">
      <div class="header-left">
        <button class="btn-back" @click="$router.back()">
          <el-icon><ArrowLeft /></el-icon>
        </button>
      </div>
      <h1 class="page-title">#{{ tag?.name || '标签' }}</h1>
      <div class="header-right"></div>
    </header>
    
    <div class="page-content">
      <div v-if="loading" class="article-list">
        <div v-for="i in 3" :key="i" class="skeleton-card">
          <div class="skeleton skeleton-cover"></div>
          <div class="skeleton skeleton-title"></div>
          <div class="skeleton skeleton-text"></div>
        </div>
      </div>
      
      <div v-else-if="articles.length" class="article-list">
        <router-link 
          v-for="article in articles" 
          :key="article.id" 
          :to="`/article/${article.slug || article.id}`"
          class="article-card"
        >
          <img 
            v-if="article.cover_image" 
            :src="getCoverUrl(article.cover_image)" 
            class="article-cover"
            loading="lazy"
          />
          <div class="article-content">
            <h3 class="article-title">{{ article.title }}</h3>
            <p class="article-excerpt">{{ truncateText(article.summary || article.content, 80) }}</p>
            <div class="article-meta">
              <span>{{ formatRelativeTime(article.created_at) }}</span>
            </div>
          </div>
        </router-link>
      </div>
      
      <div v-else class="empty-state">
        <el-icon class="empty-state-icon"><PriceTag /></el-icon>
        <p class="empty-state-text">该标签下暂无文章</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft, PriceTag } from '@element-plus/icons-vue'
import { getTag, getContents } from '@/api/content'
import { getCoverUrl, truncateText, formatRelativeTime } from '@/utils'

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

onMounted(fetchData)
</script>
