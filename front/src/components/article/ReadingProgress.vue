<template>
  <div class="reading-progress">
    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: progress + '%' }"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  showPercentage: {
    type: Boolean,
    default: false
  }
})

const progress = ref(0)

let ticking = false

function updateProgress() {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop
  const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight

  if (docHeight > 0) {
    const scrollPercent = (scrollTop / docHeight) * 100
    progress.value = Math.min(100, Math.max(0, scrollPercent))
  }

  ticking = false
}

function onScroll() {
  if (!ticking) {
    requestAnimationFrame(updateProgress)
    ticking = true
  }
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  updateProgress()
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
.reading-progress {
  width: 100%;
  height: 3px;
  background: transparent;
  position: relative;
  overflow: hidden;
}

.progress-bar {
  width: 100%;
  height: 100%;
  background: var(--border-light, rgba(0, 0, 0, 0.06));
  border-radius: 0;
  overflow: hidden;
  position: relative;
}

[data-theme='dark'] .progress-bar {
  background: rgba(255, 255, 255, 0.08);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(
    90deg,
    var(--primary-color, #409eff) 0%,
    var(--primary-color-light, #66b1ff) 100%
  );
  transition: width 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  box-shadow: 0 0 8px rgba(64, 158, 255, 0.4);
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.4) 50%,
    transparent 100%
  );
  animation: shimmer 2.5s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

@media (max-width: 768px) {
  .reading-progress {
    height: 2px;
  }
}
</style>
