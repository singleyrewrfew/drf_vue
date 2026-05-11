<template>
  <div class="article-page" :class="{ 'immersive-mode': isImmersive }">
    <div class="container">
      <el-row :gutter="24" class="article-row">
        <!-- 左侧主内容区 -->
        <el-col
          :xs="24"
          :sm="24"
          :md="isImmersive ? 24 : 17"
          class="main-col"
        >
          <div class="article-main">
            <!-- 沉浸式阅读工具栏 -->
            <Transition name="toolbar-fade">
              <div v-if="isImmersive" class="immersive-toolbar">
                <button
                  class="toolbar-btn"
                  @click="toggleImmersive"
                  title="退出沉浸模式"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M4 14h6v6M20 10h-6V4"/>
                    <line x1="14" y1="10" x2="21" y2="3"/>
                    <line x1="3" y1="21" x2="10" y2="14"/>
                  </svg>
                  <span>退出沉浸</span>
                </button>

                <button
                  v-if="headings.length > 0"
                  class="toolbar-btn"
                  @click="showFloatingTOC = true"
                  title="显示目录"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="8" y1="6" x2="21" y2="6"/>
                    <line x1="8" y1="12" x2="21" y2="12"/>
                    <line x1="8" y1="18" x2="21" y2="18"/>
                    <line x1="3" y1="6" x2="3.01" y2="6"/>
                    <line x1="3" y1="12" x2="3.01" y2="12"/>
                    <line x1="3" y1="18" x2="3.01" y2="18"/>
                  </svg>
                  <span>目录</span>
                </button>
              </div>
            </Transition>

            <template v-if="loading">
              <div class="article-skeleton">
                <el-skeleton animated>
                  <template #template>
                    <el-skeleton-item variant="h1" style="width: 80%; margin-bottom: 24px" />
                    <div style="display: flex; gap: 16px; margin-bottom: 24px">
                      <el-skeleton-item variant="circle" style="width: 40px; height: 40px" />
                      <div style="flex: 1">
                        <el-skeleton-item variant="text" style="width: 30%; margin-bottom: 8px" />
                        <el-skeleton-item variant="text" style="width: 20%" />
                      </div>
                    </div>
                    <el-skeleton-item
                      variant="image"
                      style="width: 100%; height: 300px; margin-bottom: 24px"
                    />
                    <el-skeleton-item variant="text" style="width: 100%; margin-bottom: 12px" />
                    <el-skeleton-item variant="text" style="width: 100%; margin-bottom: 12px" />
                    <el-skeleton-item variant="text" style="width: 80%" />
                  </template>
                </el-skeleton>
              </div>
            </template>
            <template v-else>
              <!-- 文章头部 -->
              <ArticleHeader
                :article="article"
                @category-click="handleCategoryClick"
                @tag-click="tag => $router.push(`/tag/${tag.slug || tag.id}`)"
              />

              <!-- 文章内容 -->
              <ArticleContent
                :content="article.content"
                :cover-image="getCoverUrl(article.cover_image)"
                :title="article.title"
                :is-loading="!fullContentLoaded"
              />
            </template>

            <!-- 文章导航 -->
            <ArticleNav :prev-article="prevArticle" :next-article="nextArticle" />

            <!-- 评论区 -->
            <CommentsSection
              v-if="article.id"
              ref="commentsSectionRef"
              :comments="comments"
              :article-id="article.id"
              @submit="handleCommentSubmit"
              @like="handleLikeComment"
              @reply="handleCommentSubmitReply"
            />
          </div>
        </el-col>

        <!-- 右侧侧边栏 (非沉浸模式下显示) -->
        <Transition name="sidebar-slide">
          <el-col
            v-if="!isImmersive"
            :xs="24"
            :sm="24"
            :md="7"
            class="sidebar-col"
          >
            <div class="sidebar">
              <TableOfContents :headings="headings" :active-id="activeHeadingId" />
              <RelatedArticles :articles="relatedArticles" />
            </div>
          </el-col>
        </Transition>
      </el-row>
    </div>

    <!-- 悬浮目录组件 -->
    <FloatingTOC
      :is-visible="showFloatingTOC"
      :headings="headings"
      :active-id="activeHeadingId"
      @close="showFloatingTOC = false"
      @select="handleTOCSelect"
    />
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { getContent, getContents, getComments, createComment, likeComment } from '@/api/content'
import { ArticleHeader, ArticleContent, ArticleNav, CommentsSection } from '@/components/article'
import RelatedArticles from '@/components/article/RelatedArticles.vue'
import TableOfContents from '@/components/article/TableOfContents.vue'
import FloatingTOC from '@/components/article/FloatingTOC.vue'
import { getCoverUrl, extractHeadings } from '@/utils'
import { useFloatingActions } from '@/composables/useFloatingActions'
import { CONFIG } from '@/constants/config'
import { MESSAGES } from '@/constants/messages'

