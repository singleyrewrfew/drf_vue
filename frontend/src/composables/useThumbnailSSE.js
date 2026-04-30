import { onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const FINAL_STATES = ['completed', 'failed']

/**
 * 缩略图生成状态实时监控（基于 SSE）
 *
 * 通过 EventSource 订阅后端缩略图生成进度，状态变更时触发回调。
 * 连接在终态（completed/failed）时自动关闭，组件卸载时清理全部连接。
 */
export function useThumbnailSSE(baseUrl) {
    const userStore = useUserStore()
    const connections = new Map()

    const subscribeToThumbnailStatus = (mediaId, callbacks = {}) => {
        if (connections.has(mediaId)) return

        const token = userStore.accessToken
        const url = `${baseUrl}/media/${mediaId}/thumbnail_status/?token=${token}`
        const eventSource = new EventSource(url)
        let lastStatus = null
        let closed = false

        const cleanup = () => {
            if (closed) return
            closed = true
            connections.delete(mediaId)
            eventSource.close()
        }

        connections.set(mediaId, { eventSource, cleanup })

        eventSource.onmessage = (event) => {
            if (closed) return

            try {
                const data = JSON.parse(event.data)

                if (data.error) {
                    cleanup()
                    return
                }

                const status = data.thumbnail_status

                if (status !== lastStatus) {
                    lastStatus = status
                    callbacks.onStatusChange?.(data)
                }

                if (FINAL_STATES.includes(status)) {
                    cleanup()
                    callbacks.onComplete?.(data)
                }
            } catch (e) {
                console.error('[SSE] Parse error:', e)
            }
        }

        eventSource.onerror = () => {
            if (closed) return
            cleanup()
            ElMessage.warning('缩略图状态监控连接中断')
        }
    }

    const closeAllConnections = () => {
        connections.forEach(({ cleanup }) => cleanup())
        connections.clear()
    }

    const subscribeToPendingVideos = (mediaList, callbacks = {}) => {
        mediaList.forEach(item => {
            if (item.is_video && ['pending', 'processing'].includes(item.thumbnail_status)) {
                subscribeToThumbnailStatus(item.id, callbacks)
            }
        })
    }

    onUnmounted(() => {
        closeAllConnections()
    })

    return {
        subscribeToThumbnailStatus,
        closeAllConnections,
        subscribeToPendingVideos,
    }
}
