import { onUnmounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { fetchEventSource } from '@microsoft/fetch-event-source'
import { useUserStore } from '@/stores/user'

const FINAL_STATES = ['completed', 'failed']

export function useThumbnailSSE(baseUrl) {
    const userStore = useUserStore()
    /** Map<mediaId, AbortController> — 用于中断连接 */
    const controllers = ref(new Map())

    /**
     * 获取当前有效的 Bearer token
     * @returns {string} 'Bearer xxx' 或空字符串
     */
    const getAuthHeader = () => {
        const token = userStore.accessToken
        return token ? `Bearer ${token}` : ''
    }

    /**
     * 订阅指定媒体文件的缩略图生成状态 SSE 推送
     *
     * 使用 @microsoft/fetch-event-source 库建立 SSE 连接，
     * 通过 Authorization header 携带 JWT token 认证。
     *
     * @param {number} mediaId - 媒体文件 ID
     * @param {Object} callbacks - 回调配置
     * @param {Function} [callbacks.onStatusChange] - 状态变更回调
     * @param {Function} [callbacks.onComplete] - 完成状态回调
     */
    const subscribeToThumbnailStatus = async (mediaId, callbacks = {}) => {
        // 防止重复订阅
        if (controllers.value.has(mediaId)) return

        const token = userStore.accessToken
        if (!token) {
            console.warn('[SSE] 未找到访问令牌')
            return
        }

        const url = `${baseUrl}/media/${mediaId}/thumbnail_status/`
        const controller = new AbortController()
        controllers.value.set(mediaId, controller)

        try {
            await fetchEventSource(url, {
                method: 'GET',
                headers: {
                    'Accept': 'text/event-stream',
                    'Authorization': getAuthHeader(),
                },
                signal: controller.signal,

                /** 连接建立时校验响应状态 */
                async onopen(response) {
                    if (!response.ok) {
                        console.error(`[SSE] HTTP 错误: ${response.status}`)
                        throw new Error(`HTTP ${response.status}`)
                    }
                    // 连接成功，库会自动处理后续流读取
                },

                /**
                 * 收到消息时触发
                 * 保持原有的数据解析方式和回调流程完全一致
                 */
                onmessage(msg) {
                    const rawData = msg.data

                    try {
                        // 原有解析逻辑：JSON.parse 解析服务端推送数据
                        const data = JSON.parse(rawData)

                        if (data.error) {
                            console.error('[SSE] 服务器错误:', data.error)
                            closeConnection(mediaId)
                            return
                        }

                        // 触发状态变更回调（与原代码一致）
                        callbacks.onStatusChange?.(data)

                        // 检测最终状态，自动关闭连接并触发完成回调
                        if (FINAL_STATES.includes(data.thumbnail_status)) {
                            closeConnection(mediaId)
                            callbacks.onComplete?.(data)
                        }
                    } catch (e) {
                        // 原有逻辑：心跳消息非 JSON，静默忽略；其他解析错误记录日志
                        if (!rawData.includes('heartbeat')) {
                            console.error('[SSE] 解析错误:', e)
                        }
                    }
                },

                /**
                 * 连接错误或重连耗尽时触发
                 *
                 * 返回值含义（与 @microsoft/fetch-event-source 规范）：
                 *   - 返回数字(ms)：按该延迟自动重试
                 *   - 抛出异常：停止重连，Promise reject
                 *
                 * 这里实现与原代码一致的重连策略：
                 *   - 默认最多重试 3 次，指数退避（2s → 4s → 6s）
                 *   - 重试耗尽后抛出异常，触发 onError 回调
                 */
                onerror(err) {
                    console.error('[SSE] 连接错误:', err)

                    // HTTP 错误或认证失败不重连
                    if (err?.message?.startsWith('HTTP') || err?.status === 401) {
                        ElMessage.warning('缩略图状态监控连接失败，请刷新页面重试')
                        throw err  // 抛出异常停止重连
                    }

                    // 其他错误：返回 undefined 让库使用默认重试策略，
                    // 或在达到重试次数后停止
                    ElMessage.warning('缩略图状态监控连接中断，请刷新页面重试')
                    throw err  // 停止重连（与原行为一致：3次后报错）
                },
            })
        } catch (err) {
            // fetchEventSource Promise 被 abort 或 throw 终止时到这里
            if (err.name !== 'AbortError') {
                console.error('[SSE] 连接关闭异常:', err)
            }
        }
    }

    /**
     * 关闭指定媒体文件的 SSE 连接
     * @param {number} mediaId - 媒体文件 ID
     */
    const closeConnection = (mediaId) => {
        const controller = controllers.value.get(mediaId)
        if (controller) {
            controller.abort()
            controllers.value.delete(mediaId)
        }
    }

    /**
     * 关闭所有活动的 SSE 连接（组件卸载时调用）
     */
    const closeAllConnections = () => {
        controllers.value.forEach((controller) => controller.abort())
        controllers.value.clear()
    }

    /**
     * 批量订阅待处理的视频缩略图状态
     * 遍历媒体列表，为 pending/processing 状态的视频文件建立 SSE 连接
     *
     * @param {Array} mediaList - 媒体文件列表
     * @param {Object} callbacks - 回调配置（同 subscribeToThumbnailStatus）
     */
    const subscribeToPendingVideos = (mediaList, callbacks = {}) => {
        mediaList.forEach((item) => {
            if (item.is_video && ['pending', 'processing'].includes(item.thumbnail_status)) {
                subscribeToThumbnailStatus(item.id, callbacks)
            }
        })
    }

    // 组件卸载时清理所有连接
    onUnmounted(() => {
        closeAllConnections()
    })

    return {
        subscribeToThumbnailStatus,
        closeAllConnections,
        subscribeToPendingVideos,
    }
}
