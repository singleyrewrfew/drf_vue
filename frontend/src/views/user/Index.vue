<template>
    <div class="user-page">
        <!-- 用户列表表格组件 -->
        <TablePage
            title="用户管理"
            create-text="新建用户"
            :data="userList"
            :loading="loading"
            :page="pagination.page"
            :page-size="pagination.page_size"
            :total="pagination.total"
            @create="handleCreate"
            @edit="handleEdit"
            @delete="handleDelete"
            @page-change="handlePageChange"
        >
            <el-table-column prop="username" label="用户名"/>
            <el-table-column prop="email" label="邮箱"/>
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
            <el-table-column prop="created_at" label="注册时间" width="180"/>
        </TablePage>
        <!-- 用户表单弹窗组件 -->
        <FormDialog
            v-model="form"
            v-model:show="dialogVisible"
            :is-edit="isEdit"
            create-title="新建用户"
            edit-title="编辑用户"
            width="600px"
            label-width="100px"
            :rules="rules"
            :loading="submitLoading"
            @submit="handleSubmit"
        >
            <el-form-item label="用户名" prop="username">
                <el-input v-model="form.username" placeholder="请输入用户名" :disabled="isEditing" maxlength="150"/>
            </el-form-item>
            <el-form-item v-if="!isEditing" label="密码" prop="password">
                <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password
                          maxlength="128"/>
            </el-form-item>
            <el-form-item v-if="!isEditing" label="确认密码" prop="password_confirm">
                <el-input v-model="form.password_confirm" type="password" placeholder="请确认密码" show-password
                          maxlength="128"/>
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
                <el-input v-model="form.email" placeholder="请输入邮箱"/>
            </el-form-item>
            <el-form-item label="角色" prop="role">
                <el-select v-model="form.role" placeholder="请选择角色" :disabled="isEditingSelf"
                           style="width: 100%">
                    <el-option v-for="role in roles" :key="role.id" :label="role.name" :value="role.id"/>
                </el-select>
                <div v-if="isEditingSelf" class="form-tip">不能修改自己的角色</div>
            </el-form-item>
            <el-form-item label="后台权限">
                <el-switch v-model="form.is_staff" active-text="允许" inactive-text="禁止"/>
                <div class="form-tip">允许访问后台管理系统</div>
            </el-form-item>
            <el-form-item label="状态">
                <el-switch v-model="form.is_active" active-text="启用" inactive-text="禁用"
                           :disabled="isEditingSelf"/>
                <div v-if="isEditingSelf" class="form-tip">不能禁用自己的账号</div>
            </el-form-item>
        </FormDialog>
    </div>
</template>

<script setup>
import {ref, reactive, computed, onMounted} from 'vue'
import {useRouter} from 'vue-router'
import {ElMessage, ElMessageBox} from 'element-plus'
import {getUsers, updateUser, deleteUser, register} from '@/api/user'
import {useUserStore} from '@/stores/user'
import TablePage from "@/components/TablePage.vue";
import FormDialog from "@/components/FormDialog.vue";
import {getRoles} from "@/api/role";

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const submitLoading = ref(false)
const userList = ref([])
const roles = ref([])
const dialogVisible = ref(false)
const editingId = ref(null)

const pagination = reactive({
    page: 1,
    page_size: 10,
    total: 0,
})

const isEditing = computed(() => !!editingId.value)
const isEdit = ref(false)

let form = reactive({
    username: '',
    password: '',
    password_confirm: '',
    email: '',
    role: null,
    is_staff: false,
    is_active: true,
})

const validatePassword = (rule, value, callback) => {
    if (!isEditing.value && !value) {
        callback(new Error('请输入密码'))
    } else if (value && value.length < 6) {
        callback(new Error('密码长度不能少于6位'))
    } else {
        callback()
    }
}

const validatePasswordConfirm = (rule, value, callback) => {
    if (!isEditing.value && !value) {
        callback(new Error('请确认密码'))
    } else if (value !== form.password) {
        callback(new Error('两次输入的密码不一致'))
    } else {
        callback()
    }
}

const rules = {
    username: [
        {required: true, message: '请输入用户名', trigger: 'blur'},
        {min: 3, max: 150, message: '用户名长度在 3 到 150 个字符', trigger: 'blur'},
    ],
    password: [{validator: validatePassword, trigger: 'blur'}],
    password_confirm: [{validator: validatePasswordConfirm, trigger: 'blur'}],
    email: [
        {type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur'},
    ],
    role: [{required: true, message: '请选择角色', trigger: 'change'}],
}

const isEditingSelf = computed(() => {
    return editingId.value === userStore.user?.id
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
        const offset = (pagination.page - 1) * pagination.page_size
        const {data} = await getUsers({
            limit: pagination.page_size,
            offset: offset
        })
        userList.value = data.results || data
        pagination.total = data.count || 0
    } catch (error) {
        ElMessage.error('获取用户列表失败')
    } finally {
        loading.value = false
    }
}

const fetchRoles = async () => {
    try {
        const {data} = await getRoles()
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
    submitLoading.value = true
    try {
        if (isEditing.value) {
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
                    await userStore.logout()
                    ElMessage.error('您的后台访问权限已被移除')
                    await router.push({name: 'Login', query: {error: 'no_permission'}})
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
        await fetchUsers()
    } catch (error) {
        const msg = error.response?.data?.error || error.response?.data?.username?.[0] || (isEditing.value ? '更新失败' : '创建失败')
        ElMessage.error(msg)
    } finally {
        submitLoading.value = false
    }
}

const handleDelete = async (row) => {
    await ElMessageBox.confirm('确定删除该用户？', '提示', {type: 'warning'})
    try {
        await deleteUser(row.id)
        ElMessage.success('删除成功')
        await fetchUsers()
    } catch (error) {
        ElMessage.error('删除失败')
    }
}

const handlePageChange = ({page, pageSize}) => {
    pagination.page = page
    pagination.page_size = pageSize
    fetchUsers()
    fetchRoles()
}

onMounted(() => {
    fetchUsers()
    fetchRoles()
})
</script>

<style scoped>
.user-page {
    padding: 0;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.form-tip {
    font-size: 12px;
    color: var(--text-tertiary);
    margin-top: 4px;
    line-height: 1.5;
    padding-left: 4px;
    display: flex;
    align-items: center;
}

.action-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    align-items: center;
}
</style>
