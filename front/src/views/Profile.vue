<template>
  <div class="profile-page">
    <div class="container">
      <el-row :gutter="24">
        <el-col :span="6">
          <div class="profile-card">
            <div class="avatar-section">
              <div class="avatar-wrapper">
                <el-avatar :size="80" :src="getAvatarUrl(userStore.user?.avatar)">
                  {{ userStore.user?.username?.charAt(0).toUpperCase() }}
                </el-avatar>
              </div>
              <h3>{{ userStore.user?.username }}</h3>
              <p>{{ userStore.user?.email }}</p>
            </div>
            <el-menu :default-active="activeMenu" @select="handleMenuSelect" class="profile-menu">
              <el-menu-item index="profile">
                <el-icon>
                  <User />
                </el-icon>
                <span>个人资料</span>
              </el-menu-item>
              <el-menu-item index="password">
                <el-icon>
                  <Lock />
                </el-icon>
                <span>修改密码</span>
              </el-menu-item>
              <el-menu-item index="comments">
                <el-icon>
                  <ChatDotRound />
                </el-icon>
                <span>我的评论</span>
              </el-menu-item>
            </el-menu>
          </div>
        </el-col>

        <el-col :span="18">
          <div class="content-card">
            <div v-if="activeMenu === 'profile'" class="animate-fade-in">
              <h2>
                <el-icon>
                  <User />
                </el-icon>
                个人资料
              </h2>
              <el-form :model="profileForm" label-position="top" class="profile-form">
                <el-form-item label="用户名">
                  <el-input v-model="profileForm.username" disabled>
                    <template #prefix>
                      <el-icon>
                        <User />
                      </el-icon>
                    </template>
                  </el-input>
                </el-form-item>
                <el-form-item label="邮箱">
                  <el-input v-model="profileForm.email">
                    <template #prefix>
                      <el-icon>
                        <Message />
                      </el-icon>
                    </template>
                  </el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="updateProfile" class="save-btn">
                    <el-icon>
                      <Check />
                    </el-icon>
                    保存修改
                  </el-button>
                </el-form-item>
              </el-form>
            </div>

            <div v-else-if="activeMenu === 'password'" class="animate-fade-in">
              <h2>
                <el-icon>
                  <Lock />
                </el-icon>
                修改密码
              </h2>
              <el-form
                ref="passwordFormRef"
                :model="passwordForm"
                :rules="passwordRules"
                label-position="top"
                class="profile-form"
              >
                <el-form-item label="当前密码" prop="old_password">
                  <el-input v-model="passwordForm.old_password" type="password" show-password>
                    <template #prefix>
                      <el-icon>
                        <Lock />
                      </el-icon>
                    </template>
                  </el-input>
                </el-form-item>
                <el-form-item label="新密码" prop="new_password">
                  <el-input v-model="passwordForm.new_password" type="password" show-password>
                    <template #prefix>
                      <el-icon>
                        <Key />
                      </el-icon>
                    </template>
                  </el-input>
                </el-form-item>
                <el-form-item label="确认新密码" prop="new_password_confirm">
                  <el-input
                    v-model="passwordForm.new_password_confirm"
                    type="password"
                    show-password
                  >
                    <template #prefix>
                      <el-icon>
                        <Key />
                      </el-icon>
                    </template>
                  </el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="changePassword" class="save-btn">
                    <el-icon>
                      <Check />
                    </el-icon>
                    修改密码
                  </el-button>
                </el-form-item>
              </el-form>
            </div>

            <div v-else-if="activeMenu === 'comments'" class="animate-fade-in">
              <h2>
                <el-icon>
                  <ChatDotRound />
                </el-icon>
                我的评论
              </h2>
              <div class="comment-list">
                <div
                  v-for="(comment, index) in comments"
                  :key="comment.id"
                  class="comment-item"
                  :style="{ animationDelay: `${index * 0.1}s` }"
                >
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
                  <el-button type="primary" @click="$router.push('/articles')"
                    >去浏览文章</el-button
                  >
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
import {
  User,
  Lock,
  ChatDotRound,
  Message,
  Check,
  Key,
  Document,
  Clock
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { updateProfile as updateProfileApi, changePassword as changePasswordApi } from '@/api/user'
import { getComments } from '@/api/content'
import { getAvatarUrl, formatDate } from '@/utils'

const userStore = useUserStore()

const activeMenu = ref('profile')
const comments = ref([])

const profileForm = reactive({
  username: userStore.user?.username || '',
  email: userStore.user?.email || ''
})

const passwordFormRef = ref()
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  new_password_confirm: ''
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
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  new_password_confirm: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    { validator: validatePasswordConfirm, trigger: 'blur' }
  ]
}

const handleMenuSelect = key => {
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
    // 处理分页数据和非分页数据
    if (data.results) {
      comments.value = data.results
    } else if (Array.isArray(data)) {
      comments.value = data
    } else {
      console.warn('Unexpected comments data format:', data)
      comments.value = []
    }
  } catch (e) {
    console.error('Failed to fetch comments:', e)
  }
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
  font-family: "KaiTi", "STKaiti", "楷体", serif;
}

