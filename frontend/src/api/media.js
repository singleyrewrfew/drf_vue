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
 * 获取单个媒体文件详情
 *
 * @param {string|number} id - 媒体文件 ID
 * @returns {Promise} 解析为媒体详情数据
 */
export const getMediaDetail = (id) => api.get(`/media/${id}/`)

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

/**
 * 获取媒体上传接口 URL
 *
 * 从 api 实例的 baseURL 派生，确保与其他 API 函数使用一致的地址。
 * 适用于需要直接访问原始 URL 的场景（如 fetch / XMLHttpRequest / 第三方库）。
 *
 * @returns {string} 媒体上传接口的完整 URL（如 /api/media/ 或 https://example.com/api/media/）
 */
export const getUploadUrl = () => `${api.defaults.baseURL}/media/`

