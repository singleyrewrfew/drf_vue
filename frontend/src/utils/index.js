import { ElMessage, ElMessageBox } from 'element-plus'

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

export const confirmDelete = async (message = '确定删除该项？此操作不可恢复。') => {
  await ElMessageBox.confirm(message, '确认删除', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
}

export const showSuccess = (message = '操作成功') => {
  ElMessage.success(message)
}

export const showError = (message = '操作失败') => {
  ElMessage.error(message)
}

export const showWarning = (message) => {
  ElMessage.warning(message)
}

export const showInfo = (message) => {
  ElMessage.info(message)
}

export const withLoading = async (fn, loadingRef) => {
  if (loadingRef && typeof loadingRef === 'object') {
    loadingRef.value = true
  }
  try {
    return await fn()
  } finally {
    if (loadingRef && typeof loadingRef === 'object') {
      loadingRef.value = false
    }
  }
}

export const formatDate = (date, format = 'YYYY-MM-DD HH:mm:ss') => {
  if (!date) return ''
  const d = new Date(date)
  if (isNaN(d.getTime())) return ''
  
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  const seconds = String(d.getSeconds()).padStart(2, '0')
  
  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}

export const formatFileSize = (bytes) => {
  if (!bytes || bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

export const truncateText = (text, maxLength = 50) => {
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
  if (obj instanceof Date) return new Date(obj)
  if (obj instanceof Array) return obj.map(item => deepClone(item))
  if (obj instanceof Object) {
    const cloned = {}
    for (const key in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        cloned[key] = deepClone(obj[key])
      }
    }
    return cloned
  }
}

export const pick = (obj, keys) => {
  const result = {}
  keys.forEach(key => {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      result[key] = obj[key]
    }
  })
  return result
}

export const omit = (obj, keys) => {
  const result = { ...obj }
  keys.forEach(key => {
    delete result[key]
  })
  return result
}

export const isEmpty = (value) => {
  if (value === null || value === undefined) return true
  if (typeof value === 'string') return value.trim() === ''
  if (Array.isArray(value)) return value.length === 0
  if (typeof value === 'object') return Object.keys(value).length === 0
  return false
}

export const generateId = () => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2)
}

export const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms))

export const retry = async (fn, retries = 3, delay = 1000) => {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn()
    } catch (error) {
      if (i === retries - 1) throw error
      await sleep(delay)
    }
  }
}
