/**
 * 系统健康检查相关 API 接口
 *
 * 用于检测后端服务是否可用，通常在应用启动或网络恢复时调用。
 */
import api from './index'

/**
 * 检查后端服务健康状态
 *
 * 向 /health/ 发送 GET 请求，用于判断后端是否在线且正常响应。
 * 前端可在以下场景使用：
 *   - 应用初始化时的连接性探测
 *   - 长时间后台运行后的存活检测
 *   - 错误页面的"重试连接"功能
 *
 * @returns {Promise} 解析为健康状态响应 { status: "ok" }
 *
 * @example
 * // 应用启动时检查后端连通性
 * try {
 *   await fetchHealth()
 *   console.log('后端服务正常')
 * } catch {
 *   console.warn('后端不可达，显示离线提示')
 * }
 */
export const fetchHealth = () => api.get('/health/')
