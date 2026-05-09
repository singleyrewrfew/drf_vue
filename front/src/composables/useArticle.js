import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getContent, getContents, getComments, createComment, likeComment } from '@/api/content'
import {
  getCoverUrl,
  getAvatarUrl,
  getArticleUrl,
  formatDate,
  formatRelativeTime,
  renderMarkdown,
  extractHeadings
} from '@/utils'
import { EMOJI_LIST, CONFIG, MESSAGES } from '@/constants'

export function useArticle() {
  const route = useRoute()
  const router = useRouter()
  const userStore = useUserStore()

  // 响应式状态
  const loading = ref(false)
  const article = ref({})
  const fullContentLoaded = ref(false)
  const comments = ref([])
  const commentContent = ref('')
  const submitting = ref(false)
  const replyToParent = ref(null)
  const replyToName = ref('')
  const replyToUserId = ref(null)
  const replyContent = ref('')
  const submittingReply = ref(false)
  const expandedReplies = ref([])
  const prevArticle = ref(null)
  const nextArticle = ref(null)
  const relatedArticles = ref([])
  const showAllComments = ref(false)
  const showCommentsDialog = ref(false)
  const showTocDrawer = ref(false)
  const activeHeadingId = ref('')
  const headings = ref([])

  // 使用统一的 Emoji 列表常量
  const emojis = EMOJI_LIST

  // 计算属性：显示的评论列表（支持展开/折叠）
  const displayComments = computed(() => {
    if (showAllComments.value) {
      return comments.value
    }
    return comments.value.slice(0, CONFIG.API.INITIAL_COMMENTS_COUNT)
  })

  // 计算属性：渲染后的文章内容（使用统一的渲染函数）
  const renderedContent = computed(() => {
    if (!article.value.content) return ''

    const html = renderMarkdown(article.value.content)
    headings.value = extractHeadings(article.value.content)
    return html
  })

  // 处理分类标签点击事件
  const handleCategoryClick = () => {
    const idOrSlug = article.value.category_slug || article.value.category
    if (idOrSlug) {
      router.push(`/category/${idOrSlug}`)
    }
  }

  // 滚动到指定标题位置（使用配置常量）
  const scrollToHeading = id => {
    const element = document.getElementById(id)
    if (element) {
      const elementPosition = element.getBoundingClientRect().top + window.pageYOffset
      window.scrollTo({
        top: elementPosition - CONFIG.UI.SCROLL_OFFSET,
        behavior: 'smooth'
      })
    }
  }

  // 处理目录项点击事件
  const handleTocClick = id => {
    showTocDrawer.value = false
    activeHeadingId.value = id
    scrollToHeading(id)
  }

  // 加载文章详情及关联数据
  const loadArticle = async () => {
    loading.value = true
    try {
      const response = await getContent(route.params.id)

      // 兼容多种响应格式
      let articleData = response.data || response
      if (articleData && typeof articleData === 'object' && 'data' in articleData && !Array.isArray(articleData.data)) {
        if (articleData.data?.id || articleData.data?.title) {
          articleData = articleData.data
        }
      }

      article.value = articleData

      // 初始化内容渲染
      initArticleContent()

      // 加载上一篇/下一篇文章
      await loadAdjacentArticles(articleData)

      // 加载相关文章
      await loadRelatedArticles(articleData)

      // 加载评论
      await loadComments()
    } catch (error) {
      console.error('Failed to load article:', error)
    } finally {
      loading.value = false
    }
  }

  // 加载相邻文章（上一篇/下一篇）
  const loadAdjacentArticles = async (currentArticle) => {
    try {
      const params = {
        category: currentArticle.category,
        exclude: currentArticle.id,
        limit: 1,
        ordering: '-created_at'
      }

      const prevResponse = await getContents(params)
      let prevData = prevResponse.data || prevResponse
      if (prevData && Array.isArray(prevData.results)) {
        if (prevData.results.length > 0) {
          prevArticle.value = prevData.results[0]
        }
      } else if (Array.isArray(prevData)) {
        if (prevData.length > 0) {
          prevArticle.value = prevData[0]
        }
      }

      const nextParams = { ...params, ordering: 'created_at' }
      const nextResponse = await getContents(nextParams)
      let nextData = nextResponse.data || nextResponse
      if (nextData && Array.isArray(nextData.results)) {
        if (nextData.results.length > 0) {
          nextArticle.value = nextData.results[0]
        }
      } else if (Array.isArray(nextData)) {
        if (nextData.length > 0) {
          nextArticle.value = nextData[0]
        }
      }
    } catch (error) {
      console.error('Failed to load adjacent articles:', error)
    }
  }

  // 加载相关文章列表
  const loadRelatedArticles = async (currentArticle) => {
    try {
      const relatedResponse = await getContents({
        category: currentArticle.category,
        exclude: currentArticle.id,
        limit: CONFIG.API.RELATED_ARTICLES_COUNT,
        ordering: '-view_count'
      })

      let relatedData = relatedResponse.data || relatedResponse

      // 处理列表响应格式
      let results = []
      if (relatedData && Array.isArray(relatedData.results)) {
        results = relatedData.results
      } else if (Array.isArray(relatedData)) {
        results = relatedData
      }

      // 过滤掉当前文章，最多取指定数量
      relatedArticles.value = results.filter(item => item.id !== currentArticle.id).slice(0, CONFIG.API.RELATED_ARTICLES_COUNT)
    } catch (error) {
      console.error('Failed to load related articles:', error)
    }
  }

  // 加载评论列表
  const loadComments = async () => {
    try {
      const response = await getComments({ article: route.params.id })
      let data = response.data || response

      // 处理评论响应格式
      if (data && Array.isArray(data.results)) {
        comments.value = data.results
      } else if (Array.isArray(data)) {
        comments.value = data
      } else {
        comments.value = []
      }
    } catch (error) {
      console.error(MESSAGES.ERROR.LOAD_COMMENTS_FAILED, error)
    }
  }

  // 初始化文章内容（检查是否需要加载完整内容）
  const initArticleContent = () => {
    if (!article.value.content) return

    // 使用配置常量判断是否为预览内容
    if (
      article.value.content === article.value.content_preview &&
      article.value.content.length === CONFIG.API.CONTENT_PREVIEW_LENGTH &&
      !fullContentLoaded.value
    ) {
      loadFullContent()
    } else {
      fullContentLoaded.value = true
    }
  }

  // 加载完整文章内容
  const loadFullContent = async () => {
    try {
      const data = await getContent(route.params.id, { full: true })
      article.value = data
      fullContentLoaded.value = true
    } catch (error) {
      console.error(MESSAGES.ERROR.LOAD_ARTICLE_FAILED, error)
    }
  }

  // 提交主评论
  const submitComment = async () => {
    if (!commentContent.value.trim()) return

    submitting.value = true
    try {
      await createComment({
        content_type: 'contents.Content',
        object_id: article.value.id,
        content: commentContent.value,
        parent: null
      })

      commentContent.value = ''
      await loadComments()
    } catch (error) {
      console.error(MESSAGES.ERROR.COMMENT_FAILED, error)
    } finally {
      submitting.value = false
    }
  }

  // 提交回复评论
  const submitReply = async parentId => {
    if (!replyContent.value.trim()) return

    submittingReply.value = true
    try {
      await createComment({
        content_type: 'contents.Content',
        object_id: article.value.id,
        content: replyContent.value,
        parent: parentId
      })

      replyContent.value = ''
      replyToParent.value = null
      await loadComments()
    } catch (error) {
      console.error(MESSAGES.ERROR.REPLY_FAILED, error)
    } finally {
      submittingReply.value = false
    }
  }

  // 处理评论点赞
  const likeCommentHandler = async comment => {
    try {
      await likeComment(comment.id)
      comment.is_liked = !comment.is_liked
      comment.like_count = (comment.like_count || 0) + (comment.is_liked ? 1 : -1)
    } catch (error) {
      console.error(MESSAGES.ERROR.COMMENT_LIKED, error)
    }
  }

  // 打开回复表单
  const openReplyForm = (commentId, userName, userId) => {
    replyToParent.value = commentId
    replyToName.value = userName
    replyToUserId.value = userId
    replyContent.value = ''
  }

  // 关闭回复表单
  const closeReplyForm = () => {
    replyToParent.value = null
    replyToName.value = ''
    replyToUserId.value = null
    replyContent.value = ''
  }

  // 切换回复展开/收起状态
  const toggleReplies = commentId => {
    const index = expandedReplies.value.indexOf(commentId)
    if (index > -1) {
      expandedReplies.value.splice(index, 1)
    } else {
      expandedReplies.value.push(commentId)
    }
  }

  // 插入表情符号到评论框
  const insertEmoji = emoji => {
    commentContent.value += emoji
  }

  // 暴露给模板的状态和方法
  return {
    loading,
    article,
    fullContentLoaded,
    comments,
    commentContent,
    submitting,
    replyToParent,
    replyToName,
    replyToUserId,
    replyContent,
    submittingReply,
    expandedReplies,
    prevArticle,
    nextArticle,
    relatedArticles,
    showAllComments,
    showCommentsDialog,
    showTocDrawer,
    activeHeadingId,
    headings,
    emojis,

    displayComments,
    renderedContent,

    loadArticle,
    loadComments,
    initArticleContent,
    loadFullContent,
    submitComment,
    submitReply,
    likeCommentHandler,
    openReplyForm,
    closeReplyForm,
    toggleReplies,
    insertEmoji,
    getCoverUrl,
    getAvatarUrl,
    getArticleUrl,
    handleCategoryClick,
    scrollToHeading,
    handleTocClick,
    formatRelativeTime,
    formatDate
  }
}
