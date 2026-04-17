<template>
  <el-container class="main-layout">
    <el-aside :width="isCollapsed ? '72px' : '240px'" class="aside">
      <div class="sidebar">
        <div class="logo" :class="{ collapsed: isCollapsed }">
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2L2 7l10 5 10-5-10-5z"/>
              <path d="M2 17l10 5 10-5"/>
              <path d="M2 12l10 5 10-5"/>
            </svg>
          </div>
          <h2 class="logo-title" :class="{ collapsed: isCollapsed }">CMS 管理</h2>
        </div>
        <nav class="nav-menu" ref="navMenuRef">
          <div class="menu-indicator" :style="{
            top: indicatorStyle.top,
            height: indicatorStyle.height,
            opacity: indicatorStyle.opacity,
            transform: `scaleY(${indicatorStyle.scaleY})`,
            transformOrigin: indicatorStyle.transformOrigin
          }"></div>

          <template v-for="(menuSection, sectionIndex) in MENU_CONFIG" :key="sectionIndex">
            <!-- 系统管理菜单需要管理员权限 -->
            <template v-if="!menuSection.requireAdmin || userStore.isAdmin()">
              <div class="menu-section" v-show="!isCollapsed">
                <span class="menu-section-title">{{ menuSection.section }}</span>
              </div>

              <router-link
                  v-for="item in menuSection.items"
                  :key="item.path"
                  :to="item.path"
                  class="menu-item"
                  :class="{ active: activeMenu === item.path, collapsed: isCollapsed }"
                  :data-path="item.path"
                  :title="isCollapsed ? item.label : ''"
              >
                <div class="menu-item-icon">
                  <el-icon>
                    <component :is="item.icon"/>
                  </el-icon>
                </div>
                <span class="menu-item-text">{{ item.label }}</span>
              </router-link>
            </template>
          </template>
        </nav>
        <div class="sidebar-footer">
          <div class="user-card" :class="{ collapsed: isCollapsed }">
            <div class="avatar-wrapper" @click="toggleCollapse"
                 :title="isCollapsed ? '展开侧边栏' : '收起侧边栏'">
              <el-avatar :size="40"
                         :src="getAvatarUrl(userStore.user?.avatar_url || userStore.user?.avatar)">
                <el-icon>
                  <UserFilled/>
                </el-icon>
              </el-avatar>
              <div class="collapse-icon">
                <el-icon>
                  <ArrowLeft v-if="!isCollapsed"/>
                  <ArrowRight v-else/>
                </el-icon>
              </div>
            </div>
            <div class="user-info" v-show="!isCollapsed">
              <span class="user-name">{{ userStore.user?.username }}</span>
              <span class="user-role">{{ userStore.user?.role_name || '用户' }}</span>
            </div>
            <el-dropdown trigger="click" placement="top-start" v-show="!isCollapsed" @click.stop>
              <div class="user-actions" @click.stop title="设置">
                <el-icon>
                  <Setting/>
                </el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="$router.push('/profile')">个人设置</el-dropdown-item>
                  <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </div>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <span class="current-page">{{ currentPageTitle }}</span>
        </div>
        <div class="header-right">
          <button class="theme-toggle" @click="toggleTheme"
                  :title="themeStore.theme === 'light' ? '切换到暗色模式' : '切换到亮色模式'">
            <el-icon v-if="themeStore.theme === 'light'">
              <Moon/>
            </el-icon>
            <el-icon v-else>
              <Sunny/>
            </el-icon>
          </button>
        </div>
      </el-header>
      <el-main class="main">
        <router-view/>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import {ref, computed, watch, onMounted, nextTick} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {useUserStore} from '@/stores/user'
import {useThemeStore} from '@/stores/theme'
import {
  Odometer,
  Document,
  Folder,
  PriceTag,
  Picture,
  ChatDotRound,
  User,
  UserFilled,
  Setting,
  Key,
  Lock,
  ArrowLeft,
  ArrowRight,
  Moon,
  Sunny
} from '@element-plus/icons-vue'
import {getAvatarUrl} from '@/utils'

