<template>
  <router-view />
  
  <div class="scroll-buttons">
    <el-button
      @click="scrollToTop"
      class="scroll-btn"
    >
      <el-icon><Top /></el-icon>
    </el-button>
    <el-button
      @click="scrollToBottom"
      class="scroll-btn"
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
  gap: 8px;
  z-index: 1000;
}

.scroll-btn {
  width: 44px;
  height: 44px;
  font-size: 20px;
  padding: 0;
  margin: 0;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
}

.scroll-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}
</style>
