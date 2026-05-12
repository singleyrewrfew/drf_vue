<template>
    <div class="user-page">
        <TablePage
            ref="tableRef"
            title="用户管理"
            create-text="新建用户"
            :data="userList"
            :loading="loading"
            v-model:page="page"
            v-model:page-size="pageSize"
            :total="total"
            @create="openCreateDialog"
            @edit="openEditDialog"
            @delete="(row) => delOp.handleDelete(row.id, refreshData)"
        >
            <el-table-column prop="username" label="用户名"/>
            <el-table-column prop="email" label="邮箱"/>
            <el-table-column prop="role_name" label="角色" width="100">
                <template #default="{ row }">
                    <StatusTag :type="ROLE_TYPE_MAP[row.role_code] || 'info'" :text="row.role_name || '未分配'"/>
                </template>
            </el-table-column>
            <el-table-column prop="is_staff" label="后台权限" width="100">
                <template #default="{ row }">
                    <StatusTag :type="PERMISSION_OPTIONS[row.is_staff]?.type" :text="PERMISSION_OPTIONS[row.is_staff]?.label"/>
                </template>
            </el-table-column>
            <el-table-column prop="is_active" label="状态" width="100">
                <template #default="{ row }">
                    <StatusTag :type="ACTIVE_OPTIONS[row.is_active]?.type" :text="ACTIVE_OPTIONS[row.is_active]?.label"/>
                </template>
            </el-table-column>
            <el-table-column prop="created_at" label="注册时间" width="180"/>
        </TablePage>

        <UserFormDialog
            ref="userFormRef"
            v-model:dialog-visible="dialogVisible"
            :submit-loading="submitLoading"
            :is-edit="formSubmit.isEdit.value"
            :editing-id="formSubmit.editingId.value"
            :roles="roles"
            @submit="handleSubmit"
        />
    </div>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue'
import {useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'
import {getUsers, register, updateUser, deleteUser} from '@/api/user'
import {getRoles} from '@/api/role'
import {useUserStore} from '@/stores/user'
import {useCrudPage} from '@/composables/useCrudPage'
import TablePage from '@/components/TablePage.vue'
import StatusTag from '@/components/StatusTag.vue'
import UserFormDialog from './components/UserFormDialog.vue'
import {ROLE_TYPE_MAP, PERMISSION_OPTIONS, ACTIVE_OPTIONS} from '@/constants/contentConfig.js'

const router = useRouter()
const userStore = useUserStore()

const {
    data: userList,
    loading,
    page,
    pageSize,
    total,
    refreshData,
    formSubmit,
    dialogVisible,
    submitLoading,
    delOp,
    tableRef
} = useCrudPage(
    async (params) => {
        const {data} = await getUsers(params)
        return data
    },
    {
        deleteFn: async (id) => await deleteUser(id),
        deleteOptions: {message: '确定删除该用户？'},
        createFn: async (formData) => await register(formData),
        updateFn: async (id, formData) => await updateUser(id, formData),
        formOptions: {
            createMessage: '创建成功',
            updateMessage: '更新成功',
        },
        paginationOptions: {defaultPageSize: 10}
    }
)

const roles = ref([])
const userFormRef = ref(null)

const fetchRoles = async () => {
    try {
        const {data} = await getRoles()
        roles.value = data.results || data
    } catch (error) {
        console.error('获取角色列表失败:', error)
    }
}

const openCreateDialog = () => {
    userFormRef.value?.resetForm()
    formSubmit.openCreate()
}

const openEditDialog = (row) => {
    userFormRef.value?.fillForm(row)
    formSubmit.openEdit(row.id)
}

const handleSubmit = async (formData) => {
    if (formSubmit.isEdit.value) {
        const editData = {
            email: formData.email,
            role: formData.role,
            is_staff: formData.is_staff,
            is_active: formData.is_active,
        }

        await formSubmit.submit(editData, async () => {
            if (formSubmit.editingId.value === userStore.user?.id) {
                await userStore.fetchProfile()
                if (!userStore.canAccessBackend()) {
                    await userStore.logout()
                    ElMessage.error('您的后台访问权限已被移除')
                    await router.push({name: 'Login', query: {error: 'no_permission'}})
                    return false
                }
            }
            refreshData()
        })
    } else {
        const createData = {
            username: formData.username,
            password: formData.password,
            password_confirm: formData.password_confirm,
            email: formData.email,
            role: formData.role,
            is_staff: formData.is_staff,
            is_active: formData.is_active,
        }

        await formSubmit.submit(createData, refreshData)
    }
}

onMounted(() => {
    fetchRoles()
})
</script>

<style scoped>
.user-page {
    padding: 0;
}
</style>
