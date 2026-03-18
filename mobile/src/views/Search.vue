<template>
  <div class="page">
    <header class="page-header">
      <div class="header-left">
        <button class="btn-back" @click="$router.back()">
          <el-icon><ArrowLeft /></el-icon>
        </button>
      </div>
      <div class="search-bar">
        <el-icon class="search-bar-icon"><Search /></el-icon>
        <input 
          v-model="keyword"
          class="search-bar-input"
          placeholder="搜索文章内容"
          @keyup.enter="handleSearch"
        />
        <button v-if="keyword" class="clear-btn" @click="handleClear">
          <el-icon><Close /></el-icon>
        </button>
      </div>
      <div class="header-right"></div>
    </header>
    
    <div class="page-content">
      <div v-if="loading && !results.length" class="feed-list">
        <Skeleton v-for="i in 5" :key="i" type="card-image" />
      </div>
      
      <template v-else-if="searched">
        <div v-if="results.length" class="feed-list">
          <router-link 
            v-for="article in results" 
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
        
        <div v-else class="empty-state">
          <el-icon class="empty-state-icon"><Search /></el-icon>
          <p class="empty-state-text">没有找到相关内容</p>
          <p class="empty-state-hint">换个关键词试试</p>
        </div>
      </template>
      
      <div v-else class="search-suggest">
        <p class="suggest-title">热门搜索</p>
        <div class="suggest-tags">
          <button 
            v-for="(tag, index) in hotTags" 
            :key="index" 
            class="suggest-tag"
            @click="searchTag(tag)"
          >
            {{ tag }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Search, Close, View, ChatDotRound, Star } from '@element-plus/icons-vue'
import { searchContents } from '@/api/content'
import { getCoverUrl, truncateText, formatRelativeTime } from '@/utils'
import Skeleton from '@/components/Skeleton.vue'

const route = useRoute()
const router = useRouter()

const keyword = ref('')
const loading = ref(false)
const searched = ref(false)
const results = ref([])
const total = ref(0)

const hotTags = ['Vue', 'React', 'Python', 'Django', '前端', '后端', '面试', '职场']

const handleSearch = async () => {
  if (!keyword.value.trim()) return
  
  loading.value = true
  searched.value = true
  
  try {
    const { data } = await searchContents(keyword.value)
    results.value = data.results || data
    total.value = data.count || results.value.length
    router.replace({ query: { q: keyword.value } })
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const handleClear = () => {
  keyword.value = ''
  results.value = []
  searched.value = false
  total.value = 0
  router.replace({ query: {} })
}

const searchTag = (tag) => {
  keyword.value = tag
  handleSearch()
}

onMounted(() => {
  if (route.query.q) {
    keyword.value = route.query.q
    handleSearch()
  }
})
</script>

<style scoped>
.clear-btn {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-tertiary);
  margin-left: 8px;
}

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

.empty-state-hint {
  font-size: 12px;
  color: var(--text-placeholder);
  margin-top: 8px;
}

.search-suggest {
  padding: 16px;
}

.suggest-title {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 16px;
}

.suggest-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.suggest-tag {
  padding: 8px 16px;
  background: var(--bg-secondary);
  border-radius: var(--radius-full);
  font-size: 13px;
  color: var(--text-secondary);
}

.suggest-tag:active {
  background: var(--bg-tertiary);
}
</style>
