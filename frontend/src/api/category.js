import api from './index'

export const getCategories = (params) => api.get('/categories/', { params })

export const getCategory = (id) => api.get(`/categories/${id}/`)

export const createCategory = (data) => api.post('/categories/', data)

export const updateCategory = (id, data) => api.put(`/categories/${id}/`, data)

export const deleteCategory = (id) => api.delete(`/categories/${id}/`)

export const getTags = (params) => api.get('/tags/', { params })

export const getTag = (id) => api.get(`/tags/${id}/`)

export const createTag = (data) => api.post('/tags/', data)

export const updateTag = (id, data) => api.put(`/tags/${id}/`, data)

export const deleteTag = (id) => api.delete(`/tags/${id}/`)
