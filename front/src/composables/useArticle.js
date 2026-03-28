import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getContent, getContents, getComments, createComment, likeComment } from '@/api/content'
import { marked } from 'marked'
import hljs from 'highlight.js'
import { getCoverUrl, getAvatarUrl, getArticleUrl, formatDate, formatRelativeTime } from '@/utils'

export function useArticle() {
    const route = useRoute()
    const router = useRouter()
    const userStore = useUserStore()
    
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
    
    const renderedContent = computed(() => {
        if (!article.value.content) return ''
        
        marked.setOptions({
            highlight: function(code, lang) {
                if (lang && hljs.getLanguage(lang)) {
                    try {
                        return hljs.highlight(code, { language: lang }).value
                    } catch (e) {
                        console.error(e)
                    }
                }
                return hljs.highlightAuto(code).value
            },
            breaks: true,
            gfm: true,
        })
        
        let html = marked.parse(article.value.content)
        extractHeadings(html)
        return html
    })
    
    const handleCategoryClick = () => {
        const idOrSlug = article.value.category_slug || article.value.category
        if (idOrSlug) {
            router.push(`/category/${idOrSlug}`)
        }
    }
    
    const extractHeadings = (html) => {
        const tempDiv = document.createElement('div')
        tempDiv.innerHTML = html
        const headingElements = tempDiv.querySelectorAll('h1, h2, h3, h4, h5, h6')
        const result = []
        headingElements.forEach((el, index) => {
            const id = `heading-${index}`
            el.id = id
            result.push({
                id,
                level: parseInt(el.tagName.charAt(1)),
                text: el.textContent,
            })
        })
        headings.value = result
    }
    
    const scrollToHeading = (id) => {
        const element = document.getElementById(id)
        if (element) {
            const headerHeight = 72
            const elementPosition = element.getBoundingClientRect().top + window.pageYOffset
            window.scrollTo({
                top: elementPosition - headerHeight - 16,
                behavior: 'smooth'
            })
        }
    }
    
    const handleTocClick = (id) => {
        showTocDrawer.value = false
        activeHeadingId.value = id
        scrollToHeading(id)
    }
    
    const loadArticle = async () => {
        loading.value = true
        try {
            const data = await getContent(route.params.id)
            article.value = data
            await initArticleContent()
            
            const params = {
                category: data.category,
                exclude: data.id,
                limit: 1,
                ordering: '-created_at'
            }
            
            const prevData = await getContents(params)
            if (prevData.results.length > 0) {
                prevArticle.value = prevData.results[0]
            }
            
            const nextParams = { ...params, ordering: 'created_at' }
            const nextData = await getContents(nextParams)
            if (nextData.results.length > 0) {
                nextArticle.value = nextData.results[0]
            }
            
            const relatedData = await getContents({
                category: data.category,
                exclude: data.id,
                limit: 5,
                ordering: '-view_count'
            })
            relatedArticles.value = relatedData.results || []
            
            await loadComments()
        } catch (error) {
            console.error('Failed to load article:', error)
        } finally {
            loading.value = false
        }
    }
    
    const loadComments = async () => {
        try {
            const data = await getComments(route.params.id)
            comments.value = data.results || []
        } catch (error) {
            console.error('Failed to load comments:', error)
        }
    }
    
    const initArticleContent = () => {
        if (!article.value.content) return
        
        marked.setOptions({
            highlight: function(code, lang) {
                if (lang && hljs.getLanguage(lang)) {
                    try {
                        return hljs.highlight(code, { language: lang }).value
                    } catch (e) {
                        console.error(e)
                    }
                }
                return hljs.highlightAuto(code).value
            },
            breaks: true,
            gfm: true,
        })
        
        let html = marked.parse(article.value.content)
        extractHeadings(html)
        
        if (article.value.content === article.value.content_preview &&
            article.value.content.length === 5000 &&
            !fullContentLoaded.value) {
            loadFullContent()
        } else {
            fullContentLoaded.value = true
        }
    }
    
    const loadFullContent = async () => {
        try {
            const data = await getContent(route.params.id, { full: true })
            article.value = data
            fullContentLoaded.value = true
        } catch (error) {
            console.error('Failed to load full content:', error)
        }
    }
    
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
            console.error('Failed to submit comment:', error)
        } finally {
            submitting.value = false
        }
    }
    
    const submitReply = async (parentId) => {
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
            console.error('Failed to submit reply:', error)
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
