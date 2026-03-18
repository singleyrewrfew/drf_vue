<template>
  <div class="page">
    <header class="page-header">
      <div class="header-left">
        <button class="btn-back" @click="$router.back()">
          <el-icon><ArrowLeft /></el-icon>
        </button>
      </div>
      <h1 class="page-title">详情</h1>
      <div class="header-right">
        <button class="btn-icon" @click="shareArticle">
          <el-icon><Share /></el-icon>
        </button>
      </div>
    </header>
    
    <div v-if="loading" class="page-content" style="padding: 0;">
      <Skeleton type="article" />
    </div>
    
    <div v-else-if="article" class="page-content" style="padding: 0;">
      <div class="article-header">
        <h1 class="article-title">{{ article.title }}</h1>
        
        <div class="article-author">
          <el-avatar :size="40" :src="getAvatarUrl(article.author_avatar)">
            {{ article.author_name?.charAt(0) }}
          </el-avatar>
          <div class="author-info">
            <span class="author-name">{{ article.author_name || '匿名用户' }}</span>
            <span class="article-time">{{ formatRelativeTime(article.created_at) }}</span>
          </div>
        </div>
      </div>
      
      <div v-if="article.cover_image" class="article-cover">
        <img :src="getCoverUrl(article.cover_image)" alt="" loading="lazy" />
      </div>
      
      <div class="article-body markdown-body" v-html="renderedContent"></div>
      
      <div v-if="article.tags?.length" class="article-tags">
        <router-link 
          v-for="tag in article.tags" 
          :key="tag.id || tag" 
          :to="`/tag/${tag.slug || tag.id || tag}`"
          class="tag"
        >
          {{ tag.name || tag }}
        </router-link>
      </div>
      
      <button 
        v-if="tocItems.length" 
        class="toc-fab" 
        @click="showToc = true"
        title="目录"
      >
        <el-icon><List /></el-icon>
      </button>
    </div>
    
    <div v-else class="page-content">
      <div class="empty-state">
        <el-icon class="empty-state-icon"><Document /></el-icon>
        <p class="empty-state-text">内容不存在或已删除</p>
      </div>
    </div>
    
    <el-drawer
      v-model="showToc"
      direction="rtl"
      size="70%"
      title="目录"
      :with-header="true"
    >
      <div class="toc-list">
        <a
          v-for="item in tocItems"
          :key="item.id"
          class="toc-item"
          :class="{ active: activeTocId === item.id }"
          :style="{ paddingLeft: (item.level - 1) * 12 + 16 + 'px' }"
          @click="scrollToHeading(item.id)"
        >
          {{ item.text }}
        </a>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Share, Document, List } from '@element-plus/icons-vue'
import { marked } from 'marked'
import hljs from 'highlight.js'
import { getContent } from '@/api/content'
import { getCoverUrl, getAvatarUrl, formatRelativeTime } from '@/utils'
import Skeleton from '@/components/Skeleton.vue'

const route = useRoute()
const loading = ref(true)
const article = ref(null)
const showToc = ref(false)
const tocItems = ref([])
const activeTocId = ref('')

let headingIdCounter = 0

const renderer = new marked.Renderer()

renderer.image = ({ href, title, text }) => {
  return `<img src="${href}" alt="${text || ''}" loading="lazy" />`
}

renderer.code = ({ text, lang }) => {
  const code = text || ''
  let language = lang || ''
  let highlighted
  
  if (language && hljs.getLanguage(language)) {
    highlighted = hljs.highlight(code, { language }).value
  } else {
    highlighted = hljs.highlightAuto(code).value
    language = highlighted.language || 'plaintext'
  }
  
  return `<pre class="code-block"><code class="hljs language-${language}">${highlighted}</code></pre>`
}

renderer.heading = ({ text, depth }) => {
  const id = `heading-${headingIdCounter++}`
  return `<h${depth} id="${id}">${text}</h${depth}>`
}

marked.setOptions({ renderer })

const renderedContent = computed(() => {
  if (!article.value?.content) return ''
  headingIdCounter = 0
  tocItems.value = []
  
  const html = marked(article.value.content)
  
  const headingRegex = /<h([1-6]) id="([^"]+)">([^<]+)<\/h\1>/g
  let match
  while ((match = headingRegex.exec(html)) !== null) {
    tocItems.value.push({
      level: parseInt(match[1]),
      id: match[2],
      text: match[3]
    })
  }
  
  return html
})

