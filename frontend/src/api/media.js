import api from './index'

// 获取媒体列表
export const getMedia = (params = {}) => api.get('/media/', { params })
// 删除媒体
export const deleteMedia = (id) => api.delete(`/media/${id}/`)
// 重新生成媒体缩略图
export const regenerateThumbnails = (id) => api.post(`/media/${id}/regenerate_thumbnails/`)

