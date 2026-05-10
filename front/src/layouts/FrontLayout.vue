<template>
  <div class="front-layout" @contextmenu.prevent="handleGlobalRightClick">
    <AppHeader
      :categories="categories"
      @open-mobile-menu="mobileMenuVisible = true"
      @logout="handleLogout"
    />

    <main class="main">
      <router-view v-slot="{ Component }">
        <transition name="fade-slide" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <AppFooter />

    <MobileMenu :visible="mobileMenuVisible" @close="mobileMenuVisible = false" />

    <!-- 全局自定义右键菜单 -->
    <Teleport to="body">
      <div
        v-show="contextMenuVisible"
        class="context-menu"
        :style="{ top: contextMenuPos.y + 'px', left: contextMenuPos.x + 'px' }"
        @click.stop
        @contextmenu.prevent
      >
        <div class="context-menu-inner">
          <div
            v-for="(item, index) in contextMenuItems"
            :key="index"
            class="context-menu-item"
            :class="{ 'is-divider': item.divider }"
            @click="handleMenuSelect(item)"
          >
            <template v-if="!item.divider">
              <span v-if="item.icon" class="menu-icon">{{ item.icon }}</span>
              <span class="menu-label">{{ item.label }}</span>
              <span v-if="item.shortcut" class="menu-shortcut">{{ item.shortcut }}</span>
            </template>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getCategories } from '@/api/content'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import MobileMenu from '@/components/MobileMenu.vue'

const router = useRouter()
const userStore = useUserStore()

const categories = ref([])
const mobileMenuVisible = ref(false)

// 右键菜单状态（内联管理）
const contextMenuVisible = ref(false)
const contextMenuPos = reactive({ x: 0, y: 0 })
const contextMenuItems = ref([])

const handleGlobalRightClick = (event) => {
  event.preventDefault()
  event.stopPropagation()

  const menuItems = [
    { label: '返回首页', icon: '🏠', action: 'home' },
    { label: '刷新页面', icon: '🔄', action: 'refresh', shortcut: 'F5' },
    { divider: true },
    { label: '复制当前链接', icon: '📋', action: 'copy', shortcut: 'Ctrl+C' },
    { label: '在新标签打开', icon: '🔗', action: 'newtab', shortcut: 'Ctrl+T' },
    { divider: true },
    { label: '切换主题', icon: '🌙', action: 'theme' }
  ]

  // 设置位置
  contextMenuPos.x = Math.min(event.clientX, window.innerWidth - 200)
  contextMenuPos.y = Math.min(event.clientY, window.innerHeight - 300)

  // 设置菜单项
  contextMenuItems.value = menuItems

  // 显示菜单
  contextMenuVisible.value = true
}

// 关闭右键菜单
const closeContextMenu = () => {
  contextMenuVisible.value = false
}

const handleMenuSelect = (item) => {
  if (!item || item.divider) return

  closeContextMenu()

  switch (item.action) {
    case 'home':
      router.push('/')
      break
    case 'refresh':
      window.location.reload()
      break
    case 'copy':
      navigator.clipboard.writeText(window.location.href).then(() => {
        alert('链接已复制到剪贴板！')
      })
      break
    case 'newtab':
      window.open(window.location.href, '_blank')
      break
    case 'bookmark':
      if (window.sidebar && window.sidebar.addPanel) {
        window.sidebar.addPanel(document.title, window.location.href, '')
      } else if (window.external) {
        window.external.AddFavorite(window.location.href, document.title)
      } else {
        alert('请使用 Ctrl+D 添加书签')
      }
      break
    case 'print':
      window.print()
      break
    case 'theme':
      const theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'
      document.documentElement.setAttribute('data-theme', theme)
      localStorage.setItem('theme', theme)
      break
    case 'source':
      console.log('查看源码:', window.location.href)
      break
    default:
      console.log('执行动作:', item.action)
  }
}

const handleLogout = async () => {
  await userStore.logout()
  router.push('/')
}

const fetchCategories = async () => {
  try {
    const { data } = await getCategories()
    // 处理分页数据和非分页数据
    let categoriesList = []
    if (data.results) {
      // 分页数据格式：{ results: [...], count: N }
      categoriesList = data.results
    } else if (Array.isArray(data)) {
      // 直接返回数组
      categoriesList = data
    } else {
      console.warn('Unexpected categories data format:', data)
      categoriesList = []
    }
    categories.value = categoriesList.slice(0, 8)
  } catch (e) {
    console.error('Failed to fetch categories:', e)
  }
}

onMounted(() => {
  fetchCategories()
  // 点击外部关闭右键菜单
  document.addEventListener('click', closeContextMenu)
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeContextMenu()
  })
})

onUnmounted(() => {
  document.removeEventListener('click', closeContextMenu)
})
</script>

<style scoped>
.front-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-color);
  position: relative;
}

/* 宣纸纹理叠加层 */
.front-layout::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(circle at 20% 50%, rgba(45, 90, 74, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(197, 61, 67, 0.02) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

.main {
  flex: 1;
  position: relative;
  z-index: 1;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.2s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* 右键菜单样式 */
.context-menu {
  position: fixed;
  z-index: 9999;
  min-width: 180px;
}

.context-menu-inner {
  background: var(--paper-cream, #ede8dc);
  border: 1.5px solid var(--paper-aged, #ddd6c8);
  border-radius: var(--radius-sm, 4px);
  box-shadow:
    0 4px 16px rgba(26, 26, 26, 0.15),
    inset 0 0 0 1px rgba(255, 255, 255, 0.3);
  padding: 4px;
  font-family: "KaiTi", "STKaiti", serif;
}

.context-menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  cursor: pointer;
  border-radius: var(--radius-xs, 2px);
  transition: all 0.2s ease;
  color: var(--ink-dark, #1a1a1a);
  font-size: 14px;
}

.context-menu-item:hover:not(.is-divider) {
  background: rgba(197, 61, 67, 0.08);
  color: var(--vermilion-color, #c53d43);
}

.context-menu-item.is-divider {
  height: 1px;
  padding: 0;
  margin: 4px 8px;
  background: var(--paper-aged, #ddd6c8);
  cursor: default;
}

.menu-icon {
  width: 16px;
  text-align: center;
  flex-shrink: 0;
}

.menu-label {
  flex: 1;
}

.menu-shortcut {
  color: var(--ink-light, #8c8c8c);
  font-size: 12px;
  margin-left: auto;
}
</style>
