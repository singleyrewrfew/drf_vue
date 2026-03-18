<template>
  <div class="front-layout">
    <header class="header">
      <div class="header-inner">
        <button class="mobile-menu-btn" @click="mobileMenuVisible = true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="3" y1="6" x2="21" y2="6" />
            <line x1="3" y1="12" x2="21" y2="12" />
            <line x1="3" y1="18" x2="21" y2="18" />
          </svg>
        </button>
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
          
          <WinDropdown 
            v-if="categories.length" 
            :items="categoryItems"
            @select="handleCategorySelect"
          >
            <template #trigger>
              <div class="nav-item">
                <el-icon><Folder /></el-icon>
                <span>分类</span>
                <el-icon class="arrow"><ArrowDown /></el-icon>
              </div>
            </template>
          </WinDropdown>
        </nav>
        
        <div class="search-box">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索文章..."
            @keyup.enter="handleSearch"
            @clear="handleSearchClear"
            clearable
            :prefix-icon="Search"
          />
        </div>
        
        <div class="user-area">
          <button class="theme-toggle" @click="themeStore.toggleTheme()" :title="themeStore.theme === 'light' ? '切换到深色模式' : '切换到浅色模式'">
            <el-icon class="theme-icon" :class="{ 'rotate': themeStore.theme === 'dark' }">
              <Sunny v-if="themeStore.theme === 'dark'" />
              <Moon v-else />
            </el-icon>
          </button>
          <template v-if="userStore.isLoggedIn">
            <WinDropdown 
              :items="userMenuItems"
              @select="handleUserMenuSelect"
            >
              <template #trigger>
                <div class="user-info">
                  <el-avatar :size="36" :src="getAvatarUrl(userStore.user?.avatar)">{{ userStore.user?.username?.charAt(0).toUpperCase() }}</el-avatar>
                  <span class="username">{{ userStore.user?.username }}</span>
                  <el-icon class="dropdown-arrow"><ArrowDown /></el-icon>
                </div>
              </template>
            </WinDropdown>
          </template>
          <template v-else>
            <el-button type="default" @click="$router.push('/login')">登录</el-button>
            <el-button type="primary" @click="$router.push('/register')">注册</el-button>
          </template>
        </div>
      </div>
    </header>
    
    <main class="main">
      <router-view v-slot="{ Component }">
        <transition name="fade-slide" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    
    <footer class="footer">
      <div class="footer-inner">
        <div class="footer-content">
          <div class="footer-brand">
            <div class="footer-logo">
              <span class="logo-icon-small">C</span>
              <span>CMS</span>
            </div>
            <p>一个简洁高效的内容管理系统，专注于内容创作与分享</p>
            <div class="footer-social">
              <a href="#" class="social-link" title="GitHub">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                  <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
                </svg>
              </a>
              <a href="#" class="social-link" title="Twitter">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                  <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                </svg>
              </a>
              <a href="#" class="social-link" title="Email">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                  <path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                </svg>
              </a>
            </div>
          </div>
          <div class="footer-links">
            <h4>快速链接</h4>
            <router-link to="/">
              <el-icon><HomeFilled /></el-icon>
              首页
            </router-link>
            <router-link to="/articles">
              <el-icon><Document /></el-icon>
              文章
            </router-link>
          </div>
          <div class="footer-contact">
            <h4>联系我们</h4>
            <p>
              <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                <path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
              </svg>
              contact@cms.com
            </p>
            <p>
              <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
              </svg>
              中国
            </p>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; {{ new Date().getFullYear() }} CMS 内容管理系统. All rights reserved.</p>
        </div>
      </div>
    </footer>
    
    <MobileMenu 
      :visible="mobileMenuVisible" 
      @close="mobileMenuVisible = false" 
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { HomeFilled, Document, Folder, FolderOpened, Search, User, SwitchButton, ArrowDown, Sunny, Moon } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { useThemeStore } from '@/stores/theme'
import { getCategories } from '@/api/content'
import WinDropdown from '@/components/WinDropdown.vue'
import MobileMenu from '@/components/MobileMenu.vue'
import { getAvatarUrl } from '@/utils'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const themeStore = useThemeStore()

const searchKeyword = ref('')
const categories = ref([])
const mobileMenuVisible = ref(false)
const previousPath = ref('')

const categoryItems = computed(() => 
  categories.value.map(cat => ({
    label: cat.name,
    value: cat.slug || cat.id
  }))
)

