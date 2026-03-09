<template>
  <div class="profile-page">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>个人信息</span>
          </template>
          <div class="avatar-section">
            <el-avatar :size="100" :src="getAvatarUrl(userStore.user?.avatar)" />
            <el-upload
              class="avatar-upload"
              :action="uploadUrl"
              :headers="headers"
              :show-file-list="false"
              :on-success="handleAvatarSuccess"
              :on-error="handleAvatarError"
            >
              <el-button type="primary" link>更换头像</el-button>
            </el-upload>
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
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { updateProfile, changePassword } from '@/api/user'

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

const getAvatarUrl = (avatar) => {
  if (!avatar) return ''
  if (avatar.startsWith('http')) return avatar
  return `http://localhost:8001${avatar}`
}

const handleAvatarSuccess = async (response) => {
  const avatarUrl = response.url || response.file
  if (avatarUrl) {
    try {
      await updateProfile({ avatar_url: avatarUrl })
      await userStore.fetchProfile()
      ElMessage.success('头像更新成功')
    } catch (error) {
      ElMessage.error('头像更新失败')
    }
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
}

.avatar-upload {
  margin-top: 12px;
}
</style>
