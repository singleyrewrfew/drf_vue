<template>
  <div>
    <!-- 桌面端目录 -->
    <div class="sidebar-card toc-card desktop-toc" v-if="!isMobile">
      <div class="sidebar-title">
        <el-icon>
          <List />
        </el-icon>
        <span>目录</span>
      </div>
      <div class="toc-list" v-if="headings.length">
        <div
          v-for="(heading, index) in filteredHeadings"
          :key="index"
          :class="['toc-item', `toc-${heading.level}`, { active: activeHeadingId === heading.id }]"
          @click="scrollToHeading(heading.id)"
        >
          {{ heading.text }}
        </div>
      </div>
      <el-empty v-else description="暂无目录" :image-size="60" />
    </div>

    <!-- 移动端目录按钮 -->
    <Teleport to="body">
      <button
        v-if="isMobile && headings.length > 0"
        class="mobile-toc-btn"
        @click="showDrawer = true"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="6" x2="21" y2="6" />
          <line x1="3" y1="12" x2="15" y2="12" />
          <line x1="3" y1="18" x2="18" y2="18" />
        </svg>
      </button>

      <Transition name="toc-drawer">
        <div v-if="showDrawer && isMobile" class="toc-drawer-overlay" @click="showDrawer = false">
          <div class="toc-drawer" @click.stop>
            <div class="toc-drawer-header">
              <span>目录</span>
              <button class="toc-drawer-close" @click="showDrawer = false">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>
            <div class="toc-drawer-content">
              <div
                v-for="(heading, index) in filteredHeadings"
                :key="index"
                :class="[
                  'toc-drawer-item',
                  `toc-level-${heading.level}`,
                  { active: activeHeadingId === heading.id }
                ]"
                @click="handleTocClick(heading.id)"
              >
                {{ heading.text }}
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { List } from '@element-plus/icons-vue'

const props = defineProps({
  headings: {
    type: Array,
    default: () => []
  }
})

const isMobile = ref(false)
const showDrawer = ref(false)
const activeHeadingId = ref('')

// 过滤出 h1-h3 级别的标题
const filteredHeadings = computed(() => {
  return props.headings.filter(heading => heading.level <= 3)
})

// 检测是否为移动端设备
const checkMobile = () => {
  isMobile.value = window.innerWidth < 768
}

// 滚动到指定标题位置
const scrollToHeading = id => {
  const element = document.getElementById(id)
  if (element) {
    const headerHeight = 72
    const elementPosition = element.getBoundingClientRect().top + window.pageYOffset
    window.scrollTo({
      top: elementPosition - headerHeight - 16,
      behavior: 'smooth'
    })
    activeHeadingId.value = id
  }
}

// 处理移动端目录项点击
const handleTocClick = id => {
  showDrawer.value = false
  activeHeadingId.value = id
  scrollToHeading(id)
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<style scoped>
.sidebar-card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 24px;
  border: 1px solid var(--border-light);
  transition: all var(--transition-fast);
}

.sidebar-card:hover {
  border-color: rgba(0, 120, 212, 0.2);
  box-shadow: var(--shadow-sm);
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 18px;
  padding-bottom: 14px;
  border-bottom: 2px solid var(--border-light);
}

.sidebar-title .el-icon {
  color: var(--primary-color);
  font-size: 20px;
}

.toc-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-height: 400px;
  overflow-y: auto;
  padding-right: 8px;
}

.toc-list::-webkit-scrollbar {
  width: 4px;
}

.toc-list::-webkit-scrollbar-track {
  background: var(--bg-secondary);
  border-radius: 2px;
}

.toc-list::-webkit-scrollbar-thumb {
  background: var(--border-dark);
  border-radius: 2px;
}

.toc-item {
  font-size: 13px;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 8px 12px;
  display: block;
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
  cursor: pointer;
  border-left: 2px solid transparent;
}

.toc-item:hover {
  color: var(--primary-color);
  background: var(--primary-bg);
  border-left-color: var(--primary-color);
}

.toc-item.active {
  color: var(--primary-color);
  background: rgba(var(--primary-rgb), 0.08);
  border-left-color: var(--primary-color);
}

.toc-2 {
  padding-left: 0;
}

.toc-3 {
  padding-left: 16px;
}

.toc-4 {
  padding-left: 32px;
}
</style>
