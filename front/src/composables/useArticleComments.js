import { ref, computed, watch, onUnmounted } from 'vue'
import { getComments, createComment, likeComment } from '@/api/content'
import { logger } from '@/utils/logger'
import { debounce } from '@/utils'
import { EMOJI_LIST, CONFIG, MESSAGES } from '@/constants'

export function useArticleComments(articleIdRef) {
  // 响应式状态
  const comments = ref([])
  const commentContent = ref('')
  const submitting = ref(false)
  const replyToParent = ref(null)
  const replyToName = ref('')
  const replyToUserId = ref(null)
  const replyContent = ref('')
  const submittingReply = ref(false)
  const expandedReplies = ref([])
  const showAllComments = ref(false)
  const hasError = ref(false)

  // 使用统一的 Emoji 列表常量
  const emojis = EMOJI_LIST

  // 计算属性：显示的评论列表（使用配置常量）
  const displayComments = computed(() => {
    if (showAllComments.value) {
      return comments.value
    }
    return comments.value.slice(0, CONFIG.API.INITIAL_COMMENTS_COUNT)
  })

  let stopWatch = null

  // 加载评论列表
  const loadComments = async id => {
    const targetId = id || (articleIdRef?.value ? String(articleIdRef.value) : null)
    if (!targetId) {
      return
    }

    hasError.value = false
    try {
      const data = await getComments({ article: targetId })
      comments.value = data.results || []
    } catch (error) {
      hasError.value = true
      logger.error(MESSAGES.ERROR.LOAD_COMMENTS_FAILED, error, { articleId: targetId })
    }
  }

  // 提交主评论（带防抖，使用配置常量）
  const submitComment = debounce(async content => {
    const commentText = content || commentContent.value
    if (!commentText?.trim() || !articleIdRef?.value || submitting.value) return

    submitting.value = true
    hasError.value = false

    try {
      await createComment({
        article: articleIdRef.value,
        content: commentText,
        parent: null
      })

      commentContent.value = ''
      await loadComments()
    } catch (error) {
      hasError.value = true
      logger.error(MESSAGES.ERROR.COMMENT_FAILED, error)
      throw error
    } finally {
      submitting.value = false
    }
  }, CONFIG.TIMING.DEBOUNCE_DELAY)

  // 提交回复评论（带防抖，使用配置常量）
  const submitReply = debounce(async (parentId, content) => {
    const replyText = content || replyContent.value
    if (!replyText?.trim() || !articleIdRef?.value || submittingReply.value) return

    submittingReply.value = true
    hasError.value = false

    try {
      await createComment({
        article: articleIdRef.value,
        content: replyText,
        parent: parentId
      })

      replyContent.value = ''
      replyToParent.value = null
      await loadComments()
    } catch (error) {
      hasError.value = true
      logger.error(MESSAGES.ERROR.REPLY_FAILED, error)
      throw error
    } finally {
      submittingReply.value = false
    }
  }, CONFIG.TIMING.DEBOUNCE_DELAY)

  // 处理评论点赞
  const likeCommentHandler = async comment => {
    try {
      await likeComment(comment.id)
      comment.is_liked = !comment.is_liked
      comment.like_count = (comment.like_count || 0) + (comment.is_liked ? 1 : -1)
    } catch (error) {
      logger.error(MESSAGES.ERROR.COMMENT_LIKED, error)
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

  // 开始监听文章 ID 变化
  const startWatching = () => {
    if (articleIdRef && !stopWatch) {
      stopWatch = watch(
        () => articleIdRef.value,
        (newId, oldId) => {
          if (newId && newId !== oldId) {
            loadComments()
          }
        }
      )
    }
  }

  // 停止监听文章 ID 变化
  const stopWatching = () => {
    if (stopWatch) {
      stopWatch()
      stopWatch = null
    }
  }

  // 组件卸载时清理监听器
  onUnmounted(() => {
    stopWatching()
  })

  // 暴露给模板的状态和方法
  return {
    comments,
    commentContent,
    submitting,
    replyToParent,
    replyToName,
    replyToUserId,
    replyContent,
    submittingReply,
    expandedReplies,
    showAllComments,
    hasError,
    emojis,
    displayComments,
    loadComments,
    submitComment,
    submitReply,
    likeCommentHandler,
    openReplyForm,
    closeReplyForm,
    toggleReplies,
    insertEmoji,
    startWatching,
    stopWatching
  }
}