// 菜单配置
const MENU_CONFIG = [
  {
    section: '主菜单',
    items: [
      {path: '/dashboard', icon: Odometer, label: '仪表盘'},
      {path: '/contents', icon: Document, label: '内容管理'},
      {path: '/categories', icon: Folder, label: '分类管理'},
      {path: '/tags', icon: PriceTag, label: '标签管理'},
      {path: '/media', icon: Picture, label: '媒体管理'},
      {path: '/comments', icon: ChatDotRound, label: '评论管理'},
    ]
  },
  {
    section: '系统管理',
    requireAdmin: true,
    items: [
      {path: '/users', icon: User, label: '用户管理'},
      {path: '/roles', icon: Key, label: '角色管理'},
      {path: '/permissions', icon: Lock, label: '权限管理'},
    ]
  }
]

// 页面标题映射
const PAGE_TITLES = {
  '/dashboard': '仪表盘',
  '/contents': '内容管理',
  '/contents/create': '新建内容',
  '/categories': '分类管理',
  '/tags': '标签管理',
  '/media': '媒体管理',
  '/comments': '评论管理',
  '/users': '用户管理',
  '/roles': '角色管理',
  '/permissions': '权限管理',
  '/profile': '个人设置'
}

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const themeStore = useThemeStore()

const isCollapsed = ref(false)
const navMenuRef = ref(null)
const indicatorStyle = ref({
  top: '0px',
  height: '0px',
  scaleY: 1,
  transformOrigin: 'top',
  opacity: 0
})

const isAnimating = ref(false)
const previousTop = ref(0)

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
}

const toggleTheme = () => {
  themeStore.toggleTheme()
}

const activeMenu = computed(() => route.path)

let animationTimeouts = []

const clearAllTimeouts = () => {
  animationTimeouts.forEach(id => clearTimeout(id))
  animationTimeouts = []
}

const addTimeout = (callback, delay) => {
  const id = setTimeout(() => {
    const index = animationTimeouts.indexOf(id)
    if (index > -1) animationTimeouts.splice(index, 1)
    callback()
  }, delay)
  animationTimeouts.push(id)
  return id
}

const animateIndicator = (fromTop, toTop, toHeight) => {
  clearAllTimeouts()
  isAnimating.value = true

  const goingDown = toTop > fromTop

  indicatorStyle.value = {
    top: `${fromTop}px`,
    height: `${toHeight}px`,
    scaleY: 1,
    transformOrigin: 'center',
    opacity: 1
  }

  addTimeout(() => {
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        const stretchY = 1.25
        indicatorStyle.value.scaleY = stretchY
        indicatorStyle.value.transformOrigin = goingDown ? 'top' : 'bottom'

        addTimeout(() => {
          indicatorStyle.value.opacity = 0

          addTimeout(() => {
            indicatorStyle.value = {
              top: `${toTop}px`,
              height: `${toHeight}px`,
              scaleY: stretchY,
              transformOrigin: goingDown ? 'bottom' : 'top',
              opacity: 1
            }

            addTimeout(() => {
              indicatorStyle.value.scaleY = 1
              indicatorStyle.value.transformOrigin = 'center'

              addTimeout(() => {
                isAnimating.value = false
              }, 167)
            }, 167)
          }, 83)
        }, 83)
      })
    })
  }, 50)
}

const updateIndicator = (animate = true) => {
  nextTick(() => {
    if (!navMenuRef.value) return

    const activeItem = navMenuRef.value.querySelector('.menu-item.active')
    if (activeItem) {
      const menuRect = navMenuRef.value.getBoundingClientRect()
      const itemRect = activeItem.getBoundingClientRect()

      const newTop = itemRect.top - menuRect.top + 8
      const newHeight = itemRect.height - 16

      if (animate && indicatorStyle.value.opacity === 1) {
        animateIndicator(previousTop.value, newTop, newHeight)
      } else {
        clearAllTimeouts()
        isAnimating.value = false
        indicatorStyle.value = {
          top: `${newTop}px`,
          height: `${newHeight}px`,
          scaleY: 1,
          opacity: 1
        }
      }

      previousTop.value = newTop
    } else {
      indicatorStyle.value.opacity = 0
    }
  })
}

watch(activeMenu, () => {
  updateIndicator(true)
})

watch(isCollapsed, () => {
  updateIndicator(false)
})

onMounted(() => {
  updateIndicator(false)
})

const currentPageTitle = computed(() => {
  const path = route.path
  if (path.includes('/contents/edit/')) return '编辑内容'
  return PAGE_TITLES[path] || 'CMS 管理'
})

