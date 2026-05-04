<template>
    <div class="role-page">
        <!--
            TablePage: 通用表格页面组件
            - :delete-disabled 系统角色不可删除（内置删除按钮自动禁用）
            - v-model:page / v-model:page-size 双向绑定分页
        -->
        <TablePage
            ref="tableRef"
            title="角色管理"
            create-text="新建角色"
            :data="roleList"
            :loading="loading"
            v-model:page="page"
            v-model:page-size="pageSize"
            :total="total"
            :delete-disabled="isSystemRole"
            @create="openCreateDialog"
            @edit="openEditDialog"
            @delete="(row) => delOp.handleDelete(row.id, refreshData)"
        >
            <!-- 角色名称：用于显示和识别角色 -->
            <el-table-column prop="name" label="角色名称" width="150"/>
            <!-- 角色代码：系统内部标识，如 admin、editor、user -->
            <el-table-column prop="code" label="角色代码" width="150"/>
            <!-- 描述：说明该角色的职责范围 -->
            <el-table-column prop="description" label="描述" show-overflow-tooltip/>
            <!-- 权限数量：该角色关联的权限总数 -->
            <el-table-column label="权限数量" width="100">
                <template #default="{ row }">
                    <el-tag type="info">{{ row.permission_count || row.permissions?.length || 0 }}</el-tag>
                </template>
            </el-table-column>
            <!-- 系统标识：系统预置角色（不可删除） -->
            <el-table-column label="系统角色" width="100">
                <template #default="{ row }">
                    <el-tag v-if="row.is_system" type="warning">系统</el-tag>
                    <span v-else>-</span>
                </template>
            </el-table-column>
            <!-- 创建时间 -->
            <el-table-column prop="created_at" label="创建时间" width="180"/>
        </TablePage>

        <!--
            FormDialog: 通用表单弹窗组件
            - :is-edit 区分创建/编辑模式（控制代码字段是否可编辑）
        -->
        <FormDialog
            v-model="form"
            v-model:show="dialogVisible"
            :is-edit="formSubmit.isEdit.value"
            create-title="新建角色"
            edit-title="编辑角色"
            width="600px"
            label-width="100px"
            :rules="rules"
            :loading="submitLoading"
            @submit="handleSubmit"
        >
            <!-- 角色名称：必填，用于显示 -->
            <el-form-item label="角色名称" prop="name">
                <el-input v-model="form.name" placeholder="请输入角色名称" maxlength="50"/>
            </el-form-item>
            <!-- 角色代码：必填，创建后不可修改（作为唯一标识） -->
            <el-form-item label="角色代码" prop="code">
                <el-input v-model="form.code" placeholder="请输入角色代码（英文）" maxlength="50"
                          :disabled="formSubmit.isEdit.value"/>
            </el-form-item>
            <!-- 描述：可选，补充说明角色用途 -->
            <el-form-item label="描述" prop="description">
                <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入描述"/>
            </el-form-item>
            <!-- 权限选择：多选下拉，关联该角色的所有权限 -->
            <el-form-item label="权限" prop="permission_ids">
                <el-select v-model="form.permission_ids" multiple placeholder="请选择权限" style="width: 100%">
                    <el-option
                        v-for="perm in permissions"
                        :key="perm.id"
                        :label="perm.name"
                        :value="perm.id"
                    >
                        <span>{{ perm.name }}</span>
                        <span style="color: var(--text-tertiary); font-size: 12px; margin-left: 8px;">
                            {{ perm.code }}
                        </span>
                    </el-option>
                </el-select>
            </el-form-item>
        </FormDialog>
    </div>
</template>

<script setup>
/**
 * @file 角色管理页面 (Role Index)
 * @description 管理系统角色的 CRUD 操作界面。
 *              角色是 RBAC 模型中的中间层，将多个权限组合成一个角色，
 *              再将角色分配给用户。
 *
 * 页面功能：
 *   1. 展示角色列表（分页表格）
 *   2. 新建角色（弹窗表单，含权限多选）
 *   3. 编辑角色（需获取详情以回填已选权限列表）
 *   4. 删除角色（系统预置角色不可删除）
 *
 * 特殊逻辑：
 *   - 系统角色（is_system=true）禁止删除
 *   - 角色代码创建后不可修改
 *   - 编辑时需要先获取角色详情（包含完整的权限 ID 列表）
 *
 * 使用的技术：
 *   - usePagination: 处理分页逻辑
 *   - useFormSubmit: 处理表单提交
 *   - useDelete: 处理删除操作
 *
 * @requires vue - Vue 3 核心库（reactive, watch, onMounted, ref）
 * @requires element-plus - UI 组件库
 * @requires @/api/role - 角色和权限相关的 API 接口
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
 */
import {reactive, watch, onMounted, ref} from 'vue'

/**
 * API 接口
 * - getRoles: 获取角色列表（支持分页）
 * - getRole: 获取单个角色详情（含完整权限列表，编辑时用）
 * - createRole: 创建新角色
 * - updateRole: 更新指定角色
 * - deleteRole: 删除指定角色
 * - getPermissions: 获取所有权限（用于表单中的权限多选下拉）
 */
import {getRoles, getRole, createRole, updateRole, deleteRole, getPermissions} from '@/api/role'
import { normalizeListResponse } from '@/api/index.js'

/** Composables */
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
 * @type {Object}
 */
const pagination = usePagination(
    /**
     * 数据获取函数
     *
     * @param {Object} params - 分页参数 {limit, offset}
     * @returns {Promise<Object>} DRF 格式的响应数据
     */
    async (params) => {
        const {data} = await getRoles(params)
        return data
    },
    {defaultPageSize: 10}
)