// 导入提取的样式文件
import '@/components/article/styles/article-markdown.css'
import '@/components/article/styles/article-responsive.css'
import '@/components/article/styles/article-toc.css'

// 路由和状态管理
const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 响应式数据定义
const loading = ref(false)
const article = ref({})
const fullContentLoaded = ref(false)
const comments = ref([])
const prevArticle = ref(null)
const nextArticle = ref(null)
const relatedArticles = ref([])
const headings = ref([])
const activeHeadingId = ref('')

// 沉浸式阅读状态
const isImmersive = ref(false)
const showFloatingTOC = ref(false)

// 悬浮按钮管理
const { registerButton, removeButton } = useFloatingActions()
let unregisterImmersiveBtn = null
let unregisterTocBtn = null

// 评论区组件引用
const commentsSectionRef = ref(null)

let scrollObserver = null

// 切换沉浸模式
function toggleImmersive() {
  isImmersive.value = !isImmersive.value

  if (isImmersive.value) {
    document.body.style.overflow = 'auto'
    nextTick(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    })
  }
}

// 处理悬浮目录选择
function handleTOCSelect(headingId) {
  showFloatingTOC.value = false
  const element = document.getElementById(headingId)
  if (element) {
    const headerHeight = isImmersive.value ? 0 : 72
    const elementPosition = element.getBoundingClientRect().top + window.pageYOffset
    window.scrollTo({
      top: elementPosition - headerHeight - 20,
      behavior: 'smooth'
    })
  }
}

// 注册悬浮按钮到全局按钮组
function registerFloatingButtons() {
  // 注册沉浸式阅读按钮（仅非沉浸模式且内容加载完成后显示）
  unregisterImmersiveBtn = registerButton({
    id: 'immersive',
    title: isImmersive.value ? '退出沉浸模式' : '沉浸式阅读',
    label: isImmersive.value ? '退出' : '沉浸',
    icon: isImmersive.value
      ? '<path d="M4 14h6v6M20 10h-6V4"/><line x1="14" y1="10" x2="21" y2="3"/><line x1="3" y1="21" x2="10" y2="14"/>'
      : '<path d="M8 3H5a2 2 0 00-2 2v3m18 0V5a2 2 0 00-2-2h-3m0 18h3a2 2 0 002-2v-3M3 16v3a2 2 0 002 2h3"/>',
    onClick: toggleImmersive,
    visible: () => fullContentLoaded.value
  })

  // 注册目录按钮（仅沉浸模式且有目录时显示）
  unregisterTocBtn = registerButton({
    id: 'toc',
    title: '显示目录',
    label: '目录',
    icon: '<line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/>',
    onClick: () => { showFloatingTOC.value = true },
    visible: () => isImmersive.value && headings.value.length > 0 && !showFloatingTOC.value
  })
}

// 注销悬浮按钮
function unregisterFloatingButtons() {
  if (unregisterImmersiveBtn) {
    unregisterImmersiveBtn()
    unregisterImmersiveBtn = null
  }
  if (unregisterTocBtn) {
    unregisterTocBtn()
    unregisterTocBtn = null
  }
}

// 设置滚动监听
function setupScrollSpy() {
  scrollObserver = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          activeHeadingId.value = entry.target.id
        }
      })
    },
    {
      rootMargin: '-80px 0px -70% 0px',
      threshold: 0
    }
  )

  setTimeout(() => {
    const headingElements = document.querySelectorAll('.markdown-body h1, .markdown-body h2, .markdown-body h3')
    headingElements.forEach(el => scrollObserver.observe(el))
  }, 100)
}

function cleanupScrollSpy() {
  if (scrollObserver) {
    scrollObserver.disconnect()
    scrollObserver = null
  }
}

onMounted(() => {
  setupScrollSpy()
  registerFloatingButtons()
})

onUnmounted(() => {
  cleanupScrollSpy()
  unregisterFloatingButtons()
})

watch(
  () => article.value.content,
  () => {
    if (article.value.content) {
      setTimeout(() => {
        cleanupScrollSpy()
        setupScrollSpy()
      }, 150)
    }
  }
)

// 处理分类标签点击事件
const handleCategoryClick = () => {
  const idOrSlug = article.value.category_slug || article.value.category
  if (idOrSlug) {
    router.push(`/category/${idOrSlug}`)
  }
}

