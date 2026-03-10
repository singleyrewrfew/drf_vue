<template>
  <div class="dashboard">
    <el-row :gutter="20" class="stat-row">
      <el-col :xs="12" :sm="6">
        <el-card shadow="hover" class="stat-card stat-card-primary">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon :size="32"><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.contents }}</div>
              <div class="stat-label">内容总数</div>
            </div>
          </div>
          <div class="stat-footer">
            <span>已发布 {{ stats.published }}</span>
            <span>草稿 {{ stats.drafts }}</span>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6">
        <el-card shadow="hover" class="stat-card stat-card-success">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon :size="32"><ChatDotRound /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.comments }}</div>
              <div class="stat-label">评论总数</div>
            </div>
          </div>
          <div class="stat-footer">
            <span>用户互动数据</span>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6">
        <el-card shadow="hover" class="stat-card stat-card-warning">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon :size="32"><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.users }}</div>
              <div class="stat-label">用户总数</div>
            </div>
          </div>
          <div class="stat-footer">
            <span>注册用户</span>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6">
        <el-card shadow="hover" class="stat-card stat-card-danger">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon :size="32"><View /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ formatNumber(stats.views) }}</div>
              <div class="stat-label">总浏览量</div>
            </div>
          </div>
          <div class="stat-footer">
            <span>累计访问</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :xs="24" :lg="16">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>最新发布内容</span>
              <el-button type="primary" link @click="$router.push('/contents')">查看全部</el-button>
            </div>
          </template>
          <el-table :data="stats.recent_contents" v-loading="loading" stripe>
            <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
            <el-table-column prop="author_name" label="作者" width="120" />
            <el-table-column prop="view_count" label="浏览量" width="100">
              <template #default="{ row }">
                <el-tag type="info" size="small">{{ row.view_count }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="发布时间" width="180" />
          </el-table>
          <el-empty v-if="!loading && stats.recent_contents.length === 0" description="暂无内容" />
        </el-card>
      </el-col>
      <el-col :xs="24" :lg="8">
        <el-card shadow="hover">
          <template #header>
            <span>快捷操作</span>
          </template>
          <div class="quick-actions">
            <div class="action-item" @click="$router.push('/contents/create')">
              <el-icon :size="24" class="action-icon"><EditPen /></el-icon>
              <span>新建内容</span>
            </div>
            <div class="action-item" @click="$router.push('/media')">
              <el-icon :size="24" class="action-icon"><Upload /></el-icon>
              <span>上传媒体</span>
            </div>
            <div class="action-item" @click="$router.push('/categories')">
              <el-icon :size="24" class="action-icon"><Folder /></el-icon>
              <span>分类管理</span>
            </div>
            <div class="action-item" @click="$router.push('/tags')">
              <el-icon :size="24" class="action-icon"><PriceTag /></el-icon>
              <span>标签管理</span>
            </div>
            <div class="action-item" @click="$router.push('/comments')">
              <el-icon :size="24" class="action-icon"><ChatDotRound /></el-icon>
              <span>评论管理</span>
            </div>
            <div class="action-item" @click="$router.push('/profile')">
              <el-icon :size="24" class="action-icon"><Setting /></el-icon>
              <span>个人设置</span>
            </div>
          </div>
        </el-card>

        <el-card shadow="hover" style="margin-top: 20px">
          <template #header>
            <span>系统信息</span>
          </template>
          <div class="system-info">
            <div class="info-item">
              <span class="info-label">媒体文件</span>
              <span class="info-value">{{ stats.media }} 个</span>
            </div>
            <div class="info-item">
              <span class="info-label">系统版本</span>
              <span class="info-value">v1.0.0</span>
            </div>
            <div class="info-item">
              <span class="info-label">框架</span>
              <span class="info-value">Django + Vue 3</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Document, ChatDotRound, User, View, EditPen, Upload, Folder, PriceTag, Setting } from '@element-plus/icons-vue'
import api from '@/api'

const loading = ref(false)
const stats = ref({
  contents: 0,
  published: 0,
  drafts: 0,
  comments: 0,
  users: 0,
  media: 0,
  views: 0,
  recent_contents: [],
})

const formatNumber = (num) => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k'
  }
  return num
}

const fetchStats = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/auth/stats/')
    stats.value = data
  } catch (error) {
    console.error('获取统计数据失败', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.stat-row {
  margin-bottom: 20px;
}

.stat-card {
  border-radius: 8px;
  overflow: hidden;
}

.stat-card :deep(.el-card__body) {
  padding: 20px;
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.stat-card-primary .stat-icon {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
}

.stat-card-success .stat-icon {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
}

.stat-card-warning .stat-icon {
  background: linear-gradient(135deg, #e6a23c 0%, #ebb563 100%);
}

.stat-card-danger .stat-icon {
  background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);
}

.stat-info {
  margin-left: 16px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.stat-footer {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #ebeef5;
  font-size: 12px;
  color: #909399;
  display: flex;
  justify-content: space-between;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  background-color: #f5f7fa;
}

.action-item:hover {
  background-color: #e6f0ff;
  transform: translateY(-2px);
}

.action-icon {
  color: #409eff;
  margin-bottom: 8px;
}

.action-item span {
  font-size: 13px;
  color: #606266;
}

.system-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #ebeef5;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  color: #909399;
  font-size: 14px;
}

.info-value {
  color: #303133;
  font-size: 14px;
  font-weight: 500;
}

@media (max-width: 768px) {
  .quick-actions {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
