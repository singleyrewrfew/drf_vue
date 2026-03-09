import api from './index'

export const getContents = (params) => api.get('/contents/', { params })

export const getContent = (id) => api.get(`/contents/${id}/`)

export const createContent = (data) => api.post('/contents/', data)

export const updateContent = (id, data) => api.put(`/contents/${id}/`, data)

export const deleteContent = (id) => api.delete(`/contents/${id}/`)

export const publishContent = (id) => api.post(`/contents/${id}/publish/`)

export const archiveContent = (id) => api.post(`/contents/${id}/archive/`)
