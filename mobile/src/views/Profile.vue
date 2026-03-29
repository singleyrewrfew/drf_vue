<template>
    <div class="page">
        <header class="page-header">
            <div class="header-left"></div>
            <h1 class="page-title">我的</h1>
            <div class="header-right">
                <button class="btn-icon" @click="themeStore.toggleTheme()">
                    <el-icon>
                        <Sunny v-if="themeStore.theme === 'dark'" />
                        <Moon v-else />
                    </el-icon>
                </button>
            </div>
        </header>

        <div class="page-content">
            <div v-if="userStore.isLoggedIn" class="user-card">
                <el-avatar :size="64" :src="getAvatarUrl(userStore.user?.avatar)">
                    {{ userStore.user?.username?.charAt(0).toUpperCase() }}
                </el-avatar>
                <div class="user-info">
                    <h2 class="user-name">{{ userStore.user?.username }}</h2>
                    <p class="user-bio">{{ userStore.user?.bio || '这个人很懒，什么都没写' }}</p>
                </div>
                <router-link to="/profile/edit" class="btn btn-outline btn-sm">编辑</router-link>
            </div>

            <div v-else class="user-card">
                <el-avatar :size="64">
                    <el-icon>
                        <User />
                    </el-icon>
                </el-avatar>
                <div class="user-info">
                    <h2 class="user-name">登录/注册</h2>
                    <p class="user-bio">登录后体验更多功能</p>
                </div>
                <button class="btn btn-primary btn-sm" @click="$router.push('/login')">登录</button>
            </div>

            <div class="menu-group">
                <router-link to="/profile/edit" class="menu-item">
                    <el-icon class="menu-icon">
                        <User />
                    </el-icon>
                    <span class="menu-label">个人资料</span>
                    <el-icon class="menu-arrow">
                        <ArrowRight />
                    </el-icon>
                </router-link>
            </div>

            <div v-if="userStore.isLoggedIn" class="menu-group">
                <button class="menu-item" @click="handleLogout">
                    <el-icon class="menu-icon" style="color: var(--danger-color)">
                        <SwitchButton />
                    </el-icon>
                    <span class="menu-label" style="color: var(--danger-color)">退出登录</span>
                </button>
            </div>

            <p class="version">版本 1.0.0</p>
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
            type: 'warning',
        })
        await userStore.logout()
        router.push('/')
    } catch (e) {
        // Cancelled
    }
}
</script>

<style scoped>
.btn-sm {
    padding: 6px 12px;
    font-size: 12px;
}

.version {
    text-align: center;
    font-size: 12px;
    color: var(--text-tertiary);
    padding: 20px;
}
</style>
