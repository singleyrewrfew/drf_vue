<template>
  <div class="content-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>内容管理</span>
          <CreateButton text="新建内容" @click="$router.push('/contents/create')" />
        </div>
      </template>
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="状态">
          <CustomSelect v-model="searchForm.status" :options="statusOptions" placeholder="全部" style="width: 120px" />
        </el-form-item>
        <el-form-item label="分类">
          <CustomSelect v-model="searchForm.category" :options="categories" label-key="name" value-key="id" placeholder="全部" style="width: 150px" />
        </el-form-item>
        <el-form-item label="搜索">
          <SearchInput v-model="searchForm.search" placeholder="标题搜索" @search="handleSearch" style="width: 220px" />
        </el-form-item>
        <el-form-item>
          <ResetButton @click="handleReset" />
          <SearchButton @click="handleSearch" style="margin-left: 12px" />
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
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <ViewButton
                v-if="row.status === 'published'"
                @click="handleView(row)"
              />
              <EditButton @click="handleEdit(row)" />
              <PublishButton
                v-if="row.status === 'draft'"
                @click="handlePublish(row)"
              />
              <DeleteButton @click="handleDelete(row)" />
            </div>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="fetchContents"
        @size-change="handleSizeChange"
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
import EditButton from '@/components/EditButton.vue'
import ViewButton from '@/components/ViewButton.vue'
import DeleteButton from '@/components/DeleteButton.vue'
import PublishButton from '@/components/PublishButton.vue'
import CreateButton from '@/components/CreateButton.vue'
import SearchButton from '@/components/SearchButton.vue'
import ResetButton from '@/components/ResetButton.vue'
import SearchInput from '@/components/SearchInput.vue'
import CustomSelect from '@/components/CustomSelect.vue'

const router = useRouter()
const loading = ref(false)
const contentList = ref([])
const categories = ref([])
const page = ref(1)
const pageSize = ref(20)
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

const statusOptions = [
  { label: '草稿', value: 'draft' },
  { label: '已发布', value: 'published' },
  { label: '已归档', value: 'archived' },
]

const fetchContents = async () => {
  loading.value = true
  try {
    const offset = (page.value - 1) * pageSize.value
    const params = {
      limit: pageSize.value,
      offset: offset
    }
    if (searchForm.status) params.status = searchForm.status
    if (searchForm.category) params.category = searchForm.category
    if (searchForm.search) params.search = searchForm.search.trim()
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

const handleReset = () => {
  searchForm.status = null
  searchForm.category = null
  searchForm.search = ''
  page.value = 1
  fetchContents()
}

const handleEdit = (row) => {
  router.push(`/contents/${row.id}/edit`)
}

const handleView = (row) => {
  window.open(`http://localhost:3000/article/${row.id}`, '_blank')
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

const handleSizeChange = () => {
  page.value = 1
  fetchContents()
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

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  align-items: center;
}
</style>

<style>
.content-select-popper {
  z-index: 9999 !important;
}
</style>
