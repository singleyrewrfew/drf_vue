<template>
  <div class="page login-page">
    <header class="page-header">
      <button class="btn-back" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
      </button>
      <h1 class="page-title">登录</h1>
    </header>
    
    <div class="page-content">
      <div class="login-form">
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
          <label class="form-label">密码</label>
          <el-input 
            v-model="form.password" 
            type="password"
            placeholder="请输入密码"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </div>
        
        <button 
          class="btn btn-primary btn-block login-btn" 
          :disabled="loading"
          @click="handleLogin"
        >
          {{ loading ? '登录中...' : '登录' }}
        </button>
        
        <div class="form-footer">
          <span class="footer-text">还没有账号？</span>
          <router-link to="/register" class="footer-link">立即注册</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const loading = ref(false)
const form = reactive({
  username: '',
  password: ''
})

const handleLogin = async () => {
  if (!form.username || !form.password) {
    ElMessage.warning('请填写用户名和密码')
    return
  }
  
  loading.value = true
  try {
    await userStore.login(form)
    ElMessage.success('登录成功')
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  background: var(--bg-color);
}

.btn-back {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-primary);
  transition: all var(--transition-fast);
}

.btn-back:active {
  background: var(--bg-secondary);
}

.login-form {
  padding: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.login-btn {
  margin-top: 24px;
  height: 44px;
  font-size: 16px;
}

.form-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  margin-top: 20px;
}

.footer-text {
  font-size: 14px;
  color: var(--text-tertiary);
}

.footer-link {
  font-size: 14px;
  color: var(--primary-color);
  font-weight: 500;
}
</style>
