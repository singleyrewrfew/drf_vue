<template>
  <header class="app-header">
    <div class="header-inner">
      <button class="mobile-menu-btn" @click="$emit('openMobileMenu')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="6" x2="21" y2="6" />
          <line x1="3" y1="12" x2="21" y2="12" />
          <line x1="3" y1="18" x2="21" y2="18" />
        </svg>
      </button>

      <div class="logo" @click="$router.push('/')">
        <span class="logo-icon">Y</span>
        <div class="logo-text">
          <span class="logo-title">YNCAQY</span>
        </div>
      </div>

      <nav class="nav">
        <router-link to="/" class="nav-item" exact-path>
          <el-icon>
            <HomeFilled />
          </el-icon>
          <span>首页</span>
        </router-link>
        <router-link to="/articles" class="nav-item">
          <el-icon>
            <Document />
          </el-icon>
          <span>文章</span>
        </router-link>

        <WinDropdown v-if="categories.length" :items="categoryItems" @select="handleCategorySelect">
          <template #trigger>
            <div class="nav-item">
              <el-icon>
                <Folder />
              </el-icon>
              <span>分类</span>
              <el-icon class="arrow">
                <ArrowDown />
              </el-icon>
            </div>
          </template>
        </WinDropdown>
      </nav>

      <div class="search-box">
        <el-input
          v-model="searchKeyword"
          placeholder="搜章寻句..."
          @keyup.enter="handleSearch"
          @clear="handleSearchClear"
          clearable
          :prefix-icon="Search"
        />
      </div>

      <div class="user-area">
        <button class="theme-toggle" @click="themeStore.toggleTheme()">
          <el-icon class="theme-icon" :class="{ rotate: themeStore.theme === 'dark' }">
            <Sunny v-if="themeStore.theme === 'dark'" />
            <Moon v-else />
          </el-icon>
        </button>

        <template v-if="userStore.isLoggedIn">
          <WinDropdown :items="userMenuItems" @select="handleUserMenuSelect">
            <template #trigger>
              <div class="user-info">
                <el-avatar :size="36" :src="userAvatar">
                  {{ username?.charAt(0).toUpperCase() }}
                </el-avatar>
                <span class="username">{{ username }}</span>
                <el-icon class="dropdown-arrow">
                  <ArrowDown />
                </el-icon>
              </div>
            </template>
          </WinDropdown>
        </template>
        <template v-else>
          <WinDropdown :items="guestMenuItems" @select="handleGuestMenuSelect">
            <template #trigger>
              <div class="guest-avatar">
                <el-avatar :size="36" class="guest-avatar-icon">游</el-avatar>
              </div>
            </template>
          </WinDropdown>
        </template>
      </div>
    </div>

    <!-- 嵌入式阅读进度条 -->
    <ReadingProgress v-if="showProgress" />
  </header>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  HomeFilled,
  Document,
  Folder,
  Search,
  ArrowDown,
  Sunny,
  Moon
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { useThemeStore } from '@/stores/theme'
import WinDropdown from '@/components/WinDropdown.vue'
import ReadingProgress from '@/components/article/ReadingProgress.vue'
import { getAvatarUrl } from '@/utils'

