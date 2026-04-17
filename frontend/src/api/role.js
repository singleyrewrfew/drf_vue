import api from './index'
// 获取角色列表（分页 / 搜索）
export const getRoles = (params) => api.get('/roles/', { params })
// 获取单个角色详情
export const getRole = (id) => api.get(`/roles/${id}/`)
// 创建角色
export const createRole = (data) => api.post('/roles/', data)
// 更新角色
export const updateRole = (id, data) => api.put(`/roles/${id}/`, data)
// 删除角色
export const deleteRole = (id) => api.delete(`/roles/${id}/`)
// 权限（Permissions）接口（和角色同结构）
export const getPermissions = (params) => api.get('/permissions/', { params })
export const getPermission = (id) => api.get(`/permissions/${id}/`)
export const createPermission = (data) => api.post('/permissions/', data)
export const updatePermission = (id, data) => api.put(`/permissions/${id}/`, data)
export const deletePermission = (id) => api.delete(`/permissions/${id}/`)
