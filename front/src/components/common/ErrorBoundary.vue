<template>
  <div v-if="hasError" class="error-boundary">
    <div class="error-content">
      <el-icon :size="64" class="error-icon">
        <WarningFilled />
      </el-icon>
      <h2>出错了</h2>
      <p>{{ errorMessage }}</p>
      <div class="error-actions">
        <el-button type="primary" @click="retry">
          <el-icon><RefreshRight /></el-icon>
          重试
        </el-button>
        <el-button @click="goHome">
          <el-icon><HomeFilled /></el-icon>
          返回首页
        </el-button>
      </div>
    </div>
  </div>
  <slot v-else></slot>
</template>

<script setup>
import { ref, onErrorCaptured } from 'vue'
import { useRouter } from 'vue-router'
import { WarningFilled, RefreshRight, HomeFilled } from '@element-plus/icons-vue'

const router = useRouter()

const hasError = ref(false)
const errorMessage = ref('页面加载失败，请重试')

onErrorCaptured((error) => {
  console.error('Error captured by ErrorBoundary:', error)
  hasError.value = true
  errorMessage.value = error.message || '页面加载失败，请重试'
  return false
})

const retry = () => {
  hasError.value = false
  errorMessage.value = ''
}

const goHome = () => {
  hasError.value = false
  errorMessage.value = ''
  router.push('/')
}
</script>

<style scoped>
.error-boundary {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 40px 20px;
}

.error-content {
  text-align: center;
  max-width: 400px;
}

.error-icon {
  color: var(--danger-color);
  margin-bottom: 24px;
}

.error-content h2 {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.error-content p {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 24px;
  line-height: 1.6;
}

.error-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.error-actions .el-button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

@media (max-width: 768px) {
  .error-boundary {
    min-height: 300px;
    padding: 24px 16px;
  }

  .error-icon :deep(.el-icon) {
    font-size: 48px !important;
  }

  .error-content h2 {
    font-size: 20px;
  }

  .error-actions {
    flex-direction: column;
  }
}
</style>
