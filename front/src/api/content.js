import api from './index'

export const getContents = (params) => api.get('/contents/', { params })

export const getContent = (id) => api.get(`/contents/${id}/`)

export const getCategories = (params) => api.get('/categories/', { params })

export const getCategory = (id) => api.get(`/categories/${id}/`)

export const getTags = (params) => api.get('/tags/', { params })

export const getTag = (id) => api.get(`/tags/${id}/`)

export const getComments = (params) => api.get('/comments/', { params })

export const createComment = (data) => api.post('/comments/', data)

export const likeComment = (id) => api.post(`/comments/${id}/like/`)

export const searchContents = (keyword) => api.get('/contents/', { params: { search: keyword } })
