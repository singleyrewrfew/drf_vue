import { ref, computed } from 'vue'
import { getComments, createComment, likeComment } from '@/api/content'

export function useArticleComments(articleId) {
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
    
    const loadComments = async (id) => {
        try {
            const data = await getComments(id || articleId)
            comments.value = data.results || []
        } catch (error) {
            console.error('Failed to load comments:', error)
        }
    }
    
    const submitComment = async (id) => {
        if (!commentContent.value.trim()) return
        
        submitting.value = true
        try {
            await createComment({
                content_type: 'contents.Content',
                object_id: id || articleId,
                content: commentContent.value,
                parent: null
            })
            
            commentContent.value = ''
            await loadComments(id || articleId)
        } catch (error) {
            console.error('Failed to submit comment:', error)
            throw error
        } finally {
            submitting.value = false
        }
    }
    
    const submitReply = async (parentId, id) => {
        if (!replyContent.value.trim()) return
        
        submittingReply.value = true
        try {
            await createComment({
                content_type: 'contents.Content',
                object_id: id || articleId,
                content: replyContent.value,
                parent: parentId
            })
            
            replyContent.value = ''
            replyToParent.value = null
            await loadComments(id || articleId)
        } catch (error) {
            console.error('Failed to submit reply:', error)
            throw error
        } finally {
            submittingReply.value = false
        }
    }
    
    const likeCommentHandler = async (comment) => {
        try {
            await likeComment(comment.id)
            comment.is_liked = !comment.is_liked
            comment.like_count = (comment.like_count || 0) + (comment.is_liked ? 1 : -1)
        } catch (error) {
            console.error('Failed to like comment:', error)
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
        emojis,
        displayComments,
        loadComments,
        submitComment,
        submitReply,
        likeCommentHandler,
        openReplyForm,
        closeReplyForm,
        toggleReplies,
        insertEmoji
    }
}
