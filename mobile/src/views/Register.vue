<template>
  <div class="page">
    <header class="page-header">
      <div class="header-left">
        <button class="btn-back" @click="$router.back()">
          <el-icon><ArrowLeft /></el-icon>
        </button>
      </div>
      <h1 class="page-title">注册</h1>
      <div class="header-right"></div>
    </header>
    
    <div class="page-content">
      <div class="form-container">
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
          <label class="form-label">邮箱</label>
          <el-input 
            v-model="form.email" 
            type="email"
            placeholder="请输入邮箱"
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
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">确认密码</label>
          <el-input 
            v-model="form.confirmPassword" 
            type="password"
            placeholder="请再次输入密码"
            size="large"
            show-password
            @keyup.enter="handleRegister"
          />
        </div>
        
        <button 
          class="btn btn-primary btn-block" 
          :disabled="loading"
          @click="handleRegister"
        >
          {{ loading ? '注册中...' : '注册' }}
        </button>
        
        <div class="form-footer">
          <span class="form-footer-text">已有账号？</span>
          <router-link to="/login" class="form-footer-link">立即登录</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const handleRegister = async () => {
  if (!form.username || !form.email || !form.password) {
    ElMessage.warning('请填写完整信息')
    return
  }
  
  if (form.password !== form.confirmPassword) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }
  
  loading.value = true
  try {
    await userStore.register({
      username: form.username,
      email: form.email,
      password: form.password
    })
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '注册失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.form-container {
  padding: 20px 0;
}
</style>
