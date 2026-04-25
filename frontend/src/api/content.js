/**
 * 内容管理相关 API 接口
 *
 * 封装文章/内容的 CRUD 操作以及发布、归档等工作流操作。
 */
import api from './index'

/**
 * 获取内容列表
 *
 * @param {Object} [params] - 查询参数 {page, page_size, status, category, tag, search, ...}
 * @returns {Promise} 解析为内容列表数据
 */
export const getContents = (params) => api.get('/contents/', { params })

/**
 * 获取单条内容详情
 *
 * @param {string|number} id - 内容 ID
 * @returns {Promise} 解析为内容详细信息
 */
export const getContent = (id) => api.get(`/contents/${id}/`)

/**
 * 创建新内容
 *
 * @param {Object} data - 内容信息 {title, body, status, category, tags, cover, ...}
 * @returns {Promise} 解析为创建的内容对象
 */
export const createContent = (data) => api.post('/contents/', data)

/**
 * 更新指定内容
 *
 * @param {string|number} id - 内容 ID
 * @param {Object} data - 要更新的字段
 * @returns {Promise} 解析为更新后的内容对象
 */
export const updateContent = (id, data) => api.put(`/contents/${id}/`, data)

/**
 * 删除指定内容
 *
 * @param {string|number} id - 内容 ID
 * @returns {Promise} 解析为删除操作结果
 */
export const deleteContent = (id) => api.delete(`/contents/${id}/`)

/**
 * 发布内容
 *
 * 将内容状态从草稿变更为已发布，使其在前端可见。
 *
 * @param {string|number} id - 内容 ID
 * @returns {Promise} 解析为发布操作结果
 */
export const publishContent = (id) => api.post(`/contents/${id}/publish/`)

/**
 * 归档（下架）内容
 *
 * 将已发布的内容变更为归档状态，使其在前端不可见但保留数据。
 *
 * @param {string|number} id - 内容 ID
 * @returns {Promise} 解析为归档操作结果
 */
export const archiveContent = (id) => api.post(`/contents/${id}/archive/`)
