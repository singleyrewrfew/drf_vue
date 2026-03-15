<template>
  <div class="register-page">
    <div class="bg-animation">
      <div class="bg-gradient"></div>
      <div class="bg-shapes">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
    
    <div class="register-container">
      <div class="register-card">
        <div class="register-header">
          <div class="register-logo">
            <span class="logo-icon">C</span>
          </div>
          <h2>创建账户</h2>
          <p>加入我们，开始您的内容之旅</p>
        </div>
        
        <el-form ref="formRef" :model="form" :rules="rules" label-position="top" class="register-form">
          <el-form-item label="用户名" prop="username">
            <el-input 
              v-model="form.username" 
              placeholder="请输入用户名"
              :prefix-icon="User"
              size="large"
            />
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input 
              v-model="form.email" 
              placeholder="请输入邮箱"
              :prefix-icon="Message"
              size="large"
            />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input 
              v-model="form.password" 
              type="password" 
              placeholder="请输入密码" 
              show-password
              :prefix-icon="Lock"
              size="large"
              @input="checkPasswordStrength"
            />
            <div v-if="form.password" class="password-strength">
              <div class="strength-bar">
                <span :class="passwordStrength >= 1 ? 'active' : ''"></span>
                <span :class="passwordStrength >= 2 ? 'active' : ''"></span>
                <span :class="passwordStrength >= 3 ? 'active' : ''"></span>
                <span :class="passwordStrength >= 4 ? 'active' : ''"></span>
              </div>
              <span class="strength-text" :class="strengthClass">{{ strengthText }}</span>
            </div>
          </el-form-item>
          <el-form-item label="确认密码" prop="password_confirm">
            <el-input 
              v-model="form.password_confirm" 
              type="password" 
              placeholder="请确认密码" 
              show-password
              :prefix-icon="Lock"
              size="large"
            />
          </el-form-item>
          <el-form-item class="terms-row">
            <el-checkbox v-model="agreeTerms">
              我已阅读并同意
              <a href="#" class="terms-link">服务条款</a>
              和
              <a href="#" class="terms-link">隐私政策</a>
            </el-checkbox>
          </el-form-item>
          <el-form-item>
            <el-button 
              type="primary" 
              @click="handleRegister" 
              :loading="loading" 
              :disabled="!agreeTerms"
              class="register-btn"
              size="large"
            >
              <span v-if="!loading">注 册</span>
              <span v-else>注册中...</span>
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="register-divider">
          <span>或</span>
        </div>
        
        <div class="social-login">
          <button class="social-btn github" title="GitHub">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
            </svg>
          </button>
          <button class="social-btn google" title="Google">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
            </svg>
          </button>
          <button class="social-btn wechat" title="微信">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <path d="M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 5.55a.59.59 0 01.213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.29.295a.326.326 0 00.167-.054l1.903-1.114a.864.864 0 01.717-.098 10.16 10.16 0 002.837.403c.276 0 .543-.027.811-.05-.857-2.578.157-4.972 1.932-6.446 1.703-1.415 3.882-1.98 5.853-1.838-.576-3.583-4.196-6.348-8.596-6.348zM5.785 5.991c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 01-1.162 1.178A1.17 1.17 0 014.623 7.17c0-.651.52-1.18 1.162-1.18zm5.813 0c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 01-1.162 1.178 1.17 1.17 0 01-1.162-1.178c0-.651.52-1.18 1.162-1.18zm5.34 2.867c-1.797-.052-3.746.512-5.28 1.786-1.72 1.428-2.687 3.72-1.78 6.22.942 2.453 3.666 4.229 6.884 4.229.826 0 1.622-.12 2.361-.336a.722.722 0 01.598.082l1.584.926a.272.272 0 00.14.045c.134 0 .24-.111.24-.247 0-.06-.023-.12-.038-.177l-.327-1.233a.582.582 0 01-.023-.156.49.49 0 01.201-.398C23.024 18.48 24 16.82 24 14.98c0-3.21-2.931-5.837-7.062-6.122zm-2.036 2.96c.535 0 .969.44.969.982a.976.976 0 01-.969.983.976.976 0 01-.969-.983c0-.542.434-.982.97-.982zm4.844 0c.535 0 .969.44.969.982a.976.976 0 01-.969.983.976.976 0 01-.969-.983c0-.542.434-.982.97-.982z"/>
            </svg>
          </button>
        </div>
        
        <div class="register-footer">
          <span>已有账号？</span>
          <el-button type="primary" link @click="$router.push('/login')">立即登录</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref()
const loading = ref(false)
const agreeTerms = ref(false)
const passwordStrength = ref(0)

const form = reactive({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
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
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' },
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' },
  ],
  password_confirm: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validatePassword, trigger: 'blur' },
  ],
}

const checkPasswordStrength = () => {
  const password = form.password
  let strength = 0
  
  if (password.length >= 6) strength++
  if (password.length >= 10) strength++
  if (/[A-Z]/.test(password) && /[a-z]/.test(password)) strength++
  if (/[0-9]/.test(password) && /[^A-Za-z0-9]/.test(password)) strength++
  
  passwordStrength.value = strength
}

