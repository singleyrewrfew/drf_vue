<template>
  <div class="page profile-page">
    <header class="page-header">
      <h1 class="page-title">我的</h1>
      <div class="header-actions">
        <button class="btn-icon" @click="themeStore.toggleTheme()">
          <el-icon><Sunny v-if="themeStore.theme === 'dark'" /><Moon v-else /></el-icon>
        </button>
      </div>
    </header>
    
    <div class="page-content">
      <div v-if="userStore.isLoggedIn" class="user-card">
        <div class="user-avatar">
          <el-avatar :size="64" :src="getAvatarUrl(userStore.user?.avatar)">
            {{ userStore.user?.username?.charAt(0).toUpperCase() }}
          </el-avatar>
        </div>
        <div class="user-info">
          <h2 class="user-name">{{ userStore.user?.username }}</h2>
          <p class="user-email">{{ userStore.user?.email }}</p>
        </div>
      </div>
      
      <div v-else class="login-prompt">
        <p class="prompt-text">登录后查看个人信息</p>
        <div class="prompt-actions">
          <button class="btn btn-primary" @click="$router.push('/login')">登录</button>
          <button class="btn btn-secondary" @click="$router.push('/register')">注册</button>
        </div>
      </div>
      
      <div v-if="userStore.isLoggedIn" class="menu-list">
        <router-link to="/profile" class="menu-item">
          <el-icon class="menu-icon"><User /></el-icon>
          <span class="menu-label">个人资料</span>
          <el-icon class="menu-arrow"><ArrowRight /></el-icon>
        </router-link>
        
        <div class="menu-divider"></div>
        
        <button class="menu-item" @click="handleLogout">
          <el-icon class="menu-icon" style="color: var(--danger-color);"><SwitchButton /></el-icon>
          <span class="menu-label" style="color: var(--danger-color);">退出登录</span>
        </button>
      </div>
      
      <div class="about-section">
        <h3 class="about-title">关于</h3>
        <p class="about-text">CMS 移动端 v1.0.0</p>
        <p class="about-text">一个简洁高效的内容管理系统</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { User, ArrowRight, SwitchButton, Sunny, Moon } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { useThemeStore } from '@/stores/theme'
import { getAvatarUrl } from '@/utils'

const router = useRouter()
const userStore = useUserStore()
const themeStore = useThemeStore()

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await userStore.logout()
    router.push('/')
  } catch (e) {
    if (e !== 'cancel') {
      console.error(e)
    }
  }
}
</script>

<style scoped>
.profile-page {
  background: var(--bg-color);
}

.header-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  width: 36px;
  height: 36px;
  border: none;
  background: var(--bg-secondary);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  transition: all var(--transition-fast);
}

.btn-icon:active {
  background: var(--bg-tertiary);
  transform: scale(0.95);
}

.user-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  margin-bottom: 16px;
}

.user-avatar {
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 4px;
}

.user-email {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.login-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  margin-bottom: 16px;
}

.prompt-text {
  font-size: 14px;
  color: var(--text-tertiary);
  margin-bottom: 16px;
}

.prompt-actions {
  display: flex;
  gap: 12px;
}

.menu-list {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  overflow: hidden;
  margin-bottom: 16px;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 14px 16px;
  background: transparent;
  border: none;
  width: 100%;
  text-align: left;
  text-decoration: none;
  transition: background var(--transition-fast);
}

.menu-item:active {
  background: var(--bg-secondary);
}

.menu-icon {
  font-size: 20px;
  color: var(--text-secondary);
  margin-right: 12px;
}

.menu-label {
  flex: 1;
  font-size: 15px;
  color: var(--text-primary);
}

.menu-arrow {
  font-size: 14px;
  color: var(--text-tertiary);
}

.menu-divider {
  height: 1px;
  background: var(--border-light);
  margin: 0 16px;
}

.about-section {
  padding: 16px;
  text-align: center;
}

.about-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 8px;
}

.about-text {
  font-size: 12px;
  color: var(--text-tertiary);
  margin: 0 0 4px;
}
</style>