// ============================================================================
// 【2.1】从 pagination 解构出顶层 Ref（模板自动解包必需）
// ============================================================================

/** @type {Ref<Array>} 角色列表数据 */
const roleList = pagination.data

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
 * @type {Object}
 */
const formSubmit = useFormSubmit(
    /** 创建新角色 */
    async (formData) => await createRole(formData),

    /** 更新已有角色 */
    async (id, formData) => await updateRole(id, formData),

    {
        createMessage: '创建成功',
        updateMessage: '更新成功',
    }
)

// ============================================================================
// 【2.2】从 formSubmit 解构出顶层 Ref
// ============================================================================

/** @type {Ref<boolean>} 弹窗显示状态 */
const dialogVisible = formSubmit.visible

/** @type {Ref<boolean>} 提交按钮加载状态 */
const submitLoading = formSubmit.loading

/**
 * 删除操作管理实例
 *
 * @type {Object}
 */
const delOp = useDelete(
    async (id) => await deleteRole(id),
    {message: '确定删除该角色？'}
)


// ============================================================================
// 【3】权限列表（辅助数据）
// ============================================================================

/**
 * 所有权限的列表（用于表单中权限多选下拉的数据源）
 * 在组件挂载时一次性加载，后续不变化。
 *
 * @type {Ref<Array>}
 */
const permissions = ref([])

/**
 * 获取权限列表
 *
 * @async
 * @returns {Promise<void>}
 */
const fetchPermissions = async () => {
    try {
        const {data} = await getPermissions()
        permissions.value = normalizeListResponse(data)
    } catch (error) {
        console.error('获取权限列表失败:', error)
    }
}


// ============================================================================
// 【4】表单数据定义
// ============================================================================

/**
 * 角色表单数据对象（响应式）
 *
 * @type {Object}
 * @property {string} name='' - 角色名称
 * @property {string} code='' - 角色代码（英文唯一标识，创建后不可改）
 * @property {string} description='' - 角色描述
 * @property {Array<number>} permission_ids=[] - 关联的权限 ID 数组
 */
let form = reactive({
    name: '',
    code: '',
    description: '',
    permission_ids: [],
})

/**
 * Element Plus 表单验证规则
 *
 * @type {Object.<string, Array>}
 */
const rules = {
    /** 角色名称：必填 */
    name: [{required: true, message: '请输入角色名称', trigger: 'blur'}],
    /** 角色代码：必填，创建后不可修改 */
    code: [{required: true, message: '请输入角色代码', trigger: 'blur'}],
}


// ============================================================================
// 【5】计算属性与判断函数
// ============================================================================

/**
 * 判断是否为系统预置角色
 *
 * 用途：系统角色（如 admin、editor）是初始化时创建的核心角色，
 *       不允许被删除，防止误操作导致系统功能异常。
 *
 * 此函数传递给 TablePage 的 :delete-disabled prop，
 *       当返回 true 时，该行对应的删除按钮会被禁用且隐藏。
 *
 * @param {Object} row - 表格行数据
 * @param {boolean} row.is_system - 是否为系统角色
 * @returns {boolean} 如果是系统角色则返回 true（禁用删除）
 */
const isSystemRole = (row) => !!row.is_system


// ============================================================================
// 【6】事件处理函数
// ============================================================================

/**
 * 打开"新建角色"弹窗
 *
 * 执行步骤：
 *   1. 重置表单为空白状态
 *   2. 调用 formSubmit.openCreate() 进入创建模式并显示弹窗
 *
 * @returns {void}
 */
const openCreateDialog = () => {
    Object.assign(form, {
        name: '', code: '', description: '', permission_ids: [],
    })
    formSubmit.openCreate()
}

/**
 * 打开"编辑角色"弹窗
 *
 * 与其他页面不同的是，编辑角色时需要额外调用 API 获取详情，
 * 因为列表数据可能不包含完整的权限 ID 列表（permissions 字段可能被精简）。
 *
 * 执行流程：
 *   1. 先调用 getRole API 获取完整的角色详情
 *   2. 将详情数据填充到表单（特别是 permission_ids）
 *   3. 进入编辑模式并打开弹窗
 *
 * @async
 * @param {Object} row - 表格中被点击的那一行数据
 * @param {number} row.id - 角色 ID
 * @returns {Promise<void>}
 */
const openEditDialog = async (row) => {
    try {
        // 获取完整角色详情（含所有关联的权限 ID）
        const {data} = await getRole(row.id)
        Object.assign(form, {
            name: data.name,
            code: data.code,
            description: data.description,
            // 从详情的 permissions 数组中提取 id 组成数组
            permission_ids: data.permissions?.map(p => p.id) || [],
        })
        formSubmit.openEdit(row.id)
    } catch (error) {
        ElMessage.error('获取角色详情失败')
    }
}

/**
 * 处理表单提交（新建或更新）
 *
 * @async
 * @returns {Promise<void>}
 */
const handleSubmit = async () => {
    const submitData = {...form}
    await formSubmit.submit(submitData, refreshData)
}


// ============================================================================
// 【7】分页变化监听与生命周期
// ============================================================================

/** TablePage 组件引用 */
const tableRef = ref(null)

/**
 * 监听页码或每页条数变化 → 自动重新请求数据
 */
watch([page, pageSize], () => {
    refreshData()
})

/**
 * 组件挂载后加载初始数据
 *
 * 同时加载两个独立数据源：
 *   1. 角色列表（分页数据）
 *   2. 权限列表（用于表单下拉选择，只需加载一次）
 */
onMounted(() => {
    refreshData()
    fetchPermissions()
})
</script>

<style scoped>
/**
 * 角色页面样式
 */
.role-page {
    padding: 0;
}
</style>
