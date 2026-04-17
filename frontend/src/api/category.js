import api from './index'

// 获取分类列表（带分页 / 筛选）
export const getCategories = (params) => api.get('/categories/', { params })
// 获取单个分类详情
export const getCategory = (id) => api.get(`/categories/${id}/`)
// 创建分类
export const createCategory = (data) => api.post('/categories/', data)
// 更新分类
export const updateCategory = (id, data) => api.put(`/categories/${id}/`, data)
// 删除分类
export const deleteCategory = (id) => api.delete(`/categories/${id}/`)
// 标签（Tags）接口（和分类完全同结构）
export const getTags = (params) => api.get('/tags/', { params })
export const getTag = (id) => api.get(`/tags/${id}/`)
export const createTag = (data) => api.post('/tags/', data)
export const updateTag = (id, data) => api.put(`/tags/${id}/`, data)
export const deleteTag = (id) => api.delete(`/tags/${id}/`)
