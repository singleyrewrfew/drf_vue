const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'
const MEDIA_BASE_URL = import.meta.env.VITE_MEDIA_BASE_URL || API_BASE_URL.replace('/api', '')

export const getMediaUrl = (path) => {
  if (!path) return ''
  if (path.startsWith('http')) return path
  
  // 处理路径中已包含 /media/ 的情况
  if (path.startsWith('/media/')) {
    return `${MEDIA_BASE_URL}${path}`
  }
  
  return `${MEDIA_BASE_URL}/media/${path}`
}

export const getCoverUrl = (coverImage, placeholder = true) => {
  if (!coverImage) {
    return placeholder ? `https://picsum.photos/400/200?random=${Math.random()}` : ''
  }
  return getMediaUrl(coverImage)
}

export const getAvatarUrl = (avatar) => {
  if (!avatar) return ''
  return getMediaUrl(avatar)
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
