/**
 * 评论管理相关 API 接口
 *
 * 封装评论的查询、审核和删除等操作。
 */
import api from './index'

/**
 * 获取评论列表
 *
 * 支持分页和筛选，可按照内容、用户、审核状态等条件过滤。
 *
 * @param {Object} [params={}] - 查询参数 {page, page_size, content_id, is_approved, ...}
 * @returns {Promise} 解析为评论列表数据
 */
export const getComments = (params = {}) => api.get('/comments/', { params })

/**
 * 审核通过指定评论
 *
 * 将评论状态标记为已审核，使其在前端可见。
 *
 * @param {string|number} id - 评论 ID
 * @returns {Promise} 解析为审核操作结果
 */
export const approveComment = (id) => api.post(`/comments/${id}/approve/`)

/**
 * 删除指定评论
 *
 * @param {string|number} id - 评论 ID
 * @returns {Promise} 解析为删除操作结果
 */
export const deleteComment = (id) => api.delete(`/comments/${id}/`)
