<template>
  <div class="page home-page">
    <header class="page-header">
      <h1 class="logo">CMS</h1>
      <div class="search-bar" @click="$router.push('/search')">
        <el-icon class="search-bar-icon"><Search /></el-icon>
        <span class="search-placeholder">搜索文章内容</span>
      </div>
      <button class="btn-icon" @click="handleTheme">
        <el-icon><Sunny v-if="themeStore.theme === 'dark'" /><Moon v-else /></el-icon>
      </button>
    </header>
    
    <nav class="tab-bar">
      <button 
        v-for="tab in tabs" 
        :key="tab.key"
        class="tab-item"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </nav>
    
    <div class="page-content">
      <div v-if="loading" class="feed-list">
        <Skeleton v-for="i in 5" :key="i" type="card-image" />
      </div>
      
      <div v-else-if="articles.length" class="feed-list">
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
      
      <div v-else class="empty-state">
        <el-icon class="empty-state-icon"><Document /></el-icon>
        <p class="empty-state-text">暂无内容</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Search, Sunny, Moon, Document } from '@element-plus/icons-vue'
import { getContents } from '@/api/content'
import { getCoverUrl, truncateText, formatRelativeTime } from '@/utils'
import { useThemeStore } from '@/stores/theme'
import Skeleton from '@/components/Skeleton.vue'

const themeStore = useThemeStore()

const tabs = [
  { key: 'recommend', label: '推荐' },
  { key: 'hot', label: '热门' },
]

const activeTab = ref('recommend')
const loading = ref(true)
const articles = ref([])

const fetchArticles = async () => {
  loading.value = true
  try {
    const params = { page_size: 10 }
    if (activeTab.value === 'hot') {
      params.ordering = '-views_count'
    }
    const { data } = await getContents(params)
    articles.value = data.results || data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const handleTheme = () => {
  themeStore.toggleTheme()
}

watch(activeTab, fetchArticles)
onMounted(fetchArticles)
</script>

<style scoped>
.home-page .page-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: var(--z-sticky);
  gap: 12px;
}

.home-page .page-content {
  padding-top: calc(var(--header-height) + 44px);
}

.logo {
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-color);
  margin: 0;
  flex-shrink: 0;
}

.home-page .search-bar {
  flex: 1;
  min-width: 0;
}

.home-page .btn-icon {
  flex-shrink: 0;
}

.search-placeholder {
  color: var(--text-placeholder);
  font-size: 14px;
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
</style>
