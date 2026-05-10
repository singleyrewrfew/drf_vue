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
          :class="['toc-item', `toc-${heading.level}`, { active: currentActiveId === heading.id }]"
          :title="heading.text"
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
                  { active: currentActiveId === heading.id }
                ]"
                :title="heading.text"
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
  },
  activeId: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['heading-click'])

const isMobile = ref(false)
const showDrawer = ref(false)
const internalActiveId = ref('')

const currentActiveId = computed(() => props.activeId || internalActiveId.value)

const filteredHeadings = computed(() => {
  return props.headings.filter(heading => heading.level <= 3)
})

const checkMobile = () => {
  isMobile.value = window.innerWidth < 768
}

const scrollToHeading = id => {
  const element = document.getElementById(id)
  if (element) {
    const headerHeight = 72
    const elementPosition = element.getBoundingClientRect().top + window.pageYOffset
    window.scrollTo({
      top: elementPosition - headerHeight - 16,
      behavior: 'smooth'
    })
    internalActiveId.value = id
    emit('heading-click', id)
  }
}

const handleTocClick = id => {
  showDrawer.value = false
  internalActiveId.value = id
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
  font-style: italic;
  font-weight: 400;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 8px 12px 8px 16px;
  display: block;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  border-left: 3px solid transparent;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  position: relative;
}

.toc-item:hover {
  color: var(--text-primary);
  background: linear-gradient(90deg, rgba(var(--primary-rgb), 0.06) 0%, transparent 100%);
}

.toc-item.active {
  color: var(--primary-color);
  background: linear-gradient(90deg, rgba(var(--primary-rgb), 0.12) 0%, rgba(var(--primary-rgb), 0.04) 100%);
  font-weight: 600;
}

.toc-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 60%;
  background: var(--primary-color);
  border-radius: 0 2px 2px 0;
  box-shadow: 0 0 6px rgba(var(--primary-rgb), 0.4);
}

/* 层级差异化样式 */
.toc-1 {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  padding-left: 12px;
  margin-top: 8px;
  border-left-width: 4px;
}

.toc-1:first-child {
  margin-top: 0;
}

.toc-1:hover {
  background: linear-gradient(90deg, rgba(var(--primary-rgb), 0.1) 0%, transparent 100%);
}

.toc-1.active {
  font-weight: 600;
  background: linear-gradient(90deg, rgba(var(--primary-rgb), 0.15) 0%, rgba(var(--primary-rgb), 0.05) 100%);
}

.toc-1.active::before {
  width: 4px;
  height: 70%;
  box-shadow: 0 0 8px rgba(var(--primary-rgb), 0.5);
}

.toc-2 {
  font-size: 13px;
  padding-left: 20px;
  border-left-width: 3px;
}

.toc-2.active {
  font-weight: 600;
}

.toc-2.active::before {
  width: 3px;
  height: 55%;
}

.toc-3 {
  font-size: 12px;
  padding-left: 28px;
  color: var(--text-tertiary);
  border-left-width: 2px;
}

.toc-3:hover {
  color: var(--text-secondary);
  background: linear-gradient(90deg, rgba(var(--primary-rgb), 0.04) 0%, transparent 100%);
}

.toc-3.active {
  color: var(--primary-color);
  font-weight: 500;
  background: linear-gradient(90deg, rgba(var(--primary-rgb), 0.08) 0%, transparent 100%);
}

.toc-3.active::before {
  width: 2px;
  height: 45%;
  box-shadow: 0 0 4px rgba(var(--primary-rgb), 0.3);
}

.mobile-toc-btn {
  position: fixed;
  right: 20px;
  bottom: 100px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--card-bg);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-md);
  cursor: pointer;
  z-index: 100;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mobile-toc-btn svg {
  width: 22px;
  height: 22px;
  color: var(--text-primary);
}

.mobile-toc-btn:hover,
.mobile-toc-btn:active {
  transform: scale(1.05);
  box-shadow: var(--shadow-lg);
}

.toc-drawer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 9998;
  display: flex;
  justify-content: flex-end;
}

.toc-drawer {
  width: min(320px, 85vw);
  height: 100%;
  background: var(--card-bg);
  box-shadow: -4px 0 24px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  animation: slideInRight 0.25s ease-out;
}

@keyframes slideInRight {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}

.toc-drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  border-bottom: 1px solid var(--border-light);
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
}

.toc-drawer-close {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  cursor: pointer;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.toc-drawer-close svg {
  width: 18px;
  height: 18px;
  color: var(--text-secondary);
}

.toc-drawer-close:hover {
  background: var(--bg-secondary);
}

.toc-drawer-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
}

.toc-drawer-item {
  font-size: 14px;
  font-style: italic;
  font-weight: 400;
  color: var(--text-secondary);
  padding: 10px 14px 10px 18px;
  margin-bottom: 4px;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  border-left: 3px solid transparent;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  position: relative;
}

.toc-drawer-item:hover {
  color: var(--text-primary);
  background: linear-gradient(90deg, rgba(var(--primary-rgb), 0.06) 0%, transparent 100%);
}

.toc-drawer-item.active {
  color: var(--primary-color);
  background: linear-gradient(90deg, rgba(var(--primary-rgb), 0.12) 0%, rgba(var(--primary-rgb), 0.04) 100%);
  font-weight: 600;
}

.toc-drawer-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 60%;
  background: var(--primary-color);
  border-radius: 0 2px 2px 0;
  box-shadow: 0 0 6px rgba(var(--primary-rgb), 0.4);
}

/* 移动端层级差异化 */
.toc-level-1 {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  padding-left: 14px;
  margin-top: 10px;
  border-left-width: 4px;
}

.toc-level-1:first-child {
  margin-top: 0;
}

.toc-level-1:hover {
  background: linear-gradient(90deg, rgba(var(--primary-rgb), 0.1) 0%, transparent 100%);
}

.toc-level-1.active {
  font-weight: 700;
  background: linear-gradient(90deg, rgba(var(--primary-rgb), 0.15) 0%, rgba(var(--primary-rgb), 0.05) 100%);
}

.toc-level-1.active::before {
  width: 4px;
  height: 70%;
  box-shadow: 0 0 8px rgba(var(--primary-rgb), 0.5);
}

.toc-level-2 {
  font-size: 14px;
  padding-left: 24px;
  border-left-width: 3px;
}

.toc-level-2.active::before {
  width: 3px;
  height: 55%;
}

.toc-level-3 {
  font-size: 13px;
  padding-left: 32px;
  color: var(--text-tertiary);
  border-left-width: 2px;
}

.toc-level-3:hover {
  color: var(--text-secondary);
  background: linear-gradient(90deg, rgba(var(--primary-rgb), 0.04) 0%, transparent 100%);
}

.toc-level-3.active {
  color: var(--primary-color);
  font-weight: 500;
}

.toc-drawer-enter-active,
.toc-drawer-leave-active {
  transition: opacity 0.25s ease;
}

.toc-drawer-enter-from,
.toc-drawer-leave-to {
  opacity: 0;
}

.toc-drawer-enter-active .toc-drawer,
.toc-drawer-leave-active .toc-drawer {
  transition: transform 0.25s ease;
}

.toc-drawer-enter-from .toc-drawer,
.toc-drawer-leave-to .toc-drawer {
  transform: translateX(100%);
}

/* 暗色模式适配 */
[data-theme='dark'] .toc-container {
  background: #27272a;
  border-color: #3f3f46;
}

[data-theme='dark'] .toc-header {
  border-bottom-color: #3f3f46;
}

[data-theme='dark'] .toc-title {
  color: var(--dark-text, #e4e4e7);
}
</style>
