<template>
  <router-view />
  
  <div class="scroll-buttons">
    <el-button
      @click="scrollToTop"
      class="scroll-btn scroll-top"
    >
      <el-icon><Top /></el-icon>
    </el-button>
    <el-button
      @click="scrollToBottom"
      class="scroll-btn scroll-bottom"
    >
      <el-icon><Bottom /></el-icon>
    </el-button>
  </div>
</template>

<script setup>
import { Top, Bottom } from '@element-plus/icons-vue'

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

const scrollToBottom = () => {
  window.scrollTo({
    top: document.documentElement.scrollHeight,
    behavior: 'smooth'
  })
}
</script>

<style scoped>
.scroll-buttons {
  position: fixed;
  right: 24px;
  bottom: 24px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 1000;
}

.scroll-btn {
  width: 40px;
  height: 40px;
  font-size: 16px;
  padding: 0;
  margin: 0;
  border-radius: var(--radius-sm);
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.scroll-btn:hover {
  background: var(--primary-bg);
  border-color: var(--primary-color);
  color: var(--primary-color);
  box-shadow: var(--shadow-md);
}

.scroll-btn:active {
  transform: scale(0.95);
}

.scroll-btn .el-icon {
  transition: transform var(--transition-fast);
}

.scroll-top:hover .el-icon {
  transform: translateY(-2px);
}

.scroll-bottom:hover .el-icon {
  transform: translateY(2px);
}
</style>
