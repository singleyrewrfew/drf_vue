import { ref, computed } from 'vue'
import { getContent, getContents } from '@/api/content'
import { marked } from 'marked'
import hljs from 'highlight.js'

export function useArticleContent() {
    const loading = ref(false)
    const article = ref({})
    const fullContentLoaded = ref(false)
    const headings = ref([])
    
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
    
    const loadArticle = async (id) => {
        loading.value = true
        try {
            const data = await getContent(id)
            article.value = data
            
            if (article.value.content === article.value.content_preview &&
                article.value.content.length === 5000 &&
                !fullContentLoaded.value) {
                await loadFullContent(id)
            } else {
                fullContentLoaded.value = true
            }
        } catch (error) {
            console.error('Failed to load article:', error)
            throw error
        } finally {
            loading.value = false
        }
    }
    
    const loadFullContent = async (id) => {
        try {
            const data = await getContent(id, { full: true })
            article.value = data
            fullContentLoaded.value = true
        } catch (error) {
            console.error('Failed to load full content:', error)
        }
    }
    
    return {
        loading,
        article,
        fullContentLoaded,
        headings,
        renderedContent,
        loadArticle,
        loadFullContent
    }
}
