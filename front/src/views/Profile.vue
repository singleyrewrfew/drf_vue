<template>
  <div class="profile-page">
    <div class="container">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="profile-card">
            <div class="avatar-section">
              <el-avatar :size="80">{{ userStore.user?.username?.charAt(0).toUpperCase() }}</el-avatar>
              <h3>{{ userStore.user?.username }}</h3>
              <p>{{ userStore.user?.email }}</p>
            </div>
            <el-menu :default-active="activeMenu" @select="handleMenuSelect">
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
            <div v-if="activeMenu === 'profile'">
              <h2>个人资料</h2>
              <el-form :model="profileForm" label-width="80px">
                <el-form-item label="用户名">
                  <el-input v-model="profileForm.username" disabled />
                </el-form-item>
                <el-form-item label="邮箱">
                  <el-input v-model="profileForm.email" />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="updateProfile">保存修改</el-button>
                </el-form-item>
              </el-form>
            </div>

            <div v-else-if="activeMenu === 'password'">
              <h2>修改密码</h2>
              <el-form ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" label-width="100px">
                <el-form-item label="当前密码" prop="old_password">
                  <el-input v-model="passwordForm.old_password" type="password" show-password />
                </el-form-item>
                <el-form-item label="新密码" prop="new_password">
                  <el-input v-model="passwordForm.new_password" type="password" show-password />
                </el-form-item>
                <el-form-item label="确认新密码" prop="new_password_confirm">
                  <el-input v-model="passwordForm.new_password_confirm" type="password" show-password />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="changePassword">修改密码</el-button>
                </el-form-item>
              </el-form>
            </div>

            <div v-else-if="activeMenu === 'comments'">
              <h2>我的评论</h2>
              <div class="comment-list">
                <div v-for="comment in comments" :key="comment.id" class="comment-item">
                  <div class="comment-content">
                    <p>{{ comment.content }}</p>
                    <div class="comment-meta">
                      <span>评论文章：{{ comment.article_title }}</span>
                      <span>{{ formatDate(comment.created_at) }}</span>
                    </div>
                  </div>
                </div>
                <el-empty v-if="comments.length === 0" description="暂无评论" />
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
import { User, Lock, ChatDotRound } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { updateProfile as updateProfileApi, changePassword as changePasswordApi } from '@/api/user'
import { getComments } from '@/api/content'

const userStore = useUserStore()

const activeMenu = ref('profile')
const comments = ref([])

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
  padding: 20px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.profile-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
}

.avatar-section {
  text-align: center;
  padding: 20px 0;
  border-bottom: 1px solid #ebeef5;
  margin-bottom: 16px;
}

.avatar-section h3 {
  margin-top: 12px;
  font-size: 18px;
  color: #303133;
}

.avatar-section p {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.content-card {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  min-height: 400px;
}

.content-card h2 {
  font-size: 18px;
  color: #303133;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.comment-content p {
  font-size: 14px;
  color: #303133;
  line-height: 1.6;
  margin-bottom: 8px;
}

.comment-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #909399;
}
</style>
