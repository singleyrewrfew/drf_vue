import api from './index'
// 获取内容列表（分页 / 筛选）
export const getContents = (params) => api.get('/contents/', { params })
// 获取单条内容详情
export const getContent = (id) => api.get(`/contents/${id}/`)
// 创建内容
export const createContent = (data) => api.post('/contents/', data)
// 更新内容
export const updateContent = (id, data) => api.put(`/contents/${id}/`, data)
// 删除内容
export const deleteContent = (id) => api.delete(`/contents/${id}/`)
// 发布内容
export const publishContent = (id) => api.post(`/contents/${id}/publish/`)
// 归档（下架）内容
export const archiveContent = (id) => api.post(`/contents/${id}/archive/`)
