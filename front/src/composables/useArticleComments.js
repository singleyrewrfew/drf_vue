import { ref, computed, watch, onUnmounted } from 'vue'
import { getComments, createComment, likeComment } from '@/api/content'
import { logger } from '@/utils/logger'
import { debounce } from '@/utils'

export function useArticleComments(articleIdRef) {
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
    
    const emojis = [
        '😀', '😂', '😍', '🥰', '😎', '🤔', '👍', '👎', '❤️', '💔',
        '🎉', '🔥', '✨', '🌟', '⭐', '💯', '💪', '🙏', '😭', '😱',
        '🤣', '😊', '🥺', '👏', '🙄', '😴', '😋', '😜', '🤪', '😇'
    ]
    
    const displayComments = computed(() => {
        if (showAllComments.value) {
            return comments.value
        }
        return comments.value.slice(0, 2)
    })
    
    let stopWatch = null
    
    const loadComments = async (id) => {
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
            logger.error('Failed to load comments', error, { articleId: targetId })
        }
    }
    
    const submitComment = debounce(async (content) => {
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
            logger.error('Failed to submit comment', error)
            throw error
        } finally {
            submitting.value = false
        }
    }, 500)
    
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
            logger.error('Failed to submit reply', error)
            throw error
        } finally {
            submittingReply.value = false
        }
    }, 500)
    
    const likeCommentHandler = async (comment) => {
        try {
            await likeComment(comment.id)
            comment.is_liked = !comment.is_liked
            comment.like_count = (comment.like_count || 0) + (comment.is_liked ? 1 : -1)
        } catch (error) {
            logger.error('Failed to like comment', error)
        }
    }
    
    const openReplyForm = (commentId, userName, userId) => {
        replyToParent.value = commentId
        replyToName.value = userName
        replyToUserId.value = userId
        replyContent.value = ''
    }
    
    const closeReplyForm = () => {
        replyToParent.value = null
        replyToName.value = ''
        replyToUserId.value = null
        replyContent.value = ''
    }
    
    const toggleReplies = (commentId) => {
        const index = expandedReplies.value.indexOf(commentId)
        if (index > -1) {
            expandedReplies.value.splice(index, 1)
        } else {
            expandedReplies.value.push(commentId)
        }
    }
    
    const insertEmoji = (emoji) => {
        commentContent.value += emoji
    }
    
    const startWatching = () => {
        if (articleIdRef && !stopWatch) {
            stopWatch = watch(() => articleIdRef.value, (newId, oldId) => {
                if (newId && newId !== oldId) {
                    loadComments()
                }
            })
        }
    }
    
    const stopWatching = () => {
        if (stopWatch) {
            stopWatch()
            stopWatch = null
        }
    }
    
    onUnmounted(() => {
        stopWatching()
    })
    
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
