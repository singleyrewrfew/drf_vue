<template>
  <el-container class="main-layout">
    <el-aside :width="isCollapsed ? '88px' : '240px'" class="aside">
      <div class="sidebar">
        <div class="logo" :class="{ collapsed: isCollapsed }">
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2L2 7l10 5 10-5-10-5z" />
              <path d="M2 17l10 5 10-5" />
              <path d="M2 12l10 5 10-5" />
            </svg>
          </div>
          <h2 class="logo-title" :class="{ collapsed: isCollapsed }">CMS 管理</h2>
        </div>
        <nav class="nav-menu">
          <div class="menu-section" v-show="!isCollapsed">
            <span class="menu-section-title">主菜单</span>
          </div>
          <router-link to="/dashboard" class="menu-item" :class="{ active: activeMenu === '/dashboard', collapsed: isCollapsed }">
            <el-tooltip :content="isCollapsed ? '仪表盘' : ''" placement="right" :disabled="!isCollapsed">
              <div class="menu-item-icon">
                <el-icon><Odometer /></el-icon>
              </div>
            </el-tooltip>
            <span class="menu-item-text">仪表盘</span>
          </router-link>
          <router-link to="/contents" class="menu-item" :class="{ active: activeMenu === '/contents', collapsed: isCollapsed }">
            <el-tooltip :content="isCollapsed ? '内容管理' : ''" placement="right" :disabled="!isCollapsed">
              <div class="menu-item-icon">
                <el-icon><Document /></el-icon>
              </div>
            </el-tooltip>
            <span class="menu-item-text">内容管理</span>
          </router-link>
          <router-link to="/categories" class="menu-item" :class="{ active: activeMenu === '/categories', collapsed: isCollapsed }">
            <el-tooltip :content="isCollapsed ? '分类管理' : ''" placement="right" :disabled="!isCollapsed">
              <div class="menu-item-icon">
                <el-icon><Folder /></el-icon>
              </div>
            </el-tooltip>
            <span class="menu-item-text">分类管理</span>
          </router-link>
          <router-link to="/tags" class="menu-item" :class="{ active: activeMenu === '/tags', collapsed: isCollapsed }">
            <el-tooltip :content="isCollapsed ? '标签管理' : ''" placement="right" :disabled="!isCollapsed">
              <div class="menu-item-icon">
                <el-icon><PriceTag /></el-icon>
              </div>
            </el-tooltip>
            <span class="menu-item-text">标签管理</span>
          </router-link>
          <router-link to="/media" class="menu-item" :class="{ active: activeMenu === '/media', collapsed: isCollapsed }">
            <el-tooltip :content="isCollapsed ? '媒体管理' : ''" placement="right" :disabled="!isCollapsed">
              <div class="menu-item-icon">
                <el-icon><Picture /></el-icon>
              </div>
            </el-tooltip>
            <span class="menu-item-text">媒体管理</span>
          </router-link>
          <router-link to="/comments" class="menu-item" :class="{ active: activeMenu === '/comments', collapsed: isCollapsed }">
            <el-tooltip :content="isCollapsed ? '评论管理' : ''" placement="right" :disabled="!isCollapsed">
              <div class="menu-item-icon">
                <el-icon><ChatDotRound /></el-icon>
              </div>
            </el-tooltip>
            <span class="menu-item-text">评论管理</span>
          </router-link>

          <template v-if="userStore.isAdmin()">
            <div class="menu-section" v-show="!isCollapsed">
              <span class="menu-section-title">系统管理</span>
            </div>
            <router-link to="/users" class="menu-item" :class="{ active: activeMenu === '/users', collapsed: isCollapsed }">
              <el-tooltip :content="isCollapsed ? '用户管理' : ''" placement="right" :disabled="!isCollapsed">
                <div class="menu-item-icon">
                  <el-icon><User /></el-icon>
                </div>
              </el-tooltip>
              <span class="menu-item-text">用户管理</span>
            </router-link>
            <router-link to="/roles" class="menu-item" :class="{ active: activeMenu === '/roles', collapsed: isCollapsed }">
              <el-tooltip :content="isCollapsed ? '角色管理' : ''" placement="right" :disabled="!isCollapsed">
                <div class="menu-item-icon">
                  <el-icon><Key /></el-icon>
                </div>
              </el-tooltip>
              <span class="menu-item-text">角色管理</span>
            </router-link>
            <router-link to="/permissions" class="menu-item" :class="{ active: activeMenu === '/permissions', collapsed: isCollapsed }">
              <el-tooltip :content="isCollapsed ? '权限管理' : ''" placement="right" :disabled="!isCollapsed">
                <div class="menu-item-icon">
                  <el-icon><Lock /></el-icon>
                </div>
              </el-tooltip>
              <span class="menu-item-text">权限管理</span>
            </router-link>
          </template>
        </nav>
        <div class="sidebar-footer">
          <div class="collapse-btn" @click="toggleCollapse">
            <el-icon>
              <ArrowLeft v-if="!isCollapsed" />
              <ArrowRight v-else />
            </el-icon>
          </div>
          <div class="user-card" :class="{ collapsed: isCollapsed }">
            <el-tooltip :content="isCollapsed ? userStore.user?.username : ''" placement="right" :disabled="!isCollapsed">
              <el-avatar :size="isCollapsed ? 36 : 40" :src="getAvatarUrl(userStore.user?.avatar_url || userStore.user?.avatar)">
                <el-icon><UserFilled /></el-icon>
              </el-avatar>
            </el-tooltip>
            <div class="user-info">
              <span class="user-name">{{ userStore.user?.username }}</span>
              <span class="user-role">{{ userStore.user?.role_name || '用户' }}</span>
            </div>
            <el-dropdown trigger="click" placement="top" v-show="!isCollapsed">
              <div class="user-actions">
                <el-icon><Setting /></el-icon>
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
        <div class="header-breadcrumb">
          <span class="current-page">{{ currentPageTitle }}</span>
        </div>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Odometer, Document, Folder, PriceTag, Picture, ChatDotRound, User, UserFilled, Setting, Key, Lock, ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import { getAvatarUrl } from '@/utils'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isCollapsed = ref(false)

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
}

