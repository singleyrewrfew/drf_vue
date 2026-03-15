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
  right: 30px;
  bottom: 30px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 1000;
}

.scroll-btn {
  width: 48px;
  height: 48px;
  font-size: 20px;
  padding: 0;
  margin: 0;
  border-radius: 50%;
  background: var(--primary-gradient);
  border: none;
  color: #fff;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.scroll-btn:hover {
  transform: translateY(-4px) scale(1.1);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
  background: var(--primary-gradient);
  color: #fff;
}

.scroll-btn:active {
  transform: translateY(-2px) scale(1.05);
}

.scroll-btn .el-icon {
  transition: transform 0.3s ease;
}

.scroll-top:hover .el-icon {
  transform: translateY(-3px);
}

.scroll-bottom:hover .el-icon {
  transform: translateY(3px);
}
</style>
