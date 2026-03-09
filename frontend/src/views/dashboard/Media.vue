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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import api from '@/api'

const userStore = useUserStore()
const loading = ref(false)
const mediaList = ref([])
const page = ref(1)
const total = ref(0)

const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api'
const uploadUrl = computed(() => `${baseUrl}/media/`)
const headers = computed(() => ({ Authorization: `Bearer ${userStore.token}` }))

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
  const fileUrl = row.url || row.file
  if (fileUrl) {
    const fullUrl = fileUrl.startsWith('http') ? fileUrl : `http://localhost:8001${fileUrl}`
    window.open(fullUrl, '_blank')
  } else {
    ElMessage.warning('文件 URL 不可用')
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
</style>
