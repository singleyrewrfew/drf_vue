<template>
  <div class="profile-page">
    <div class="profile-header">
      <h1 class="page-title">个人设置</h1>
      <p class="page-subtitle">管理您的账户信息和安全设置</p>
    </div>
    
    <div class="profile-content">
      <div class="profile-card">
        <div class="card-header">
          <div class="card-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
          </div>
          <div class="card-title">
            <h3>个人信息</h3>
            <p>您的头像和基本资料</p>
          </div>
        </div>
        
        <div class="card-body">
          <div class="avatar-section">
            <div class="avatar-wrapper">
              <el-avatar :size="100" :src="getAvatarUrl(userStore.user?.avatar_url || userStore.user?.avatar)" />
            </div>
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
                <UploadButtonSmall>上传头像</UploadButtonSmall>
              </el-upload>
              <UploadButtonSmall @click="showMediaDialog = true">从媒体库选择</UploadButtonSmall>
            </div>
          </div>
          
          <div class="info-list">
            <div class="info-item">
              <div class="info-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
                <span>用户名</span>
              </div>
              <div class="info-value">{{ userStore.user?.username }}</div>
            </div>
            <div class="info-item">
              <div class="info-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                  <polyline points="22,6 12,13 2,6" />
                </svg>
                <span>邮箱</span>
              </div>
              <div class="info-value">{{ userStore.user?.email }}</div>
            </div>
            <div class="info-item">
              <div class="info-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                </svg>
                <span>角色</span>
              </div>
              <div class="info-value">
                <span class="role-tag" :class="userStore.user?.role_code || 'user'">
                  {{ userStore.user?.role_name || '未分配' }}
                </span>
              </div>
            </div>
            <div class="info-item">
              <div class="info-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                  <line x1="16" y1="2" x2="16" y2="6" />
                  <line x1="8" y1="2" x2="8" y2="6" />
                  <line x1="3" y1="10" x2="21" y2="10" />
                </svg>
                <span>注册时间</span>
              </div>
              <div class="info-value">{{ userStore.user?.created_at }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="profile-card">
        <div class="card-header">
          <div class="card-icon success">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
            </svg>
          </div>
          <div class="card-title">
            <h3>修改邮箱</h3>
            <p>更新您的邮箱地址</p>
          </div>
        </div>
        
        <div class="card-body">
          <el-form ref="formRef" :model="form" :rules="rules" class="profile-form">
            <el-form-item prop="email">
              <div class="form-group">
                <label class="form-label">新邮箱</label>
                <div class="input-wrapper">
                  <div class="input-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                      <polyline points="22,6 12,13 2,6" />
                    </svg>
                  </div>
                  <input v-model="form.email" type="email" placeholder="请输入新邮箱" class="form-input" />
                </div>
              </div>
            </el-form-item>
            <div class="form-actions">
              <button type="button" class="save-btn" @click="handleUpdateProfile" :disabled="loading">
                <span v-if="!loading">保存修改</span>
                <span v-else class="loading-spinner"></span>
              </button>
            </div>
          </el-form>
        </div>
      </div>
      
      <div class="profile-card">
        <div class="card-header">
          <div class="card-icon warning">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
              <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>
          </div>
          <div class="card-title">
            <h3>修改密码</h3>
            <p>定期更换密码可以提高账户安全性</p>
          </div>
        </div>
        
        <div class="card-body">
          <el-form ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" class="profile-form">
            <el-form-item prop="old_password">
              <div class="form-group">
                <label class="form-label">原密码</label>
                <div class="input-wrapper">
                  <div class="input-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                      <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                    </svg>
                  </div>
                  <input v-model="passwordForm.old_password" :type="showOldPassword ? 'text' : 'password'" placeholder="请输入原密码" class="form-input" />
                  <div class="input-suffix" @click="showOldPassword = !showOldPassword">
                    <svg v-if="showOldPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
                      <line x1="1" y1="1" x2="23" y2="23" />
                    </svg>
                    <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                  </div>
                </div>
              </div>
            </el-form-item>
            <el-form-item prop="new_password">
              <div class="form-group">
                <label class="form-label">新密码</label>
                <div class="input-wrapper">
                  <div class="input-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                      <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                    </svg>
                  </div>
                  <input v-model="passwordForm.new_password" :type="showNewPassword ? 'text' : 'password'" placeholder="请输入新密码" class="form-input" />
                  <div class="input-suffix" @click="showNewPassword = !showNewPassword">
                    <svg v-if="showNewPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
                      <line x1="1" y1="1" x2="23" y2="23" />
                    </svg>
                    <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                  </div>
                </div>
              </div>
            </el-form-item>
            <el-form-item prop="new_password_confirm">
              <div class="form-group">
                <label class="form-label">确认新密码</label>
                <div class="input-wrapper">
                  <div class="input-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                      <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                    </svg>
                  </div>
                  <input v-model="passwordForm.new_password_confirm" :type="showConfirmPassword ? 'text' : 'password'" placeholder="请再次输入新密码" class="form-input" />
                  <div class="input-suffix" @click="showConfirmPassword = !showConfirmPassword">
                    <svg v-if="showConfirmPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
                      <line x1="1" y1="1" x2="23" y2="23" />
                    </svg>
                    <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                  </div>
                </div>
              </div>
            </el-form-item>
            <div class="form-actions">
              <button type="button" class="save-btn warning" @click="handleChangePassword" :disabled="passwordLoading">
                <span v-if="!passwordLoading">修改密码</span>
                <span v-else class="loading-spinner"></span>
              </button>
            </div>
          </el-form>
        </div>
      </div>
    </div>

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
import UploadButtonSmall from '@/components/UploadButtonSmall.vue'

const userStore = useUserStore()
const formRef = ref()
const passwordFormRef = ref()
const loading = ref(false)
const passwordLoading = ref(false)
const showOldPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

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
  } catch (error) {
    console.error('获取媒体列表失败:', error)
  } finally {
    mediaLoading.value = false
  }
}

