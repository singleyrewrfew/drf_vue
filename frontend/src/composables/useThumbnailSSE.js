import { onUnmounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const FINAL_STATES = ['completed', 'failed']

class FetchEventSource {
    constructor(url, options = {}) {
        this.url = url
        this.options = options
        this.controller = null
        this.closed = false
        this.reader = null
    }

    async connect() {
        this.controller = new AbortController()

        try {
            const response = await fetch(this.url, {
                method: 'GET',
                headers: {
                    'Accept': 'text/event-stream',
                    'Cache-Control': 'no-cache',
                    ...this.options.headers,
                },
                signal: this.controller.signal,
            })

            if (!response.ok) {
                console.error(`[SSE] HTTP Error: ${response.status}`)
                throw new Error(`HTTP ${response.status}`)
            }

            this.reader = response.body.getReader()
            const decoder = new TextDecoder()
            let buffer = ''

            while (!this.closed) {
                const { done, value } = await this.reader.read()

                if (done) break

                buffer += decoder.decode(value, { stream: true })
                const lines = buffer.split('\n')
                buffer = lines.pop() || ''

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6)
                        this.options.onMessage?.(data)
                    }
                }
            }
        } catch (error) {
            if (error.name !== 'AbortError') {
                console.error('[SSE] Connection error:', error)
                this.options.onError?.(error)
            }
        }
    }

    close() {
        this.closed = true
        this.controller?.abort()
        this.reader?.cancel()
    }
}

export function useThumbnailSSE(baseUrl) {
    const userStore = useUserStore()
    const connections = ref(new Map())

    const subscribeToThumbnailStatus = (mediaId, callbacks = {}) => {
        if (connections.value.has(mediaId)) return

        const token = userStore.accessToken
        if (!token) {
            console.warn('[SSE] No access token available')
            return
        }

        const url = `${baseUrl}/media/${mediaId}/thumbnail_status/`

        const eventSource = new FetchEventSource(url, {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
            onMessage: (rawData) => {
                try {
                    const data = JSON.parse(rawData)

                    if (data.error) {
                        console.error('[SSE] Server error:', data.error)
                        closeConnection(mediaId)
                        return
                    }

                    callbacks.onStatusChange?.(data)

                    if (FINAL_STATES.includes(data.thumbnail_status)) {
                        closeConnection(mediaId)
                        callbacks.onComplete?.(data)
                    }
                } catch (e) {
                    console.error('[SSE] Parse error:', e)
                }
            },
            onError: (error) => {
                console.error('[SSE] Connection error:', error)
                closeConnection(mediaId)
                ElMessage.warning('缩略图状态监控连接中断')
            },
        })

        connections.value.set(mediaId, eventSource)
        eventSource.connect()
    }

    const closeConnection = (mediaId) => {
        const conn = connections.value.get(mediaId)
        if (conn) {
            conn.close()
            connections.value.delete(mediaId)
        }
    }

    const closeAllConnections = () => {
        connections.value.forEach((conn) => conn.close())
        connections.value.clear()
    }

    const subscribeToPendingVideos = (mediaList, callbacks = {}) => {
        mediaList.forEach((item) => {
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
