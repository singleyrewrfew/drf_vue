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
                        :before-upload="validateFile"
                        :on-success="onUploadSuccess"
                        :on-error="handleUploadError"
                        :on-progress="handleUploadProgress"
                        :on-change="handleFileChange"
                        :show-file-list="false"
                        multiple
                    >
                        <UploadButton 
                            :loading="uploading" 
                            :progress="uploadProgress"
                            :text="uploadButtonText"
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
                    <ThumbnailStatus 
                        v-if="row.is_video" 
                        :status="row.thumbnail_status"
                        @retry="handleRegenerateThumbnails(row)"
                    />
                    <span v-else>-</span>
                </template>
            </el-table-column>
            <el-table-column prop="uploader_name" label="上传者" width="120"/>
            <el-table-column prop="created_at" label="上传时间" width="180"/>
            <el-table-column prop="url" label="文件路径" width="180" show-overflow-tooltip/>
            <template #actions="{ row }">
                <PreviewButton @click="openPreview(row)"/>
                <el-button type="primary" size="small" @click="copyLink(row)">
                    复制链接
                </el-button>
            </template>
        </TablePage>

        <el-dialog
            v-model="previewVisible"
            :title="previewFile?.filename || '预览'"
            :width="dialogWidth"
            destroy-on-close
        >
            <div class="preview-container">
                <img v-if="isImage" :src="previewUrl" class="preview-image" alt="预览图片"/>
                <VideoPlayer
                    v-else-if="isVideo"
                    :key="previewFile?.id"
                    :src="previewUrl"
                    :poster="videoPoster"
                    :thumbnails="videoThumbnails"
                    :thumbnails-count="videoThumbnailsCount"
                    @error="onVideoError"
                />
                <audio v-else-if="isAudio" :src="previewUrl" controls class="preview-audio"/>
                <div v-else class="preview-unsupported">
                    <el-icon :size="64"><Document/></el-icon>
                    <p>该文件类型不支持预览</p>
                    <el-button type="primary" @click="downloadFile">下载文件</el-button>
                </div>
            </div>
        </el-dialog>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document } from '@element-plus/icons-vue'
import VideoPlayer from '@/components/VideoPlayer.vue'
import TablePage from '@/components/TablePage.vue'
import PreviewButton from '@/components/PreviewButton.vue'
import UploadButton from '@/components/UploadButton.vue'
import ThumbnailStatus from '@/components/ThumbnailStatus.vue'
import { useMediaUpload, useMediaPreview, useThumbnailSSE } from '@/composables'
import { deleteMedia, getMedia, regenerateThumbnails } from '@/api/media'

const baseUrl = import.meta.env.VITE_API_BASE_URL || '/api'

const pagination = reactive({ page: 1, page_size: 10, total: 0 })
const loading = ref(false)
const mediaList = ref([])

const {
    uploading, uploadProgress, uploadUrl, uploadHeaders, uploadButtonText,
    validateFile, handleFileChange, handleUploadProgress, handleUploadSuccess, handleUploadError,
} = useMediaUpload(baseUrl)

const {
    previewVisible, previewFile, videoPoster,
    isImage, isVideo, isAudio, previewUrl,
    videoThumbnails, videoThumbnailsCount, dialogWidth,
    openPreview, copyLink, downloadFile, onVideoError,
} = useMediaPreview(baseUrl)

const { subscribeToThumbnailStatus, closeAllConnections, subscribeToPendingVideos } = useThumbnailSSE(baseUrl)

const formatSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
}

const updateMediaFromSSE = (sseData) => {
    const mediaId = sseData.media_id
    const index = mediaList.value.findIndex(m => m.id === mediaId)
    if (index === -1) return
    mediaList.value[index].thumbnail_status = sseData.thumbnail_status
    if (sseData.thumbnails_url) {
        mediaList.value[index].thumbnails_url = sseData.thumbnails_url
    }
    if (sseData.thumbnails_count) {
        mediaList.value[index].thumbnails_count = sseData.thumbnails_count
    }
}

const sseCallbacks = {
    onStatusChange: updateMediaFromSSE,
    onComplete: updateMediaFromSSE,
}

const fetchMedia = async () => {
    loading.value = true
    try {
        const offset = (pagination.page - 1) * pagination.page_size
        const { data } = await getMedia({ limit: pagination.page_size, offset })
        mediaList.value = data.results || data
        pagination.total = data.count || mediaList.value.length
        subscribeToPendingVideos(mediaList.value, sseCallbacks)
    } catch {
        ElMessage.error('获取媒体列表失败')
    } finally {
        loading.value = false
    }
}

const handlePageChange = ({ page, pageSize }) => {
    pagination.page = page
    pagination.page_size = pageSize
    fetchMedia()
}

const onUploadSuccess = (response, file, fileList) => {
    handleUploadSuccess(response, file, fileList, {
        onSuccess: (mediaData) => {
            if (mediaData?.is_video && mediaData?.id) {
                subscribeToThumbnailStatus(mediaData.id, sseCallbacks)
            }
            if (mediaData?.id) {
                const exists = mediaList.value.some(m => m.id === mediaData.id)
                if (!exists) {
                    mediaList.value.unshift(mediaData)
                    pagination.total += 1
                }
            }
        }
    })
}

const handleDelete = async (row) => {
    await ElMessageBox.confirm('确定删除该文件？', '提示', { type: 'warning' })
    try {
        await deleteMedia(row.id)
        ElMessage.success('删除成功')
        await fetchMedia()
    } catch {
        ElMessage.error('删除失败')
    }
}

const handleRegenerateThumbnails = async (row) => {
    try {
        await regenerateThumbnails(row.id)
        ElMessage.success('缩略图生成任务已启动')
        await fetchMedia()
    } catch {
        ElMessage.error('启动缩略图生成失败')
    }
}

onMounted(() => fetchMedia())
onUnmounted(() => closeAllConnections())
</script>

<style scoped>
.media-page { padding: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.preview-container { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 300px; }
.preview-image { max-width: 100%; max-height: 60vh; object-fit: contain; }
.preview-audio { width: 100%; }
.preview-unsupported { display: flex; flex-direction: column; align-items: center; gap: 16px; color: #909399; }
.preview-unsupported p { margin: 0; }
</style>