const activeMenu = computed(() => route.path)

const pageTitles = {
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

const currentPageTitle = computed(() => {
  const path = route.path
  if (path.includes('/contents/edit/')) return '编辑内容'
  return pageTitles[path] || 'CMS 管理'
})

const handleLogout = async () => {
  await userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.main-layout {
  height: 100vh;
}

.aside {
  background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  overflow: hidden;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.sidebar {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.logo {
  height: 70px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.logo.collapsed {
  justify-content: center;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  flex-shrink: 0;
}

.logo-icon svg {
  width: 20px;
  height: 20px;
  color: #fff;
}

.logo h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  letter-spacing: 1px;
  white-space: nowrap;
  opacity: 1;
  width: auto;
  transition: opacity 0.2s ease, width 0.3s ease;
  overflow: hidden;
}

.logo-title.collapsed {
  opacity: 0;
  width: 0;
}

.nav-menu {
  flex: 1;
  padding: 16px 12px;
  overflow-y: auto;
}

.nav-menu::-webkit-scrollbar {
  width: 4px;
}

.nav-menu::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

.menu-section {
  margin-top: 16px;
  margin-bottom: 8px;
  padding: 0 12px;
}

.menu-section:first-child {
  margin-top: 0;
}

.menu-section-title {
  font-size: 11px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.4);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  margin: 4px 0;
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.menu-item.collapsed {
  justify-content: center;
  padding: 12px;
  gap: 0;
}

.menu-item.collapsed {
  justify-content: center;
  padding: 12px;
}

.menu-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  border-radius: 0 3px 3px 0;
  transform: scaleY(0);
  transition: transform 0.3s ease;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
}

.menu-item.active {
  background: linear-gradient(90deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.1) 100%);
  color: #fff;
}

.menu-item.active::before {
  transform: scaleY(1);
}

.menu-item-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
}

.menu-item:hover .menu-item-icon {
  background: rgba(255, 255, 255, 0.1);
}

.menu-item.active .menu-item-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.menu-item-icon .el-icon {
  font-size: 18px;
}

.menu-item-text {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  opacity: 1;
  transition: opacity 0.2s ease;
  overflow: hidden;
}

.menu-item.collapsed .menu-item-text {
  opacity: 0;
  width: 0;
  overflow: hidden;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.collapse-btn {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.collapse-btn:hover {
  background: rgba(255, 255, 255, 0.15);
}

.collapse-btn .el-icon {
  font-size: 18px;
  transition: transform 0.3s ease;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  transition: all 0.3s ease;
  height: 64px;
  box-sizing: border-box;
}

.user-card.collapsed {
  justify-content: center;
  padding: 8px;
  gap: 0;
  height: 52px;
}

.user-card:hover {
  background: rgba(255, 255, 255, 0.1);
}

.user-card .el-avatar {
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
  opacity: 1;
  transition: opacity 0.2s ease, width 0.3s ease, margin 0.3s ease;
  overflow: hidden;
}

.user-card.collapsed .user-info {
  opacity: 0;
  width: 0;
  margin: 0;
  padding: 0;
  height: 0;
  overflow: hidden;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
}

.user-actions {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  transition: all 0.3s ease;
}

.user-actions:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.header {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}

.header-breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
}

.current-page {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.main {
  background-color: #f0f2f5;
}
</style>
