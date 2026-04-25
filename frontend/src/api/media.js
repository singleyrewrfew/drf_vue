/**
 * 媒体管理相关 API 接口
 *
 * 封装媒体文件的查询、删除和缩略图生成等操作。
 */
import api from './index'

/**
 * 获取媒体文件列表
 *
 * @param {Object} [params={}] - 查询参数 {page, page_size, type, search, ...}
 * @returns {Promise} 解析为媒体列表数据
 */
export const getMedia = (params = {}) => api.get('/media/', { params })

/**
 * 删除指定媒体文件
 *
 * @param {string|number} id - 媒体文件 ID
 * @returns {Promise} 解析为删除操作结果
 */
export const deleteMedia = (id) => api.delete(`/media/${id}/`)

/**
 * 重新生成媒体文件的缩略图
 *
 * 用于视频等需要生成预览图的媒体类型，触发后端重新处理缩略图。
 *
 * @param {string|number} id - 媒体文件 ID
 * @returns {Promise} 解析为操作结果
 */
export const regenerateThumbnails = (id) => api.post(`/media/${id}/regenerate_thumbnails/`)

