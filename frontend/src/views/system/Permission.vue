<template>
  <TablePage
    title="权限管理"
    :data="permissionList"
    :loading="loading"
    create-text="新建权限"
    :page="page"
    :page-size="pageSize"
    :total="total"
    @create="handleCreate"
    @edit="handleEdit"
    @delete="handleDelete"
    @page-change="handlePageChange"
  >
    <el-table-column prop="name" label="权限名称" width="200" />
    <el-table-column prop="code" label="权限代码" width="250">
      <template #default="{ row }">
        <el-tag type="info">{{ row.code }}</el-tag>
      </template>
    </el-table-column>
    <el-table-column prop="description" label="描述" show-overflow-tooltip />
    <el-table-column prop="created_at" label="创建时间" width="180" />
  </TablePage>

  <FormDialog
    v-model="form"
    v-model:show="dialogVisible"
    :is-edit="isEdit"
    create-title="新建权限"
    edit-title="编辑权限"
    width="500px"
    label-width="100px"
    :rules="rules"
    :loading="submitting"
    @submit="handleSubmit"
  >
    <el-form-item label="权限名称" prop="name">
      <el-input v-model="form.name" placeholder="请输入权限名称" maxlength="100" />
    </el-form-item>
    <el-form-item label="权限代码" prop="code">
      <el-input v-model="form.code" placeholder="如: content.create, user.delete" maxlength="100" />
    </el-form-item>
    <el-form-item label="描述" prop="description">
      <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入描述" />
    </el-form-item>
  </FormDialog>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getPermissions, createPermission, updatePermission, deletePermission } from '@/api/role'
import TablePage from '@/components/TablePage.vue'
import FormDialog from '@/components/FormDialog.vue'

const loading = ref(false)
const submitting = ref(false)
const permissionList = ref([])
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)

const form = reactive({
  name: '',
  code: '',
  description: '',
})

const rules = {
  name: [{ required: true, message: '请输入权限名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入权限代码', trigger: 'blur' }],
}

const fetchPermissions = async () => {
  loading.value = true
  try {
    const offset = (page.value - 1) * pageSize.value
    const { data } = await getPermissions({
      limit: pageSize.value,
      offset: offset
    })
    permissionList.value = data.results || data
    total.value = data.count || permissionList.value.length
  } catch (error) {
    ElMessage.error('获取权限列表失败')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  form.name = ''
  form.code = ''
  form.description = ''
  editId.value = null
}

const handleCreate = () => {
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  editId.value = row.id
  form.name = row.name
  form.code = row.code
  form.description = row.description
  dialogVisible.value = true
}

const handleSubmit = async () => {
  submitting.value = true
  try {
    if (isEdit.value) {
      await updatePermission(editId.value, form)
      ElMessage.success('更新成功')
    } else {
      await createPermission(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchPermissions()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (row) => {
  await ElMessageBox.confirm('确定删除该权限？删除后关联角色的权限也会被移除。', '提示', { type: 'warning' })
  try {
    await deletePermission(row.id)
    ElMessage.success('删除成功')
    fetchPermissions()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

const handlePageChange = ({ page: p, pageSize: ps }) => {
  page.value = p
  pageSize.value = ps
  fetchPermissions()
}

onMounted(() => {
  fetchPermissions()
})
</script>
