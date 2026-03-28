const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'
const MEDIA_BASE_URL = import.meta.env.VITE_MEDIA_BASE_URL || ''

export const getMediaUrl = (path) => {
  if (!path) return ''
  if (path.startsWith('http')) return path
  if (path.startsWith('/media/')) {
    return `${MEDIA_BASE_URL}${path}`
  }
  return `${MEDIA_BASE_URL}/media/${path}`
}

export const getCoverUrl = (coverImage, placeholder = true) => {
  if (!coverImage) {
    return placeholder ? `https://picsum.photos/800/400?random=${Math.random().toString(36).substring(7)}` : ''
  }
  if (coverImage.startsWith('http')) return coverImage
  if (coverImage.startsWith('/media/')) {
    return `${MEDIA_BASE_URL}${coverImage}`
  }
  return `${MEDIA_BASE_URL}/media/${coverImage}`
}

export const getAvatarUrl = (avatar) => {
  if (!avatar) return ''
  if (avatar.startsWith('http')) return avatar
  if (avatar.startsWith('/media/')) {
    return `${MEDIA_BASE_URL}${avatar}`
  }
  return `${MEDIA_BASE_URL}/media/${avatar}`
}

export const getArticleUrl = (article) => {
  return `/article/${article.slug || article.id}`
}

export const formatDate = (dateStr, locale = 'zh-CN') => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString(locale)
}

export const formatDateTime = (dateStr, locale = 'zh-CN') => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString(locale)
}

export const formatRelativeTime = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (seconds < 60) return '刚刚'
  if (minutes < 60) return `${minutes} 分钟前`
  if (hours < 24) return `${hours} 小时前`
  if (days < 7) return `${days} 天前`
  if (days < 30) return `${Math.floor(days / 7)} 周前`
  if (days < 365) return `${Math.floor(days / 30)} 个月前`
  return `${Math.floor(days / 365)} 年前`
}

export const truncateText = (text, maxLength = 100) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength) + '...'
}

export const debounce = (fn, delay = 300) => {
  let timer = null
  return function (...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

export const throttle = (fn, delay = 300) => {
  let lastTime = 0
  return function (...args) {
    const now = Date.now()
    if (now - lastTime >= delay) {
      lastTime = now
      fn.apply(this, args)
    }
  }
}

export const deepClone = (obj) => {
  if (obj === null || typeof obj !== 'object') return obj
  if (obj instanceof Date) return new Date(obj.getTime())
  if (obj instanceof Array) return obj.map(item => deepClone(item))
  if (typeof obj === 'object') {
    const cloned = {}
    for (const key in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        cloned[key] = deepClone(obj[key])
      }
    }
    return cloned
  }
  return obj
}

export const serializeParams = (params) => {
  if (!params || typeof params !== 'object') return ''
  const searchParams = new URLSearchParams()
  Object.keys(params).forEach(key => {
    const value = params[key]
    if (value !== null && value !== undefined && value !== '') {
      if (Array.isArray(value)) {
        value.forEach(item => searchParams.append(key, item))
      } else {
        searchParams.append(key, value)
      }
    }
  })
  return searchParams.toString()
}

export const parseQuery = (queryString) => {
  if (!queryString) return {}
  const params = new URLSearchParams(queryString)
  const result = {}
  for (const [key, value] of params) {
    if (result[key]) {
      if (Array.isArray(result[key])) {
        result[key].push(value)
      } else {
        result[key] = [result[key], value]
      }
    } else {
      result[key] = value
    }
  }
  return result
}

export const generateId = () => {
  return Math.random().toString(36).substring(2, 9)
}

export const sleep = (ms) => {
  return new Promise(resolve => setTimeout(resolve, ms))
}

export const isExternalLink = (url) => {
  if (!url) return false
  return url.startsWith('http://') || url.startsWith('https://')
}

export const highlightText = (text, keyword) => {
  if (!text || !keyword) return text
  const regex = new RegExp(`(${keyword})`, 'gi')
  return text.replace(regex, '<mark>$1</mark>')
}

export const stripHtml = (html) => {
  if (!html) return ''
  return html.replace(/<[^>]*>/g, '')
}

export const getReadingTime = (content, wordsPerMinute = 200) => {
  if (!content) return 0
  const text = stripHtml(content)
  const wordCount = text.length
  return Math.ceil(wordCount / wordsPerMinute)
}
