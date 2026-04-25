/**
 * 用户相关 API 接口
 *
 * 封装所有与用户认证、信息管理相关的 HTTP 请求。
 */
import api from './index'

/**
 * 用户登录
 *
 * @param {Object} data - 登录凭证 {username, password}
 * @returns {Promise} 解析为登录响应 {access, refresh, user}
 */
export const login = (data) => api.post('/auth/login/', data)

/**
 * 用户注册
 *
 * @param {Object} data - 注册信息 {username, email, password, ...}
 * @returns {Promise} 解析为注册响应
 */
export const register = (data) => api.post('/auth/', data)

/**
 * 用户登出
 *
 * @param {Object} data - 包含 refresh token {refresh}
 * @returns {Promise} 解析为登出响应
 */
export const logout = (data) => api.post('/auth/logout/', data)

/**
 * 刷新访问令牌
 *
 * @param {Object} data - 包含 refresh token {refresh}
 * @returns {Promise} 解析为新的 token 对 {access, refresh}
 */
export const refreshToken = (data) => api.post('/auth/refresh/', data)

/**
 * 获取当前用户个人资料
 *
 * @returns {Promise} 解析为用户信息对象
 */
export const getProfile = () => api.get('/auth/profile/')

/**
 * 修改当前用户个人资料
 *
 * @param {Object} data - 要更新的字段 {email, avatar, role, is_staff, ...}
 * @returns {Promise} 解析为更新后的用户信息
 */
export const updateProfile = (data) => api.put('/auth/update_profile/', data)

/**
 * 修改当前用户密码
 *
 * @param {Object} data - 密码信息 {old_password, new_password, confirm_password}
 * @returns {Promise} 解析为操作结果
 */
export const changePassword = (data) => api.post('/auth/change_password/', data)

/**
 * 获取用户列表（支持分页和筛选）
 *
 * @param {Object} [params] - 查询参数 {limit, offset, search, ...}
 * @returns {Promise} 解析为用户列表数据
 */
export const getUsers = (params) => api.get('/auth/', { params })

/**
 * 获取单个用户详情
 *
 * @param {string|number} id - 用户 ID
 * @returns {Promise} 解析为用户详细信息
 */
export const getUser = (id) => api.get(`/auth/${id}/`)

/**
 * 修改指定用户信息（管理员操作）
 *
 * @param {string|number} id - 用户 ID
 * @param {Object} data - 要更新的字段
 * @returns {Promise} 解析为更新后的用户信息
 */
export const updateUser = (id, data) => api.put(`/auth/${id}/`, data)

/**
 * 删除指定用户（管理员操作）
 *
 * @param {string|number} id - 用户 ID
 * @returns {Promise} 解析为删除操作结果
 */
export const deleteUser = (id) => api.delete(`/auth/${id}/`)
