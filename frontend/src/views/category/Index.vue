<template>
  <div class="category-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>分类管理</span>
          <el-button type="primary" @click="handleAdd">新建分类</el-button>
        </div>
      </template>
      <el-table :data="categoryList" v-loading="loading" stripe row-key="id">
        <el-table-column prop="name" label="分类名称" />
        <el-table-column prop="slug" label="URL别名" />
        <el-table-column prop="parent_name" label="父分类" />
        <el-table-column prop="sort_order" label="排序" width="80" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑分类' : '新建分类'" width="500px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="别名" prop="slug">
          <el-input v-model="form.slug" placeholder="URL别名，留空自动生成" />
        </el-form-item>
        <el-form-item label="父分类">
          <el-select v-model="form.parent" placeholder="请选择父分类" clearable>
            <el-option v-for="cat in parentCategories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sort_order" :min="0" />
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
import { getCategories, createCategory, updateCategory, deleteCategory } from '@/api/category'

const loading = ref(false)
const submitLoading = ref(false)
const categoryList = ref([])
const dialogVisible = ref(false)
const editingId = ref(null)
const formRef = ref()

const form = reactive({
  name: '',
  slug: '',
  parent: '',
  description: '',
  sort_order: 0,
})

const rules = {
  name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }],
}

const isEdit = computed(() => !!editingId.value)

const parentCategories = computed(() => {
  return categoryList.value.filter((cat) => cat.id !== editingId.value)
})

const fetchCategories = async () => {
  loading.value = true
  try {
    const { data } = await getCategories()
    categoryList.value = data.results || data
  } catch (error) {
    ElMessage.error('获取分类列表失败')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  Object.assign(form, {
    name: '',
    slug: '',
    parent: '',
    description: '',
    sort_order: 0,
  })
  editingId.value = null
}

const handleAdd = () => {
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row) => {
  editingId.value = row.id
  Object.assign(form, {
    name: row.name,
    slug: row.slug,
    parent: row.parent || '',
    description: row.description,
    sort_order: row.sort_order,
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  await formRef.value.validate()
  submitLoading.value = true
  try {
    if (isEdit.value) {
      await updateCategory(editingId.value, form)
      ElMessage.success('更新成功')
    } else {
      await createCategory(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchCategories()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  } finally {
    submitLoading.value = false
  }
}

const handleDelete = async (row) => {
  await ElMessageBox.confirm('确定删除该分类？', '提示', { type: 'warning' })
  try {
    await deleteCategory(row.id)
    ElMessage.success('删除成功')
    fetchCategories()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.category-page {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
