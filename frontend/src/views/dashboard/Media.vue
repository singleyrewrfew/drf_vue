<template>
    <div class="media-page">
        <TablePage
            title="媒体管理"
            :show-create="false"
            :show-edit="false"
            :data="mediaList"
            :loading="loading"
            :page="pagination.page"
            :page-size="pagination.page_size"
            :total="pagination.total"
            @delete="handleDelete"
            @page-change="handlePageChange"
        >
            <template #header>
                <div class="card-header">
                    <span>媒体管理</span>
                    <el-upload
                        :action="uploadUrl"
                        :headers="uploadHeaders"
                        :before-upload="beforeUpload"
                        :on-success="handleUploadSuccess"
                        :on-error="handleUploadError"
                        :on-progress="handleUploadProgress"
                        :show-file-list="false"
                        multiple
                    >
                        <UploadButton :loading="uploading" :progress="uploadProgress"/>
                    </el-upload>
                </div>
            </template>
            <el-table-column prop="filename" label="文件名" min-width="200" show-overflow-tooltip/>
            <el-table-column prop="file_type" label="类型" width="150"/>
            <el-table-column prop="file_size" label="大小" width="100">
                <template #default="{ row }">
                    {{ formatSize(row.file_size) }}
                </template>
            </el-table-column>
            <el-table-column label="缩略图" width="150">
                <template #default="{ row }">
                    <template v-if="row.is_video">
                        <div class="thumbnail-status">
                            <el-tag v-if="row.thumbnail_status === 'pending'" type="info" size="small">等待中
                            </el-tag>
                            <el-tag v-else-if="row.thumbnail_status === 'processing'" type="warning" size="small">
                      <span style="display: inline-flex; align-items: center; gap: 4px;">
                        <el-icon class="is-loading"><Loading/></el-icon>
                        <span>生成中</span>
                      </span>
                            </el-tag>
                            <el-tag v-else-if="row.thumbnail_status === 'completed'" type="success" size="small">
                                已完成
                            </el-tag>
                            <div v-else-if="row.thumbnail_status === 'failed'" class="failed-status">
                                <el-tag type="danger" size="small">失败</el-tag>
                                <RetryButton @click="handleRegenerateThumbnails(row)"/>
                            </div>
                        </div>
                    </template>
                    <span v-else>-</span>
                </template>
            </el-table-column>
            <el-table-column prop="uploader_name" label="上传者" width="120"/>
            <el-table-column prop="created_at" label="上传时间" width="180"/>
            <el-table-column prop="url" label="文件路径" width="180" show-overflow-tooltip/>
            <template #actions="{ row }">
                <PreviewButton @click="handlePreview(row)"/>
                <el-button
                    type="primary"
                    size="small"
                    @click="handleCopyLink(row)"
                >
                    复制链接
                </el-button>
            </template>
        </TablePage>

        <el-dialog
            v-model="previewVisible"
            :title="previewFile?.filename || '预览'"
            width="900px"
            destroy-on-close
        >
            <div class="preview-container">
                <img
                    v-if="isImage"
                    :src="previewUrl"
                    class="preview-image"
                    alt="预览图片"
                />
                <VideoPlayer
                    v-else-if="isVideo"
                    :src="previewUrl"
                    :poster="videoPoster"
                    :thumbnails="previewFile?.thumbnails_url"
                    :thumbnails-count="previewFile?.thumbnails_count || 0"
                    @ready="onVideoReady"
                    @error="onVideoError"
                />
                <audio
                    v-else-if="isAudio"
                    :src="previewUrl"
                    controls
                    class="preview-audio"
                />
                <div v-else class="preview-unsupported">
                    <el-icon :size="64">
                        <Document/>
                    </el-icon>
                    <p>该文件类型不支持预览</p>
                    <el-button type="primary" @click="downloadFile">下载文件</el-button>
                </div>
            </div>
        </el-dialog>
    </div>
</template>