const filteredMedia = computed(() => {
  let images = mediaList.value.filter(media => {
    return media.is_image || (media.file_type && media.file_type.startsWith('image/'))
  })
  
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
    let avatarPath = selectedMedia.value.url
    
    if (avatarPath && avatarPath.startsWith('http')) {
      const mediaIndex = avatarPath.indexOf('/media/')
      if (mediaIndex !== -1) {
        avatarPath = avatarPath.substring(mediaIndex)
      }
    }
    
    if (!avatarPath.startsWith('/media/') && !avatarPath.startsWith('media/')) {
      avatarPath = '/media/' + avatarPath
    }
    
    if (!avatarPath) {
      ElMessage.error('未找到媒体路径')
      return
    }
    
    await updateProfile({ avatar_url: avatarPath })
    await userStore.fetchProfile(true)
    ElMessage.success('头像更新成功')
    showMediaDialog.value = false
    selectedMedia.value = null
    mediaSearch.value = ''
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '头像更新失败')
  }
}

const handleAvatarSuccess = async (response) => {
  if (response && response.url) {
    try {
      let avatarPath = response.url
      if (avatarPath && avatarPath.startsWith('http')) {
        const mediaIndex = avatarPath.indexOf('/media/')
        if (mediaIndex !== -1) {
          avatarPath = avatarPath.substring(mediaIndex)
        }
      }
      
      if (!avatarPath.startsWith('/media/') && !avatarPath.startsWith('media/')) {
        avatarPath = '/media/' + avatarPath
      }
      
      await updateProfile({ avatar_url: avatarPath })
      await userStore.fetchProfile(true)
      ElMessage.success('头像更新成功')
    } catch (error) {
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
  padding: 24px;
  max-width: 900px;
  margin: 0 auto;
}

.profile-header {
  margin-bottom: 32px;
}

.page-title {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #303133;
}

.page-subtitle {
  margin: 8px 0 0;
  font-size: 14px;
  color: #909399;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.profile-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.03) 100%);
  border-bottom: 1px solid #f0f0f0;
}

.card-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-icon svg {
  width: 24px;
  height: 24px;
  color: #fff;
}

.card-icon.success {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.card-icon.warning {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.card-title h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.card-title p {
  margin: 4px 0 0;
  font-size: 13px;
  color: #909399;
}

.card-body {
  padding: 24px;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-bottom: 24px;
  margin-bottom: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.avatar-wrapper {
  position: relative;
  cursor: pointer;
}

.avatar-wrapper :deep(.el-avatar) {
  border: 3px solid #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.avatar-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.avatar-upload {
  display: inline-flex;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: #f9fafb;
  border-radius: 10px;
}

.info-label {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #606266;
  font-size: 14px;
}

.info-label svg {
  width: 18px;
  height: 18px;
  color: #909399;
}

.info-value {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
}

.role-tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.role-tag.admin {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
  color: #667eea;
}

.role-tag.editor {
  background: linear-gradient(135deg, rgba(240, 147, 251, 0.15) 0%, rgba(245, 87, 108, 0.15) 100%);
  color: #f5576c;
}

.role-tag.user {
  background: rgba(144, 147, 153, 0.15);
  color: #909399;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background: #f5f7fa;
  border: 2px solid transparent;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.input-wrapper:focus-within {
  background: #fff;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.input-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
  flex-shrink: 0;
}

.input-icon svg {
  width: 18px;
  height: 18px;
}

.form-input {
  flex: 1;
  height: 44px;
  border: none;
  background: transparent;
  font-size: 14px;
  color: #303133;
  outline: none;
}

.form-input::placeholder {
  color: #c0c4cc;
}

.input-suffix {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
  cursor: pointer;
  transition: color 0.3s ease;
  flex-shrink: 0;
}

.input-suffix:hover {
  color: #667eea;
}

.input-suffix svg {
  width: 18px;
  height: 18px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 8px;
}

.save-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 24px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.35);
  position: relative;
  overflow: hidden;
}

.save-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.6s ease;
}

.save-btn:hover::before {
  left: 100%;
}

.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.45);
}

.save-btn.warning {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  box-shadow: 0 4px 12px rgba(245, 87, 108, 0.35);
}

.save-btn.warning:hover {
  box-shadow: 0 6px 16px rgba(245, 87, 108, 0.45);
}

.save-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

:deep(.el-form-item) {
  margin-bottom: 0;
}

:deep(.el-form-item__error) {
  padding-top: 4px;
  padding-left: 12px;
}

/* 媒体库对话框样式 */
.media-list-container {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 8px 8px 24px 8px;
  max-height: 400px;
}

.media-list-container :deep(.el-col) {
  margin-bottom: 16px;
}

.media-card-selected {
  border: 2px solid #667eea !important;
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
