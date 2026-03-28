import { ref } from 'vue'
import { getContents } from '@/api/content'

export function useArticleNavigation() {
    const prevArticle = ref(null)
    const nextArticle = ref(null)
    const relatedArticles = ref([])
    
    const loadNavigation = async (article) => {
        if (!article?.id || !article?.category) return
        
        const params = {
            category: article.category,
            exclude: article.id,
            limit: 1,
            ordering: '-created_at'
        }
        
        try {
            const prevData = await getContents(params)
            if (prevData.results?.length > 0) {
                prevArticle.value = prevData.results[0]
            }
            
            const nextParams = { ...params, ordering: 'created_at' }
            const nextData = await getContents(nextParams)
            if (nextData.results?.length > 0) {
                nextArticle.value = nextData.results[0]
            }
            
            const relatedData = await getContents({
                category: article.category,
                exclude: article.id,
                limit: 5,
                ordering: '-view_count'
            })
            relatedArticles.value = relatedData.results || []
        } catch (error) {
            console.error('Failed to load navigation:', error)
        }
    }
    
    const reset = () => {
        prevArticle.value = null
        nextArticle.value = null
        relatedArticles.value = []
    }
    
    return {
        prevArticle,
        nextArticle,
        relatedArticles,
        loadNavigation,
        reset
    }
}
