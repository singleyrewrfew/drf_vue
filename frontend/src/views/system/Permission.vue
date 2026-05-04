<template>
    <div class="permission-page">
        <!--
            TablePage: 通用表格页面组件
            - v-model:page / v-model:page-size 双向绑定分页
            - @create/@edit/@delete 分别触发对应的 CRUD 操作回调
        -->
        <TablePage
            ref="tableRef"
            title="权限管理"
            create-text="新建权限"
            :data="permissionList"
            :loading="loading"
            v-model:page="page"
            v-model:page-size="pageSize"
            :total="total"
            @create="openCreateDialog"
            @edit="openEditDialog"
            @delete="(row) => delOp.handleDelete(row.id, refreshData)"
        >
            <!-- 权限名称：用于显示和识别权限 -->
            <el-table-column prop="name" label="权限名称" width="200"/>
            <!-- 权限代码：系统内部标识，如 content.create、user.delete -->
            <el-table-column prop="code" label="权限代码" width="250">
                <template #default="{ row }">
                    <el-tag type="info">{{ row.code }}</el-tag>
                </template>
            </el-table-column>
            <!-- 描述：说明该权限的作用范围 -->
            <el-table-column prop="description" label="描述" show-overflow-tooltip/>
            <!-- 创建时间 -->
            <el-table-column prop="created_at" label="创建时间" width="180"/>
        </TablePage>

        <!--
            FormDialog: 通用表单弹窗组件
            - :is-edit 区分创建/编辑模式（控制表单标题）
        -->
        <FormDialog
            v-model="form"
            v-model:show="dialogVisible"
            :is-edit="formSubmit.isEdit.value"
            create-title="新建权限"
            edit-title="编辑权限"
            width="500px"
            label-width="100px"
            :rules="rules"
            :loading="submitLoading"
            @submit="handleSubmit"
        >
            <!-- 权限名称：必填，用于显示 -->
            <el-form-item label="权限名称" prop="name">
                <el-input v-model="form.name" placeholder="请输入权限名称" maxlength="100"/>
            </el-form-item>
            <!-- 权限代码：必填，用于后端权限校验，格式如 content.create -->
            <el-form-item label="权限代码" prop="code">
                <el-input v-model="form.code" placeholder="如: content.create, user.delete" maxlength="100"/>
            </el-form-item>
            <!-- 描述：可选，补充说明该权限的用途 -->
            <el-form-item label="描述" prop="description">
                <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入描述"/>
            </el-form-item>
        </FormDialog>
    </div>
</template>

<script setup>
/**
 * @file 权限管理页面 (Permission Index)
 * @description 管理系统权限的 CRUD 操作界面。
 *              权限是 RBAC（基于角色的访问控制）模型中的最小粒度单元，
 *              每个权限代表一个具体的操作能力。
 *
 * 页面功能：
 *   1. 展示权限列表（分页表格）
 *   2. 新建权限（弹窗表单）
 *   3. 编辑权限（复用新建表单，预填数据）
 *   4. 删除权限（二次确认后执行，同时移除关联角色的权限）
 *
 * 使用的技术：
 *   - usePagination: 处理分页逻辑
 *   - useFormSubmit: 处理表单提交（创建/编辑模式切换、提交状态）
 *   - useDelete: 处理删除操作（含自定义确认提示文字）
 *
 * @requires vue - Vue 3 核心库（reactive, watch, onMounted, ref）
 * @requires element-plus - UI 组件库
 * @requires @/api/role - 权限相关的 API 接口（与角色共用 API 模块）
 * @requires @/composables/usePagination - 分页组合式函数
 * @requires @/composables/useFormSubmit - 表单提交和删除组合式函数
 * @requires @/components/TablePage.vue - 通用表格页面组件
 * @requires @/components/FormDialog.vue - 通用表单弹窗组件
 */

// ============================================================================
// 【1】依赖导入
// ============================================================================

/**
 * Vue 响应式 API
 * - reactive: 创建深层响应式对象（用于表单数据）
 * - watch: 监听分页变化自动刷新数据
 * - onMounted: 生命周期钩子
 * - ref: 创建响应式引用
 */
import {reactive, watch, onMounted, ref} from 'vue'

/**
 * API 接口（权限管理相关接口定义在 role 模块中）
 * - getPermissions: 获取权限列表（支持分页参数 limit/offset）
 * - createPermission: 创建新权限
 * - updatePermission: 更新指定权限
 * - deletePermission: 删除指定权限（关联角色的权限也会被移除）
 */
import {getPermissions, createPermission, updatePermission, deletePermission} from '@/api/role'

/**
 * Composables
 *
 * usePagination: 封装分页逻辑（offset 计算、DRF 格式兼容、状态管理）
 * useFormSubmit: 封装创建/编辑表单流程（对话框控制、模式切换、提交状态、消息提示）
 * useDelete: 封含删除流程（确认框、请求、提示）
 */
import {usePagination} from '@/composables/usePagination'
import {useFormSubmit, useDelete} from '@/composables/useFormSubmit'

/** 业务组件 */
import TablePage from '@/components/TablePage.vue'
import FormDialog from '@/components/FormDialog.vue'


// ============================================================================
// 【2】Composables 初始化
// ============================================================================

