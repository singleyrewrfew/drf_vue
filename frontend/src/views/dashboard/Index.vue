<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background-color: #409eff">
              <el-icon :size="24"><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.contents }}</div>
              <div class="stat-label">内容总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background-color: #67c23a">
              <el-icon :size="24"><ChatDotRound /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.comments }}</div>
              <div class="stat-label">评论总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background-color: #e6a23c">
              <el-icon :size="24"><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.users }}</div>
              <div class="stat-label">用户总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background-color: #f56c6c">
              <el-icon :size="24"><View /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.views }}</div>
              <div class="stat-label">总浏览量</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-card style="margin-top: 20px">
      <template #header>
        <span>欢迎使用 CMS 内容管理系统</span>
      </template>
      <p>这是一个基于 Django REST Framework + Vue 3 构建的内容管理系统。</p>
      <p>功能特性：</p>
      <ul>
        <li>用户管理：注册、登录、权限控制</li>
        <li>内容管理：文章的增删改查、发布、归档</li>
        <li>分类标签：多级分类、标签管理</li>
        <li>媒体管理：图片、文件上传</li>
        <li>评论系统：评论审核、嵌套回复</li>
      </ul>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Document, ChatDotRound, User, View } from '@element-plus/icons-vue'

const stats = ref({
  contents: 0,
  comments: 0,
  users: 0,
  views: 0,
})

onMounted(() => {
  stats.value = {
    contents: 128,
    comments: 256,
    users: 32,
    views: 1024,
  }
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.stat-info {
  margin-left: 16px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}
</style>