// 处理评论提交（区分主评论和回复）
const handleCommentSubmit = ({ content, parentId }) => {
  if (parentId === null) {
    submitCommentMain(content)
  } else {
    submitReplyMain(parentId, content)
  }
}

// 提交主评论
const submitCommentMain = async content => {
  if (!content.trim()) return

  try {
    await createComment({
      article: route.params.id,
      content: content
    })

    await loadComments()
    ElMessage.success(MESSAGES.SUCCESS.COMMENT_SUBMITTED)
  } catch (error) {
    console.error('Failed to submit comment:', error)
    ElMessage.error(MESSAGES.ERROR.COMMENT_FAILED)
  }
}

// 提交回复评论
const submitReplyMain = async (parentId, content) => {
  if (!content.trim()) return

  try {
    await createComment({
      article: route.params.id,
      content: content,
      parent: parentId
    })

    await loadComments()
    ElMessage.success(MESSAGES.SUCCESS.REPLY_SUBMITTED)
  } catch (error) {
    console.error('Failed to submit reply:', error)
    ElMessage.error(MESSAGES.ERROR.REPLY_FAILED)
  }
}

// 处理评论点赞
const handleLikeComment = async comment => {
  try {
    await likeComment(comment.id)
    comment.is_liked = !comment.is_liked
    comment.like_count = (comment.like_count || 0) + (comment.is_liked ? 1 : -1)
  } catch (error) {
    console.error('Failed to like comment:', error)
  }
}

// 处理回复按钮点击
const handleReply = (commentId, userName, userId) => {
  if (commentsSectionRef.value) {
    commentsSectionRef.value.openReplyForm(commentId, userName, userId)
  }
}

// 处理提交回复评论
const handleCommentSubmitReply = async ({ content, parentId, replyToUser }) => {
  if (!content.trim()) return

  try {
    await createComment({
      article: route.params.id,
      content: content,
      parent: parentId,
      reply_to_id: replyToUser || null
    })

    await loadComments()
    ElMessage.success(MESSAGES.SUCCESS.REPLY_SUBMITTED)
  } catch (error) {
    console.error('Failed to submit reply:', error)
    ElMessage.error(MESSAGES.ERROR.REPLY_FAILED)
  }
}

// 获取文章详情
const fetchArticle = async () => {
  loading.value = true
  fullContentLoaded.value = false
  try {
    const articleId = route.params.slug || route.params.id
    const response = await getContent(articleId)

    let articleData = response.data || response

    if (articleData && typeof articleData === 'object' && 'data' in articleData && !Array.isArray(articleData.data)) {
      if (articleData.data?.id || articleData.data?.title) {
        articleData = articleData.data
      }
    }

    article.value = articleData

    // 使用预览内容优化首屏加载
    if (articleData.content_preview && articleData.content && articleData.content.length > articleData.content_preview.length) {
      article.value.content = articleData.content_preview
    }

    // 使用统一的工具函数提取目录标题
    headings.value = extractHeadings(article.value.content)

    // 设置完整内容已加载标记
    if (!articleData.content_preview || articleData.content === articleData.content_preview) {
      fullContentLoaded.value = true
    }

    // 并行加载评论和相关文章
    Promise.all([fetchComments(), fetchRelatedArticles()]).catch(e => {
      console.error('加载评论或相关文章失败:', e)
    })
  } catch (e) {
    console.error('Failed to fetch article:', e)

    if (e.response?.status === 404) {
      router.replace({ name: 'NotFound' })
    } else if (e.response?.status === 401) {
      router.push('/login')
    } else {
      ElMessage.error(MESSAGES.ERROR.ARTICLE_NOT_FOUND)
    }
  } finally {
    loading.value = false
  }
}

// 获取文章评论列表
const fetchComments = async () => {
  try {
    const articleId = route.params.slug || route.params.id
    const response = await getComments({ article: articleId })
    let data = response.data || response

    if (data && Array.isArray(data.results)) {
      comments.value = data.results
    } else if (Array.isArray(data)) {
      comments.value = data
    } else {
      comments.value = []
    }
  } catch (e) {
    console.error('Failed to fetch comments:', e)
  }
}

// 别名
const loadComments = fetchComments

// 获取相关文章列表
const fetchRelatedArticles = async () => {
  try {
    const params = { status: 'published', page_size: CONFIG.API.RELATED_ARTICLES_COUNT }
    if (article.value.category) {
      params.category = article.value.category
    }

    const response = await getContents(params)
    let data = response.data || response

    let results = []
    if (data && Array.isArray(data.results)) {
      results = data.results
    } else if (Array.isArray(data)) {
      results = data
    }

    relatedArticles.value = results.filter(item => item.id !== article.value.id).slice(0, 5)
  } catch (e) {
    console.error('Failed to fetch related articles:', e)
  }
}

