<template>
  <div class="content-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>内容管理</span>
          <el-button type="primary" @click="$router.push('/contents/create')">新建内容</el-button>
        </div>
      </template>
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="全部" clearable popper-class="content-select-popper" style="width: 120px">
            <el-option label="草稿" value="draft" />
            <el-option label="已发布" value="published" />
            <el-option label="已归档" value="archived" />
          </el-select>
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="searchForm.category" placeholder="全部" clearable popper-class="content-select-popper" style="width: 150px">
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="搜索">
          <el-input v-model="searchForm.search" placeholder="标题搜索" clearable style="width: 200px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="contentList" v-loading="loading" stripe>
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
        <el-table-column prop="author_name" label="作者" width="120" />
        <el-table-column prop="category_name" label="分类" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusMap[row.status]?.type">
              {{ statusMap[row.status]?.label }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="view_count" label="浏览量" width="100" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button
              v-if="row.status === 'draft'"
              type="success"
              link
              @click="handlePublish(row)"
            >
              发布
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
        @current-change="fetchContents"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getContents, deleteContent, publishContent } from '@/api/content'
import api from '@/api'

const router = useRouter()
const loading = ref(false)
const contentList = ref([])
const categories = ref([])
const page = ref(1)
const total = ref(0)

const searchForm = reactive({
  status: null,
  category: null,
  search: '',
})

const statusMap = {
  draft: { label: '草稿', type: 'info' },
  published: { label: '已发布', type: 'success' },
  archived: { label: '已归档', type: 'warning' },
}

const fetchContents = async () => {
  loading.value = true
  try {
    const params = { page: page.value, ...searchForm }
    Object.keys(params).forEach((key) => {
      if (!params[key]) delete params[key]
    })
    const { data } = await getContents(params)
    contentList.value = data.results || data
    total.value = data.count || contentList.value.length
  } catch (error) {
    ElMessage.error('获取内容列表失败')
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const { data } = await api.get('/categories/')
    categories.value = data.results || data
    console.log('Categories loaded:', categories.value)
  } catch (error) {
    console.error(error)
  }
}

const handleSearch = () => {
  page.value = 1
  fetchContents()
}

const handleEdit = (row) => {
  router.push(`/contents/${row.id}/edit`)
}

const handlePublish = async (row) => {
  try {
    await publishContent(row.id)
    ElMessage.success('发布成功')
    fetchContents()
  } catch (error) {
    ElMessage.error('发布失败')
  }
}

const handleDelete = async (row) => {
  await ElMessageBox.confirm('确定删除该内容？', '提示', { type: 'warning' })
  try {
    await deleteContent(row.id)
    ElMessage.success('删除成功')
    fetchContents()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  fetchContents()
  fetchCategories()
})
</script>

<style scoped>
.content-page {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 16px;
}
</style>

<style>
.content-select-popper {
  z-index: 9999 !important;
}
</style>
