<template>
  <div class="page">
    <header class="page-header">
      <div class="header-left">
        <button class="btn-back" @click="$router.back()">
          <el-icon><ArrowLeft /></el-icon>
        </button>
      </div>
      <h1 class="page-title">登录</h1>
      <div class="header-right"></div>
    </header>
    
    <div class="page-content">
      <div class="login-header">
        <h1 class="login-title">CMS</h1>
        <p class="login-subtitle">内容管理系统</p>
      </div>
      
      <div class="login-form">
        <div class="form-group">
          <el-input 
            v-model="form.username" 
            placeholder="用户名"
            size="large"
            clearable
          />
        </div>
        
        <div class="form-group">
          <el-input 
            v-model="form.password" 
            type="password"
            placeholder="密码"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </div>
        
        <button 
          class="btn btn-primary btn-block btn-lg" 
          :disabled="loading"
          @click="handleLogin"
        >
          {{ loading ? '登录中...' : '登录' }}
        </button>
        
        <div class="form-footer">
          <span class="form-footer-text">还没有账号？</span>
          <router-link to="/register" class="form-footer-link">立即注册</router-link>
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
    router.push(route.query.redirect || '/')
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-header {
  text-align: center;
  padding: 40px 0 32px;
}

.login-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--primary-color);
  margin: 0 0 8px;
}

.login-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

.login-form {
  padding: 0 24px;
}
</style>