/**
 * 分页列表管理实例
 *
 * @type {Object} usePagination 的返回值
 * @property {Ref<number>} page - 当前页码（从 1 开始）
 * @property {Ref<number>} pageSize - 每页条数（默认 10）
 * @property {Ref<number>} total - 总记录数
 * @property {Ref<boolean>} loading - 是否正在加载
 * @property {Ref<Array>} data - 当前页的数据列表
 * @property {Function} fetchData(params?) - 发起请求获取数据
 */
const pagination = usePagination(
    /**
     * 数据获取函数
     *
     * @param {Object} params - 分页参数 {limit, offset}
     * @returns {Promise<Object>} 响应数据（兼容 DRF 格式或数组格式）
     */
    async (params) => {
        const {data} = await getPermissions(params)
        return data
    },
    {defaultPageSize: 10}
)

// ============================================================================
// 【2.1】从 pagination 解构出顶层 Ref（模板自动解包必需）
// ============================================================================

/** @type {Ref<Array>} 权限列表数据 */
const permissionList = pagination.data

/** @type {Ref<boolean>} 加载状态 */
const loading = pagination.loading

/** @type {Ref<number>} 当前页码 */
const page = pagination.page

/** @type {Ref<number>} 每页显示条数 */
const pageSize = pagination.pageSize

/** @type {Ref<number>} 总记录数 */
const total = pagination.total

/**
 * 刷新数据的快捷方法
 * @returns {Promise<void>}
 */
const refreshData = () => pagination.fetchData()

/**
 * 表单提交管理实例
 *
 * @type {Object} useFormSubmit 的返回值
 */
const formSubmit = useFormSubmit(
    /** 创建新权限 */
    async (formData) => await createPermission(formData),

    /** 更新已有权限 */
    async (id, formData) => await updatePermission(id, formData),

    {
        createMessage: '创建成功',
        updateMessage: '更新成功',
    }
)

// ============================================================================
// 【2.2】从 formSubmit 解构出顶层 Ref（模板自动解包必需）
// ============================================================================

/** @type {Ref<boolean>} 弹窗显示状态 */
const dialogVisible = formSubmit.visible

/** @type {Ref<boolean>} 提交按钮加载状态 */
const submitLoading = formSubmit.loading

/**
 * 删除操作管理实例
 *
 * 注意：删除权限时会同步移除关联角色的对应权限，
 * 所以确认提示信息需要特别提醒用户这一副作用。
 *
 * @type {Object} useDelete 的返回值
 */
const delOp = useDelete(
    async (id) => await deletePermission(id),
    {
        message: '确定删除该权限？删除后关联角色的权限也会被移除。',
    }
)


// ============================================================================
// 【3】表单数据定义
// ============================================================================

/**
 * 表单默认值模板（用于重置表单时快速恢复初始状态）
 *
 * @type {Object}
 * @property {string} name='' - 权限名称
 * @property {string} code='' - 权限代码（如 content.create）
 * @property {string} description='' - 权限描述
 */
const defaultForm = {
    name: '',
    code: '',
    description: '',
}

/**
 * 权限表单数据对象（响应式）
 *
 * 使用 reactive 而非 ref，适合多字段对象直接修改属性的场景。
 *
 * @type {Object} 响应式表单数据（结构同 defaultForm）
 */
let form = reactive({...defaultForm})

/**
 * Element Plus 表单验证规则
 *
 * @type {Object.<string, Array>}
 */
const rules = {
    /** 权限名称：必填 */
    name: [{required: true, message: '请输入权限名称', trigger: 'blur'}],
    /** 权限代码：必填，用于后端权限校验 */
    code: [{required: true, message: '请输入权限代码', trigger: 'blur'}],
}


// ============================================================================
// 【4】事件处理函数
// ============================================================================

/**
 * 打开"新建权限"弹窗
 *
 * 执行步骤：
 *   1. 重置表单为默认值
 *   2. 调用 formSubmit.openCreate() 进入创建模式并显示弹窗
 *
 * @returns {void}
 */
const openCreateDialog = () => {
    Object.assign(form, {...defaultForm})
    formSubmit.openCreate()
}

/**
 * 打开"编辑权限"弹窗
 *
 * 从行数据填充表单字段。
 *
 * @param {Object} row - 表格中被点击的那一行数据
 * @param {number} row.id - 权限 ID
 * @param {string} row.name - 权限名称
 * @param {string} row.code - 权限代码
 * @param {string} row.description - 权限描述
 * @returns {void}
 */
const openEditDialog = (row) => {
    Object.assign(form, {
        name: row.name,
        code: row.code,
        description: row.description,
    })
    formSubmit.openEdit(row.id)
}

/**
 * 处理表单提交（新建或更新）
 *
 * 这是 FormDialog @submit 事件的处理器。
 *
 * @async
 * @returns {Promise<void>}
 */
const handleSubmit = async () => {
    // 浅拷贝表单数据
    const submitData = {...form}
    await formSubmit.submit(submitData, refreshData)
}


// ============================================================================
// 【5】分页变化监听与生命周期
// ============================================================================

/** TablePage 组件引用 */
const tableRef = ref(null)

/**
 * 监听页码或每页条数变化 → 自动重新请求数据
 *
 * 合并监听避免切换 pageSize 时产生双重 API 请求。
 */
watch([page, pageSize], () => {
    refreshData()
})

/**
 * 组件挂载后加载第一页权限数据
 */
onMounted(() => {
    refreshData()
})
</script>

<style scoped>
/**
 * 权限页面样式
 */
.permission-page {
    padding: 0;
}
</style>
