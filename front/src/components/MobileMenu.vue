<template>
    <Teleport to="body">
        <Transition name="drawer">
            <div v-if="visible" class="mobile-menu-overlay" @click="$emit('close')">
                <div class="mobile-menu" @click.stop>
                    <div class="menu-header">
                        <div class="logo">
                            <span class="logo-text">CMS</span>
                        </div>
                        <button class="close-btn" @click="$emit('close')">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="18" y1="6" x2="6" y2="18"/>
                                <line x1="6" y1="6" x2="18" y2="18"/>
                            </svg>
                        </button>
                    </div>

                    <div class="menu-content">
                        <nav class="menu-nav">
                            <router-link to="/" class="menu-item" @click="$emit('close')">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                                    <polyline points="9 22 9 12 15 12 15 22"/>
                                </svg>
                                <span>首页</span>
                            </router-link>
                            <router-link to="/articles" class="menu-item" @click="$emit('close')">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                    <polyline points="14 2 14 8 20 8"/>
                                    <line x1="16" y1="13" x2="8" y2="13"/>
                                    <line x1="16" y1="17" x2="8" y2="17"/>
                                    <polyline points="10 9 9 9 8 9"/>
                                </svg>
                                <span>文章</span>
                            </router-link>
                        </nav>

                        <div class="menu-divider"></div>

                        <div v-if="userStore.isLoggedIn" class="menu-user">
                            <div class="user-info">
                                <el-avatar :size="40" :src="userStore.user?.avatar_url">
                                    {{ userStore.user?.username?.charAt(0)?.toUpperCase() }}
                                </el-avatar>
                                <div class="user-details">
                                    <span class="username">{{ userStore.user?.username }}</span>
                                    <span class="email">{{ userStore.user?.email }}</span>
                                </div>
                            </div>
                            <nav class="menu-nav">
                                <router-link to="/profile" class="menu-item" @click="$emit('close')">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                                        <circle cx="12" cy="7" r="4"/>
                                    </svg>
                                    <span>个人中心</span>
                                </router-link>
                                <button class="menu-item logout-btn" @click="handleLogout">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                                        <polyline points="16 17 21 12 16 7"/>
                                        <line x1="21" y1="12" x2="9" y2="12"/>
                                    </svg>
                                    <span>退出登录</span>
                                </button>
                            </nav>
                        </div>

                        <div v-else class="menu-auth">
                            <router-link to="/login" class="auth-btn login" @click="$emit('close')">
                                登录
                            </router-link>
                            <router-link to="/register" class="auth-btn register" @click="$emit('close')">
                                注册
                            </router-link>
                        </div>
                    </div>

                    <div class="menu-footer">
                        <button class="theme-toggle" @click="toggleTheme">
                            <svg v-if="isDark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="5"/>
                                <line x1="12" y1="1" x2="12" y2="3"/>
                                <line x1="12" y1="21" x2="12" y2="23"/>
                                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
                                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
                                <line x1="1" y1="12" x2="3" y2="12"/>
                                <line x1="21" y1="12" x2="23" y2="12"/>
                                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
                                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
                            </svg>
                            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
                            </svg>
                            <span>{{ isDark ? '浅色模式' : '深色模式' }}</span>
                        </button>
                    </div>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script setup>
import {computed} from 'vue'
import {useRouter} from 'vue-router'
import {useUserStore} from '@/stores/user'
import {useThemeStore} from '@/stores/theme'

defineProps({
    visible: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['close'])

const router = useRouter()
const userStore = useUserStore()
const themeStore = useThemeStore()

const isDark = computed(() => themeStore.isDark)

const toggleTheme = () => {
    themeStore.toggleTheme()
}

const handleLogout = () => {
    userStore.logout()
    emit('close')
    router.push('/')
}
</script>

<style scoped>
.mobile-menu-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: var(--z-modal);
    display: flex;
    justify-content: flex-end;
}

