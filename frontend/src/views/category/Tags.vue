<template>
  <div class="tags-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>标签管理</span>
          <el-button type="primary" @click="handleAdd">新建标签</el-button>
        </div>
      </template>
      <el-table :data="tagList" v-loading="loading" stripe>
        <el-table-column prop="name" label="标签名称" />
        <el-table-column prop="slug" label="URL别名" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑标签' : '新建标签'" width="400px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入标签名称" />
        </el-form-item>
        <el-form-item label="别名">
          <el-input v-model="form.slug" placeholder="URL别名，留空自动生成" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getTags, createTag, updateTag, deleteTag } from '@/api/category'

const loading = ref(false)
const submitLoading = ref(false)
const tagList = ref([])
const dialogVisible = ref(false)
const editingId = ref(null)
const formRef = ref()

const form = reactive({
  name: '',
  slug: '',
})

const rules = {
  name: [{ required: true, message: '请输入标签名称', trigger: 'blur' }],
}

const isEdit = computed(() => !!editingId.value)

const fetchTags = async () => {
  loading.value = true
  try {
    const { data } = await getTags()
    tagList.value = data.results || data
  } catch (error) {
    ElMessage.error('获取标签列表失败')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  Object.assign(form, { name: '', slug: '' })
  editingId.value = null
}

const handleAdd = () => {
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row) => {
  editingId.value = row.id
  Object.assign(form, { name: row.name, slug: row.slug })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  await formRef.value.validate()
  submitLoading.value = true
  try {
    const submitData = { ...form }
    if (!submitData.slug) {
      delete submitData.slug
    }
    if (isEdit.value) {
      await updateTag(editingId.value, submitData)
      ElMessage.success('更新成功')
    } else {
      await createTag(submitData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchTags()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  } finally {
    submitLoading.value = false
  }
}

const handleDelete = async (row) => {
  await ElMessageBox.confirm('确定删除该标签？', '提示', { type: 'warning' })
  try {
    await deleteTag(row.id)
    ElMessage.success('删除成功')
    fetchTags()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  fetchTags()
})
</script>

<style scoped>
.tags-page {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
