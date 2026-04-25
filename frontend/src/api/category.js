/**
 * 分类和标签管理相关 API 接口
 *
 * 封装分类和标签的 CRUD 操作，用于内容管理系统的元数据管理。
 */
import api from './index'

/**
 * 获取分类列表
 *
 * @param {Object} [params] - 查询参数 {page, page_size, search, ...}
 * @returns {Promise} 解析为分类列表数据
 */
export const getCategories = (params) => api.get('/categories/', { params })

/**
 * 获取单个分类详情
 *
 * @param {string|number} id - 分类 ID
 * @returns {Promise} 解析为分类详细信息
 */
export const getCategory = (id) => api.get(`/categories/${id}/`)

/**
 * 创建新分类
 *
 * @param {Object} data - 分类信息 {name, slug, description, parent, ...}
 * @returns {Promise} 解析为创建的分类对象
 */
export const createCategory = (data) => api.post('/categories/', data)

/**
 * 更新指定分类
 *
 * @param {string|number} id - 分类 ID
 * @param {Object} data - 要更新的字段
 * @returns {Promise} 解析为更新后的分类对象
 */
export const updateCategory = (id, data) => api.put(`/categories/${id}/`, data)

/**
 * 删除指定分类
 *
 * @param {string|number} id - 分类 ID
 * @returns {Promise} 解析为删除操作结果
 */
export const deleteCategory = (id) => api.delete(`/categories/${id}/`)

/**
 * 获取标签列表
 *
 * @param {Object} [params] - 查询参数 {page, page_size, search, ...}
 * @returns {Promise} 解析为标签列表数据
 */
export const getTags = (params) => api.get('/tags/', { params })

/**
 * 获取单个标签详情
 *
 * @param {string|number} id - 标签 ID
 * @returns {Promise} 解析为标签详细信息
 */
export const getTag = (id) => api.get(`/tags/${id}/`)

/**
 * 创建新标签
 *
 * @param {Object} data - 标签信息 {name, slug, description, ...}
 * @returns {Promise} 解析为创建的标签对象
 */
export const createTag = (data) => api.post('/tags/', data)

/**
 * 更新指定标签
 *
 * @param {string|number} id - 标签 ID
 * @param {Object} data - 要更新的字段
 * @returns {Promise} 解析为更新后的标签对象
 */
export const updateTag = (id, data) => api.put(`/tags/${id}/`, data)

/**
 * 删除指定标签
 *
 * @param {string|number} id - 标签 ID
 * @returns {Promise} 解析为删除操作结果
 */
export const deleteTag = (id) => api.delete(`/tags/${id}/`)
