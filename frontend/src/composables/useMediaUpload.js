import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const UPLOAD_CONFIG = {
    MAX_SIZE: 10 * 1024 * 1024,
    REFRESH_DELAY: 500,
    RESET_DELAY: 2000,
    ALLOWED_TYPES: [
        'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml',
        'video/mp4', 'video/webm', 'video/ogg', 'video/quicktime',
        'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ],
    ALLOWED_EXTENSIONS: [
        '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg',
        '.mp4', '.webm', '.ogg', '.mov',
        '.pdf', '.doc', '.docx'
    ]
}

export function useMediaUpload(baseUrl) {
    const userStore = useUserStore()

    const uploading = ref(false)
    const uploadProgress = ref(0)
    const totalUploadFiles = ref(0)
    const completedFiles = ref(0)
    const fileProgressMap = ref(new Map())

    const uploadUrl = computed(() => `${baseUrl}/media/`)

    const uploadHeaders = computed(() => ({
        'Authorization': `Bearer ${userStore.accessToken}`
    }))

    const uploadButtonText = computed(() => {
        if (totalUploadFiles.value === 0) return '上传文件'
        if (completedFiles.value === totalUploadFiles.value) {
            return `已完成 (${completedFiles.value}/${totalUploadFiles.value}个文件)`
        }
        return `上传中 (${completedFiles.value}/${totalUploadFiles.value}个文件)`
    })

    const resetUploadState = () => {
        uploading.value = false
        totalUploadFiles.value = 0
        completedFiles.value = 0
        fileProgressMap.value.clear()
        uploadProgress.value = 0
    }

    const validateFile = (file) => {
        const isVideo = file.type.startsWith('video/')

        if (!isVideo && file.size > UPLOAD_CONFIG.MAX_SIZE) {
            ElMessage.error('文件大小不能超过 10MB（视频文件不限大小）')
            return false
        }

        if (!UPLOAD_CONFIG.ALLOWED_TYPES.includes(file.type)) {
            ElMessage.error(
                `不支持的文件类型：${file.type}。支持的类型：图片（jpg, png, gif, webp, svg）、视频（mp4, webm, ogg）、文档（pdf, doc, docx）`
            )
            return false
        }

        const ext = '.' + file.name.split('.').pop().toLowerCase()
        if (!UPLOAD_CONFIG.ALLOWED_EXTENSIONS.includes(ext)) {
            ElMessage.error(
                `不支持的文件扩展名：${ext}。支持的扩展名：${UPLOAD_CONFIG.ALLOWED_EXTENSIONS.join(', ')}`
            )
            return false
        }

        return true
    }

    const handleFileChange = (file, fileList) => {
        if (file.status === 'ready' && totalUploadFiles.value === 0) {
            totalUploadFiles.value = fileList.length
            completedFiles.value = 0
        }
    }

    const handleUploadProgress = (event, file) => {
        uploading.value = true
        fileProgressMap.value.set(file.uid, event.percent)

        const totalPercent = Array.from(fileProgressMap.value.values()).reduce((sum, p) => sum + p, 0)
        const fileCount = fileProgressMap.value.size
        uploadProgress.value = Math.round(totalPercent / fileCount)
    }

    const handleUploadSuccess = (response, file, fileList, callbacks = {}) => {
        fileProgressMap.value.delete(file.uid)
        completedFiles.value += 1

        if (callbacks.onSuccess) {
            callbacks.onSuccess(response.data)
        }

        if (completedFiles.value === totalUploadFiles.value) {
            uploadProgress.value = 100
            ElMessage.success(`成功上传 ${fileList.length} 个文件`)

            if (callbacks.onAllComplete) {
                setTimeout(() => callbacks.onAllComplete(), UPLOAD_CONFIG.REFRESH_DELAY)
            }

            setTimeout(() => resetUploadState(), UPLOAD_CONFIG.RESET_DELAY)
        }
    }

    const handleUploadError = (error, file) => {
        fileProgressMap.value.delete(file.uid)
        completedFiles.value += 1

        if (completedFiles.value === totalUploadFiles.value) {
            uploadProgress.value = 100
            setTimeout(() => resetUploadState(), UPLOAD_CONFIG.RESET_DELAY)
        }

        const errorMsg = error?.response?.data?.file?.[0] || error?.response?.data?.error || '上传失败'
        ElMessage.error(`${file.name}: ${errorMsg}`)
    }

    return {
        uploading,
        uploadProgress,
        uploadUrl,
        uploadHeaders,
        uploadButtonText,
        validateFile,
        handleFileChange,
        handleUploadProgress,
        handleUploadSuccess,
        handleUploadError,
    }
}
