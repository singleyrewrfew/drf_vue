<template>
  <div class="media-page">
    <el-card>
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
            <UploadButton :loading="uploading" :progress="uploadProgress" />
          </el-upload>
        </div>
      </template>
      <el-table :data="mediaList" v-loading="loading" stripe>
        <el-table-column prop="filename" label="文件名" min-width="200" show-overflow-tooltip />
        <el-table-column prop="file_type" label="类型" width="150" />
        <el-table-column prop="file_size" label="大小" width="100">
          <template #default="{ row }">
            {{ formatSize(row.file_size) }}
          </template>
        </el-table-column>
        <el-table-column label="缩略图" width="150">
          <template #default="{ row }">
            <template v-if="row.is_video">
              <div class="thumbnail-status">
                <el-tag v-if="row.thumbnail_status === 'pending'" type="info" size="small">等待中</el-tag>
                <el-tag v-else-if="row.thumbnail_status === 'processing'" type="warning" size="small">
                  <span style="display: inline-flex; align-items: center; gap: 4px;">
                    <el-icon class="is-loading"><Loading /></el-icon>
                    <span>生成中</span>
                  </span>
                </el-tag>
                <el-tag v-else-if="row.thumbnail_status === 'completed'" type="success" size="small">已完成</el-tag>
                <div v-else-if="row.thumbnail_status === 'failed'" class="failed-status">
                  <el-tag type="danger" size="small">失败</el-tag>
                  <RetryButton @click="handleRegenerateThumbnails(row)" />
                </div>
              </div>
            </template>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="uploader_name" label="上传者" width="120" />
        <el-table-column prop="created_at" label="上传时间" width="180" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <PreviewButton @click="handlePreview(row)" />
              <DeleteButton @click="handleDelete(row)" />
            </div>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="fetchMedia"
        @size-change="handleSizeChange"
      />
    </el-card>

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
          <el-icon :size="64"><Document /></el-icon>
          <p>该文件类型不支持预览</p>
          <el-button type="primary" @click="downloadFile">下载文件</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document, Loading } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { getMediaUrl } from '@/utils'
import VideoPlayer from '@/components/VideoPlayer.vue'
import PreviewButton from '@/components/PreviewButton.vue'
import DeleteButton from '@/components/DeleteButton.vue'
import UploadButton from '@/components/UploadButton.vue'
import RetryButton from '@/components/RetryButton.vue'
import api from '@/api'

const userStore = useUserStore()
const loading = ref(false)
const mediaList = ref([])
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const previewVisible = ref(false)
const previewFile = ref(null)
const videoPoster = ref('')
const uploading = ref(false)
const uploadProgress = ref(0)
let refreshTimer = null

const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api'
const uploadUrl = computed(() => `${baseUrl}/media/`)
const uploadHeaders = computed(() => {
  const token = userStore.token
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
    const offset = (page.value - 1) * pageSize.value
    const { data } = await api.get('/media/', { 
      params: { 
        limit: pageSize.value,
        offset: offset
      }
    })
    mediaList.value = data.results || data
    total.value = data.count || mediaList.value.length
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

const onVideoReady = () => {}

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
  await ElMessageBox.confirm('确定删除该文件？', '提示', { type: 'warning' })
  try {
    await api.delete(`/media/${row.id}/`)
    ElMessage.success('删除成功')
    fetchMedia()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

const handleRegenerateThumbnails = async (row) => {
  try {
    await api.post(`/media/${row.id}/regenerate_thumbnails/`)
    ElMessage.success('缩略图生成任务已启动')
    fetchMedia()
  } catch (error) {
    ElMessage.error('启动缩略图生成失败')
  }
}

const handleSizeChange = () => {
  page.value = 1
  fetchMedia()
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
</style>
