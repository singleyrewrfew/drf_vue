<template>
  <AuthCard title="创建账户" subtitle="加入我们，开始您的内容之旅">
    <template #form>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        class="auth-form"
      >
        <AuthFormField
          v-model="form.username"
          label="用户名"
          prop="username"
          placeholder="请输入用户名"
          icon="user"
        />

        <AuthFormField
          v-model="form.email"
          label="邮箱"
          prop="email"
          type="text"
          placeholder="请输入邮箱"
          icon="message"
        />

        <el-form-item label="密码" prop="password" class="password-field">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
            size="default"
          />
          <PasswordStrength :password="form.password" />
        </el-form-item>

        <AuthFormField
          v-model="form.password_confirm"
          label="确认密码"
          prop="password_confirm"
          type="password"
          placeholder="请确认密码"
          icon="lock"
          show-password
        />

        <div class="terms-row">
          <el-checkbox v-model="agreeTerms">
            我已阅读并同意
            <a href="#" class="terms-link">服务条款</a>
            和
            <a href="#" class="terms-link">隐私政策</a>
          </el-checkbox>
        </div>

        <AuthSubmitButton
          text="注 册"
          loading-text="注册中..."
          :loading="loading"
          :disabled="!agreeTerms"
          @click="handleRegister"
        />
      </el-form>
    </template>

    <template #footer>
      <span>已有账号？</span>
      <el-button type="primary" link @click="$router.push('/login')">立即登录</el-button>
    </template>
  </AuthCard>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Lock } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import AuthCard from '@/components/auth/AuthCard.vue'
import AuthFormField from '@/components/auth/AuthFormField.vue'
import AuthSubmitButton from '@/components/auth/AuthSubmitButton.vue'
import PasswordStrength from '@/components/auth/PasswordStrength.vue'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref()
const loading = ref(false)
const agreeTerms = ref(false)

const form = reactive({
  username: '',
  email: '',
  password: '',
  password_confirm: ''
})

const validatePassword = (rule, value, callback) => {
  if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
  ],
  password_confirm: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validatePassword, trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  await formRef.value.validate()
  loading.value = true
  try {
    await userStore.register(form)
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch (error) {
    const msg =
      error.response?.data?.username?.[0] || error.response?.data?.email?.[0] || '注册失败'
    ElMessage.error(msg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.password-field {
  margin-bottom: 16px;
}

.password-field :deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--text-primary);
  padding-bottom: 6px;
  font-size: 13px;
}

.terms-row {
  margin-bottom: 20px;
}

.terms-row :deep(.el-checkbox__label) {
  font-size: 12px;
  color: var(--text-secondary);
}

.terms-link {
  color: var(--primary-color);
  transition: color var(--transition-fast);
}

.terms-link:hover {
  color: var(--primary-dark);
}
</style>