const handleCategorySelect = (item) => {
  router.push(`/category/${item.value}`)
}

const userMenuItems = [
  { label: '个人中心', value: 'profile' },
  { label: '退出登录', value: 'logout' }
]

const handleUserMenuSelect = (item) => {
  if (item.value === 'profile') {
    router.push('/profile')
  } else if (item.value === 'logout') {
    handleLogout()
  }
}

const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    if (route.path !== '/search') {
      previousPath.value = route.fullPath
    }
    router.push({ path: '/search', query: { q: searchKeyword.value } })
  }
}

const handleSearchClear = () => {
  if (route.path === '/search') {
    if (previousPath.value) {
      router.push(previousPath.value)
    } else {
      router.push('/')
    }
  }
}

watch(searchKeyword, (newVal, oldVal) => {
  if (oldVal && !newVal && route.path === '/search') {
    if (previousPath.value) {
      router.push(previousPath.value)
    } else {
      router.push('/')
    }
  }
})

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
  background: var(--bg-color);
}

.mobile-menu-btn {
  display: none;
  width: 40px;
  height: 40px;
  border: none;
  background: transparent;
  color: var(--text-primary);
  cursor: pointer;
  border-radius: var(--radius-sm);
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.mobile-menu-btn:hover {
  background: var(--bg-secondary);
}

.mobile-menu-btn svg {
  width: 22px;
  height: 22px;
}

.header {
  background: var(--bg-primary);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid var(--border-light);
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
}

.header-inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 24px;
  height: var(--header-height);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  flex-shrink: 0;
  transition: transform var(--transition-fast);
}

.logo:hover {
  transform: scale(1.02);
}

.logo-icon {
  width: 44px;
  height: 44px;
  background: var(--primary-color);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 22px;
  font-weight: bold;
  transition: all var(--transition-fast);
}

.logo:hover .logo-icon {
  transform: scale(1.02);
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-color);
  line-height: 1.2;
}

.logo-subtitle {
  font-size: 11px;
  color: var(--text-secondary);
  letter-spacing: 0.5px;
}

.nav {
  display: flex;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
}

.nav-item .arrow {
  font-size: 10px;
  margin-left: 2px;
  transition: transform var(--transition-fast);
}

.nav-item:hover .arrow {
  transform: rotate(180deg);
}

.nav-item:hover {
  color: var(--primary-color);
  background: var(--primary-bg);
}

.nav-item.router-link-exact-active {
  color: var(--primary-color);
  background: var(--primary-bg);
  font-weight: 600;
}

.search-box {
  flex: 1;
  max-width: 360px;
}

.search-box :deep(.el-input__wrapper) {
  border-radius: var(--radius-sm);
  background: var(--bg-secondary);
  box-shadow: none;
  padding: 4px 12px;
  border: 1px solid transparent;
  transition: all var(--transition-fast);
}

.search-box :deep(.el-input__wrapper:hover) {
  background: var(--bg-secondary);
  border-color: var(--border-color);
}

.search-box :deep(.el-input__wrapper.is-focus) {
  background: var(--bg-primary);
  border-color: var(--primary-color);
  box-shadow: 0 0 0 1px var(--primary-color);
}

.search-box :deep(.el-input__inner) {
  font-size: 14px;
}

.search-box :deep(.el-input__inner::placeholder) {
  color: var(--text-placeholder);
}

.search-box :deep(.el-input__clear) {
  color: var(--text-tertiary);
  transition: color var(--transition-fast);
}

.search-box :deep(.el-input__clear:hover) {
  color: var(--primary-color);
}

.user-area {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.theme-toggle {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  background: var(--bg-secondary);
  border: 1px solid transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-fast);
  color: var(--text-secondary);
}

