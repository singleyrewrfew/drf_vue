<template>
  <div class="comments-page">
    <el-card>
      <template #header>
        <span>评论管理</span>
      </template>
      <el-table :data="commentList" v-loading="loading" stripe>
        <el-table-column prop="content" label="评论内容" min-width="200" show-overflow-tooltip />
        <el-table-column prop="article_title" label="文章" width="150" />
        <el-table-column prop="user_name" label="评论者" width="120" />
        <el-table-column prop="is_approved" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_approved ? 'success' : 'warning'">
              {{ row.is_approved ? '已审核' : '待审核' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button
              v-if="!row.is_approved"
              type="success"
              link
              @click="handleApprove(row)"
            >
              审核
            </el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
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
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/api'

const loading = ref(false)
const commentList = ref([])
const page = ref(1)
const total = ref(0)

const fetchComments = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/comments/', { params: { page: page.value, all: true } })
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
</style>
