import api from './index'

export const getRoles = (params) => api.get('/roles/', { params })

export const getRole = (id) => api.get(`/roles/${id}/`)

export const createRole = (data) => api.post('/roles/', data)

export const updateRole = (id, data) => api.put(`/roles/${id}/`, data)

export const deleteRole = (id) => api.delete(`/roles/${id}/`)

export const getPermissions = (params) => api.get('/permissions/', { params })

export const getPermission = (id) => api.get(`/permissions/${id}/`)

export const createPermission = (data) => api.post('/permissions/', data)

export const updatePermission = (id, data) => api.put(`/permissions/${id}/`, data)

export const deletePermission = (id) => api.delete(`/permissions/${id}/`)
