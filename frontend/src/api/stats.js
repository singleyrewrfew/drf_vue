/**
 * 统计数据相关 API 接口
 *
 * 封装仪表盘统计数据的获取操作。
 */
import api from './index.js'

/**
 * 获取仪表盘统计数据
 *
 * 根据用户角色返回不同的统计数据：
 * - 管理员：所有内容、用户、评论、媒体等全局统计
 * - 编辑者/普通用户：个人相关内容统计
 *
 * @returns {Promise} 解析为统计数据对象
 */
export const fetchStats = () => api.get('/auth/stats/')
