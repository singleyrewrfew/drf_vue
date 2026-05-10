<template>
  <div class="front-layout">
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
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
</style>
