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
            <div class="feed-header">
              <span class="feed-author-name">{{ article.author_name || '匿名用户' }}</span>
              <span class="feed-dot">·</span>
              <span class="feed-time">{{ formatRelativeTime(article.created_at) }}</span>
              <span v-if="article.category_name" class="feed-category">{{ article.category_name }}</span>
            </div>
            
            <div class="feed-body">
              <div class="feed-content">
                <h3 class="feed-title">{{ article.title }}</h3>
                <p v-if="article.summary || article.content" class="feed-excerpt">
                  {{ truncateText(article.summary || article.content, 100) }}
                </p>
              </div>
              <img 
                v-if="article.cover_image" 
                :src="getCoverUrl(article.cover_image)" 
                class="feed-image"
                loading="lazy"
              />
            </div>
            
            <div class="feed-footer">
              <span v-if="article.views_count" class="feed-stat">
                <el-icon><View /></el-icon>
                {{ article.views_count }}
              </span>
              <span v-if="article.comments_count" class="feed-stat">
                <el-icon><ChatDotRound /></el-icon>
                {{ article.comments_count }}
              </span>
              <span v-if="article.likes_count" class="feed-stat">
                <el-icon><Star /></el-icon>
                {{ article.likes_count }}
              </span>
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
import { Search, Document, Loading, View, ChatDotRound, Star } from '@element-plus/icons-vue'
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
  background: var(--bg-color);
}

.feed-card {
  display: block;
  text-decoration: none;
  background: var(--card-bg);
  margin-bottom: 10px;
  border-radius: var(--radius-md);
  overflow: hidden;
}

.feed-header {
  display: flex;
  align-items: center;
  padding: 12px 16px 8px;
  font-size: 12px;
  color: var(--text-tertiary);
}

.feed-author-name {
  color: var(--text-secondary);
  font-weight: 500;
}

.feed-dot {
  margin: 0 4px;
}

.feed-category {
  margin-left: auto;
  color: var(--primary-color);
  background: var(--primary-bg);
  padding: 2px 8px;
  border-radius: var(--radius-full);
  font-size: 11px;
}

.feed-body {
  display: flex;
  padding: 0 16px 12px;
  gap: 12px;
}

.feed-content {
  flex: 1;
  min-width: 0;
}

.feed-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.5;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.feed-excerpt {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin: 0;
}

.feed-image {
  width: 100px;
  height: 75px;
  object-fit: cover;
  border-radius: var(--radius-sm);
  flex-shrink: 0;
}

.feed-footer {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 0 16px 12px;
  font-size: 12px;
  color: var(--text-tertiary);
}

.feed-stat {
  display: flex;
  align-items: center;
  gap: 4px;
}

.feed-stat .el-icon {
  font-size: 14px;
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
