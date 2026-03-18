<template>
  <div class="mobile-layout">
    <router-view v-slot="{ Component }">
      <keep-alive :include="['Home', 'Articles', 'Profile']">
        <component :is="Component" />
      </keep-alive>
    </router-view>
    
    <nav v-if="showTabBar" class="tab-bar">
      <router-link 
        v-for="item in tabItems" 
        :key="item.path" 
        :to="item.path"
        class="tab-item"
        :class="{ active: isActive(item.path) }"
      >
        <el-icon class="tab-icon">
          <component :is="item.icon" />
        </el-icon>
        <span class="tab-label">{{ item.label }}</span>
      </router-link>
    </nav>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { HomeFilled, Document, User } from '@element-plus/icons-vue'

const route = useRoute()

const showTabBar = computed(() => route.meta.showTabBar !== false)

const tabItems = [
  { path: '/', label: '首页', icon: HomeFilled },
  { path: '/articles', label: '文章', icon: Document },
  { path: '/profile', label: '我的', icon: User },
]

const isActive = (path) => {
  if (path === '/') {
    return route.path === '/'
  }
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

.tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: var(--tab-bar-height);
  background: var(--bg-primary);
  border-top: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding-bottom: var(--safe-area-bottom);
  z-index: var(--z-fixed);
}

.tab-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  padding: 6px 0;
  color: var(--text-tertiary);
  text-decoration: none;
  transition: all var(--transition-fast);
}

.tab-icon {
  font-size: 22px;
  transition: transform var(--transition-fast);
}

.tab-label {
  font-size: 11px;
  font-weight: 500;
}

.tab-item:active .tab-icon {
  transform: scale(0.9);
}

.tab-item.active {
  color: var(--primary-color);
}

.tab-item.active .tab-icon {
  transform: scale(1.05);
}
</style>
