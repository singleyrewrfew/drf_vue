<template>
  <div class="profile-page">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>个人信息</span>
          </template>
          <div class="avatar-section">
            <el-avatar :size="100" :src="getAvatarUrl(userStore.user?.avatar_url || userStore.user?.avatar)" />
            <div class="avatar-actions">
              <el-upload
                class="avatar-upload"
                :action="uploadUrl"
                :headers="headers"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :on-error="handleAvatarError"
                name="file"
              >
                <el-button type="primary" link>上传头像</el-button>
              </el-upload>
              <el-button type="primary" link @click="showMediaDialog = true">从媒体库选择</el-button>
            </div>
          </div>
          <el-descriptions :column="1" border style="margin-top: 20px">
            <el-descriptions-item label="用户名">{{ userStore.user?.username }}</el-descriptions-item>
            <el-descriptions-item label="邮箱">{{ userStore.user?.email }}</el-descriptions-item>
            <el-descriptions-item label="角色">
              <el-tag :type="getRoleType(userStore.user?.role_code)">
                {{ userStore.user?.role_name || '未分配' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="注册时间">{{ userStore.user?.created_at }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card>
          <template #header>
            <span>修改信息</span>
          </template>
          <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="form.email" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleUpdateProfile" :loading="loading">
                保存修改
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
        <el-card style="margin-top: 20px">
          <template #header>
            <span>修改密码</span>
          </template>
          <el-form ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" label-width="100px">
            <el-form-item label="原密码" prop="old_password">
              <el-input v-model="passwordForm.old_password" type="password" show-password />
            </el-form-item>
            <el-form-item label="新密码" prop="new_password">
              <el-input v-model="passwordForm.new_password" type="password" show-password />
            </el-form-item>
            <el-form-item label="确认新密码" prop="new_password_confirm">
              <el-input v-model="passwordForm.new_password_confirm" type="password" show-password />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleChangePassword" :loading="passwordLoading">
                修改密码
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>

    <!-- 媒体库选择对话框 -->
    <el-dialog 
      v-model="showMediaDialog" 
      title="从媒体库选择头像" 
      width="800px"
      center
      :close-on-click-modal="false"
    >
      <el-input v-model="mediaSearch" placeholder="搜索媒体文件" style="margin-bottom: 16px" clearable />
      <div class="media-list-container">
        <el-row :gutter="16" v-loading="mediaLoading">
          <el-col :span="6" v-for="media in filteredMedia" :key="media.id">
            <el-card shadow="hover" :class="{'media-card-selected': selectedMedia?.id === media.id}" @click="selectedMedia = media">
              <img :src="getMediaUrl(media.url)" class="media-image" />
              <div class="media-info">
                <span class="media-name">{{ media.filename }}</span>
              </div>
            </el-card>
          </el-col>
        </el-row>
        <el-empty v-if="!mediaLoading && filteredMedia.length === 0" description="暂无媒体文件" />
      </div>
      <template #footer>
        <el-button @click="showMediaDialog = false">取消</el-button>
        <el-button type="primary" @click="handleMediaSelect" :disabled="!selectedMedia">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { updateProfile, changePassword } from '@/api/user'
import { getAvatarUrl } from '@/utils'
import api from '@/api'

const userStore = useUserStore()
const formRef = ref()
const passwordFormRef = ref()
const loading = ref(false)
const passwordLoading = ref(false)

const form = reactive({
  email: '',
})

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  new_password_confirm: '',
})

const rules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' },
  ],
}

const validatePassword = (rule, value, callback) => {
  if (value !== passwordForm.new_password) {
    callback(new Error('两次密码不一致'))
  } else {
    callback()
  }
}

const passwordRules = {
  old_password: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' },
  ],
  new_password_confirm: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    { validator: validatePassword, trigger: 'blur' },
  ],
}

const getRoleType = (roleCode) => {
  const typeMap = {
    admin: 'danger',
    editor: 'warning',
    user: 'info',
  }
  return typeMap[roleCode] || 'info'
}

const uploadUrl = computed(() => `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api'}/media/`)
const headers = computed(() => ({ Authorization: `Bearer ${userStore.token}` }))

// 媒体库相关
const showMediaDialog = ref(false)
const mediaLoading = ref(false)
const mediaList = ref([])
const mediaSearch = ref('')
const selectedMedia = ref(null)

const getMediaUrl = (file) => {
  if (!file) return ''
  if (file.startsWith('http')) return file
  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api'
  return `${baseUrl.replace('/api', '')}${file}`
}

const fetchMedia = async () => {
  mediaLoading.value = true
  try {
    const { data } = await api.get('/media/', { params: { limit: 50 } })
    mediaList.value = data.results || data
    console.log('媒体列表:', mediaList.value)
  } catch (error) {
    console.error('获取媒体列表失败:', error)
  } finally {
    mediaLoading.value = false
  }
}

const filteredMedia = computed(() => {
  // 只显示图片类型的媒体
  let images = mediaList.value.filter(media => {
    // 检查 is_image 字段或 file_type 以 image/ 开头
    return media.is_image || (media.file_type && media.file_type.startsWith('image/'))
  })
  
  // 如果有搜索关键字，进一步过滤
  if (mediaSearch.value) {
    images = images.filter(media => 
      (media.filename || media.name || '')?.toLowerCase().includes(mediaSearch.value.toLowerCase())
    )
  }
  
  return images
})

