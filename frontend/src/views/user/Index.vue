<template>
  <div class="user-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button type="primary" @click="handleCreate">新建用户</el-button>
        </div>
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
        <el-table-column prop="is_staff" label="后台权限" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_staff ? 'success' : 'info'">
              {{ row.is_staff ? '允许' : '禁止' }}
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
            <el-button type="primary" link @click="handleEdit(row)" :disabled="isCurrentUser(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)" :disabled="isCurrentUser(row)">删除</el-button>
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

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑用户' : '新建用户'" width="500px" destroy-on-close>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" :disabled="isEdit" maxlength="150" />
        </el-form-item>
        <el-form-item v-if="!isEdit" label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password maxlength="128" />
        </el-form-item>
        <el-form-item v-if="!isEdit" label="确认密码" prop="password_confirm">
          <el-input v-model="form.password_confirm" type="password" placeholder="请确认密码" show-password maxlength="128" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" placeholder="请选择角色" :disabled="isEditingSelf" style="width: 100%">
            <el-option v-for="role in roles" :key="role.id" :label="role.name" :value="role.id" />
          </el-select>
          <div v-if="isEditingSelf" class="form-tip">不能修改自己的角色</div>
        </el-form-item>
        <el-form-item label="后台权限">
          <el-switch v-model="form.is_staff" active-text="允许" inactive-text="禁止" />
          <div class="form-tip">允许访问后台管理系统</div>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.is_active" active-text="启用" inactive-text="禁用" :disabled="isEditingSelf" />
          <div v-if="isEditingSelf" class="form-tip">不能禁用自己的账号</div>
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
import { getUsers, updateUser, deleteUser, register } from '@/api/user'
import { useUserStore } from '@/stores/user'
import api from '@/api'

const userStore = useUserStore()
const loading = ref(false)
const submitLoading = ref(false)
const userList = ref([])
const roles = ref([])
const page = ref(1)
const total = ref(0)
const dialogVisible = ref(false)
const editingId = ref(null)
const formRef = ref()

const isEdit = computed(() => !!editingId.value)

const form = reactive({
  username: '',
  password: '',
  password_confirm: '',
  email: '',
  role: null,
  is_staff: false,
  is_active: true,
})

const validatePassword = (rule, value, callback) => {
  if (!isEdit.value && !value) {
    callback(new Error('请输入密码'))
  } else if (value && value.length < 6) {
    callback(new Error('密码长度不能少于6位'))
  } else {
    callback()
  }
}

const validatePasswordConfirm = (rule, value, callback) => {
  if (!isEdit.value && !value) {
    callback(new Error('请确认密码'))
  } else if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 150, message: '用户名长度在 3 到 150 个字符', trigger: 'blur' },
  ],
  password: [{ validator: validatePassword, trigger: 'blur' }],
  password_confirm: [{ validator: validatePasswordConfirm, trigger: 'blur' }],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' },
  ],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }],
}

const isEditingSelf = computed(() => {
  return editingId.value === userStore.user?.id
})

const isCurrentUser = (row) => {
  return row.id === userStore.user?.id
}

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
    const { data } = await api.get('/roles/')
    roles.value = data.results || data
  } catch (error) {
    console.error(error)
  }
}

const resetForm = () => {
  form.username = ''
  form.password = ''
  form.password_confirm = ''
  form.email = ''
  form.role = null
  form.is_staff = false
  form.is_active = true
  editingId.value = null
}

const handleCreate = () => {
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row) => {
  editingId.value = row.id
  Object.assign(form, {
    username: row.username,
    password: '',
    password_confirm: '',
    email: row.email,
    role: row.role,
    is_staff: row.is_staff,
    is_active: row.is_active,
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  await formRef.value.validate()
  submitLoading.value = true
  try {
    if (isEdit.value) {
      await updateUser(editingId.value, {
        email: form.email,
        role: form.role,
        is_staff: form.is_staff,
        is_active: form.is_active,
      })
      ElMessage.success('更新成功')
      
      // 如果修改的是当前用户，强制刷新用户信息并可能跳转
      if (editingId.value === userStore.user?.id) {
        await userStore.fetchProfile()
        if (!userStore.canAccessBackend()) {
          // 如果当前用户失去了后台权限，清除登录状态并跳转
          userStore.logout()
          ElMessage.error('您的后台访问权限已被移除')
          router.push({ name: 'Login', query: { error: 'no_permission' } })
          return
        }
      }
    } else {
      await register({
        username: form.username,
        password: form.password,
        password_confirm: form.password_confirm,
        email: form.email,
        role: form.role,
        is_staff: form.is_staff,
        is_active: form.is_active,
      })
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchUsers()
  } catch (error) {
    const msg = error.response?.data?.error || error.response?.data?.username?.[0] || (isEdit.value ? '更新失败' : '创建失败')
    ElMessage.error(msg)
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}
</style>
