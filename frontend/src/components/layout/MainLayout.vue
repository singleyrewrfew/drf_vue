<template>
  <el-container class="main-layout">
    <el-aside width="220px" class="aside">
      <div class="logo">
        <h2>CMS 管理</h2>
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Odometer /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/contents">
          <el-icon><Document /></el-icon>
          <span>内容管理</span>
        </el-menu-item>
        <el-menu-item index="/categories">
          <el-icon><Folder /></el-icon>
          <span>分类管理</span>
        </el-menu-item>
        <el-menu-item index="/tags">
          <el-icon><PriceTag /></el-icon>
          <span>标签管理</span>
        </el-menu-item>
        <el-menu-item index="/media">
          <el-icon><Picture /></el-icon>
          <span>媒体管理</span>
        </el-menu-item>
        <el-menu-item index="/comments">
          <el-icon><ChatDotRound /></el-icon>
          <span>评论管理</span>
        </el-menu-item>
        <el-menu-item v-if="userStore.isAdmin()" index="/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
        <el-sub-menu v-if="userStore.isAdmin()" index="system">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>系统管理</span>
          </template>
          <el-menu-item index="/roles">
            <el-icon><Key /></el-icon>
            <span>角色管理</span>
          </el-menu-item>
          <el-menu-item index="/permissions">
            <el-icon><Lock /></el-icon>
            <span>权限管理</span>
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="header-right">
          <el-dropdown>
            <span class="user-info">
              <el-avatar :size="32" :src="getAvatarUrl(userStore.user?.avatar_url || userStore.user?.avatar)">
                <el-icon><UserFilled /></el-icon>
              </el-avatar>
              <span class="username">{{ userStore.user?.username }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="$router.push('/profile')">个人设置</el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Odometer, Document, Folder, PriceTag, Picture, ChatDotRound, User, UserFilled, Setting, Key, Lock } from '@element-plus/icons-vue'
import { getAvatarUrl } from '@/utils'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

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
  background-color: #304156;
}

.aside :deep(.el-menu) {
  border-right: none;
}

.aside :deep(.el-menu-item) {
  height: 50px;
  line-height: 50px;
}

.aside :deep(.el-sub-menu__title) {
  height: 50px;
  line-height: 50px;
}

.aside :deep(.el-sub-menu .el-menu) {
  background-color: #1f2d3d;
}

.aside :deep(.el-sub-menu .el-menu-item) {
  min-width: auto;
  width: 100%;
  padding-left: 50px !important;
  background-color: #1f2d3d;
}

.aside :deep(.el-sub-menu .el-menu-item:hover) {
  background-color: #001528;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.logo h2 {
  margin: 0;
  font-size: 18px;
}

.header {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 20px;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.username {
  margin-left: 8px;
}

.main {
  background-color: #f0f2f5;
}
</style>