const handleLogout = async () => {
  await userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.main-layout {
  height: 100vh;
  background: var(--bg-color);
}

.aside {
  background: var(--sidebar-bg);
  overflow: hidden;
  transition: width 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  border-right: 1px solid var(--sidebar-border);
}

.sidebar {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.logo {
  height: 40px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 12px 12px 12px;
}

.logo.collapsed {
  justify-content: center;
  padding: 20px 16px 12px 16px;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: var(--primary-color);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.logo.collapsed .logo-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
}

.logo-icon svg {
  width: 20px;
  height: 20px;
  color: #fff;
}

.logo.collapsed .logo-icon svg {
  width: 18px;
  height: 18px;
}

.logo h2 {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: var(--sidebar-text);
  letter-spacing: 0;
  white-space: nowrap;
  opacity: 1;
  width: auto;
  transition: opacity 0.15s ease;
  overflow: hidden;
}

.logo-title.collapsed {
  opacity: 0;
  width: 0;
}

.nav-menu {
  flex: 1;
  padding: 4px 8px;
  overflow-y: auto;
  position: relative;
}

.nav-menu::-webkit-scrollbar {
  width: 0;
}

.sidebar.collapsed .nav-menu {
  padding: 4px 0;
}

.menu-indicator {
  position: absolute;
  left: 12px;
  width: 3px;
  background: var(--primary-color);
  border-radius: 2px;
  opacity: 0;
  pointer-events: none;
  z-index: 1;
  transition: top 0.15s cubic-bezier(0.4, 0, 0.2, 1),
  height 0.15s cubic-bezier(0.4, 0, 0.2, 1),
  opacity 0.1s ease,
  transform 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}

.menu-section {
  margin-top: 16px;
  margin-bottom: 4px;
  padding: 0 16px;
  height: 20px;
  display: flex;
  align-items: center;
}

.menu-section:first-child {
  margin-top: 8px;
}

.menu-section-title {
  font-size: 12px;
  font-weight: 400;
  color: var(--sidebar-text-secondary);
  letter-spacing: 0;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 16px;
  height: 40px;
  padding: 0 12px;
  margin: 2px 0;
  border-radius: var(--radius-sm);
  color: var(--sidebar-text);
  text-decoration: none;
  transition: background 0.1s ease;
  position: relative;
  overflow: hidden;
}

.menu-item.collapsed {
  justify-content: center;
  padding: 0 16px;
  gap: 0;
}

.menu-item:hover {
  background: var(--sidebar-hover-bg);
}

.menu-item.active {
  background: var(--sidebar-active-bg);
  color: var(--primary-color);
}

.menu-item-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.menu-item-icon .el-icon {
  font-size: 18px;
}

.menu-item-text {
  font-size: 14px;
  font-weight: 400;
  white-space: nowrap;
  opacity: 1;
  transition: opacity 0.15s ease;
  overflow: hidden;
}

.menu-item.collapsed .menu-item-text {
  opacity: 0;
  width: 0;
  overflow: hidden;
}

.sidebar-footer {
  padding: 8px;
  border-top: 1px solid var(--sidebar-border);
}

.user-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
  cursor: pointer;
  position: relative;
}

.user-card.collapsed {
  justify-content: center;
  padding: 8px;
  gap: 0;
}

.user-card:hover {
  background: var(--sidebar-hover-bg);
}

.avatar-wrapper {
  position: relative;
  flex-shrink: 0;
  width: 36px;
  height: 36px;
}

.avatar-wrapper :deep(.el-avatar) {
  width: 36px !important;
  height: 36px !important;
  min-width: 36px;
  min-height: 36px;
}

.collapse-icon {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 16px;
  height: 16px;
  background: var(--primary-color);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0.8);
  transition: all 0.15s ease;
}

.user-card:hover .collapse-icon {
  opacity: 1;
  transform: scale(1);
}

.collapse-icon .el-icon {
  font-size: 10px;
  color: #fff;
}

.user-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
  overflow: hidden;
  transition: opacity 0.15s ease, width 0.15s ease;
}

.user-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--sidebar-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 12px;
  color: var(--sidebar-text-secondary);
}

.user-actions {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-xs);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--sidebar-text-secondary);
  cursor: pointer;
  transition: background 0.1s ease;
}

.user-actions:hover {
  background: var(--sidebar-hover-bg);
  color: var(--sidebar-text);
}

.header {
  background: var(--card-bg);
  box-shadow: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  border-bottom: 1px solid var(--border-color);
  height: 48px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.current-page {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.theme-toggle {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  background: transparent;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.1s ease;
  color: var(--text-secondary);
}

.theme-toggle:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.main {
  background: var(--bg-color);
  padding: 20px;
}
</style>
