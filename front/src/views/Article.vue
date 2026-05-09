<template>
  <div class="article-page">
    <div class="container">
      <el-row :gutter="24">
        <!-- 左侧主内容区 -->
        <el-col :span="17">
          <div class="article-main">
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
              @reply="handleReply"
            />
          </div>
        </el-col>

        <!-- 右侧侧边栏 -->
        <el-col :span="7">
          <div class="sidebar">
            <RelatedArticles :articles="relatedArticles" />
            <TableOfContents :headings="headings" />
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { getContent, getContents, getComments, createComment, likeComment } from '@/api/content'
import { ArticleHeader, ArticleContent, ArticleNav, CommentsSection } from '@/components/article'
import RelatedArticles from '@/components/article/RelatedArticles.vue'
import TableOfContents from '@/components/article/TableOfContents.vue'
import { getCoverUrl, extractHeadings } from '@/utils'
import { CONFIG, MESSAGES } from '@/constants'

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

// 评论区组件引用
const commentsSectionRef = ref(null)

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

// 获取文章详情
const fetchArticle = async () => {
  loading.value = true
  fullContentLoaded.value = false
  try {
    const articleId = route.params.slug || route.params.id
    const response = await getContent(articleId)

    // 兼容多种响应格式：
    // 格式1: { data: 文章对象 } (axios 拦截器处理后)
    // 格式2: { data: { data: 文章对象 } } (原始 DRF 响应)
    // 格式3: 直接是文章对象
    let articleData = response.data || response

    // 如果还有嵌套的 data 字段（DRF Response 格式）
    if (articleData && typeof articleData === 'object' && 'data' in articleData && !Array.isArray(articleData.data)) {
      // 检查是否真的是文章对象（有 id 或 title）
      if (articleData.data?.id || articleData.data?.title) {
        articleData = articleData.data
      }
    }

    article.value = articleData

    // 使用预览内容优化首屏加载
    if (articleData.content_preview && articleData.content && articleData.content.length > articleData.content_preview.length) {
      article.value.content = articleData.content_preview
    }

    // 提取目录标题
    headings.value = extractHeadingsFromMarkdown(article.value.content)

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
      // 未授权，跳转登录
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

    // 处理评论响应格式
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

    // 处理列表响应格式
    let results = []
    if (data && Array.isArray(data.results)) {
      results = data.results
    } else if (Array.isArray(data)) {
      results = data
    }

    // 过滤掉当前文章，最多取 5 篇
    relatedArticles.value = results.filter(item => item.id !== article.value.id).slice(0, 5)
  } catch (e) {
    console.error('Failed to fetch related articles:', e)
  }
}

// 从 Markdown 内容中提取标题（简化版）
const extractHeadingsFromMarkdown = content => {
  if (!content) return []

  const result = []
  const idCounters = {}

  // 移除代码块
  const contentWithoutCodeBlocks = content
    .replace(/```[\s\S]*?```/g, '')
    .replace(/~~~[\s\S]*?~~~/g, '')

  // 匹配 Markdown 标题
  const headingRegex = /^(#{1,6})\s+(.+)$/gm
  let match

  while ((match = headingRegex.exec(contentWithoutCodeBlocks)) !== null) {
    const level = match[1].length
    let text = match[2].trim()

    // 清理 Markdown 格式符号
    text = text
      .replace(/\*\*(.+?)\*\*/g, '$1')
      .replace(/\*(.+?)\*/g, '$1')
      .replace(/__(.+?)__/g, '$1')
      .replace(/_(.+?)_/g, '$1')
      .replace(/`(.+?)`/g, '$1')
      .replace(/\[(.+?)\]\(.+?\)/g, '$1')
      .replace(/!\[(.+?)\]\(.+?\)/g, '$1')
      .trim()

    // 过滤空标题和过长标题
    if (text && text.length < 200) {
      const baseId = text
        .toLowerCase()
        .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
        .replace(/^-+|-+$/g, '')

      if (idCounters[baseId] === undefined) {
        idCounters[baseId] = 0
      } else {
        idCounters[baseId]++
      }

      const id = idCounters[baseId] === 0 ? baseId : `${baseId}-${idCounters[baseId]}`

      result.push({
        id: id,
        level: level,
        text: text
      })
    }
  }

  return result
}

// 监听路由参数变化
watch(
  () => route.params.id,
  () => {
    if (route.params.id) {
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
}

.container {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 24px;
}

.article-main {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 40px;
  border: 1px solid var(--border-light);
  animation: fadeInUp 0.15s ease-out;
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
</style>
