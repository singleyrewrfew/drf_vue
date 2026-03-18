<template>
  <div class="page">
    <header class="page-header">
      <div class="header-left">
        <button class="btn-back" @click="$router.back()">
          <el-icon><ArrowLeft /></el-icon>
        </button>
      </div>
      <h1 class="page-title">个人资料</h1>
      <div class="header-right"></div>
    </header>
    
    <div class="page-content">
      <div class="profile-form">
        <div class="avatar-section">
          <el-avatar :size="80" :src="getAvatarUrl(form.avatar)">
            {{ userStore.user?.username?.charAt(0).toUpperCase() }}
          </el-avatar>
          <button class="btn btn-outline" @click="handleAvatarChange">更换头像</button>
        </div>
        
        <div class="form-section">
          <div class="form-group">
            <label class="form-label">用户名</label>
            <el-input 
              v-model="form.username" 
              placeholder="请输入用户名"
              size="large"
              clearable
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">邮箱</label>
            <el-input 
              v-model="form.email" 
              type="email"
              placeholder="请输入邮箱"
              size="large"
              clearable
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">昵称</label>
            <el-input 
              v-model="form.nickname" 
              placeholder="请输入昵称"
              size="large"
              clearable
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">个人简介</label>
            <el-input 
              v-model="form.bio" 
              type="textarea"
              :rows="3"
              placeholder="介绍一下自己吧..."
              resize="none"
            />
          </div>
        </div>
        
        <div class="form-actions">
          <button 
            class="btn btn-primary btn-block btn-lg" 
            :disabled="saving"
            @click="handleSave"
          >
            {{ saving ? '保存中...' : '保存修改' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { updateProfile } from '@/api/user'
import { getAvatarUrl } from '@/utils'

const router = useRouter()
const userStore = useUserStore()

const saving = ref(false)
const form = reactive({
  username: '',
  email: '',
  nickname: '',
  bio: '',
  avatar: ''
})

onMounted(() => {
  if (userStore.user) {
    form.username = userStore.user.username || ''
    form.email = userStore.user.email || ''
    form.nickname = userStore.user.nickname || ''
    form.bio = userStore.user.bio || ''
    form.avatar = userStore.user.avatar || ''
  }
})

const handleAvatarChange = () => {
  ElMessage.info('头像上传功能开发中')
}

const handleSave = async () => {
  if (!form.username.trim()) {
    ElMessage.warning('用户名不能为空')
    return
  }
  
  saving.value = true
  try {
    await updateProfile({
      username: form.username,
      email: form.email,
      nickname: form.nickname,
      bio: form.bio
    })
    await userStore.fetchProfile()
    ElMessage.success('保存成功')
    router.back()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.profile-form {
  padding: 20px 16px;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px 0;
  margin-bottom: 8px;
}

.avatar-section .btn {
  margin-top: 16px;
}

.form-section {
  margin-bottom: 24px;
}

.form-actions {
  padding-top: 8px;
}
</style>
