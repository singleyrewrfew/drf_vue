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
                        :on-change="handleFileChange"
                        :show-file-list="false"
                        multiple
                    >
                        <UploadButton 
                            :loading="uploading" 
                            :progress="uploadProgress"
                            :text="totalUploadFiles > 0 ? (completedFiles === totalUploadFiles ? `已完成 (${completedFiles}/${totalUploadFiles}个文件)` : `上传中 (${completedFiles}/${totalUploadFiles}个文件)`) : '上传文件'"
                        />
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
                            <el-tag v-if="row.thumbnail_status === 'pending'" type="info" size="small">
                                <span style="display: inline-flex; align-items: center; gap: 4px;">
                                    <el-icon class="is-loading"><Loading/></el-icon>
                                    <span>等待中</span>
                                </span>
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
                    :key="previewFile?.id"
                    :src="previewUrl"
                    :poster="videoPoster"
                    :thumbnails="videoThumbnails"
                    :thumbnails-count="videoThumbnailsCount"
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
import {ref, computed, onMounted, onUnmounted, reactive, nextTick} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Document, Loading} from '@element-plus/icons-vue'
import {useUserStore} from '@/stores/user'
import {getMediaUrl} from '@/utils'
import VideoPlayer from '@/components/VideoPlayer.vue'
import TablePage from '@/components/TablePage.vue'
import PreviewButton from '@/components/PreviewButton.vue'
import UploadButton from '@/components/UploadButton.vue'
import RetryButton from '@/components/RetryButton.vue'
import {deleteMedia, getMedia, getMediaDetail, regenerateThumbnails} from '@/api/media'

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
const uploadingFiles = ref([]) // 存储正在上传的文件列表
const totalUploadFiles = ref(0) // 存储本次上传的总文件数
const completedFiles = ref(0) // 存储已完成的文件数
const fileProgressMap = ref(new Map()) // 存储每个文件的进度 {uid: percent}
let refreshTimer = null
let eventSources = new Map() // 存储 SSE 连接

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

// 只有在缩略图生成完成时才传递缩略图 URL
const videoThumbnails = computed(() => {
    if (!previewFile.value) return ''
    // 只有 completed 状态才返回缩略图 URL
    if (previewFile.value.thumbnail_status === 'completed' && previewFile.value.thumbnails_url) {
        return previewFile.value.thumbnails_url
    }
    return ''
})

const videoThumbnailsCount = computed(() => {
    if (!previewFile.value) return 0
    // 只有 completed 状态才返回缩略图数量
    if (previewFile.value.thumbnail_status === 'completed') {
        return previewFile.value.thumbnails_count || 0
    }
    return 0
})

const handlePageChange = ({page, pageSize}) => {
    pagination.page = page
    pagination.page_size = pageSize
    fetchMedia()
}

const hasProcessingThumbnails = () => {
    return mediaList.value.some(item => 
        item.is_video && (item.thumbnail_status === 'pending' || item.thumbnail_status === 'processing')
    )
}

/**
 * 为单个视频文件建立 SSE 连接，实时监听状态变化
 */
