<template>
  <div class="user-page">
    <el-card>
      <template #header>
        <span>用户管理</span>
      </template>
      <el-table :data="userList" v-loading="loading" stripe>
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="role_name" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="getRoleType(row.role_code)">
              {{ row.role_name || '未分配' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="注册时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
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
        @current-change="fetchUsers"
      />
    </el-card>

    <el-dialog v-model="dialogVisible" title="编辑用户" width="500px">
      <el-form ref="formRef" :model="form" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="form.username" disabled />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="form.role" placeholder="请选择角色">
            <el-option v-for="role in roles" :key="role.id" :label="role.name" :value="role.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.is_active" active-text="启用" inactive-text="禁用" />
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUsers, updateUser, deleteUser } from '@/api/user'
import api from '@/api'

const loading = ref(false)
const submitLoading = ref(false)
const userList = ref([])
const roles = ref([])
const page = ref(1)
const total = ref(0)
const dialogVisible = ref(false)
const editingId = ref(null)
const formRef = ref()

const form = reactive({
  username: '',
  email: '',
  role: null,
  is_active: true,
})

const getRoleType = (roleCode) => {
  const typeMap = {
    admin: 'danger',
    editor: 'warning',
    user: 'info',
  }
  return typeMap[roleCode] || 'info'
}

const fetchUsers = async () => {
  loading.value = true
  try {
    const { data } = await getUsers({ page: page.value })
    userList.value = data.results || data
    total.value = data.count || userList.value.length
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const fetchRoles = async () => {
  try {
    const { data } = await api.get('/roles/roles/')
    roles.value = data.results || data
  } catch (error) {
    console.error(error)
  }
}

const handleEdit = (row) => {
  editingId.value = row.id
  Object.assign(form, {
    username: row.username,
    email: row.email,
    role: row.role,
    is_active: row.is_active,
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  submitLoading.value = true
  try {
    await updateUser(editingId.value, form)
    ElMessage.success('更新成功')
    dialogVisible.value = false
    fetchUsers()
  } catch (error) {
    ElMessage.error('更新失败')
  } finally {
    submitLoading.value = false
  }
}

const handleDelete = async (row) => {
  await ElMessageBox.confirm('确定删除该用户？', '提示', { type: 'warning' })
  try {
    await deleteUser(row.id)
    ElMessage.success('删除成功')
    fetchUsers()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  fetchUsers()
  fetchRoles()
})
</script>

<style scoped>
.user-page {
  padding: 20px;
}
</style>