const scrollToHeading = (id) => {
  showToc.value = false
  const el = document.getElementById(id)
  if (el) {
    const pageContent = document.querySelector('.page-content')
    const headerOffset = 60
    const elementPosition = el.offsetTop
    
    if (pageContent) {
      pageContent.scrollTo({
        top: elementPosition - headerOffset,
        behavior: 'smooth'
      })
    }
    activeTocId.value = id
  }
}

const updateActiveToc = () => {
  const pageContent = document.querySelector('.page-content')
  if (!pageContent) return
  
  const scrollTop = pageContent.scrollTop + 80
  let currentId = ''
  
  for (const item of tocItems.value) {
    const el = document.getElementById(item.id)
    if (el && el.offsetTop <= scrollTop) {
      currentId = item.id
    }
  }
  
  activeTocId.value = currentId
}

watch(() => article.value, async () => {
  if (article.value) {
    await nextTick()
    const pageContent = document.querySelector('.page-content')
    if (pageContent) {
      pageContent.addEventListener('scroll', updateActiveToc)
    }
  }
})

const fetchArticle = async () => {
  loading.value = true
  try {
    const { data } = await getContent(route.params.id)
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
    }
  } else {
    await navigator.clipboard.writeText(window.location.href)
    ElMessage.success('链接已复制')
  }
}

onMounted(fetchArticle)
</script>

<style scoped>
.article-header {
  padding: 16px;
  padding-bottom: 0;
}

.article-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.5;
  margin: 0 0 16px;
}

