import { ref, computed } from 'vue'
import { getContent } from '@/api/content'
import { renderMarkdown, extractHeadings } from '@/utils'
import { logger } from '@/utils/logger'
import { CONFIG, MESSAGES } from '@/constants'

export function useArticleContent() {
  // 响应式状态
  const loading = ref(false)
  const article = ref({})
  const fullContentLoaded = ref(false)
  const headings = ref([])
  const hasError = ref(false)

  // 计算属性：渲染后的文章内容（使用统一的渲染函数）
  const renderedContent = computed(() => {
    if (!article.value.content) return ''

    try {
      const html = renderMarkdown(article.value.content)
      headings.value = extractHeadings(article.value.content)
      return html
    } catch (error) {
      hasError.value = true
      logger.error(MESSAGES.ERROR.LOAD_ARTICLE_FAILED, error)
      return ''
    }
  })

  // 加载文章内容
  const loadArticle = async id => {
    loading.value = true
    hasError.value = false

    try {
      const data = await getContent(id)
      article.value = data
      fullContentLoaded.value = true
      return data
    } catch (error) {
      hasError.value = true
      logger.error(MESSAGES.ERROR.LOAD_ARTICLE_FAILED, error, { articleId: id })
      throw error
    } finally {
      loading.value = false
    }
  }

  // 检查并加载完整内容（使用配置常量）
  const checkAndLoadFullContent = async id => {
    if (!article.value.content || fullContentLoaded.value) {
      return
    }

    const isPreview = article.value.content === article.value.content_preview
    const isLongContent = article.value.content?.length >= CONFIG.API.CONTENT_PREVIEW_LENGTH

    if (isPreview && isLongContent) {
      await loadFullContent(id)
    }
  }

  // 加载完整文章内容
  const loadFullContent = async id => {
    try {
      const data = await getContent(id, { full: true })
      article.value = data
      fullContentLoaded.value = true
    } catch (error) {
      logger.error(MESSAGES.ERROR.LOAD_ARTICLE_FAILED, error, { articleId: id })
      throw error
    }
  }

  // 暴露给模板的状态和方法
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