// 监听路由参数变化
watch(
  () => route.params.id,
  () => {
    if (route.params.id) {
      // 退出沉浸模式
      isImmersive.value = false
      showFloatingTOC.value = false
      fetchArticle()
    }
  },
  { immediate: true }
)
</script>

<style scoped>
.article-page {
  padding: 32px 0;
  background: var(--bg-color);
  min-height: calc(100vh - var(--header-height));
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 暗色模式 */
[data-theme='dark'] .article-page {
  background: var(--bg-color);
}

/* 沉浸式阅读模式 */
.article-page.immersive-mode {
  padding: 0;
  background: #fafaf9;
}

[data-theme='dark'] .article-page.immersive-mode {
  background: #1a1a1a;
}

.container {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 24px;
  transition: max-width 0.4s ease;
}

.immersive-mode .container {
  max-width: 900px;
  padding: 0 32px;
}

.article-row {
  transition: all 0.4s ease;
}

.main-col,
.sidebar-col {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.article-main {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 40px;
  border: 1px solid var(--border-light);
  animation: fadeInUp 0.15s ease-out;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 暗色模式 - 文章主内容区 */
[data-theme='dark'] .article-main {
  background: var(--card-bg);
  border-color: var(--border-light);
}

.immersive-mode .article-main {
  background: transparent;
  border: none;
  border-radius: 0;
  padding: 48px 0;
  box-shadow: none;
}

[data-theme='dark'] .immersive-mode .article-main {
  background: transparent;
}

/* 沉浸模式 - 隐藏评论区 */
.immersive-mode :deep(.comments-section) {
  display: none;
}

/* 沉浸模式下的排版优化 */
.immersive-mode .article-main :deep(.markdown-body) {
  font-size: 18px;
  line-height: 1.9;
  letter-spacing: 0.02em;
}

.immersive-mode .article-main :deep(.markdown-body p) {
  margin-bottom: 28px;
  text-align: justify;
}

.immersive-mode .article-main :deep(.markdown-body h1),
.immersive-mode .article-main :deep(.markdown-body h2),
.immersive-mode .article-main :deep(.markdown-body h3) {
  margin-top: 48px;
  margin-bottom: 24px;
}

.immersive-mode .article-main :deep(.markdown-body code) {
  font-size: 15px;
}

.immersive-mode .article-main :deep(.markdown-body pre) {
  margin: 32px 0;
  padding: 24px;
  border-radius: 12px;
}

@media (max-width: 768px) {
  .immersive-mode .article-main {
    padding: 24px 0;
  }

  .immersive-mode .article-main :deep(.markdown-body) {
    font-size: 16px;
    line-height: 1.8;
  }

  .immersive-mode .container {
    padding: 0 16px;
  }
}

.article-skeleton {
  padding: 24px 0;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
  align-self: flex-start;
  position: sticky;
  top: 96px;
  max-height: calc(100vh - 116px);
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.sidebar::-webkit-scrollbar {
  display: none;
}

/* ====== 沉浸模式工具栏 ====== */
.immersive-toolbar {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 0 24px 0;
  border-bottom: 1px solid var(--border-light);
  margin-bottom: 32px;
  animation: slideDown 0.35s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.toolbar-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  background: rgba(var(--primary-rgb), 0.06);
  border: 1px solid rgba(var(--primary-rgb), 0.15);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.toolbar-btn:hover {
  color: var(--primary-color);
  background: rgba(var(--primary-rgb), 0.12);
  border-color: rgba(var(--primary-rgb), 0.25);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(var(--primary-rgb), 0.15);
}

.toolbar-btn svg {
  width: 16px;
  height: 16px;
}

@media (max-width: 768px) {
  .immersive-toolbar {
    flex-wrap: wrap;
    gap: 8px;
  }

  .toolbar-btn {
    padding: 7px 12px;
    font-size: 12px;
  }
}

/* ====== 过渡动画 ====== */

/* 侧边栏滑出动画 */
.sidebar-slide-enter-active,
.sidebar-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.sidebar-slide-enter-from,
.sidebar-slide-leave-to {
  opacity: 0;
  transform: translateX(30px);
  max-height: 0;
  overflow: hidden;
}

/* 工具栏淡入淡出 */
.toolbar-fade-enter-active,
.toolbar-fade-leave-active {
  transition: all 0.3s ease;
}

.toolbar-fade-enter-from,
.toolbar-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* 按钮淡入淡出 */
.btn-fade-enter-active,
.btn-fade-leave-active {
  transition: all 0.3s ease;
}

.btn-fade-enter-from,
.btn-fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
