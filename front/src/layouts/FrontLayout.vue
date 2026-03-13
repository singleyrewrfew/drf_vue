<template>
  <div class="front-layout">
    <header class="header">
      <div class="header-inner">
        <div class="logo" @click="$router.push('/')">
          <span class="logo-icon">C</span>
          <div class="logo-text">
            <span class="logo-title">CMS</span>
            <span class="logo-subtitle">内容管理系统</span>
          </div>
        </div>
        
        <nav class="nav">
          <router-link to="/" class="nav-item" exact-path>
            <el-icon><HomeFilled /></el-icon>
            <span>首页</span>
          </router-link>
          <router-link to="/articles" class="nav-item">
            <el-icon><Document /></el-icon>
            <span>文章</span>
          </router-link>
          
          <el-dropdown v-if="categories.length" trigger="hover" placement="bottom-start">
            <div class="nav-item">
              <el-icon><Folder /></el-icon>
              <span>分类</span>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item v-for="cat in categories" :key="cat.id" @click="$router.push(`/category/${cat.slug || cat.id}`)">
                  {{ cat.name }}
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </nav>
        
        <div class="search-box">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索文章..."
            @keyup.enter="handleSearch"
            clearable
            :prefix-icon="Search"
          />
        </div>
        
        <div class="user-area">
          <template v-if="userStore.isLoggedIn">
            <el-dropdown trigger="click">
              <div class="user-info">
                <el-avatar :size="36" :src="getAvatarUrl(userStore.user?.avatar)">{{ userStore.user?.username?.charAt(0).toUpperCase() }}</el-avatar>
                <span class="username">{{ userStore.user?.username }}</span>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="$router.push('/profile')">
                    <el-icon><User /></el-icon>个人中心
                  </el-dropdown-item>
                  <el-dropdown-item divided @click="handleLogout">
                    <el-icon><SwitchButton /></el-icon>退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <el-button type="default" @click="$router.push('/login')">登录</el-button>
            <el-button type="primary" @click="$router.push('/register')">注册</el-button>
          </template>
        </div>
      </div>
    </header>
    
    <main class="main">
      <router-view />
    </main>
    
    <footer class="footer">
      <div class="footer-inner">
        <div class="footer-content">
          <div class="footer-brand">
            <span class="footer-logo">CMS</span>
            <p>一个简洁高效的内容管理系统</p>
          </div>
          <div class="footer-links">
            <h4>快速链接</h4>
            <router-link to="/">首页</router-link>
            <router-link to="/articles">文章</router-link>
          </div>
          <div class="footer-contact">
            <h4>联系我们</h4>
            <p>邮箱: contact@cms.com</p>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; {{ new Date().getFullYear() }} CMS 内容管理系统. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { HomeFilled, Document, Folder, Search, User, SwitchButton } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { getCategories } from '@/api/content'

const router = useRouter()
const userStore = useUserStore()

const searchKeyword = ref('')
const categories = ref([])

const getAvatarUrl = (avatar) => {
  if (!avatar) return ''
  if (avatar.startsWith('http')) return avatar
  return `http://localhost:8001${avatar}`
}

const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    router.push({ path: '/search', query: { q: searchKeyword.value } })
  }
}

const handleLogout = async () => {
  await userStore.logout()
  router.push('/')
}

const fetchCategories = async () => {
  try {
    const { data } = await getCategories()
    categories.value = (data.results || data).slice(0, 8)
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.front-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f0f2f5;
}

.header {
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  flex-shrink: 0;
}

.logo-icon {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 22px;
  font-weight: bold;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  line-height: 1.2;
}

.logo-subtitle {
  font-size: 11px;
  color: #909399;
}

.nav {
  display: flex;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  color: #606266;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.3s;
  cursor: pointer;
  font-size: 14px;
}

.nav-item .arrow {
  font-size: 12px;
  margin-left: 2px;
}

.nav-item:hover {
  color: #409eff;
  background: #ecf5ff;
}

.nav-item.router-link-exact-active {
  color: #409eff;
  background: #ecf5ff;
  font-weight: 500;
}

.search-box {
  flex: 1;
  max-width: 400px;
}

.search-box :deep(.el-input__wrapper) {
  border-radius: 20px;
  background: #f5f7fa;
  box-shadow: none;
}

.search-box :deep(.el-input__wrapper:hover),
.search-box :deep(.el-input__wrapper.is-focus) {
  background: #fff;
  box-shadow: 0 0 0 1px #409eff;
}

.user-area {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 24px;
  transition: all 0.3s;
}

.user-info .el-avatar {
  border-radius: 4px !important;
}

.user-info:hover {
  background: #f5f7fa;
}

.username {
  color: #303133;
  font-weight: 500;
}

.main {
  flex: 1;
}

.footer {
  background: #1a1a2e;
  color: #fff;
  margin-top: auto;
}

.footer-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 24px 20px;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  gap: 60px;
  padding-bottom: 30px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-brand {
  max-width: 300px;
}

.footer-logo {
  font-size: 28px;
  font-weight: bold;
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.footer-brand p {
  margin-top: 12px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  line-height: 1.6;
}

.footer-links h4,
.footer-contact h4 {
  font-size: 16px;
  margin-bottom: 16px;
  color: #fff;
}

.footer-links a {
  display: block;
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  padding: 6px 0;
  font-size: 14px;
  transition: color 0.3s;
}

.footer-links a:hover {
  color: #409eff;
}

.footer-contact p {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
}

.footer-bottom {
  padding-top: 20px;
  text-align: center;
}

.footer-bottom p {
  color: rgba(255, 255, 255, 0.4);
  font-size: 13px;
}

@media (max-width: 768px) {
  .header-inner {
    gap: 16px;
    padding: 0 16px;
  }
  
  .logo-text {
    display: none;
  }
  
  .nav {
    display: none;
  }
  
  .search-box {
    max-width: 200px;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 30px;
  }
}
</style>
