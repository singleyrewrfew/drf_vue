const getMediaBaseUrl = () => {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api'
  return apiBaseUrl.replace(/\/api\/?$/, '')
}

export const getAvatarUrl = (avatar) => {
  if (!avatar) return ''
  if (avatar.startsWith('http')) return avatar
  const baseUrl = getMediaBaseUrl()
  if (avatar.startsWith('/media/')) {
    return `${baseUrl}${avatar}`
  }
  return `${baseUrl}/media/${avatar}`
}

export const getMediaUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  const baseUrl = getMediaBaseUrl()
  if (url.startsWith('/media/')) {
    return `${baseUrl}${url}`
  }
  return `${baseUrl}/media/${url}`
}