const props = defineProps({
  categories: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['openMobileMenu', 'logout'])

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const themeStore = useThemeStore()

const searchKeyword = ref('')
const previousPath = ref('')

// 只在文章详情页显示进度条
const showProgress = computed(() => {
  return route.path.startsWith('/article/')
})

// 强制触发头像更新
const userAvatar = computed(() => getAvatarUrl(userStore.user?.avatar))
const username = computed(() => userStore.user?.username)

// 组件挂载时检查用户状态
onMounted(() => {
  // 如果有 token 但没有 user 信息，重新获取
  if (userStore.isLoggedIn && !userStore.user) {
    userStore.fetchProfile().catch(err => {
      console.error('[AppHeader] Failed to fetch profile:', err)
    })
  }
})

const categoryItems = computed(() =>
  props.categories.map(cat => ({
    label: cat.name,
    value: cat.slug || cat.id
  }))
)

const userMenuItems = [
  { label: '个人中心', value: 'profile' },
  { label: '退出登录', value: 'logout' }
]

const guestMenuItems = [
  { label: '登录', value: 'login' },
  { label: '注册', value: 'register' }
]

const handleCategorySelect = item => {
  router.push(`/category/${item.value}`)
}

const handleUserMenuSelect = item => {
  if (item.value === 'profile') {
    router.push('/profile')
  } else if (item.value === 'logout') {
    emit('logout')
  }
}

const handleGuestMenuSelect = item => {
  if (item.value === 'login') {
    router.push('/login')
  } else if (item.value === 'register') {
    router.push('/register')
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
</script>

<style scoped>
.app-header {
  background: linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 2px solid var(--border-color);
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
  background: var(--bg-tertiary);
}

.mobile-menu-btn svg {
  width: 22px;
  height: 22px;
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
  width: 42px;
  height: 42px;
  background: var(--vermilion-color);
  border-radius: var(--radius-xs);
  border: 2px solid var(--ink-dark);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 22px;
  font-weight: bold;
  font-family: 'SimSun', serif;
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.2),
    2px 2px 8px rgba(197, 61, 67, 0.3);
  transition: all var(--transition-fast);
}

.logo:hover .logo-icon {
  transform: scale(1.05) rotate(-3deg);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.25),
    3px 3px 12px rgba(197, 61, 67, 0.4);
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-size: 22px;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.2;
  letter-spacing: var(--tracking-wide);
  font-family: var(--font-display);
}

.nav {
  display: flex;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: var(--radius-xs);
  transition: all var(--transition-fast);
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  font-family: var(--font-sans);
  letter-spacing: var(--tracking-normal);
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

.nav-item::after {
  display: none;
}

.nav-item.router-link-exact-active {
  color: var(--primary-color);
  background: var(--primary-bg);
  font-weight: 600;
  position: relative;
}

.nav-item.router-link-exact-active::after {
  content: '';
  position: absolute;
  bottom: 2px;
  left: 50%;
  transform: translateX(-50%);
  width: 16px;
  height: 2px;
  background: var(--primary-color);
  border-radius: 1px;
}

.search-box {
  flex: 1;
  max-width: 360px;
}

.search-box :deep(.el-input__wrapper) {
  border-radius: var(--radius-xs);
  background: var(--bg-secondary);
  box-shadow: none;
  padding: 4px 12px;
  border: 1px solid var(--border-light);
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
  font-family: var(--font-sans);
}

.search-box :deep(.el-input__inner::placeholder) {
  color: var(--text-placeholder);
  font-style: italic;
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
  border-radius: var(--radius-xs);
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
  color: var(--primary-color);
  border-color: var(--border-color);
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
  border-radius: var(--radius-xs);
  transition: all var(--transition-fast);
  background: transparent;
}

.user-info .el-avatar {
  border-radius: var(--radius-xs) !important;
  border: 1px solid var(--border-color);
  transition: all var(--transition-fast);
}

.user-info:hover {
  background: var(--primary-bg);
}

.user-info:hover .el-avatar {
  box-shadow: 0 0 0 2px var(--primary-color);
}

.username {
  color: var(--text-primary);
  font-weight: 500;
  font-size: 14px;
  font-family: var(--font-sans);
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

.guest-avatar {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px 4px 4px;
  border-radius: var(--radius-xs);
  transition: all var(--transition-fast);
  background: transparent;
}

.guest-avatar:hover {
  background: var(--primary-bg);
}

.guest-avatar-icon {
  background: var(--vermilion-color) !important;
  color: #fff !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  border-radius: var(--radius-xs) !important;
  border: 2px solid var(--ink-dark) !important;
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.2),
    1px 1px 4px rgba(197, 61, 67, 0.3) !important;
  transition: all var(--transition-fast);
}

.guest-avatar:hover .guest-avatar-icon {
  box-shadow: 0 0 0 2px var(--vermilion-color), 2px 2px 8px rgba(197, 61, 67, 0.4);
  transform: scale(1.05);
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
}
</style>
