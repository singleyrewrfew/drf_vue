<template>
  <div class="page">
    <header class="page-header">
      <div class="header-left"></div>
      <h1 class="page-title">发现</h1>
      <div class="header-right">
        <button class="btn-icon" @click="$router.push('/search')">
          <el-icon><Search /></el-icon>
        </button>
      </div>
    </header>
    
    <div class="page-content">
      <div v-if="loading && !articles.length" class="feed-list">
        <Skeleton v-for="i in 5" :key="i" type="card-image" />
      </div>
      
      <template v-else-if="articles.length">
        <div class="feed-list">
          <router-link 
            v-for="article in articles" 
            :key="article.id" 
            :to="`/article/${article.slug || article.id}`"
            class="feed-card"
          >
            <h3 class="feed-title">{{ article.title }}</h3>
            
            <p v-if="article.summary || article.content" class="feed-excerpt">
              {{ truncateText(article.summary || article.content, 120) }}
            </p>
            
            <img 
              v-if="article.cover_image" 
              :src="getCoverUrl(article.cover_image)" 
              class="feed-image-single"
              loading="lazy"
            />
            
            <div class="feed-meta">
              <span class="feed-author-name">{{ article.author_name || '匿名用户' }}</span>
              <span>{{ formatRelativeTime(article.created_at) }}</span>
            </div>
          </router-link>
        </div>
        
        <div v-if="hasMore" class="loading-more">
          <template v-if="loadingMore">
            <el-icon class="loading-icon"><Loading /></el-icon>
            <span>加载中...</span>
          </template>
          <button v-else class="btn btn-secondary btn-block" @click="loadMore">
            加载更多
          </button>
        </div>
      </template>
      
      <div v-else class="empty-state">
        <el-icon class="empty-state-icon"><Document /></el-icon>
        <p class="empty-state-text">暂无内容</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, Document, Loading } from '@element-plus/icons-vue'
import { getContents } from '@/api/content'
import { getCoverUrl, truncateText, formatRelativeTime } from '@/utils'
import Skeleton from '@/components/Skeleton.vue'

const loading = ref(true)
const loadingMore = ref(false)
const articles = ref([])
const page = ref(1)
const hasMore = ref(true)

const fetchArticles = async (isLoadMore = false) => {
  if (isLoadMore) loadingMore.value = true
  else loading.value = true
  
  try {
    const { data } = await getContents({ page: page.value, page_size: 10 })
    const results = data.results || data
    articles.value = isLoadMore ? [...articles.value, ...results] : results
    hasMore.value = data.next || results.length >= 10
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

const loadMore = () => {
  page.value++
  fetchArticles(true)
}

onMounted(() => fetchArticles())
</script>

<style scoped>
.feed-list {
  background: var(--card-bg);
}

.feed-card {
  display: block;
  text-decoration: none;
}

.feed-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: var(--text-tertiary);
}

.feed-author-name {
  color: var(--text-secondary);
}

.loading-more {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  color: var(--text-tertiary);
  font-size: 13px;
}

.loading-icon {
  animation: spin 1s linear infinite;
  margin-right: 8px;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
