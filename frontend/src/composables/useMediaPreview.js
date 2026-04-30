import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { getMediaUrl } from '@/utils'

/**
 * 媒体文件预览功能
 *
 * 管理预览对话框的状态、文件类型判断、URL 生成以及链接复制/下载操作。
 */
export function useMediaPreview(baseUrl) {
    const previewVisible = ref(false)
    const previewFile = ref(null)
    const videoPoster = ref('')

    const mediaType = computed(() => {
        if (!previewFile.value) return 'unknown'
        const type = previewFile.value.file_type || ''
        if (type.startsWith('image/')) return 'image'
        if (type.startsWith('video/')) return 'video'
        if (type.startsWith('audio/')) return 'audio'
        return 'unknown'
    })

    const isImage = computed(() => mediaType.value === 'image')
    const isVideo = computed(() => mediaType.value === 'video')
    const isAudio = computed(() => mediaType.value === 'audio')

    const previewUrl = computed(() => {
        if (!previewFile.value) return ''
        if (isVideo.value) {
            return `${baseUrl}/media/${previewFile.value.id}/`
        }
        const url = previewFile.value.url || previewFile.value.file
        return getMediaUrl(url)
    })

    const videoThumbnails = computed(() => {
        if (!previewFile.value) return ''
        if (previewFile.value.thumbnail_status === 'completed' && previewFile.value.thumbnails_url) {
            return previewFile.value.thumbnails_url
        }
        return ''
    })

    const videoThumbnailsCount = computed(() => {
        if (!previewFile.value) return 0
        if (previewFile.value.thumbnail_status === 'completed') {
            return previewFile.value.thumbnails_count || 0
        }
        return 0
    })

    const dialogWidth = computed(() => {
        return window.innerWidth < 768 ? '95%' : '900px'
    })

    const openPreview = (row) => {
        previewFile.value = row
        previewVisible.value = true
    }

    const copyLink = (row) => {
        const fileUrl = getMediaUrl(row.file)

        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(fileUrl).then(() => {
                ElMessage.success('链接已复制到剪贴板')
            }).catch(() => {
                fallbackCopyText(fileUrl)
            })
        } else {
            fallbackCopyText(fileUrl)
        }
    }

    const fallbackCopyText = (text) => {
        const textArea = document.createElement('textarea')
        textArea.value = text
        textArea.style.cssText = `
            position: fixed; top: 0; left: 0;
            width: 2em; height: 2em; padding: 0;
            border: none; outline: none; box-shadow: none;
            background: transparent; opacity: 0;
        `
        document.body.appendChild(textArea)
        textArea.focus()
        textArea.select()

        try {
            document.execCommand('copy')
            ElMessage.success('链接已复制到剪贴板')
        } catch {
            ElMessage.error('复制失败，请手动复制')
        } finally {
            document.body.removeChild(textArea)
        }
    }

    const downloadFile = () => {
        if (!previewUrl.value) return
        const link = document.createElement('a')
        link.href = previewUrl.value
        link.download = previewFile.value?.filename || 'download'
        link.target = '_blank'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
    }

    const onVideoError = () => {
        ElMessage.error('视频加载失败，请检查视频格式或网络连接')
    }

    return {
        previewVisible,
        previewFile,
        videoPoster,
        isImage,
        isVideo,
        isAudio,
        previewUrl,
        videoThumbnails,
        videoThumbnailsCount,
        dialogWidth,
        openPreview,
        copyLink,
        downloadFile,
        onVideoError,
    }
}
