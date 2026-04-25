/**
 * 角色和权限管理相关 API 接口
 *
 * 封装角色和权限的 CRUD 操作，用于后台权限管理系统。
 */
import api from './index'

/**
 * 获取角色列表
 *
 * @param {Object} [params] - 查询参数 {page, page_size, search, ...}
 * @returns {Promise} 解析为角色列表数据
 */
export const getRoles = (params) => api.get('/roles/', { params })

/**
 * 获取单个角色详情
 *
 * @param {string|number} id - 角色 ID
 * @returns {Promise} 解析为角色详细信息
 */
export const getRole = (id) => api.get(`/roles/${id}/`)

/**
 * 创建新角色
 *
 * @param {Object} data - 角色信息 {name, code, description, permissions, ...}
 * @returns {Promise} 解析为创建的角色对象
 */
export const createRole = (data) => api.post('/roles/', data)

/**
 * 更新指定角色
 *
 * @param {string|number} id - 角色 ID
 * @param {Object} data - 要更新的字段
 * @returns {Promise} 解析为更新后的角色对象
 */
export const updateRole = (id, data) => api.put(`/roles/${id}/`, data)

/**
 * 删除指定角色
 *
 * @param {string|number} id - 角色 ID
 * @returns {Promise} 解析为删除操作结果
 */
export const deleteRole = (id) => api.delete(`/roles/${id}/`)

/**
 * 获取权限列表
 *
 * @param {Object} [params] - 查询参数 {page, page_size, search, ...}
 * @returns {Promise} 解析为权限列表数据
 */
export const getPermissions = (params) => api.get('/permissions/', { params })

/**
 * 获取单个权限详情
 *
 * @param {string|number} id - 权限 ID
 * @returns {Promise} 解析为权限详细信息
 */
export const getPermission = (id) => api.get(`/permissions/${id}/`)

/**
 * 创建新权限
 *
 * @param {Object} data - 权限信息 {name, code, description, ...}
 * @returns {Promise} 解析为创建的权限对象
 */
export const createPermission = (data) => api.post('/permissions/', data)

/**
 * 更新指定权限
 *
 * @param {string|number} id - 权限 ID
 * @param {Object} data - 要更新的字段
 * @returns {Promise} 解析为更新后的权限对象
 */
export const updatePermission = (id, data) => api.put(`/permissions/${id}/`, data)

/**
 * 删除指定权限
 *
 * @param {string|number} id - 权限 ID
 * @returns {Promise} 解析为删除操作结果
 */
export const deletePermission = (id) => api.delete(`/permissions/${id}/`)