const subscribeToThumbnailStatus = (mediaId) => {
    // 如果已经存在连接，直接返回（避免重复订阅）
    if (eventSources.has(mediaId)) {
        console.log('[SSE] Connection already exists for', mediaId, ', skipping')
        return
    }
    
    const token = userStore.accessToken
    // EventSource 不支持自定义 headers，通过 URL 参数传递 token
    const url = `${baseUrl}/media/${mediaId}/thumbnail_status/?token=${token}`
    
    console.log('[SSE] Subscribing to media:', mediaId)
    
    // 创建 EventSource
    const eventSource = new EventSource(url)
    
    eventSource.onopen = () => {
        console.log('[SSE] Connection opened for media:', mediaId)
    }
    
    eventSource.onmessage = async (event) => {
        try {
            const data = JSON.parse(event.data)
            
            if (data.error) {
                console.error('[SSE] Error for', mediaId, ':', data.error)
                eventSource.close()
                eventSources.delete(mediaId)
                return
            }
            
            console.log('[SSE] Received update for', mediaId, ':', data.thumbnail_status)
            
            // 更新本地列表中的状态
            const mediaIndex = mediaList.value.findIndex(m => m.id === data.media_id)
            if (mediaIndex !== -1) {
                // 使用 splice 触发 Vue 响应式更新
                const oldStatus = mediaList.value[mediaIndex].thumbnail_status
                mediaList.value[mediaIndex].thumbnail_status = data.thumbnail_status
                
                console.log('[SSE] Updated media', mediaId, 'from', oldStatus, 'to', data.thumbnail_status)
                
                // 如果任务完成，重新获取媒体信息以更新缩略图 URL
                if (data.thumbnail_status === 'completed') {
                    console.log('[SSE] Refreshing media info for', mediaId)
                    try {
                        const {data: mediaDetail} = await getMediaDetail(mediaId)
                        
                        // 更新列表中的完整信息
                        // 使用 splice 确保触发 Vue 响应式更新
                        mediaList.value.splice(mediaIndex, 1, {
                            ...mediaList.value[mediaIndex],
                            ...mediaDetail
                        })
                        console.log('[SSE] Media info refreshed, thumbnails_url:', mediaDetail.thumbnails_url)
                        
                        // 如果当前正在预览该视频，强制更新 previewFile 以触发缩略图重载
                        if (previewFile.value && previewFile.value.id === mediaId) {
                            await nextTick()
                            // 使用 nextTick 确保 DOM 更新后再赋值，或者直接替换整个对象引用
                            const updatedPreview = {
                                ...mediaDetail,
                                // 保留一些可能不在 detail 接口返回但预览需要的字段（如果需要的话）
                            }
                            previewFile.value = updatedPreview
                            console.log('[SSE] Force updated previewFile for thumbnail reload', updatedPreview.thumbnails_url)
                        }
                    } catch (error) {
                        console.error('[SSE] Failed to refresh media info:', error)
                    }
                }
                
                // 如果任务完成或失败，关闭连接
                if (['completed', 'failed'].includes(data.thumbnail_status)) {
                    console.log('[SSE] Task finished for', mediaId, ', closing connection')
                    eventSource.close()
                    eventSources.delete(mediaId)
                }
            } else {
                console.warn('[SSE] Media not found in list:', data.media_id)
            }
        } catch (error) {
            console.error('[SSE] Parse error:', error)
        }
    }
    
    eventSource.onerror = (error) => {
        console.error('[SSE] Connection error for', mediaId, ':', error)
        eventSource.close()
        eventSources.delete(mediaId)
    }
    
    eventSources.set(mediaId, eventSource)
}

/**
 * 关闭所有 SSE 连接
 */