const handleMediaSelect = async () => {
  if (!selectedMedia.value) return
  
  try {
    // 获取媒体的 URL
    let avatarPath = selectedMedia.value.url
    
    console.log('原始媒体 URL:', avatarPath)
    
    // 如果是完整 URL，提取相对路径
    if (avatarPath && avatarPath.startsWith('http')) {
      // 从完整 URL 中提取 /media/ 部分
      const mediaIndex = avatarPath.indexOf('/media/')
      if (mediaIndex !== -1) {
        avatarPath = avatarPath.substring(mediaIndex)
        console.log('提取的相对路径:', avatarPath)
      }
    }
    
    // 确保路径以 /media/ 开头
    if (!avatarPath.startsWith('/media/') && !avatarPath.startsWith('media/')) {
      avatarPath = '/media/' + avatarPath
    }
    
    console.log('最终头像路径:', avatarPath)
    
    if (!avatarPath) {
      ElMessage.error('未找到媒体路径')
      return
    }
    
    // 传递相对路径给后端
    const response = await updateProfile({ avatar_url: avatarPath })
    console.log('更新响应:', response)
    
    // 强制刷新用户信息
    await userStore.fetchProfile(true)
    ElMessage.success('头像更新成功')
    showMediaDialog.value = false
    selectedMedia.value = null
    mediaSearch.value = ''
  } catch (error) {
    console.error('头像更新失败:', error)
    ElMessage.error(error.response?.data?.message || '头像更新失败')
  }
}

const handleAvatarSuccess = async (response) => {
  console.log('上传响应:', response)
  
  // 上传到媒体库成功，获取返回的 URL
  if (response && response.url) {
    try {
      // 处理路径格式
      let avatarPath = response.url
      if (avatarPath && avatarPath.startsWith('http')) {
        const mediaIndex = avatarPath.indexOf('/media/')
        if (mediaIndex !== -1) {
          avatarPath = avatarPath.substring(mediaIndex)
        }
      }
      
      // 确保路径以 /media/ 开头
      if (!avatarPath.startsWith('/media/') && !avatarPath.startsWith('media/')) {
        avatarPath = '/media/' + avatarPath
      }
      
      console.log('上传后头像路径:', avatarPath)
      
      // 更新用户头像
      await updateProfile({ avatar_url: avatarPath })
      await userStore.fetchProfile(true)
      ElMessage.success('头像更新成功')
    } catch (error) {
      console.error('头像更新失败:', error)
      ElMessage.error(error.response?.data?.message || '头像更新失败')
    }
  } else {
    ElMessage.error('头像上传失败：未返回媒体信息')
  }
}

const handleAvatarError = () => {
  ElMessage.error('头像上传失败')
}

const handleUpdateProfile = async () => {
  await formRef.value.validate()
  loading.value = true
  try {
    await updateProfile(form)
    await userStore.fetchProfile()
    ElMessage.success('修改成功')
  } catch (error) {
    ElMessage.error('修改失败')
  } finally {
    loading.value = false
  }
}

const handleChangePassword = async () => {
  await passwordFormRef.value.validate()
  passwordLoading.value = true
  try {
    await changePassword(passwordForm)
    ElMessage.success('密码修改成功')
    Object.assign(passwordForm, {
      old_password: '',
      new_password: '',
      new_password_confirm: '',
    })
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '密码修改失败')
  } finally {
    passwordLoading.value = false
  }
}

onMounted(() => {
  form.email = userStore.user?.email || ''
  fetchMedia()
})
</script>

<style scoped>
.profile-page {
  padding: 20px;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
}

.avatar-actions {
  display: flex;
  gap: 16px;
  margin-top: 16px;
  justify-content: center;
  align-items: center;
}

.avatar-upload {
  display: inline-flex;
}

.avatar-upload :deep(.el-button) {
  white-space: nowrap;
}

.media-list-container {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 8px 8px 24px 8px;
}

.media-list-container :deep(.el-col) {
  margin-bottom: 16px;
}

.media-list-container :deep(.el-row) {
  margin-bottom: 0 !important;
}

.media-card-selected {
  border: 2px solid #409eff;
}

.media-image {
  width: 100%;
  height: 120px;
  object-fit: contain;
  cursor: pointer;
  background-color: #f5f7fa;
}

.media-info {
  padding: 8px 0;
  text-align: center;
  overflow: hidden;
}

.media-name {
  font-size: 12px;
  color: #606266;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%;
}
</style>

<style>
/* 全局样式：确保对话框固定不动且内容完整显示 */
.el-dialog {
  position: fixed !important;
  top: 50% !important;
  left: 50% !important;
  transform: translate(-50%, -50%) !important;
  margin: 0 !important;
  height: 80vh !important;
  max-height: 80vh !important;
  display: flex !important;
  flex-direction: column !important;
}

.el-dialog__header {
  flex-shrink: 0 !important;
}

.el-dialog__body {
  overflow: hidden !important;
  padding: 20px !important;
  flex: 1 !important;
  display: flex !important;
  flex-direction: column !important;
  min-height: 0 !important;
}

.el-dialog__footer {
  flex-shrink: 0 !important;
}
</style>
