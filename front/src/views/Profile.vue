<template>
  <div class="profile-page">
    <div class="container">
      <el-row :gutter="24">
        <el-col :span="6">
          <div class="profile-card">
            <div class="avatar-section">
              <div class="avatar-wrapper">
                <el-avatar :size="80" :src="getAvatarUrl(userStore.user?.avatar)">{{ userStore.user?.username?.charAt(0).toUpperCase() }}</el-avatar>
              </div>
              <h3>{{ userStore.user?.username }}</h3>
              <p>{{ userStore.user?.email }}</p>
            </div>
            <el-menu :default-active="activeMenu" @select="handleMenuSelect" class="profile-menu">
              <el-menu-item index="profile">
                <el-icon><User /></el-icon>
                <span>个人资料</span>
              </el-menu-item>
              <el-menu-item index="password">
                <el-icon><Lock /></el-icon>
                <span>修改密码</span>
              </el-menu-item>
              <el-menu-item index="comments">
                <el-icon><ChatDotRound /></el-icon>
                <span>我的评论</span>
              </el-menu-item>
            </el-menu>
          </div>
        </el-col>

        <el-col :span="18">
          <div class="content-card">
            <div v-if="activeMenu === 'profile'" class="animate-fade-in">
              <h2>
                <el-icon><User /></el-icon>
                个人资料
              </h2>
              <el-form :model="profileForm" label-position="top" class="profile-form">
                <el-form-item label="用户名">
                  <el-input v-model="profileForm.username" disabled>
                    <template #prefix>
                      <el-icon><User /></el-icon>
                    </template>
                  </el-input>
                </el-form-item>
                <el-form-item label="邮箱">
                  <el-input v-model="profileForm.email">
                    <template #prefix>
                      <el-icon><Message /></el-icon>
                    </template>
                  </el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="updateProfile" class="save-btn">
                    <el-icon><Check /></el-icon>
                    保存修改
                  </el-button>
                </el-form-item>
              </el-form>
            </div>

            <div v-else-if="activeMenu === 'password'" class="animate-fade-in">
              <h2>
                <el-icon><Lock /></el-icon>
                修改密码
              </h2>
              <el-form ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" label-position="top" class="profile-form">
                <el-form-item label="当前密码" prop="old_password">
                  <el-input v-model="passwordForm.old_password" type="password" show-password>
                    <template #prefix>
                      <el-icon><Lock /></el-icon>
                    </template>
                  </el-input>
                </el-form-item>
                <el-form-item label="新密码" prop="new_password">
                  <el-input v-model="passwordForm.new_password" type="password" show-password>
                    <template #prefix>
                      <el-icon><Key /></el-icon>
                    </template>
                  </el-input>
                </el-form-item>
                <el-form-item label="确认新密码" prop="new_password_confirm">
                  <el-input v-model="passwordForm.new_password_confirm" type="password" show-password>
                    <template #prefix>
                      <el-icon><Key /></el-icon>
                    </template>
                  </el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="changePassword" class="save-btn">
                    <el-icon><Check /></el-icon>
                    修改密码
                  </el-button>
                </el-form-item>
              </el-form>
            </div>

            <div v-else-if="activeMenu === 'comments'" class="animate-fade-in">
              <h2>
                <el-icon><ChatDotRound /></el-icon>
                我的评论
              </h2>
              <div class="comment-list">
                <div v-for="(comment, index) in comments" :key="comment.id" class="comment-item" :style="{ animationDelay: `${index * 0.1}s` }">
                  <div class="comment-content">
                    <p>{{ comment.content }}</p>
                    <div class="comment-meta">
                      <span class="article-title">
                        <el-icon><Document /></el-icon>
                        {{ comment.article_title }}
                      </span>
                      <span class="comment-date">
                        <el-icon><Clock /></el-icon>
                        {{ formatDate(comment.created_at) }}
                      </span>
                    </div>
                  </div>
                </div>
                <el-empty v-if="comments.length === 0" description="暂无评论">
                  <el-button type="primary" @click="$router.push('/articles')">去浏览文章</el-button>
                </el-empty>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { User, Lock, ChatDotRound, Message, Check, Key, Document, Clock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { updateProfile as updateProfileApi, changePassword as changePasswordApi } from '@/api/user'
import { getComments } from '@/api/content'

const userStore = useUserStore()

const activeMenu = ref('profile')
const comments = ref([])

const getAvatarUrl = (avatar) => {
  if (!avatar) return ''
  if (avatar.startsWith('http')) return avatar
  return `http://localhost:8001${avatar}`
}

const profileForm = reactive({
  username: userStore.user?.username || '',
  email: userStore.user?.email || '',
})

const passwordFormRef = ref()
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  new_password_confirm: '',
})

