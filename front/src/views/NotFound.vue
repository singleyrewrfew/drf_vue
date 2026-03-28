<template>
  <div class="not-found-page">
    <div class="not-found-content">
      <h1 class="error-code">404</h1>
      <h2 class="error-title">页面未找到</h2>
      <p class="error-message">抱歉，您访问的页面不存在或已被删除</p>
      <div class="error-actions">
        <el-button type="primary" size="large" @click="$router.push('/')">
          <el-icon><HomeFilled /></el-icon>
          返回首页
        </el-button>
        <el-button size="large" @click="$router.go(-1)">
          <el-icon><Back /></el-icon>
          返回上一页
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { HomeFilled, Back } from '@element-plus/icons-vue'
</script>

<style scoped>
.not-found-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - var(--header-height) - 200px);
  padding: 40px 20px;
  background: var(--bg-color);
}

.not-found-content {
  text-align: center;
  max-width: 500px;
}

.error-code {
  font-size: 140px;
  font-weight: 900;
  color: var(--primary-color);
  line-height: 1;
  margin-bottom: 0;
  text-shadow: 4px 4px 0 var(--primary-light);
}

.error-title {
  font-size: 32px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 24px 0 12px;
}

.error-message {
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: 40px;
  line-height: 1.6;
}

.error-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.error-actions .el-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  font-size: 15px;
}

@media (max-width: 768px) {
  .error-code {
    font-size: 100px;
  }

  .error-title {
    font-size: 24px;
  }

  .error-message {
    font-size: 14px;
  }

  .error-actions {
    flex-direction: column;
  }

  .error-actions .el-button {
    width: 100%;
  }
}

@media (max-width: 576px) {
  .error-code {
    font-size: 80px;
  }

  .error-title {
    font-size: 20px;
  }
}
</style>
