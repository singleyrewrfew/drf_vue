<template>
    <TablePage
        title="角色管理"
        :data="roleList"
        :loading="loading"
        create-text="新建角色"
        :page="pagination.page"
        :page-size="pagination.page_size"
        :total="pagination.total"
        @create="handleCreate"
        @edit="handleEdit"
        @delete="handleDelete"
        @page-change="handlePageChange"
    >
        <el-table-column prop="name" label="角色名称" width="150"/>
        <el-table-column prop="code" label="角色代码" width="150"/>
        <el-table-column prop="description" label="描述" show-overflow-tooltip/>
        <el-table-column label="权限数量" width="100">
            <template #default="{ row }">
                <el-tag type="info">{{ row.permission_count || row.permissions?.length || 0 }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column label="系统角色" width="100">
            <template #default="{ row }">
                <el-tag v-if="row.is_system" type="warning">系统</el-tag>
                <span v-else>-</span>
            </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180"/>

        <template #actions="{ row }">
            <DeleteButton v-if="row.is_system" disabled/>
        </template>
    </TablePage>

    <FormDialog
        v-model="form"
        v-model:show="dialogVisible"
        :is-edit="isEdit"
        create-title="新建角色"
        edit-title="编辑角色"
        width="600px"
        label-width="100px"
        :rules="rules"
        :loading="submitting"
        @submit="handleSubmit"
    >
        <el-form-item label="角色名称" prop="name">
            <el-input v-model="form.name" placeholder="请输入角色名称" maxlength="50"/>
        </el-form-item>
        <el-form-item label="角色代码" prop="code">
            <el-input v-model="form.code" placeholder="请输入角色代码（英文）" maxlength="50" :disabled="isEdit"/>
        </el-form-item>
        <el-form-item label="描述" prop="description">
            <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入描述"/>
        </el-form-item>
        <el-form-item label="权限" prop="permission_ids">
            <el-select v-model="form.permission_ids" multiple placeholder="请选择权限" style="width: 100%">
                <el-option v-for="perm in permissions" :key="perm.id" :label="perm.name" :value="perm.id">
                    <span>{{ perm.name }}</span>
                    <span style="color: var(--text-tertiary); font-size: 12px; margin-left: 8px;">{{ perm.code }}</span>
                </el-option>
            </el-select>
        </el-form-item>
    </FormDialog>
</template>

<script setup>
import {ref, reactive, onMounted} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {getRoles, getRole, createRole, updateRole, deleteRole, getPermissions} from '@/api/role'
import TablePage from '@/components/TablePage.vue'
import FormDialog from '@/components/FormDialog.vue'

const loading = ref(false)
const submitting = ref(false)
const roleList = ref([])
const permissions = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)

const pagination = reactive({
    page: 1,
    page_size: 10,
    total: 0,
})

const form = reactive({
    name: '',
    code: '',
    description: '',
    permission_ids: [],
})

const rules = {
    name: [{required: true, message: '请输入角色名称', trigger: 'blur'}],
    code: [{required: true, message: '请输入角色代码', trigger: 'blur'}],
}

const fetchRoles = async () => {
    loading.value = true
    try {
        const offset = (pagination.page - 1) * pagination.page_size
        const {data} = await getRoles({
            limit: pagination.page_size,
            offset: offset
        })
        roleList.value = data.results || data
        pagination.total = data.count || 0
    } catch (error) {
        ElMessage.error('获取角色列表失败')
    } finally {
        loading.value = false
    }
}

const fetchPermissions = async () => {
    try {
        const {data} = await getPermissions()
        permissions.value = data.results || data
    } catch (error) {
        console.error('获取权限列表失败', error)
    }
}

const resetForm = () => {
    form.name = ''
    form.code = ''
    form.description = ''
    form.permission_ids = []
}

const handleCreate = () => {
    isEdit.value = false
    editId.value = null
    resetForm()
    dialogVisible.value = true
}

const handleEdit = async (row) => {
    isEdit.value = true
    editId.value = row.id
    try {
        const {data} = await getRole(row.id)
        form.name = data.name
        form.code = data.code
        form.description = data.description
        form.permission_ids = data.permissions?.map(p => p.id) || []
        dialogVisible.value = true
    } catch (error) {
        ElMessage.error('获取角色详情失败')
    }
}

const handleSubmit = async () => {
    submitting.value = true
    try {
        if (isEdit.value) {
            await updateRole(editId.value, form)
            ElMessage.success('更新成功')
        } else {
            await createRole(form)
            ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchRoles()
    } catch (error) {
        ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
    } finally {
        submitting.value = false
    }
}

const handleDelete = async (row) => {
    if (row.is_system) return
    await ElMessageBox.confirm('确定删除该角色？', '提示', {type: 'warning'})
    try {
        await deleteRole(row.id)
        ElMessage.success('删除成功')
        if (roleList.value.length === 1 && pagination.page > 1) {
            pagination.page--
        }
        fetchRoles()
    } catch (error) {
        ElMessage.error('删除失败')
    }
}

const handlePageChange = ({page, pageSize}) => {
    pagination.page = page
    pagination.page_size = pageSize
    fetchRoles()
}

onMounted(() => {
    fetchRoles()
    fetchPermissions()
})
</script>
