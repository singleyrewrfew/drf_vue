<template>
    <div class="mobile-layout">
        <router-view v-slot="{ Component }">
            <keep-alive :include="['Home', 'Articles', 'Profile']">
                <component :is="Component" />
            </keep-alive>
        </router-view>

        <ScrollButtons />

        <nav v-if="showTabBar" class="bottom-nav">
            <router-link
                v-for="item in tabItems"
                :key="item.path"
                :to="item.path"
                class="nav-item"
                :class="{ active: isActive(item.path) }"
            >
                <el-icon class="nav-icon">
                    <component :is="item.icon" />
                </el-icon>
                <span class="nav-label">{{ item.label }}</span>
            </router-link>
        </nav>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { HomeFilled, Document, User } from '@element-plus/icons-vue'
import ScrollButtons from '@/components/ScrollButtons.vue'

const route = useRoute()

const showTabBar = computed(() => route.meta.showTabBar !== false)

const tabItems = [
    { path: '/', label: '首页', icon: HomeFilled },
    { path: '/articles', label: '发现', icon: Document },
    { path: '/profile', label: '我的', icon: User },
]

const isActive = path => {
    if (path === '/') return route.path === '/'
    return route.path.startsWith(path)
}
</script>

<style scoped>
.mobile-layout {
    min-height: 100vh;
    min-height: 100dvh;
    display: flex;
    flex-direction: column;
    background: var(--bg-color);
}

.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: var(--tab-bar-height);
    background: var(--bg-primary);
    display: flex;
    align-items: center;
    justify-content: space-around;
    padding-bottom: var(--safe-area-bottom);
    z-index: var(--z-fixed);
}

.bottom-nav::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: var(--border-color);
    transform: scaleY(0.5);
}

.nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2px;
    padding: 4px 24px;
    color: var(--text-tertiary);
    text-decoration: none;
    transition: color var(--transition-fast);
}

.nav-icon {
    font-size: 24px;
}

.nav-label {
    font-size: 10px;
    font-weight: 500;
}

.nav-item.active {
    color: var(--primary-color);
}

.nav-item:active {
    opacity: 0.6;
}
</style>