const strengthText = computed(() => {
  const texts = ['', '弱', '中', '强', '很强']
  return texts[passwordStrength.value]
})

const strengthClass = computed(() => {
  const classes = ['', 'weak', 'medium', 'strong', 'very-strong']
  return classes[passwordStrength.value]
})

const handleRegister = async () => {
  await formRef.value.validate()
  loading.value = true
  try {
    await userStore.register(form)
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch (error) {
    const msg = error.response?.data?.username?.[0] || error.response?.data?.email?.[0] || '注册失败'
    ElMessage.error(msg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  padding: 40px 0;
}

.bg-animation {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
}

.bg-gradient {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  background-size: 400% 400%;
  animation: gradient 15s ease infinite;
}

@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.bg-shapes {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.bg-shapes span {
  position: absolute;
  display: block;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 20s infinite;
}

.bg-shapes span:nth-child(1) {
  width: 80px;
  height: 80px;
  left: 10%;
  top: 20%;
  animation-delay: 0s;
}

.bg-shapes span:nth-child(2) {
  width: 120px;
  height: 120px;
  left: 20%;
  bottom: 20%;
  animation-delay: 2s;
}

.bg-shapes span:nth-child(3) {
  width: 60px;
  height: 60px;
  left: 60%;
  top: 40%;
  animation-delay: 4s;
}

.bg-shapes span:nth-child(4) {
  width: 100px;
  height: 100px;
  right: 10%;
  top: 10%;
  animation-delay: 1s;
}

.bg-shapes span:nth-child(5) {
  width: 150px;
  height: 150px;
  right: 20%;
  bottom: 10%;
  animation-delay: 3s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
    opacity: 0.5;
  }
  50% {
    transform: translateY(-40px) rotate(180deg);
    opacity: 1;
  }
}

.register-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 420px;
  padding: 20px;
}

.register-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: var(--radius-xl);
  padding: 40px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.register-header {
  text-align: center;
  margin-bottom: 28px;
}

.register-logo {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.logo-icon {
  width: 56px;
  height: 56px;
  background: var(--primary-gradient);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 28px;
  font-weight: bold;
  box-shadow: var(--shadow-primary-lg);
}

.register-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.register-header p {
  color: var(--text-secondary);
  font-size: 14px;
}

.register-form {
  margin-bottom: 20px;
}

.register-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--text-primary);
  padding-bottom: 8px;
}

.register-form :deep(.el-input__wrapper) {
  border-radius: var(--radius-md);
  padding: 4px 16px;
  box-shadow: none;
  border: 1px solid var(--border-color);
  transition: all var(--transition-fast);
}

.register-form :deep(.el-input__wrapper:hover) {
  border-color: var(--primary-light);
}

.register-form :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--primary-bg);
}

.password-strength {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
}

.strength-bar {
  display: flex;
  gap: 4px;
}

.strength-bar span {
  width: 32px;
  height: 4px;
  border-radius: 2px;
  background: var(--border-color);
  transition: all var(--transition-fast);
}

.strength-bar span.active {
  background: var(--danger-color);
}

.strength-bar span:nth-child(2).active {
  background: var(--warning-color);
}

.strength-bar span:nth-child(3).active {
  background: var(--success-light);
}

.strength-bar span:nth-child(4).active {
  background: var(--success-color);
}

.strength-text {
  font-size: 12px;
  font-weight: 500;
}

.strength-text.weak { color: var(--danger-color); }
.strength-text.medium { color: var(--warning-color); }
.strength-text.strong { color: var(--success-light); }
.strength-text.very-strong { color: var(--success-color); }

.terms-row {
  margin-bottom: 20px;
}

.terms-row :deep(.el-checkbox__label) {
  font-size: 13px;
  color: var(--text-secondary);
}

.terms-link {
  color: var(--primary-color);
  transition: color var(--transition-fast);
}

.terms-link:hover {
  color: var(--primary-dark);
}

.register-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: var(--radius-md);
  letter-spacing: 2px;
}

.register-btn:disabled {
  opacity: 0.6;
}

.register-divider {
  display: flex;
  align-items: center;
  margin: 20px 0;
}

.register-divider::before,
.register-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border-color);
}

.register-divider span {
  padding: 0 16px;
  color: var(--text-tertiary);
  font-size: 13px;
}

.social-login {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 20px;
}

.social-btn {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-fast);
  color: var(--text-secondary);
}

.social-btn:hover {
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.social-btn.github:hover {
  background: #24292e;
  color: #fff;
  border-color: #24292e;
}

.social-btn.google:hover {
  background: #fff;
  border-color: #4285F4;
}

.social-btn.wechat:hover {
  background: #07C160;
  color: #fff;
  border-color: #07C160;
}

.register-footer {
  text-align: center;
  color: var(--text-secondary);
  font-size: 14px;
  padding-top: 20px;
  border-top: 1px solid var(--border-light);
}

.register-footer .el-button {
  font-weight: 500;
  margin-left: 4px;
}

@media (max-width: 480px) {
  .register-card {
    padding: 32px 24px;
  }
  
  .register-header h2 {
    font-size: 22px;
  }
  
  .register-page {
    padding: 20px 0;
  }
}
</style>