const closeAllEventSources = () => {
    eventSources.forEach((es) => es.close())
    eventSources.clear()
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
        
        // 为所有 pending/processing 状态的视频建立 SSE 连接
        mediaList.value.forEach(item => {
            if (item.is_video && ['pending', 'processing'].includes(item.thumbnail_status)) {
                subscribeToThumbnailStatus(item.id)
            }
        })
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

const handleUploadProgress = (event, file, fileList) => {
    uploading.value = true
    
    // 记录每个文件的进度
    fileProgressMap.value.set(file.uid, event.percent)
    
    // 计算平均进度
    const totalPercent = Array.from(fileProgressMap.value.values()).reduce((sum, p) => sum + p, 0)
    const fileCount = fileProgressMap.value.size
    uploadProgress.value = Math.round(totalPercent / fileCount)
    
    // 更新文件列表
    uploadingFiles.value = fileList
}

const handleFileChange = (file, fileList) => {
    // 当文件被添加到上传列表时，设置总文件数
    if (file.status === 'ready' && totalUploadFiles.value === 0) {
        totalUploadFiles.value = fileList.length
        completedFiles.value = 0 // 重置已完成计数
        console.log('[Upload] Total files selected:', totalUploadFiles.value)
    }
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

const handleUploadSuccess = (response, file, fileList) => {
    // 从进度映射中移除已完成的文件
    fileProgressMap.value.delete(file.uid)
    
    // 增加已完成文件计数
    completedFiles.value += 1
    
    // 更新正在上传的文件列表（用于内部逻辑）
    uploadingFiles.value = fileList.filter(f => f.status === 'uploading')
    
    console.log('[Upload] File uploaded:', response.data?.id, `Completed: ${completedFiles.value}/${totalUploadFiles.value}`)
    
    // 如果是视频文件，立即为它建立 SSE 连接
    if (response.data?.is_video && response.data?.id) {
        const mediaId = response.data.id
        
        // 检查是否已经存在该视频的 SSE 连接
        if (!eventSources.has(mediaId)) {
            console.log('[Upload] Subscribing to new video:', mediaId)
            subscribeToThumbnailStatus(mediaId)
        } else {
            console.log('[Upload] SSE already exists for', mediaId, ', skipping')
        }
        
        // 将新上传的视频添加到列表顶部（如果不存在）
        const exists = mediaList.value.some(m => m.id === mediaId)
        if (!exists) {
            mediaList.value.unshift(response.data)
            pagination.total += 1
        } else {
            // 更新现有记录
            const index = mediaList.value.findIndex(m => m.id === mediaId)
            if (index !== -1) {
                mediaList.value[index] = {...mediaList.value[index], ...response.data}
            }
        }
    }
    
    // 如果所有文件都上传完成
    if (completedFiles.value === totalUploadFiles.value) {
        // uploading.value = false  // 不要立即设置为 false，保持 loading 状态
        uploadProgress.value = 100 // 保持进度为 100%
        
        ElMessage.success(`成功上传 ${fileList.length} 个文件`)
        
        // 延迟刷新列表，确保所有数据都已同步
        setTimeout(() => {
            fetchMedia()
        }, 500)
        
        // 再延迟 2 秒后重置状态，让用户看到完成状态
        setTimeout(() => {
            uploading.value = false // 现在才设置为 false
            totalUploadFiles.value = 0 // 重置总文件数
            completedFiles.value = 0 // 重置已完成文件数
            fileProgressMap.value.clear() // 清空进度映射
            uploadProgress.value = 0
        }, 2000)
    }
}

const handleUploadError = (error, file, fileList) => {
    // 从进度映射中移除失败的文件
    fileProgressMap.value.delete(file.uid)
    
    // 增加已完成文件计数（失败也算完成）
    completedFiles.value += 1
    
    // 更新正在上传的文件列表（用于内部逻辑）
    uploadingFiles.value = fileList.filter(f => f.status === 'uploading')
    
    // 如果所有文件都处理完成（成功或失败）
    if (completedFiles.value === totalUploadFiles.value) {
        // uploading.value = false  // 不要立即设置为 false，保持 loading 状态
        uploadProgress.value = 100 // 保持进度为 100%
        
        // 延迟 2 秒后重置状态
        setTimeout(() => {
            uploading.value = false // 现在才设置为 false
            totalUploadFiles.value = 0 // 重置总文件数
            completedFiles.value = 0 // 重置已完成文件数
            fileProgressMap.value.clear()
            uploadProgress.value = 0
        }, 2000)
    }
    
    const errorMsg = error?.response?.data?.file?.[0] || error?.response?.data?.error || '上传失败'
    ElMessage.error(`${file.name}: ${errorMsg}`)
}

const handlePreview = (row) => {
    previewFile.value = row
    previewVisible.value = true
    // 重置 poster，避免显示旧视频的海报
    videoPoster.value = ''
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
    // 关闭所有 SSE 连接，防止内存泄漏
    closeAllEventSources()
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