.container {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 24px;
}

.profile-card {
  background: var(--paper-cream, #ede8dc);
  border-radius: var(--radius-sm, 4px);
  padding: 24px;
  border: 1.5px solid var(--paper-aged, #ddd6c8);
  position: sticky;
  top: 96px;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px 0;
  border-bottom: 2px solid var(--paper-aged, #ddd6c8);
  margin-bottom: 20px;
}

.avatar-wrapper {
  position: relative;
}

.avatar-wrapper::before {
  content: '';
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  background: var(--vermilion-color, #c53d43);
  border-radius: 50%;
  z-index: -1;
  opacity: 0.15;
}

.avatar-section .el-avatar {
  border: 3px solid var(--vermilion-color, #c53d43);
  box-shadow: 0 2px 8px rgba(197, 61, 67, 0.25);
}

.avatar-section h3 {
  margin-top: 16px;
  font-size: 20px;
  color: var(--ink-dark, #1a1a1a);
  font-weight: 700;
  font-family: "Noto Serif SC", "SimSun", serif;
  letter-spacing: 0.05em;
}

.avatar-section p {
  font-size: 14px;
  color: var(--ink-medium, #595959);
  margin-top: 6px;
  font-family: "KaiTi", "STKaiti", serif;
}

.profile-menu {
  border: none !important;
}

.profile-menu .el-menu-item {
  border-radius: var(--radius-xs, 2px);
  margin: 4px 0;
  transition: all var(--transition-fast);
  font-family: "KaiTi", "STKaiti", serif;
  letter-spacing: 0.05em;
}

.profile-menu .el-menu-item:hover {
  background: rgba(197, 61, 67, 0.08) !important;
  color: var(--vermilion-color, #c53d43) !important;
}

.profile-menu .el-menu-item.is-active {
  background: var(--vermilion-color, #c53d43) !important;
  color: #fff !important;
}

.profile-menu .el-menu-item.is-active .el-icon {
  color: #fff !important;
}

.content-card {
  background: var(--paper-cream, #ede8dc);
  border-radius: var(--radius-sm, 4px);
  padding: 32px;
  min-height: 500px;
  border: 1.5px solid var(--paper-aged, #ddd6c8);
}

.content-card h2 {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 20px;
  color: var(--ink-dark, #1a1a1a);
  margin-bottom: 28px;
  padding-bottom: 16px;
  border-bottom: 2px solid var(--paper-aged, #ddd6c8);
  font-family: "Noto Serif SC", "SimSun", serif;
  font-weight: 700;
  letter-spacing: 0.08em;
}

.content-card h2 .el-icon {
  color: var(--vermilion-color, #c53d43);
  font-size: 22px;
}

.profile-form {
  max-width: 500px;
}

.profile-form :deep(.el-form-item__label) {
  font-weight: 600;
  color: var(--ink-dark, #1a1a1a);
  font-family: "KaiTi", "STKaiti", serif;
  letter-spacing: 0.03em;
}

.profile-form :deep(.el-input__wrapper) {
  border-radius: var(--radius-xs, 2px);
  padding: 4px 12px;
  box-shadow: none;
  border: 1.5px solid var(--paper-aged, #ddd6c8);
  transition: all var(--transition-fast);
  background: var(--bg-primary, #f5f2eb);
}

.profile-form :deep(.el-input__wrapper:hover) {
  border-color: var(--ink-medium, #595959);
}

.profile-form :deep(.el-input__wrapper.is-focus) {
  border-color: var(--vermilion-color, #c53d43);
  box-shadow: 0 0 0 1px rgba(197, 61, 67, 0.12);
}

.profile-form :deep(.el-input.is-disabled .el-input__wrapper) {
  background: var(--bg-secondary);
}

.save-btn {
  padding: 12px 28px;
  font-weight: 600;
  border-radius: var(--radius-xs, 2px);
  background: var(--vermilion-color, #c53d43) !important;
  border: none !important;
  letter-spacing: 0.1em;
  font-family: "KaiTi", "STKaiti", serif;
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.15),
    1px 1px 6px rgba(197, 61, 67, 0.3);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.save-btn:hover {
  background: var(--vermilion-hover, #a02f33) !important;
  transform: translateY(-1px);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.2),
    0 4px 12px rgba(197, 61, 67, 0.35);
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  padding: 20px;
  background: var(--bg-primary, #f5f2eb);
  border-radius: var(--radius-xs, 2px);
  border: 1.5px solid var(--paper-aged, #ddd6c8);
  transition: all var(--transition-fast);
  animation: fadeInUp 0.15s ease-out backwards;
}

.comment-item:hover {
  border-color: var(--vermilion-color, #c53d43);
}

.comment-content p {
  font-size: 15px;
  color: var(--ink-dark, #1a1a1a);
  line-height: 1.7;
  margin-bottom: 12px;
  font-family: "KaiTi", "STKaiti", serif;
}

.comment-meta {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: var(--ink-light, #8c8c8c);
}

.comment-meta span {
  display: flex;
  align-items: center;
  gap: 6px;
}

.article-title {
  color: var(--vermilion-color, #c53d43);
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
  .profile-page {
    padding: 16px 0;
  }

  .container {
    padding: 0 16px;
  }

  .el-col-6 {
    max-width: 100%;
    flex: 0 0 100%;
  }

  .el-col-18 {
    max-width: 100%;
    flex: 0 0 100%;
  }

  .profile-card {
    position: static;
    margin-bottom: 20px;
    padding: 20px;
  }

  .avatar-section {
    padding: 16px 0;
    margin-bottom: 16px;
  }

  .avatar-section .el-avatar {
    width: 60px !important;
    height: 60px !important;
  }

  .avatar-section h3 {
    font-size: 18px;
    margin-top: 12px;
  }

  .avatar-section p {
    font-size: 13px;
  }

  .profile-menu {
    display: flex;
    gap: 8px;
  }

  .profile-menu .el-menu-item {
    flex: 1;
    justify-content: center;
    padding: 12px 8px;
    font-size: 13px;
  }

  .profile-menu .el-menu-item span {
    display: none;
  }

  .profile-menu .el-menu-item .el-icon {
    margin-right: 0;
    font-size: 18px;
  }

  .content-card {
    padding: 20px;
    min-height: auto;
  }

  .content-card h2 {
    font-size: 18px;
    margin-bottom: 20px;
    padding-bottom: 12px;
  }

  .profile-form {
    max-width: 100%;
  }

  .comment-item {
    padding: 16px;
  }

  .comment-content p {
    font-size: 14px;
  }

  .comment-meta {
    flex-direction: column;
    gap: 8px;
  }
}

@media (max-width: 576px) {
  .profile-card {
    padding: 16px;
  }

  .avatar-section {
    padding: 12px 0;
  }

  .avatar-section .el-avatar {
    width: 50px !important;
    height: 50px !important;
  }

  .avatar-section h3 {
    font-size: 16px;
  }

  .profile-menu .el-menu-item {
    padding: 10px 6px;
  }

  .content-card {
    padding: 16px;
  }

  .content-card h2 {
    font-size: 16px;
  }

  .save-btn {
    width: 100%;
  }
}

/* ===================================
   暗色模式适配
   Dark Mode Styles
   =================================== */

[data-theme='dark'] .profile-page {
  background: var(--bg-color);
}

[data-theme='dark'] .profile-card,
[data-theme='dark'] .content-card {
  background: #27272a;
  border-color: #3f3f46;
}

[data-theme='dark'] .avatar-section {
  border-bottom-color: #3f3f46;
}

[data-theme='dark'] .avatar-wrapper::before {
  background: rgba(197, 61, 67, 0.4);
}

[data-theme='dark'] .avatar-section h3 {
  color: #e4e4e7;
}

[data-theme='dark'] .avatar-section p {
  color: #a1a1aa;
}

[data-theme='dark'] .profile-menu .el-menu-item:hover {
  background: rgba(197, 61, 67, 0.15) !important;
}

[data-theme='dark'] .content-card h2 {
  color: #e4e4e7;
  border-bottom-color: #3f3f46;
}

[data-theme='dark'] .content-card h2 .el-icon {
  color: #ef4444;
}

[data-theme='dark'] .profile-form :deep(.el-form-item__label) {
  color: #e4e4e7;
}

[data-theme='dark'] .profile-form :deep(.el-input__wrapper) {
  background: #3f3f46;
  border-color: #52525b;
}

[data-theme='dark'] .profile-form :deep(.el-input__wrapper:hover) {
  border-color: #71717a;
}

[data-theme='dark'] .profile-form :deep(.el-input__wrapper.is-focus) {
  border-color: #ef4444;
  box-shadow: 0 0 0 1px rgba(239, 68, 68, 0.15);
}

[data-theme='dark'] .profile-form :deep(.el-input.is-disabled .el-input__wrapper) {
  background: #27272a;
}

[data-theme='dark'] .save-btn {
  background: #dc2626 !important;
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.15),
    1px 1px 6px rgba(220, 38, 38, 0.35);
}

[data-theme='dark'] .save-btn:hover {
  background: #b91c1c !important;
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.2),
    0 4px 12px rgba(220, 38, 38, 0.45);
}

[data-theme='dark'] .comment-item {
  background: #3f3f46;
  border-color: #52525b;
}

[data-theme='dark'] .comment-item:hover {
  border-color: #ef4444;
}

[data-theme='dark'] .comment-content p {
  color: #e4e4e7;
}

[data-theme='dark'] .comment-meta {
  color: #a1a1aa;
}

[data-theme='dark'] .article-title {
  color: #f87171;
}
</style>
