<template>
  <Teleport to="body">
    <Transition name="fab-group">
      <div v-if="shouldShow" class="floating-actions" :class="{ 'has-extra': extraButtons.length > 0 }">
        <!-- 额外按钮区域（动态注册） -->
        <div v-if="extraButtons.length > 0" class="extra-buttons">
          <ActionButton
            v-for="btn in extraButtons"
            :key="btn.id"
            v-show="!btn.visible || btn.visible()"
            :variant="btn.id === 'immersive' ? 'immersive' : btn.id === 'toc' ? 'toc' : 'default'"
            :title="btn.title || ''"
            :label="btn.label"
            :icon="btn.icon"
            :icon-component="btn.iconComponent"
            @click="btn.onClick"
          />
        </div>

        <!-- 默认滚动按钮 -->
        <div class="scroll-buttons">
          <ActionButton
            variant="scrollTop"
            title="回到顶部"
            icon="M18 15l-6-6-6 6"
            @click="handleScrollTop"
          />

          <ActionButton
            variant="scrollBottom"
            title="滚动到底部"
            icon="M6 9l6 6 6-6"
            @click="handleScrollBottom"
          />
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useFloatingActions } from '@/composables/useFloatingActions'
import ActionButton from './ActionButton.vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: true
  }
})

const route = useRoute()
const { extraButtons } = useFloatingActions()

const authPages = ['/login', '/register']

const shouldShow = computed(() => {
  if (!props.visible) return false
  return !authPages.includes(route.path)
})

const handleScrollTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const handleScrollBottom = () => {
  window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'smooth' })
}
</script>

<style scoped>
.floating-actions {
  position: fixed;
  right: 24px;
  bottom: 24px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 1000;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.floating-actions.has-extra {
  bottom: 80px;
}

.extra-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
  animation: slideUpFadeIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes slideUpFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.scroll-buttons {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

@media (max-width: 768px) {
  .floating-actions {
    right: 16px;
    bottom: 16px;
  }

  .floating-actions.has-extra {
    bottom: 70px;
  }

  .scroll-buttons {
    gap: 6px;
  }

  .extra-buttons {
    gap: 8px;
  }
}

/* ====== 过渡动画 ====== */
.fab-group-enter-active,
.fab-group-leave-active {
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.fab-group-enter-from,
.fab-group-leave-to {
  opacity: 0;
  transform: translateX(30px) scale(0.9);
}

/* 暗色模式适配 */
[data-theme='dark'] .fab-container {
  background: #27272a;
  border-color: #3f3f46;
}

[data-theme='dark'] .fab-btn {
  background: #3f3f46;
  border-color: #52525b;
  color: #a1a1aa;
}

[data-theme='dark'] .fab-btn:hover {
  background: var(--dark-vermilion, #dc2626);
  border-color: var(--dark-vermilion, #dc2626);
}
</style>