const validatePasswordConfirm = (rule, value, callback) => {
  if (value !== passwordForm.new_password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const passwordRules = {
  old_password: [{ required: true, message: '请输入当前密码', trigger: 'blur' }],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' },
  ],
  new_password_confirm: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    { validator: validatePasswordConfirm, trigger: 'blur' },
  ],
}

const handleMenuSelect = (key) => {
  activeMenu.value = key
  if (key === 'comments') {
    fetchComments()
  }
}

const updateProfile = async () => {
  try {
    await updateProfileApi({ email: profileForm.email })
    ElMessage.success('保存成功')
    userStore.fetchProfile()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

const changePassword = async () => {
  await passwordFormRef.value.validate()
  try {
    await changePasswordApi(passwordForm)
    ElMessage.success('密码修改成功')
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.new_password_confirm = ''
  } catch (e) {
    ElMessage.error(e.response?.data?.old_password?.[0] || '修改失败')
  }
}

const fetchComments = async () => {
  try {
    const { data } = await getComments({ user: userStore.user?.id })
    comments.value = data.results || data
  } catch (e) {
    console.error(e)
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

onMounted(() => {
  profileForm.username = userStore.user?.username || ''
  profileForm.email = userStore.user?.email || ''
})
</script>

<style scoped>
.profile-page {
  padding: 32px 0;
  min-height: calc(100vh - var(--header-height) - 200px);
  background: var(--bg-color);
}

.container {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 24px;
}

.profile-card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 24px;
  border: 1px solid var(--border-light);
  position: sticky;
  top: 96px;
}

.avatar-section {
  text-align: center;
  padding: 24px 0;
  border-bottom: 2px solid var(--border-light);
  margin-bottom: 20px;
}

.avatar-wrapper {
  display: inline-block;
  position: relative;
}

.avatar-wrapper::before {
  content: '';
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  background: var(--primary-color);
  border-radius: 50%;
  z-index: -1;
  opacity: 0.15;
}

.avatar-section .el-avatar {
  border: 4px solid #fff;
  box-shadow: var(--shadow-lg);
}

.avatar-section h3 {
  margin-top: 16px;
  font-size: 20px;
  color: var(--text-primary);
  font-weight: 600;
}

.avatar-section p {
  font-size: 14px;
  color: var(--text-tertiary);
  margin-top: 6px;
}

.profile-menu {
  border: none !important;
}

.profile-menu .el-menu-item {
  border-radius: var(--radius-sm);
  margin: 4px 0;
  transition: all var(--transition-fast);
}

.profile-menu .el-menu-item:hover {
  background: var(--primary-bg) !important;
}

.profile-menu .el-menu-item.is-active {
  background: var(--primary-color) !important;
  color: #fff !important;
}

.profile-menu .el-menu-item.is-active .el-icon {
  color: #fff !important;
}

.content-card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 32px;
  min-height: 500px;
  border: 1px solid var(--border-light);
}

.content-card h2 {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 20px;
  color: var(--text-primary);
  margin-bottom: 28px;
  padding-bottom: 16px;
  border-bottom: 2px solid var(--border-light);
}

.content-card h2 .el-icon {
  color: var(--primary-color);
  font-size: 22px;
}

.profile-form {
  max-width: 500px;
}

.profile-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--text-primary);
}

.profile-form :deep(.el-input__wrapper) {
  border-radius: var(--radius-sm);
  padding: 4px 12px;
  box-shadow: none;
  border: 1px solid var(--border-color);
  transition: all var(--transition-fast);
}

.profile-form :deep(.el-input__wrapper:hover) {
  border-color: var(--border-dark);
}

.profile-form :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 1px var(--primary-color);
}

.profile-form :deep(.el-input.is-disabled .el-input__wrapper) {
  background: var(--bg-secondary);
}

.save-btn {
  padding: 12px 28px;
  font-weight: 500;
  border-radius: var(--radius-sm);
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  padding: 20px;
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  transition: all var(--transition-fast);
  animation: fadeInUp 0.15s ease-out backwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.comment-item:hover {
  border-color: rgba(0, 120, 212, 0.2);
}

.comment-content p {
  font-size: 15px;
  color: var(--text-primary);
  line-height: 1.7;
  margin-bottom: 12px;
}

.comment-meta {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: var(--text-tertiary);
}

.comment-meta span {
  display: flex;
  align-items: center;
  gap: 6px;
}

.article-title {
  color: var(--primary-color);
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .profile-card {
    position: static;
    margin-bottom: 24px;
  }
}
</style>
