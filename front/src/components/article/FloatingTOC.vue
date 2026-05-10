<template>
  <Teleport to="body">
    <Transition name="floating-toc">
      <div v-if="isVisible" class="floating-toc-overlay" @click.self="close">
        <div class="floating-toc-panel">
          <div class="toc-panel-header">
            <span class="panel-title">目录导航</span>
            <button class="panel-close-btn" @click="close">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <div class="toc-panel-content">
            <div
              v-for="(heading, index) in headings"
              :key="index"
              :class="['floating-toc-item', `level-${heading.level}`, { active: activeId === heading.id }]"
              :title="heading.text"
              @click="handleClick(heading)"
            >
              {{ heading.text }}
            </div>

            <div v-if="!headings.length" class="empty-hint">
              暂无目录
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false
  },
  headings: {
    type: Array,
    default: () => []
  },
  activeId: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['close', 'select'])

function close() {
  emit('close')
}

function handleClick(heading) {
  emit('select', heading.id)
}
</script>

<style scoped>
.floating-toc-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  z-index: 9999;
  display: flex;
  justify-content: flex-end;
  padding: 80px 40px 40px 40px;
}

.floating-toc-panel {
  width: min(380px, 85vw);
  max-height: calc(100vh - 120px);
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: slideInRight 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

[data-theme='dark'] .floating-toc-panel {
  background: rgba(30, 30, 35, 0.97);
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(100%) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

.toc-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(135deg, rgba(var(--primary-rgb), 0.05), transparent);
}

.panel-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: 0.5px;
}

.panel-close-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  cursor: pointer;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s ease;
  color: var(--text-secondary);
}

.panel-close-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  transform: rotate(90deg);
}

.panel-close-btn svg {
  width: 20px;
  height: 20px;
}

.toc-panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 12px 16px;

  scrollbar-width: thin;
  scrollbar-color: var(--border-color) transparent;
}

.toc-panel-content::-webkit-scrollbar {
  width: 6px;
}

.toc-panel-content::-webkit-scrollbar-track {
  background: transparent;
}

.toc-panel-content::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 3px;
}

.floating-toc-item {
  font-size: 13px;
  font-style: italic;
  font-weight: 400;
  color: var(--text-secondary);
  padding: 8px 16px 8px 18px;
  margin-bottom: 4px;
  border-radius: 0 8px 8px 0;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  border-left: 3px solid transparent;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  position: relative;
}

.floating-toc-item:hover {
  color: var(--text-primary);
  background: linear-gradient(90deg, rgba(var(--primary-rgb), 0.06) 0%, transparent 100%);
}

.floating-toc-item.active {
  color: var(--primary-color);
  background: linear-gradient(90deg, rgba(var(--primary-rgb), 0.12) 0%, rgba(var(--primary-rgb), 0.04) 100%);
  font-weight: 600;
}

.floating-toc-item.active::before {
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

/* 层级差异化 - 与普通目录完全一致 */
.level-1 {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  padding-left: 12px;
  margin-top: 8px;
  border-left-width: 4px;
}

.level-1:first-child {
  margin-top: 0;
}

.level-1:hover {
  background: linear-gradient(90deg, rgba(var(--primary-rgb), 0.1) 0%, transparent 100%);
}

.level-1.active {
  font-weight: 600;
  background: linear-gradient(90deg, rgba(var(--primary-rgb), 0.15) 0%, rgba(var(--primary-rgb), 0.05) 100%);
}

.level-1.active::before {
  width: 4px;
  height: 70%;
  box-shadow: 0 0 8px rgba(var(--primary-rgb), 0.5);
}

.level-2 {
  font-size: 13px;
  padding-left: 20px;
  border-left-width: 3px;
}

.level-2.active::before {
  width: 3px;
  height: 55%;
}

.level-3 {
  font-size: 12px;
  padding-left: 28px;
  color: var(--text-tertiary);
  border-left-width: 2px;
}

.level-3:hover {
  color: var(--text-secondary);
  background: linear-gradient(90deg, rgba(var(--primary-rgb), 0.04) 0%, transparent 100%);
}

.level-3.active {
  color: var(--primary-color);
  font-weight: 500;
  background: linear-gradient(90deg, rgba(var(--primary-rgb), 0.08) 0%, transparent 100%);
}

.level-3.active::before {
  width: 2px;
  height: 45%;
  box-shadow: 0 0 4px rgba(var(--primary-rgb), 0.3);
}

.empty-hint {
  text-align: center;
  color: var(--text-tertiary);
  padding: 48px 20px;
  font-size: 14px;
}

/* 过渡动画 */
.floating-toc-enter-active,
.floating-toc-leave-active {
  transition: all 0.3s ease;
}

.floating-toc-enter-from,
.floating-toc-leave-to {
  opacity: 0;
}

.floating-toc-enter-active .floating-toc-panel,
.floating-toc-leave-active .floating-toc-panel {
  transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.floating-toc-enter-from .floating-toc-panel,
.floating-toc-leave-to .floating-toc-panel {
  transform: translateX(100%) scale(0.95);
}

@media (max-width: 768px) {
  .floating-toc-overlay {
    padding: 70px 16px 16px 16px;
  }

  .floating-toc-panel {
    width: min(320px, 90vw);
    max-height: calc(100vh - 88px);
    border-radius: 14px;
  }

  .toc-panel-header {
    padding: 16px 20px;
  }

  .panel-title {
    font-size: 16px;
  }

  .toc-panel-content {
    padding: 10px 12px;
  }

  .floating-toc-item {
    font-size: 13px;
    padding: 10px 14px;
  }

  .level-1 {
    font-size: 14px;
    padding-left: 12px;
  }

  .level-2 {
    padding-left: 20px;
  }

  .level-3 {
    padding-left: 28px;
  }
}
</style>