<script setup>
import {ref, computed, onMounted, onUnmounted, reactive} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Document, Loading} from '@element-plus/icons-vue'
import {useUserStore} from '@/stores/user'
import {getMediaUrl} from '@/utils'
import VideoPlayer from '@/components/VideoPlayer.vue'
import TablePage from '@/components/TablePage.vue'
import PreviewButton from '@/components/PreviewButton.vue'
import UploadButton from '@/components/UploadButton.vue'
import RetryButton from '@/components/RetryButton.vue'
import {deleteMedia, getMedia, regenerateThumbnails} from '@/api/media'

const pagination = reactive({
    page: 1,
    page_size: 10,
    total: 0,
})

const userStore = useUserStore()
const loading = ref(false)
const mediaList = ref([])
const previewVisible = ref(false)
const previewFile = ref(null)
const videoPoster = ref('')
const uploading = ref(false)
const uploadProgress = ref(0)
let refreshTimer = null

const baseUrl = import.meta.env.VITE_API_BASE_URL || '/api'
const uploadUrl = computed(() => `${baseUrl}/media/`)
const uploadHeaders = computed(() => {
    const token = userStore.accessToken
    return {
        'Authorization': `Bearer ${token}`
    }
})

const isImage = computed(() => {
    if (!previewFile.value) return false
    const type = previewFile.value.file_type || ''
    return type.startsWith('image/')
})

const isVideo = computed(() => {
    if (!previewFile.value) return false
    const type = previewFile.value.file_type || ''
    return type.startsWith('video/')
})

const isAudio = computed(() => {
    if (!previewFile.value) return false
    const type = previewFile.value.file_type || ''
    return type.startsWith('audio/')
})

const previewUrl = computed(() => {
    if (!previewFile.value) return ''
    if (isVideo.value) {
        return `${baseUrl}/media/${previewFile.value.id}/`
    }
    const url = previewFile.value.url || previewFile.value.file
    return getMediaUrl(url)
})

const handlePageChange = ({page, pageSize}) => {
    pagination.page = page
    pagination.page_size = pageSize
    fetchMedia()
}

const hasProcessingThumbnails = () => {
    return mediaList.value.some(item => item.thumbnail_status === 'pending' || item.thumbnail_status === 'processing')
}

const startAutoRefresh = () => {
    if (refreshTimer) {
        clearInterval(refreshTimer)
    }
    refreshTimer = setInterval(() => {
        if (hasProcessingThumbnails()) {
            fetchMedia()
        } else {
            clearInterval(refreshTimer)
            refreshTimer = null
        }
    }, 3000)
}

const fetchMedia = async () => {
    loading.value = true
    try {
        const offset = (pagination.page - 1) * pagination.page_size
        const {data} = await getMedia({
            limit: pagination.page_size,
            offset: offset
        })
        mediaList.value = data.results || data
        pagination.total = data.count || mediaList.value.length
        if (hasProcessingThumbnails()) {
            startAutoRefresh()
        }
    } catch (error) {
        ElMessage.error('获取媒体列表失败')
    } finally {
        loading.value = false
    }
}

const formatSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
}

const handleUploadProgress = (event) => {
    uploading.value = true
    uploadProgress.value = Math.round(event.percent)
}

