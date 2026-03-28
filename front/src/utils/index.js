const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

// 处理媒体资源的基础 URL
const MEDIA_BASE_URL = (() => {
  // 如果是相对路径 (如 /api),则使用完整后端地址
  if (API_BASE_URL === '/api' || !API_BASE_URL.startsWith('http')) {
    return 'http://localhost:8000' // 默认后端服务器地址
  }
  // 如果是完整 URL (如 http://localhost:8000/api),去掉 /api 部分
  return API_BASE_URL.replace(/\/api\/?$/, '')
})()
export const getMediaUrl = (path) => {
  if (!path) return ''
  // 如果已经是完整 URL(以 http 开头),直接返回
  if (path.startsWith('http')) return path
  // 后端返回的路径已经包含 /media/,直接拼接 base URL 即可
  const baseUrl = API_BASE_URL === '/api' || !API_BASE_URL.startsWith('http') 
    ? 'http://localhost:8000' 
    : API_BASE_URL.replace(/\/api\/?$/, '')
  return `${baseUrl}${path}`
}

export const getCoverUrl = (coverImage, placeholder = true) => {
  if (!coverImage) {
    return placeholder ? `https://picsum.photos/800/400?random=${Math.random()}` : ''
  }
  // 如果已经是完整 URL(以 http 开头),直接返回
  if (coverImage.startsWith('http')) return coverImage
  // 后端返回的路径已经包含 /media/,直接拼接 base URL 即可
  const baseUrl = API_BASE_URL === '/api' || !API_BASE_URL.startsWith('http') 
    ? 'http://localhost:8000' 
    : API_BASE_URL.replace(/\/api\/?$/, '')
  return `${baseUrl}${coverImage}`
}

export const getAvatarUrl = (avatar) => {
  if (!avatar) return ''
  // 如果已经是完整 URL(以 http 开头),直接返回
  if (avatar.startsWith('http')) return avatar
  // 后端返回的路径已经包含 /media/,直接拼接 base URL 即可
  const baseUrl = API_BASE_URL === '/api' || !API_BASE_URL.startsWith('http') 
    ? 'http://localhost:8000' 
    : API_BASE_URL.replace(/\/api\/?$/, '')
  return `${baseUrl}${avatar}`
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

  if (days > 7) {
    return formatDate(dateStr)
  } else if (days > 0) {
    return `${days}天前`
  } else if (hours > 0) {
    return `${hours}小时前`
  } else if (minutes > 0) {
    return `${minutes}分钟前`
  } else {
    return '刚刚'
  }
}

export const truncateText = (text, maxLength = 100) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength) + '...'
}
