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
import { ArrowLeft, Search, Close } from '@element-plus/icons-vue'
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
