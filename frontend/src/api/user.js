import api from './index'
// 登录
export const login = (data) => api.post('/auth/login/', data)
// 注册
export const register = (data) => api.post('/auth/', data)
// 登出
export const logout = (data) => api.post('/auth/logout/', data)
// 刷新 token
export const refreshToken = (data) => api.post('/auth/refresh/', data)
// 获取个人资料
export const getProfile = () => api.get('/auth/profile/')
// 修改个人资料
export const updateProfile = (data) => api.put('/auth/update_profile/', data)
// 修改密码
export const changePassword = (data) => api.post('/auth/change_password/', data)
// 获取用户列表（带分页/筛选参数）
export const getUsers = (params) => api.get('/auth/', { params })
// 获取单个用户（params 形式）
export const getUser = (id) => api.get(`/auth/${id}/`)
// 修改用户
export const updateUser = (id, data) => api.put(`/auth/${id}/`, data)
// 删除用户
export const deleteUser = (id) => api.delete(`/auth/${id}/`)
