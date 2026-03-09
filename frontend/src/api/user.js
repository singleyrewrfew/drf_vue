import api from './index'

export const login = (data) => api.post('/auth/login/', data)

export const register = (data) => api.post('/auth/', data)

export const logout = (data) => api.post('/auth/logout/', data)

export const getProfile = () => api.get('/auth/profile/')

export const updateProfile = (data) => api.put('/auth/update_profile/', data)

export const changePassword = (data) => api.post('/auth/change_password/', data)

export const getUsers = (params) => api.get('/auth/', { params })

export const getUser = (id) => api.get(`/auth/${id}/`)

export const updateUser = (id, data) => api.put(`/auth/${id}/`, data)

export const deleteUser = (id) => api.delete(`/auth/${id}/`)