const beforeUpload = (file) => {
    // 验证文件大小（视频除外）
    const isVideo = file.type.startsWith('video/')
    if (!isVideo) {
        const maxSize = 10 * 1024 * 1024
        if (file.size > maxSize) {
            ElMessage.error('文件大小不能超过 10MB（视频文件不限大小）')
            return false
        }
    }

    // 验证文件类型
    const allowedTypes = [
        'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml',
        'video/mp4', 'video/webm', 'video/ogg', 'video/quicktime',
        'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]

    if (!allowedTypes.includes(file.type)) {
        ElMessage.error(
            `不支持的文件类型：${file.type}。支持的类型：图片（jpg, png, gif, webp, svg）、视频（mp4, webm, ogg）、文档（pdf, doc, docx）`
        )
        return false
    }

    // 验证文件扩展名
    const allowedExtensions = [
        '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg',
        '.mp4', '.webm', '.ogg', '.mov',
        '.pdf', '.doc', '.docx'
    ]
    const ext = '.' + file.name.split('.').pop().toLowerCase()
    if (!allowedExtensions.includes(ext)) {
        ElMessage.error(
            `不支持的文件扩展名：${ext}。支持的扩展名：${allowedExtensions.join(', ')}`
        )
        return false
    }

    return true
}

const handleUploadSuccess = () => {
    uploading.value = false
    uploadProgress.value = 0
    ElMessage.success('上传成功')
    fetchMedia()
}

const handleUploadError = (error) => {
    uploading.value = false
    uploadProgress.value = 0
    const errorMsg = error?.response?.data?.file?.[0] || error?.response?.data?.error || '上传失败'
    ElMessage.error(errorMsg)
}

const handlePreview = (row) => {
    previewFile.value = row
    previewVisible.value = true
}

const handleCopyLink = (row) => {
    const fileUrl = getMediaUrl(row.file)

    // 优先使用 Clipboard API
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(fileUrl).then(() => {
            ElMessage.success('链接已复制到剪贴板')
        }).catch(() => {
            fallbackCopyText(fileUrl)
        })
    } else {
        // 降级方案
        fallbackCopyText(fileUrl)
    }
}

// 降级复制方法
const fallbackCopyText = (text) => {
    const textArea = document.createElement('textarea')
    textArea.value = text
    textArea.style.position = 'fixed'
    textArea.style.top = '0'
    textArea.style.left = '0'
    textArea.style.width = '2em'
    textArea.style.height = '2em'
    textArea.style.padding = '0'
    textArea.style.border = 'none'
    textArea.style.outline = 'none'
    textArea.style.boxShadow = 'none'
    textArea.style.background = 'transparent'
    textArea.style.opacity = '0'

    document.body.appendChild(textArea)
    textArea.focus()
    textArea.select()

    try {
        const successful = document.execCommand('copy')
        if (successful) {
            ElMessage.success('链接已复制到剪贴板')
        } else {
            ElMessage.error('复制失败，请手动复制')
        }
    } catch (err) {
        ElMessage.error('浏览器不支持复制，请手动复制')
    } finally {
        document.body.removeChild(textArea)
    }
}

const onVideoReady = () => {
}

const onVideoError = (error) => {
    ElMessage.error('视频加载失败，请检查视频格式或网络连接')
}

const downloadFile = () => {
    if (previewUrl.value) {
        const link = document.createElement('a')
        link.href = previewUrl.value
        link.download = previewFile.value?.filename || 'download'
        link.target = '_blank'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
    }
}

const handleDelete = async (row) => {
    await ElMessageBox.confirm('确定删除该文件？', '提示', {type: 'warning'})
    try {
        await deleteMedia(row.id)
        ElMessage.success('删除成功')
        await fetchMedia()
    } catch (error) {
        ElMessage.error('删除失败')
    }
}

const handleRegenerateThumbnails = async (row) => {
    try {
        // await api.post(`/media/${row.id}/regenerate_thumbnails/`)
        await regenerateThumbnails(row.id)
        ElMessage.success('缩略图生成任务已启动')
        await fetchMedia()
    } catch (error) {
        ElMessage.error('启动缩略图生成失败')
    }
}

onMounted(() => {
    fetchMedia()
})

onUnmounted(() => {
    if (refreshTimer) {
        clearInterval(refreshTimer)
        refreshTimer = null
    }
})
</script>

<style scoped>
.media-page {
    padding: 20px;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.preview-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 300px;
}

.preview-image {
    max-width: 100%;
    max-height: 60vh;
    object-fit: contain;
}

.preview-audio {
    width: 100%;
}

.preview-unsupported {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    color: #909399;
}

.preview-unsupported p {
    margin: 0;
}

.action-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    align-items: center;
}

.action-buttons .el-button {
    padding: 4px 8px;
    font-size: 12px;
}
</style>
