<template>
  <div class="dashboard">
    <!-- 管理员显示全部统计卡片 -->
    <template v-if="isAdmin">
      <el-row :gutter="20" class="stat-row">
        <el-col :xs="12" :sm="6">
          <StatCard :value="stats.contents" label="内容总数" type="primary">
            <template #icon><el-icon :size="28"><Document /></el-icon></template>
            <template #footer>已发布 {{ stats.published }} · 草稿 {{ stats.drafts }}</template>
          </StatCard>
        </el-col>
        <el-col :xs="12" :sm="6">
          <StatCard :value="stats.comments" label="评论总数" type="success">
            <template #icon><el-icon :size="28"><ChatDotRound /></el-icon></template>
            <template #footer>用户互动数据</template>
          </StatCard>
        </el-col>
        <el-col :xs="12" :sm="6">
          <StatCard :value="stats.users" label="用户总数" type="warning">
            <template #icon><el-icon :size="28"><User /></el-icon></template>
            <template #footer>注册用户</template>
          </StatCard>
        </el-col>
        <el-col :xs="12" :sm="6">
          <StatCard :value="formatNumber(stats.views)" label="总浏览量" type="danger">
            <template #icon><el-icon :size="28"><View /></el-icon></template>
            <template #footer>累计访问</template>
          </StatCard>
        </el-col>
      </el-row>
    </template>

    <!-- 非管理员只显示个人统计 -->
    <template v-else>
      <el-row :gutter="20" class="stat-row">
        <el-col :xs="12" :sm="8">
          <StatCard :value="stats.my_contents || 0" label="我的内容" type="primary">
            <template #icon><el-icon :size="28"><Document /></el-icon></template>
            <template #footer>已发布 {{ stats.my_published || 0 }} · 草稿 {{ stats.my_drafts || 0 }}</template>
          </StatCard>
        </el-col>
        <el-col :xs="12" :sm="8">
          <StatCard :value="formatNumber(stats.my_views || 0)" label="我的浏览量" type="success">
            <template #icon><el-icon :size="28"><View /></el-icon></template>
            <template #footer>累计访问</template>
          </StatCard>
        </el-col>
        <el-col :xs="12" :sm="8">
          <StatCard :value="stats.my_comments || 0" label="我的评论" type="warning">
            <template #icon><el-icon :size="28"><ChatDotRound /></el-icon></template>
            <template #footer>互动数据</template>
          </StatCard>
        </el-col>
      </el-row>
    </template>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :xs="24" :lg="16">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>{{ isAdmin ? '最新发布内容' : '我的最新发布' }}</span>
              <ViewAllButton :text="isAdmin ? '查看全部' : '查看我的'" @click="$router.push('/contents')" />
            </div>
          </template>
          <el-table :data="stats.recent_contents" v-loading="loading" stripe>
            <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
            <el-table-column prop="author_name" label="作者" width="120" v-if="isAdmin" />
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
            <QuickActionCard title="新建内容" type="primary" @click="$router.push('/contents/create')">
              <EditPen />
            </QuickActionCard>
            <QuickActionCard title="上传媒体" type="success" @click="$router.push('/media')">
              <Upload />
            </QuickActionCard>
            <QuickActionCard title="个人设置" type="warning" @click="$router.push('/profile')">
              <Setting />
            </QuickActionCard>
            <template v-if="isAdmin">
              <QuickActionCard title="分类管理" type="info" @click="$router.push('/categories')">
                <Folder />
              </QuickActionCard>
              <QuickActionCard title="标签管理" type="primary" @click="$router.push('/tags')">
                <PriceTag />
              </QuickActionCard>
              <QuickActionCard title="评论管理" type="success" @click="$router.push('/comments')">
                <ChatDotRound />
              </QuickActionCard>
            </template>
            <template v-else-if="isEditor">
              <QuickActionCard title="内容管理" type="info" @click="$router.push('/contents')">
                <Document />
              </QuickActionCard>
            </template>
          </div>
        </el-card>

        <el-card shadow="hover" style="margin-top: 20px" v-if="isAdmin">
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
import { ref, computed, onMounted } from 'vue'
import { Document, ChatDotRound, User, View, EditPen, Upload, Folder, PriceTag, Setting } from '@element-plus/icons-vue'
import api from '@/api'
import { useUserStore } from '@/stores/user'
import ViewAllButton from '@/components/ViewAllButton.vue'
import StatCard from '@/components/StatCard.vue'
import QuickActionCard from '@/components/QuickActionCard.vue'

const userStore = useUserStore()
const loading = ref(false)
const stats = ref({
  contents: 0,
  published: 0,
  drafts: 0,
  comments: 0,
  users: 0,
  media: 0,
  views: 0,
  my_contents: 0,
  my_published: 0,
  my_drafts: 0,
  my_comments: 0,
  my_views: 0,
  recent_contents: [],
})

const isAdmin = computed(() => userStore.isAdmin())
const isEditor = computed(() => userStore.isEditor())

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
    stats.value = {
      ...stats.value,
      ...data,
    }
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
  padding: 0;
}

.stat-row {
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.system-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid var(--border-light);
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  color: var(--text-secondary);
  font-size: 13px;
}

.info-value {
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 500;
}

@media (max-width: 768px) {
  .quick-actions {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
