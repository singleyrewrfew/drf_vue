import { ref, computed } from 'vue'
import { getContent } from '@/api/content'
import { renderMarkdown, extractHeadings, CONTENT_PREVIEW_LENGTH } from '@/utils/markdown'
import { logger } from '@/utils/logger'

export function useArticleContent() {
    const loading = ref(false)
    const article = ref({})
    const fullContentLoaded = ref(false)
    const headings = ref([])
    const hasError = ref(false)
    
    const renderedContent = computed(() => {
        if (!article.value.content) return ''
        
        try {
            const html = renderMarkdown(
                article.value.content,
                `article-${article.value.id}`
            )
            const { html: htmlWithIds, headings: extractedHeadings } = extractHeadings(html)
            headings.value = extractedHeadings
            return htmlWithIds
        } catch (error) {
            hasError.value = true
            logger.error('Failed to render content', error)
            return ''
        }
    })
    
    const loadArticle = async (id) => {
        loading.value = true
        hasError.value = false
        
        try {
            const data = await getContent(id)
            article.value = data
            fullContentLoaded.value = true
            return data
        } catch (error) {
            hasError.value = true
            logger.error('Failed to load article', error, { articleId: id })
            throw error
        } finally {
            loading.value = false
        }
    }
    
    const checkAndLoadFullContent = async (id) => {
        if (!article.value.content || fullContentLoaded.value) {
            return
        }
        
        const isPreview = article.value.content === article.value.content_preview
        const isLongContent = article.value.content?.length >= CONTENT_PREVIEW_LENGTH
        
        if (isPreview && isLongContent) {
            await loadFullContent(id)
        }
    }
    
    const loadFullContent = async (id) => {
        try {
            const data = await getContent(id, { full: true })
            article.value = data
            fullContentLoaded.value = true
        } catch (error) {
            logger.error('Failed to load full content', error, { articleId: id })
            throw error
        }
    }
    
    return {
        loading,
        article,
        fullContentLoaded,
        headings,
        hasError,
        renderedContent,
        loadArticle,
        checkAndLoadFullContent,
        loadFullContent
    }
}
