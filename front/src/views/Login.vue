<template>
  <div class="login-page">
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
    
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <div class="login-logo">
            <span class="logo-icon">C</span>
          </div>
          <h2>欢迎回来</h2>
          <p>登录您的账户继续探索</p>
        </div>
        
        <el-form ref="formRef" :model="form" :rules="rules" label-position="top" class="login-form">
          <el-form-item label="用户名" prop="username">
            <el-input 
              v-model="form.username" 
              placeholder="请输入用户名"
              :prefix-icon="User"
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
              @keyup.enter="handleLogin"
            />
          </el-form-item>
          <el-form-item class="remember-row">
            <el-checkbox v-model="rememberMe">记住我</el-checkbox>
            <a href="#" class="forgot-link">忘记密码？</a>
          </el-form-item>
          <el-form-item>
            <el-button 
              type="primary" 
              @click="handleLogin" 
              :loading="loading" 
              class="login-btn"
              size="large"
            >
              <span v-if="!loading">登 录</span>
              <span v-else>登录中...</span>
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="login-divider">
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
        
        <div class="login-footer">
          <span>还没有账号？</span>
          <el-button type="primary" link @click="$router.push('/register')">立即注册</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const formRef = ref()
const loading = ref(false)
const rememberMe = ref(false)

const form = reactive({
  username: '',
  password: '',
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
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
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: var(--bg-color);
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
  background: linear-gradient(135deg, #0078D4 0%, #106EBE 50%, #005A9E 100%);
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

.login-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 420px;
  padding: 20px;
}

.login-card {
  background: var(--card-bg);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: var(--radius-lg);
  padding: 40px;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-lg);
  animation: fadeInUp 0.15s ease-out;
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

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-logo {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.logo-icon {
  width: 56px;
  height: 56px;
  background: var(--primary-color);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 28px;
  font-weight: bold;
}

.login-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.login-header p {
  color: var(--text-secondary);
  font-size: 14px;
}

.login-form {
  margin-bottom: 24px;
}

.login-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--text-primary);
  padding-bottom: 8px;
}

.login-form :deep(.el-input__wrapper) {
  border-radius: var(--radius-sm);
  padding: 4px 12px;
  box-shadow: none;
  border: 1px solid var(--border-color);
  transition: all var(--transition-fast);
}

.login-form :deep(.el-input__wrapper:hover) {
  border-color: var(--border-dark);
}

.login-form :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 1px var(--primary-color);
}

.remember-row {
  margin-bottom: 20px;
}

.remember-row :deep(.el-form-item__content) {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.forgot-link {
  color: var(--primary-color);
  font-size: 13px;
  transition: color var(--transition-fast);
}

.forgot-link:hover {
  color: var(--primary-dark);
}

.login-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: var(--radius-sm);
  letter-spacing: 2px;
}

.login-divider {
  display: flex;
  align-items: center;
  margin: 24px 0;
}

.login-divider::before,
.login-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border-color);
}

.login-divider span {
  padding: 0 16px;
  color: var(--text-tertiary);
  font-size: 13px;
}

.social-login {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 24px;
}

.social-btn {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-fast);
  color: var(--text-secondary);
}

.social-btn:hover {
  border-color: var(--primary-color);
  background: var(--primary-bg);
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

.login-footer {
  text-align: center;
  color: var(--text-secondary);
  font-size: 14px;
  padding-top: 20px;
  border-top: 1px solid var(--border-light);
}

.login-footer .el-button {
  font-weight: 500;
  margin-left: 4px;
}

@media (max-width: 480px) {
  .login-card {
    padding: 32px 24px;
  }
  
  .login-header h2 {
    font-size: 22px;
  }
}
</style>