.mobile-menu {
    width: 280px;
    max-width: 80vw;
    height: 100%;
    background: var(--card-bg);
    display: flex;
    flex-direction: column;
    box-shadow: var(--shadow-xl);
}

.menu-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    border-bottom: 1px solid var(--border-light);
}

.logo {
    display: flex;
    align-items: center;
    gap: 8px;
}

.logo-text {
    font-size: 20px;
    font-weight: 700;
    color: var(--primary-color);
}

.close-btn {
    width: 32px;
    height: 32px;
    border: none;
    background: transparent;
    color: var(--text-secondary);
    cursor: pointer;
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all var(--transition-fast);
}

.close-btn:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
}

.close-btn svg {
    width: 18px;
    height: 18px;
}

.menu-content {
    flex: 1;
    overflow-y: auto;
    padding: 16px 0;
}

.menu-nav {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 0 12px;
}

.menu-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    color: var(--text-primary);
    text-decoration: none;
    border-radius: var(--radius-sm);
    transition: all var(--transition-fast);
    cursor: pointer;
    border: none;
    background: transparent;
    width: 100%;
    text-align: left;
    font-size: 15px;
}

.menu-item svg {
    width: 20px;
    height: 20px;
    color: var(--text-secondary);
    flex-shrink: 0;
}

.menu-item:hover {
    background: var(--primary-bg);
    color: var(--primary-color);
}

.menu-item:hover svg {
    color: var(--primary-color);
}

.menu-item.router-link-active {
    background: var(--primary-bg);
    color: var(--primary-color);
}

.menu-item.router-link-active svg {
    color: var(--primary-color);
}

.menu-divider {
    height: 1px;
    background: var(--border-light);
    margin: 16px 20px;
}

.menu-user {
    padding-top: 8px;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 20px;
    margin-bottom: 8px;
}

.user-details {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
}

.username {
    font-size: 15px;
    font-weight: 500;
    color: var(--text-primary);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.email {
    font-size: 13px;
    color: var(--text-tertiary);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.logout-btn {
    color: var(--danger-color);
}

.logout-btn svg {
    color: var(--danger-color);
}

.logout-btn:hover {
    background: var(--danger-bg);
    color: var(--danger-color);
}

.menu-auth {
    display: flex;
    gap: 12px;
    padding: 16px 20px;
}

.auth-btn {
    flex: 1;
    padding: 12px 16px;
    text-align: center;
    border-radius: var(--radius-sm);
    font-size: 15px;
    font-weight: 500;
    text-decoration: none;
    transition: all var(--transition-fast);
}

.auth-btn.login {
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-primary);
}

.auth-btn.login:hover {
    border-color: var(--primary-color);
    color: var(--primary-color);
}

.auth-btn.register {
    background: var(--primary-color);
    color: #fff;
}

.auth-btn.register:hover {
    background: var(--primary-hover);
}

.menu-footer {
    padding: 16px 20px;
    border-top: 1px solid var(--border-light);
}

.theme-toggle {
    display: flex;
    align-items: center;
    gap: 12px;
    width: 100%;
    padding: 12px 16px;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    background: transparent;
    color: var(--text-primary);
    font-size: 15px;
    cursor: pointer;
    transition: all var(--transition-fast);
}

.theme-toggle svg {
    width: 20px;
    height: 20px;
    color: var(--text-secondary);
}

.theme-toggle:hover {
    border-color: var(--primary-color);
    color: var(--primary-color);
}

.theme-toggle:hover svg {
    color: var(--primary-color);
}

/* 过渡动画 */
.drawer-enter-active,
.drawer-leave-active {
    transition: all 0.25s ease;
}

.drawer-enter-active .mobile-menu,
.drawer-leave-active .mobile-menu {
    transition: transform 0.25s ease;
}

.drawer-enter-from,
.drawer-leave-to {
    background: rgba(0, 0, 0, 0);
}

.drawer-enter-from .mobile-menu,
.drawer-leave-to .mobile-menu {
    transform: translateX(100%);
}
</style>
