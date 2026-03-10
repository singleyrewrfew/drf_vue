<template>
  <div class="media-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>媒体管理</span>
          <el-upload
            :action="uploadUrl"
            :headers="headers"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
            :show-file-list="false"
            multiple
          >
            <el-button type="primary">上传文件</el-button>
          </el-upload>
        </div>
      </template>
      <el-table :data="mediaList" v-loading="loading" stripe>
        <el-table-column prop="filename" label="文件名" />
        <el-table-column prop="file_type" label="类型" width="150" />
        <el-table-column prop="file_size" label="大小" width="100">
          <template #default="{ row }">
            {{ formatSize(row.file_size) }}
          </template>
        </el-table-column>
        <el-table-column prop="uploader_name" label="上传者" width="120" />
        <el-table-column prop="created_at" label="上传时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" link @click="handlePreview(row)">预览</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        v-model:current-page="page"
        :page-size="20"
        :total="total"
        layout="total, prev, pager, next"
        style="margin-top: 20px; justify-content: flex-end"
        @current-change="fetchMedia"
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
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { getMediaUrl } from '@/utils'
import VideoPlayer from '@/components/VideoPlayer.vue'
import api from '@/api'

const userStore = useUserStore()
const loading = ref(false)
const mediaList = ref([])
const page = ref(1)
const total = ref(0)
const previewVisible = ref(false)
const previewFile = ref(null)
const videoPoster = ref('')

const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api'
const uploadUrl = computed(() => `${baseUrl}/media/`)
const headers = computed(() => ({ Authorization: `Bearer ${userStore.token}` }))

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

const fetchMedia = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/media/', { params: { page: page.value } })
    mediaList.value = data.results || data
    total.value = data.count || mediaList.value.length
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

const handleUploadSuccess = () => {
  ElMessage.success('上传成功')
  fetchMedia()
}

const handleUploadError = () => {
  ElMessage.error('上传失败')
}

const handlePreview = (row) => {
  previewFile.value = row
  previewVisible.value = true
}

const onVideoReady = () => {
  console.log('Video player ready')
}

const onVideoError = (error) => {
  console.error('Video load error:', error)
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

onMounted(() => {
  fetchMedia()
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
</style>