.theme-toggle:hover {
  background: var(--primary-bg);
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.theme-icon {
  font-size: 18px;
  transition: all var(--transition-normal);
}

.theme-icon.rotate {
  transform: rotate(180deg);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 6px 12px 6px 6px;
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
  background: transparent;
}

.user-info .el-avatar {
  border-radius: var(--radius-sm) !important;
  border: none;
  transition: all var(--transition-fast);
}

.user-info:hover {
  background: var(--primary-bg);
}

.user-info:hover .el-avatar {
  box-shadow: 0 0 0 2px var(--primary-light);
}

.username {
  color: var(--text-primary);
  font-weight: 500;
  font-size: 14px;
}

.dropdown-arrow {
  font-size: 10px;
  color: var(--text-tertiary);
  transition: transform var(--transition-fast);
}

.user-info:hover .dropdown-arrow {
  transform: rotate(180deg);
  color: var(--primary-color);
}

.main {
  flex: 1;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.15s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

.footer {
  background: var(--bg-secondary);
  color: var(--text-primary);
  margin-top: auto;
  border-top: 1px solid var(--border-color);
}

.footer-inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 60px 24px 24px;
}

.footer-content {
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr;
  gap: 60px;
  padding-bottom: 40px;
  border-bottom: 1px solid var(--border-color);
}

.footer-brand {
  max-width: 320px;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 16px;
}

.logo-icon-small {
  width: 36px;
  height: 36px;
  background: var(--primary-color);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.footer-brand p {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.7;
  margin-bottom: 20px;
}

.footer-social {
  display: flex;
  gap: 12px;
}

.social-link {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  transition: all var(--transition-fast);
}

.social-link:hover {
  background: var(--primary-color);
  color: #fff;
}

.footer-links h4,
.footer-contact h4 {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 20px;
  color: var(--text-primary);
  letter-spacing: 0.5px;
}

.footer-links a {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 8px 0;
  font-size: 14px;
  transition: all var(--transition-fast);
}

.footer-links a:hover {
  color: var(--primary-color);
}

.footer-links a .el-icon {
  font-size: 16px;
  opacity: 0.6;
}

.footer-links a:hover .el-icon {
  opacity: 1;
}

.footer-contact p {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text-secondary);
  font-size: 14px;
  margin-bottom: 12px;
}

.footer-contact p svg {
  opacity: 0.6;
}

.footer-bottom {
  padding-top: 24px;
  text-align: center;
}

.footer-bottom p {
  color: var(--text-tertiary);
  font-size: 13px;
}

@media (max-width: 1024px) {
  .footer-content {
    grid-template-columns: 1fr 1fr;
    gap: 40px;
  }
  
  .footer-brand {
    grid-column: 1 / -1;
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .mobile-menu-btn {
    display: flex;
  }
  
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
    max-width: 180px;
  }
  
  .user-area {
    display: none;
  }
  
  .username {
    display: none;
  }
  
  .dropdown-arrow {
    display: none;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .footer-inner {
    padding: 40px 16px 20px;
  }
  
  .footer-brand {
    max-width: 100%;
    text-align: center;
    order: 1;
  }
  
  .footer-logo {
    justify-content: center;
    font-size: 20px;
    margin-bottom: 12px;
  }
  
  .logo-icon-small {
    width: 32px;
    height: 32px;
    font-size: 16px;
  }
  
  .footer-brand p {
    font-size: 13px;
    margin-bottom: 16px;
  }
  
  .footer-social {
    justify-content: center;
  }
  
  .social-link {
    width: 36px;
    height: 36px;
  }
  
  .footer-links,
  .footer-contact {
    text-align: center;
    order: 2;
  }
  
  .footer-links h4,
  .footer-contact h4 {
    font-size: 14px;
    margin-bottom: 12px;
  }
  
  .footer-links a {
    justify-content: center;
    padding: 6px 0;
    font-size: 13px;
  }
  
  .footer-contact p {
    justify-content: center;
    font-size: 13px;
    margin-bottom: 8px;
  }
  
  .footer-bottom {
    padding-top: 16px;
  }
  
  .footer-bottom p {
    font-size: 12px;
  }
}

@media (max-width: 576px) {
  .footer-inner {
    padding: 32px 12px 16px;
  }
  
  .footer-content {
    gap: 20px;
  }
  
  .footer-logo {
    font-size: 18px;
  }
  
  .logo-icon-small {
    width: 28px;
    height: 28px;
    font-size: 14px;
  }
  
  .footer-brand p {
    font-size: 12px;
  }
  
  .social-link {
    width: 32px;
    height: 32px;
  }
  
  .social-link svg {
    width: 16px;
    height: 16px;
  }
  
  .footer-links h4,
  .footer-contact h4 {
    font-size: 13px;
    margin-bottom: 10px;
  }
  
  .footer-links a,
  .footer-contact p {
    font-size: 12px;
  }
  
  .footer-bottom p {
    font-size: 11px;
  }
}
</style>
