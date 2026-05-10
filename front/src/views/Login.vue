<template>
  <AuthCard title="欢迎回来" subtitle="登录您的账户继续探索">
    <template #form>
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" class="auth-form">
        <AuthFormField
          v-model="form.username"
          label="用户名"
          prop="username"
          placeholder="请输入用户名"
          icon="user"
        />

        <AuthFormField
          v-model="form.password"
          label="密码"
          prop="password"
          type="password"
          placeholder="请输入密码"
          icon="lock"
          show-password
          @keyup.enter="handleLogin"
        />

        <div class="form-options">
          <el-checkbox v-model="rememberMe">记住我</el-checkbox>
          <a href="#" class="forgot-link">忘记密码？</a>
        </div>

        <AuthSubmitButton
          text="登 录"
          loading-text="登录中..."
          :loading="loading"
          @click="handleLogin"
        />
      </el-form>
    </template>

    <template #footer>
      <span>还没有账号？</span>
      <el-button type="primary" link @click="$router.push('/register')">立即注册</el-button>
    </template>
  </AuthCard>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import AuthCard from '@/components/auth/AuthCard.vue'
import AuthFormField from '@/components/auth/AuthFormField.vue'
import AuthSubmitButton from '@/components/auth/AuthSubmitButton.vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const formRef = ref()
const loading = ref(false)
const rememberMe = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  await formRef.value.validate()
  loading.value = true
  try {
    await userStore.login(form)
    ElMessage.success('登录成功')
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.form-options :deep(.el-checkbox__label) {
  font-size: 13px;
  color: var(--text-secondary);
}

.forgot-link {
  color: var(--primary-color);
  font-size: 13px;
  transition: color var(--transition-fast);
}

.forgot-link:hover {
  color: var(--primary-dark);
}
</style>