.article-author {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.author-name {
  font-size: 15px;
  font-weight: 500;
  color: var(--text-primary);
}

.article-time {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-top: 2px;
}

.article-cover {
  margin: 16px 0;
}

.article-cover img {
  width: 100%;
  display: block;
}

.article-body {
  padding: 16px;
  padding-bottom: 0;
}

.article-tags {
  padding: 16px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.markdown-body {
  font-size: 15px;
  line-height: 1.8;
  color: var(--text-primary);
  word-break: break-word;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4),
.markdown-body :deep(h5),
.markdown-body :deep(h6) {
  margin-top: 24px;
  margin-bottom: 12px;
  font-weight: 600;
  line-height: 1.4;
  color: var(--text-primary);
}

.markdown-body :deep(h1) { font-size: 20px; }
.markdown-body :deep(h2) { font-size: 18px; }
.markdown-body :deep(h3) { font-size: 16px; }
.markdown-body :deep(h4) { font-size: 15px; }

.markdown-body :deep(p) {
  margin-bottom: 16px;
}

.markdown-body :deep(a) {
  color: var(--primary-color);
}

.markdown-body :deep(img) {
  max-width: 100%;
  border-radius: var(--radius-md);
  margin: 12px 0;
}

.markdown-body :deep(.code-block) {
  background: #282c34;
  padding: 16px;
  border-radius: var(--radius-md);
  overflow-x: auto;
  margin: 16px 0;
  -webkit-overflow-scrolling: touch;
}

.markdown-body :deep(.code-block code) {
  font-family: var(--font-mono);
  font-size: 13px;
  line-height: 1.6;
  color: #abb2bf;
  background: transparent;
  padding: 0;
}

.markdown-body :deep(pre) {
  background: var(--bg-secondary);
  padding: 12px;
  border-radius: var(--radius-md);
  overflow-x: auto;
  margin: 12px 0;
}

.markdown-body :deep(code) {
  font-family: var(--font-mono);
  font-size: 13px;
}

.markdown-body :deep(p code) {
  background: var(--bg-secondary);
  padding: 2px 6px;
  border-radius: var(--radius-sm);
}

.markdown-body :deep(blockquote) {
  border-left: 3px solid var(--primary-color);
  padding-left: 12px;
  margin: 12px 0;
  color: var(--text-secondary);
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 20px;
  margin: 12px 0;
}

.markdown-body :deep(li) {
  margin-bottom: 6px;
}

.markdown-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
  display: block;
  overflow-x: auto;
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  border: 1px solid var(--border-color);
  padding: 8px 12px;
  text-align: left;
}

.markdown-body :deep(th) {
  background: var(--bg-secondary);
  font-weight: 500;
}

.markdown-body :deep(hr) {
  border: none;
  height: 1px;
  background: var(--border-color);
  margin: 20px 0;
}

.markdown-body :deep(strong),
.markdown-body :deep(b) {
  font-weight: 600;
  color: var(--text-primary);
}

.markdown-body :deep(em),
.markdown-body :deep(i) {
  font-style: italic;
}

.markdown-body :deep(del),
.markdown-body :deep(s) {
  text-decoration: line-through;
  color: var(--text-tertiary);
}

.markdown-body :deep(mark) {
  background: #fff3b0;
  padding: 2px 4px;
  border-radius: 2px;
}

:global(.dark) .markdown-body :deep(mark),
:global([data-theme="dark"]) .markdown-body :deep(mark) {
  background: #5c4a00;
}

.markdown-body :deep(kbd) {
  display: inline-block;
  padding: 2px 6px;
  font-size: 12px;
  font-family: var(--font-mono);
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  box-shadow: inset 0 -1px 0 var(--border-color);
}

.markdown-body :deep(sup),
.markdown-body :deep(sub) {
  font-size: 0.75em;
  vertical-align: baseline;
  position: relative;
  top: -0.5em;
}

.markdown-body :deep(sub) {
  top: 0.2em;
}

.markdown-body :deep(details) {
  margin: 12px 0;
  padding: 12px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.markdown-body :deep(summary) {
  cursor: pointer;
  font-weight: 500;
  color: var(--text-primary);
}

.markdown-body :deep(details[open] summary) {
  margin-bottom: 12px;
}

.markdown-body :deep(ul) {
  list-style-type: disc;
}

.markdown-body :deep(ol) {
  list-style-type: decimal;
}

.markdown-body :deep(ul ul) {
  list-style-type: circle;
}

.markdown-body :deep(ul ul ul) {
  list-style-type: square;
}

.markdown-body :deep(.task-list-item) {
  list-style: none;
  margin-left: -20px;
}

.markdown-body :deep(.task-list-item input) {
  margin-right: 8px;
  vertical-align: middle;
}

.markdown-body :deep(abbr) {
  border-bottom: 1px dotted var(--text-tertiary);
  cursor: help;
}

.markdown-body :deep(pre code) {
  background: transparent;
  padding: 0;
}

.markdown-body :deep(figure) {
  margin: 16px 0;
}

.markdown-body :deep(figcaption) {
  font-size: 12px;
  color: var(--text-tertiary);
  text-align: center;
  margin-top: 8px;
}

.markdown-body :deep(.hljs-keyword),
.markdown-body :deep(.hljs-selector-tag),
.markdown-body :deep(.hljs-built_in) {
  color: #c678dd;
}

.markdown-body :deep(.hljs-string),
.markdown-body :deep(.hljs-title),
.markdown-body :deep(.hljs-section),
.markdown-body :deep(.hljs-attribute) {
  color: #98c379;
}

.markdown-body :deep(.hljs-number),
.markdown-body :deep(.hljs-literal),
.markdown-body :deep(.hljs-variable) {
  color: #d19a66;
}

.markdown-body :deep(.hljs-comment),
.markdown-body :deep(.hljs-quote) {
  color: #5c6370;
  font-style: italic;
}

.markdown-body :deep(.hljs-function) {
  color: #61afef;
}

.markdown-body :deep(.hljs-params) {
  color: #abb2bf;
}

.markdown-body :deep(.hljs-class .hljs-title),
.markdown-body :deep(.hljs-type) {
  color: #e5c07b;
}

.markdown-body :deep(.hljs-tag),
.markdown-body :deep(.hljs-name) {
  color: #e06c75;
}

.markdown-body :deep(.hljs-attr) {
  color: #d19a66;
}

.markdown-body :deep(.hljs-symbol),
.markdown-body :deep(.hljs-bullet) {
  color: #61afef;
}

.markdown-body :deep(.hljs-meta) {
  color: #61afef;
}

.markdown-body :deep(.hljs-addition) {
  background: rgba(152, 195, 121, 0.15);
  color: #98c379;
}

.markdown-body :deep(.hljs-deletion) {
  background: rgba(224, 108, 117, 0.15);
  color: #e06c75;
}

.markdown-body :deep(.hljs-emphasis) {
  font-style: italic;
}

.markdown-body :deep(.hljs-strong) {
  font-weight: bold;
}

.toc-list {
  padding: 0;
}

.toc-item {
  display: block;
  padding: 12px 16px;
  font-size: 14px;
  color: var(--text-secondary);
  text-decoration: none;
  border-left: 2px solid transparent;
  transition: all var(--transition-fast);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.toc-item:active {
  background: var(--bg-secondary);
}

.toc-item.active {
  color: var(--primary-color);
  border-left-color: var(--primary-color);
  background: var(--primary-bg);
}

.toc-fab {
  position: fixed;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--card-bg);
  box-shadow: var(--shadow-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  z-index: var(--z-sticky);
  transition: all var(--transition-fast);
}

.toc-fab:active {
  transform: translateY(-50%) scale(0.95);
  background: var(--bg-secondary);
}

:global(.dark) .toc-fab,
:global([data-theme="dark"]) .toc-fab {
  background: var(--bg-tertiary);
}
</style>
