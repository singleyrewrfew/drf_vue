<template>
  <div class="page article-page">
    <header class="page-header">
      <button class="btn-back" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
      </button>
      <h1 class="page-title">文章详情</h1>
      <div class="header-actions">
        <button class="btn-icon" @click="shareArticle">
          <el-icon><Share /></el-icon>
        </button>
      </div>
    </header>
    
    <div v-if="loading" class="page-content">
      <div class="skeleton skeleton-cover"></div>
      <div class="skeleton skeleton-title" style="margin: 16px; height: 24px;"></div>
      <div class="skeleton skeleton-text" style="margin: 0 16px; height: 16px;"></div>
    </div>
    
    <div v-else-if="article" class="page-content">
      <img 
        v-if="article.cover_image" 
        :src="getCoverUrl(article.cover_image)" 
        class="article-cover"
      />
      
      <div class="article-body">
        <h1 class="article-title">{{ article.title }}</h1>
        
        <div class="article-meta">
          <span class="meta-item">
            <el-icon><Calendar /></el-icon>
            {{ formatDate(article.created_at) }}
          </span>
          <span v-if="article.category_name" class="meta-item">
            <el-icon><Folder /></el-icon>
            {{ article.category_name }}
          </span>
          <span v-if="article.author_name" class="meta-item">
            <el-icon><User /></el-icon>
            {{ article.author_name }}
          </span>
        </div>
        
        <div v-if="article.tags && article.tags.length" class="article-tags">
          <router-link 
            v-for="tag in article.tags" 
            :key="tag.id || tag" 
            :to="`/tag/${tag.slug || tag.id || tag}`"
            class="tag"
          >
            #{{ tag.name || tag }}
          </router-link>
        </div>
        
        <div class="article-content" v-html="renderedContent"></div>
      </div>
    </div>
    
    <div v-else class="page-content">
      <div class="empty-state">
        <el-icon class="empty-state-icon"><Document /></el-icon>
        <p class="empty-state-text">文章不存在</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Share, Calendar, Folder, User, Document } from '@element-plus/icons-vue'
import { marked } from 'marked'
import { getContent, getContentBySlug } from '@/api/content'
import { getCoverUrl, formatDate } from '@/utils'

const route = useRoute()
const loading = ref(true)
const article = ref(null)

const renderedContent = computed(() => {
  if (!article.value?.content) return ''
  return marked(article.value.content)
})

const fetchArticle = async () => {
  loading.value = true
  try {
    const id = route.params.id
    const { data } = await getContent(id)
    article.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const shareArticle = async () => {
  if (navigator.share) {
    try {
      await navigator.share({
        title: article.value?.title,
        url: window.location.href
      })
    } catch (e) {
      console.log('Share cancelled')
    }
  } else {
    await navigator.clipboard.writeText(window.location.href)
    ElMessage.success('链接已复制')
  }
}

onMounted(() => {
  fetchArticle()
})
</script>

<style scoped>
.article-page {
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
}

.btn-back:active {
  background: var(--bg-secondary);
}

.header-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  transition: all var(--transition-fast);
}

.btn-icon:active {
  background: var(--bg-secondary);
}

.skeleton-cover {
  height: 200px;
  border-radius: 0;
}

.skeleton-title {
  border-radius: var(--radius-sm);
}

.skeleton-text {
  border-radius: var(--radius-sm);
}

.article-cover {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.article-body {
  padding: 16px;
}

.article-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.4;
  margin: 0 0 12px;
}

.article-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-tertiary);
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.tag {
  padding: 4px 10px;
  background: var(--primary-bg);
  color: var(--primary-color);
  border-radius: var(--radius-full);
  font-size: 12px;
  text-decoration: none;
}

.article-content {
  font-size: 15px;
  line-height: 1.8;
  color: var(--text-primary);
}

.article-content :deep(h1),
.article-content :deep(h2),
.article-content :deep(h3),
.article-content :deep(h4) {
  margin: 24px 0 12px;
  font-weight: 600;
}

.article-content :deep(p) {
  margin: 0 0 16px;
}

.article-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: var(--radius-md);
  margin: 12px 0;
}

.article-content :deep(pre) {
  background: var(--bg-secondary);
  padding: 12px;
  border-radius: var(--radius-md);
  overflow-x: auto;
  font-size: 13px;
}

.article-content :deep(code) {
  font-family: var(--font-mono);
  background: var(--bg-secondary);
  padding: 2px 6px;
  border-radius: var(--radius-xs);
  font-size: 13px;
}

.article-content :deep(blockquote) {
  border-left: 3px solid var(--primary-color);
  padding-left: 12px;
  margin: 16px 0;
  color: var(--text-secondary);
}

.article-content :deep(ul),
.article-content :deep(ol) {
  padding-left: 20px;
  margin: 12px 0;
}

.article-content :deep(a) {
  color: var(--primary-color);
}
</style>
