<template>
  <div class="comments-page">
    <el-card>
      <template #header>
        <span>{{ isAdmin ? '评论管理' : '我的评论' }}</span>
      </template>
      <el-table :data="commentList" v-loading="loading" stripe>
        <el-table-column prop="content" label="评论内容" min-width="250" show-overflow-tooltip />
        <el-table-column prop="article_title" label="所属文章" width="180" show-overflow-tooltip />
        <el-table-column label="评论类型" width="100">
          <template #default="{ row }">
            <el-tag :type="row.parent ? 'info' : 'primary'" size="small">
              {{ row.parent ? '回复' : '主评论' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="user_name" label="评论者" width="120" v-if="!isAdmin" />
        <el-table-column label="回复对象" width="120">
          <template #default="{ row }">
            <span v-if="row.reply_to_name">@{{ row.reply_to_name }}</span>
            <span v-else style="color: #909399;">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="like_count" label="点赞数" width="90" align="center">
          <template #default="{ row }">
            <span>{{ row.like_count || 0 }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="is_approved" label="审核状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_approved ? 'success' : 'warning'">
              {{ row.is_approved ? '已审核' : '待审核' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="150" fixed="right" v-if="isAdmin">
          <template #default="{ row }">
            <div class="action-buttons">
              <ApproveButton
                v-if="!row.is_approved"
                @click="handleApprove(row)"
              />
              <DeleteButton @click="handleDelete(row)" />
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right" v-else>
          <template #default="{ row }">
            <div class="action-buttons">
              <DeleteButton @click="handleDelete(row)" />
            </div>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        v-model:current-page="page"
        :page-size="20"
        :total="total"
        layout="total, prev, pager, next"
        style="margin-top: 20px; justify-content: flex-end"
        @current-change="fetchComments"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/api'
import { useUserStore } from '@/stores/user'
import ApproveButton from '@/components/ApproveButton.vue'
import DeleteButton from '@/components/DeleteButton.vue'

const userStore = useUserStore()
const loading = ref(false)
const commentList = ref([])
const page = ref(1)
const total = ref(0)

const isAdmin = computed(() => userStore.user?.role_code === 'admin' || userStore.user?.is_superuser)

const fetchComments = async () => {
  loading.value = true
  try {
    const params = { page: page.value }
    // 非管理员只显示自己的评论
    if (!isAdmin.value) {
      params.my = true
    } else {
      params.all = true
    }
    const { data } = await api.get('/comments/', { params })
    commentList.value = data.results || data
    total.value = data.count || commentList.value.length
  } catch (error) {
    ElMessage.error('获取评论列表失败')
  } finally {
    loading.value = false
  }
}

const handleApprove = async (row) => {
  try {
    await api.post(`/comments/${row.id}/approve/`)
    ElMessage.success('审核通过')
    fetchComments()
  } catch (error) {
    ElMessage.error('审核失败')
  }
}

const handleDelete = async (row) => {
  await ElMessageBox.confirm('确定删除该评论？', '提示', { type: 'warning' })
  try {
    await api.delete(`/comments/${row.id}/`)
    ElMessage.success('删除成功')
    fetchComments()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  fetchComments()
})
</script>

<style scoped>
.comments-page {
  padding: 20px;
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  align-items: center;
}
</style>
