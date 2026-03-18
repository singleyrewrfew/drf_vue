<template>
  <div class="page search-page">
    <header class="page-header">
      <button class="btn-back" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
      </button>
      <div class="search-input-wrapper">
        <el-input 
          v-model="keyword"
          placeholder="搜索文章..."
          size="large"
          clearable
          @keyup.enter="handleSearch"
          @clear="handleClear"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
    </header>
    
    <div class="page-content">
      <div v-if="loading && !results.length" class="skeleton-list">
        <div v-for="i in 3" :key="i" class="skeleton-card">
          <div class="skeleton skeleton-cover"></div>
          <div class="skeleton skeleton-title"></div>
          <div class="skeleton skeleton-text"></div>
        </div>
      </div>
      
      <div v-else-if="searched && results.length" class="result-info">
        找到 {{ total }} 篇相关文章
      </div>
      
      <div v-if="results.length" class="article-list">
        <router-link 
          v-for="article in results" 
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
              <span class="article-date">{{ formatRelativeTime(article.created_at) }}</span>
            </div>
          </div>
        </router-link>
      </div>
      
      <div v-else-if="searched && !results.length" class="empty-state">
        <el-icon class="empty-state-icon"><Search /></el-icon>
        <p class="empty-state-text">未找到相关文章</p>
      </div>
      
      <div v-else class="empty-state">
        <el-icon class="empty-state-icon"><Search /></el-icon>
        <p class="empty-state-text">输入关键词搜索文章</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Search } from '@element-plus/icons-vue'
import { searchContents } from '@/api/content'
import { getCoverUrl, truncateText, formatRelativeTime } from '@/utils'

const route = useRoute()
const router = useRouter()

const keyword = ref('')
const loading = ref(false)
const searched = ref(false)
const results = ref([])
const total = ref(0)

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
  results.value = []
  searched.value = false
  total.value = 0
}

onMounted(() => {
  if (route.query.q) {
    keyword.value = route.query.q
    handleSearch()
  }
})
</script>

<style scoped>
.search-page {
  background: var(--bg-color);
}

.btn-back {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-primary);
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.btn-back:active {
  background: var(--bg-secondary);
}

.search-input-wrapper {
  flex: 1;
  margin-left: 8px;
}

.result-info {
  font-size: 13px;
  color: var(--text-tertiary);
  margin-bottom: 12px;
}

.skeleton-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skeleton-card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.skeleton-cover {
  height: 120px;
}

.skeleton-title {
  height: 18px;
  margin: 12px 12px 8px;
  border-radius: var(--radius-sm);
}

.skeleton-text {
  height: 14px;
  margin: 0 12px 12px;
  width: 60%;
  border-radius: var(--radius-sm);
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.article-card {
  display: flex;
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  overflow: hidden;
  text-decoration: none;
  transition: all var(--transition-fast);
}

.article-card:active {
  transform: scale(0.98);
}

.article-cover {
  width: 100px;
  height: 80px;
  object-fit: cover;
  flex-shrink: 0;
}

.article-content {
  flex: 1;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-width: 0;
}

.article-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
  margin: 0 0 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-excerpt {
  font-size: 12px;
  color: var(--text-tertiary);
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  color: var(--text-tertiary);
}
</style>
