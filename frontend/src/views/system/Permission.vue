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
        <el-table-column prop="name" label="权限名称" width="200"/>
        <el-table-column prop="code" label="权限代码" width="250">
            <template #default="{ row }">
                <el-tag type="info">{{ row.code }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" show-overflow-tooltip/>
        <el-table-column prop="created_at" label="创建时间" width="180"/>
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
            <el-input v-model="form.name" placeholder="请输入权限名称" maxlength="100"/>
        </el-form-item>
        <el-form-item label="权限代码" prop="code">
            <el-input v-model="form.code" placeholder="如: content.create, user.delete" maxlength="100"/>
        </el-form-item>
        <el-form-item label="描述" prop="description">
            <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入描述"/>
        </el-form-item>
    </FormDialog>
</template>

<script setup>
/**
 * 权限管理页面
 *
 * 提供权限的增删改查功能，包括权限列表展示、新建、编辑、删除操作。
 * 支持分页加载和表单验证。
 */
import {ref, reactive, computed, onMounted} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {getPermissions, createPermission, updatePermission, deletePermission} from '@/api/role'
import TablePage from '@/components/TablePage.vue'
import FormDialog from '@/components/FormDialog.vue'

/**
 * 加载状态控制
 */
const loading = ref(false)
const submitting = ref(false)
const deleting = ref(false)

/**
 * 权限列表数据
 */
const permissionList = ref([])

/**
 * 分页参数
 */
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

/**
 * 对话框状态
 */
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)

/**
 * 表单默认值模板
 */
const defaultForm = {
    name: '',
    code: '',
    description: '',
}

/**
 * 表单响应式数据
 */
let form = reactive({ ...defaultForm })

/**
 * 表单验证规则
 */
const rules = {
    name: [{required: true, message: '请输入权限名称', trigger: 'blur'}],
    code: [{required: true, message: '请输入权限代码', trigger: 'blur'}],
}

/**
 * 获取权限列表数据
 *
 * 根据当前页码和每页条数请求后端接口，支持多种数据格式兼容。
 */
const fetchPermissions = async () => {
    loading.value = true
    try {
        const offset = (page.value - 1) * pageSize.value
        const {data} = await getPermissions({
            limit: pageSize.value,
            offset: offset
        })

        // 兼容不同的后端响应格式
        if (Array.isArray(data)) {
            permissionList.value = data
            total.value = data.length
        } else if (data && Array.isArray(data.results)) {
            permissionList.value = data.results
            total.value = data.count || data.results.length
        } else {
            permissionList.value = []
            total.value = 0
            console.warn('Unexpected data format:', data)
        }
    } catch (error) {
        const errorMessage = error.response?.data?.message || '获取权限列表失败'
        ElMessage.error(errorMessage)
    } finally {
        loading.value = false
    }
}

/**
 * 重置表单数据到初始状态
 */
const resetForm = () => {
    Object.assign(form, defaultForm)
    editId.value = null
}

/**
 * 处理新建权限按钮点击
 *
 * 打开对话框并清空表单，设置为新建模式。
 */
const handleCreate = () => {
    isEdit.value = false
    resetForm()
    dialogVisible.value = true
}

/**
 * 处理编辑权限按钮点击
 *
 * 填充表单数据并打开对话框，设置为编辑模式。
 *
 * @param {Object} row - 当前行数据
 */
const handleEdit = (row) => {
    isEdit.value = true
    editId.value = row.id
    form.name = row.name
    form.code = row.code
    form.description = row.description
    dialogVisible.value = true
}

/**
 * 处理表单提交
 *
 * 根据是否为编辑模式调用相应的 API 接口，成功后刷新列表。
 */
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
        await fetchPermissions()
    } catch (error) {
        const errorMessage = error.response?.data?.message || (isEdit.value ? '更新失败' : '创建失败')
        ElMessage.error(errorMessage)
    } finally {
        submitting.value = false
    }
}

/**
 * 处理删除权限
 *
 * 显示确认对话框，用户确认后调用删除接口并刷新列表。
 *
 * @param {Object} row - 当前行数据
 */
const handleDelete = async (row) => {
    try {
        await ElMessageBox.confirm('确定删除该权限？删除后关联角色的权限也会被移除。', '提示', {
            type: 'warning',
            confirmButtonText: '确定',
            cancelButtonText: '取消'
        })

        deleting.value = true
        await deletePermission(row.id)
        ElMessage.success('删除成功')
        await fetchPermissions()
    } catch (error) {
        // 用户取消操作不显示错误消息
        if (error !== 'cancel') {
            const errorMessage = error.response?.data?.message || '删除失败'
            ElMessage.error(errorMessage)
        }
    } finally {
        deleting.value = false
    }
}

/**
 * 处理分页变化
 *
 * 更新页码和每页条数，重新加载数据。
 *
 * @param {Object} params - 分页参数 {page, pageSize}
 */
const handlePageChange = ({page: p, pageSize: ps}) => {
    page.value = p
    pageSize.value = ps
    fetchPermissions()
}

/**
 * 组件挂载时加载初始数据
 */
onMounted(() => {
    fetchPermissions()
})
</script>
