<template>
    <div class="user-page">
        <!--
            TablePage: 通用表格页面组件
            - 封装了表格、分页、操作按钮（新建/编辑/删除）的统一布局
            - :data 绑定分页后的数据列表（支持 Ref，自动 unref 解包）
            - :loading 控制表格加载动画（支持 Ref）
            - :page / :page-size 使用 v-model 双向绑定，内部变化时自动同步
            - @create/@edit/@delete 分别触发对应的 CRUD 操作回调
        -->
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
            <!-- 用户名：唯一标识用户的登录名 -->
            <el-table-column prop="username" label="用户名"/>
            <!-- 邮箱：用于找回密码和系统通知 -->
            <el-table-column prop="email" label="邮箱"/>
            <!-- 角色标签：根据角色类型显示不同颜色 -->
            <el-table-column prop="role_name" label="角色" width="100">
                <template #default="{ row }">
                    <StatusTag :type="getRoleType(row.role_code)" :text="row.role_name || '未分配'"/>
                </template>
            </el-table-column>
            <!-- 后台权限：是否允许访问后台管理系统 -->
            <el-table-column prop="is_staff" label="后台权限" width="100">
                <template #default="{ row }">
                    <StatusTag :type="row.is_staff ? 'success' : 'info'" :text="row.is_staff ? '允许' : '禁止'"/>
                </template>
            </el-table-column>
            <!-- 账号状态：正常或禁用（禁用后无法登录） -->
            <el-table-column prop="is_active" label="状态" width="100">
                <template #default="{ row }">
                    <StatusTag :type="row.is_active ? 'success' : 'danger'" :text="row.is_active ? '正常' : '禁用'"/>
                </template>
            </el-table-column>
            <!-- 注册时间：账号创建时间 -->
            <el-table-column prop="created_at" label="注册时间" width="180"/>
        </TablePage>

        <!--
            FormDialog: 通用表单弹窗组件
            - v-model 双向绑定表单数据对象
            - v-model:show 控制弹窗显示/隐藏（绑定 formSubmit.visible）
            - :is-edit 区分创建/编辑模式（控制密码字段显示）
            - :rules Element Plus 表单验证规则
            - :loading 提交按钮的加载状态（防止重复提交）
            - @submit 用户点击确定时触发
        -->
        <FormDialog
            v-model="form"
            v-model:show="dialogVisible"
            :is-edit="formSubmit.isEdit.value"
            create-title="新建用户"
            edit-title="编辑用户"
            width="600px"
            label-width="100px"
            :rules="rules"
            :loading="submitLoading"
            @submit="handleSubmit"
        >
            <!-- 用户名：创建时必填，编辑时不可修改（作为主标识） -->
            <el-form-item label="用户名" prop="username">
                <el-input v-model="form.username" placeholder="请输入用户名" :disabled="formSubmit.isEdit.value" maxlength="150"/>
            </el-form-item>
            <!-- 密码：仅在创建模式显示，编辑模式下不修改密码 -->
            <el-form-item v-if="!formSubmit.isEdit.value" label="密码" prop="password">
                <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password maxlength="128"/>
            </el-form-item>
            <!-- 确认密码：需与密码一致 -->
            <el-form-item v-if="!formSubmit.isEdit.value" label="确认密码" prop="password_confirm">
                <el-input v-model="form.password_confirm" type="password" placeholder="请确认密码" show-password maxlength="128"/>
            </el-form-item>
            <!-- 邮箱：用于通知和找回密码 -->
            <el-form-item label="邮箱" prop="email">
                <el-input v-model="form.email" placeholder="请输入邮箱"/>
            </el-form-item>
            <!-- 角色：决定用户在系统中的权限范围 -->
            <el-form-item label="角色" prop="role">
                <el-select v-model="form.role" placeholder="请选择角色" :disabled="isEditingSelf" style="width: 100%">
                    <el-option v-for="role in roles" :key="role.id" :label="role.name" :value="role.id"/>
                </el-select>
                <div v-if="isEditingSelf" class="form-tip">不能修改自己的角色</div>
            </el-form-item>
            <!-- 后台权限：是否允许访问后台管理系统 -->
            <el-form-item label="后台权限">
                <el-switch v-model="form.is_staff" active-text="允许" inactive-text="禁止"/>
                <div class="form-tip">允许访问后台管理系统</div>
            </el-form-item>
            <!-- 账号状态：禁用后该用户无法登录 -->
            <el-form-item label="状态">
                <el-switch v-model="form.is_active" active-text="启用" inactive-text="禁用" :disabled="isEditingSelf"/>
                <div v-if="isEditingSelf" class="form-tip">不能禁用自己的账号</div>
            </el-form-item>
        </FormDialog>
    </div>
</template>

<script setup>
/**
 * @file 用户管理页面 (User Index)
 * @description 管理系统用户的 CRUD 操作界面。
 *              本页面使用 Composables 消除重复代码，
 *              并包含特殊的业务逻辑：编辑自身时的权限保护。
 *
 * 使用的技术：
 *   - usePagination: 处理分页逻辑（数据加载、页码切换、offset/limit 计算）
 *   - useFormSubmit: 处理表单提交（创建/编辑模式切换、提交状态、成功/失败提示）
 *   - useDelete: 处理删除操作（确认对话框、删除请求、结果提示）
 *
 * 页面功能：
 *   1. 展示用户列表（分页表格，含角色标签和状态标签）
 *   2. 新建用户（弹窗表单，含密码确认）
 *   3. 编辑用户（复用表单，不可修改用户名和密码）
 *   4. 删除用户（二次确认后执行）
 *   5. 特殊逻辑：编辑自己时禁止修改角色和状态
 *
 * @requires vue - Vue 3 核心库（reactive, computed, watch, onMounted, ref）
 * @requires vue-router - Vue Router（编辑自身失去权限时跳转登录页）
 * @requires element-plus - UI 组件库（ElMessage 消息提示）
 * @requires @/api/user - 用户相关的 API 接口
 * @requires @/api/role - 角色相关的 API 接口
 * @requires @/stores/user - 用户状态管理（Pinia Store）
 * @requires @/composables/usePagination - 分页组合式函数
 * @requires @/composables/useFormSubmit - 表单提交和删除组合式函数
 * @requires @/components/TablePage.vue - 通用表格页面组件
 * @requires @/components/FormDialog.vue - 通用表单弹窗组件
 */

// ============================================================================
// 【1】依赖导入
// ============================================================================

/**
 * Vue 响应式 API + Vue Router
 * - reactive: 创建深层响应式对象（用于表单数据）
 * - computed: 创建计算属性（如 isEditingSelf 判断）
 * - watch: 监听响应式变化（分页切换时自动刷新数据）
 * - onMounted: 生命周期钩子（组件挂载后加载数据）
 * - ref: 创建响应式引用（TablePage 组件引用等）
 */
import {reactive, computed, watch, onMounted, ref} from 'vue'

/** Vue Router 实例（用于编辑自身失去权限后的页面跳转） */
import {useRouter} from 'vue-router'

/** Element Plus 消息提示组件 */
import {ElMessage} from 'element-plus'

/**
 * API 接口
 * - getUsers: 获取用户列表（支持分页参数 limit/offset）
 * - register: 创建新用户（注册接口）
 * - updateUser: 更新指定用户信息
 * - deleteUser: 删除指定用户
 * - getRoles: 获取角色列表（用于下拉选择）
 */
import {getUsers, register, updateUser, deleteUser} from '@/api/user'
import {getRoles} from '@/api/role'

/** Pinia 用户 Store（获取当前登录用户信息） */
import {useUserStore} from '@/stores/user'

/**
 * Composables（组合式函数）
 *
 * usePagination:
 *   封装分页相关的一切逻辑：
 *   - 自动计算 offset = (page - 1) * pageSize
 *   - 自动处理 DRF 返回格式 { results: [], count: N }
 *   - 提供 loading/page/pageSize/total/data 等响应式状态
 *   - 提供 fetchData() 方法发起请求
 *
 * useFormSubmit:
 *   封装创建/编辑表单的通用流程：
 *   - 管理 dialog 显示/隐藏（visible）
 *   - 区分创建和编辑模式（isEdit / editingId）
 *   - 管理 submit 按钮加载状态（loading）
 *   - 统一处理成功/失败消息提示
 *   - 提供 openCreate() / openEdit() / submit() 方法
 *
 * useDelete:
 *   封装删除操作的完整流程：
 *   - 自动弹出 ElMessageBox.confirm 二次确认框
 *   - 管理 loading 防止重复点击
 *   - 统一处理成功/失败消息提示
 *   - 提供 handleDelete(id, onSuccessCallback) 方法
 */
import {usePagination} from '@/composables/usePagination'
import {useFormSubmit, useDelete} from '@/composables/useFormSubmit'

/**
 * 业务组件
 * - TablePage: 封装了 el-table + 分页 + 工具栏（新建按钮）的复合组件
 * - FormDialog: 封装了 el-dialog + el-form + footer 按钮（确定/取消）的复合组件
 */
import TablePage from '@/components/TablePage.vue'
import FormDialog from '@/components/FormDialog.vue'
import StatusTag from '@/components/StatusTag.vue'


// ============================================================================
// 【2】Composables 初始化（核心业务逻辑）
// ============================================================================

/** Vue Router 实例 */
const router = useRouter()

/** 当前登录用户的 Pinia Store */
const userStore = useUserStore()

/**
 * 分页列表管理实例
 *
 * 通过 usePagination 封装，自动处理以下内容：
 *   ✅ offset 计算（无需手写 (page-1)*pageSize）
 *   ✅ DRF 响应格式兼容（无需手写 data.results || data）
 *   ✅ total 计数更新
 *   ✅ loading 加载状态
 *   ✅ 错误捕获
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
     * @param {Object} params - 分页参数（由 usePagination 自动组装）
     * @param {number} params.limit - 每页条数
     * @param {number} params.offset - 偏移量
     * @returns {Promise<Object>} DRF 格式的响应数据
     */
    async (params) => {
        const {data} = await getUsers(params)
        return data
    },
    {defaultPageSize: 10}
)

// ============================================================================
// 【2.1】从 pagination 解构出顶层 Ref（模板自动解包必需）
// ============================================================================

/** @type {Ref<Array>} 用户列表数据 */
const userList = pagination.data

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
 * 注意：由于用户提交有特殊的"编辑自身"逻辑（权限检查、可能跳转登录），
 * useFormSubmit 的标准流程会在 onSuccess 回调之前完成。
 * 这里通过自定义 onSuccess 回调来处理特殊场景。
 *
 * @type {Object} useFormSubmit 的返回值
 */
const formSubmit = useFormSubmit(
    /**
     * 创建函数 — 通过 register 接口创建新用户
     *
     * @param {Object} formData - 表单数据
     * @returns {Promise<Object>}
     */
    async (formData) => await register(formData),

    /**
     * 更新函数 — 更新用户信息（不含 username 和 password）
     *
     * @param {number|string} id - 要更新的用户 ID
     * @param {Object} formData - 表单数据（仅 email/role/is_staff/is_active）
     * @returns {Promise<Object>}
     */
    async (id, formData) => await updateUser(id, formData),

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
 * @type {Object} useDelete 的返回值
 */
const delOp = useDelete(
    async (id) => await deleteUser(id),
    {message: '确定删除该用户？'}
)


// ============================================================================
// 【3】角色列表与辅助数据
// ============================================================================

/**
 * 角色列表（用于表单中的角色下拉选择）
 * 在组件挂载时一次性获取，后续不变化。
 *
 * @type {Ref<Array>} 角色数组，每项包含 id/name/code 等字段
 */
const roles = ref([])

/**
 * 获取角色列表
 *
 * @async
 * @returns {Promise<void>}
 */
const fetchRoles = async () => {
    try {
        const {data} = await getRoles()
        roles.value = data.results || data
    } catch (error) {
        console.error('获取角色列表失败:', error)
    }
}


// ============================================================================
// 【4】表单数据定义与验证规则
// ============================================================================

/**
 * 用户表单数据对象（响应式）
 *
 * @type {Object}
 * @property {string} username='' - 用户名（必填，3-150字符）
 * @property {string} password='' - 密码（仅创建时填写，≥6位）
 * @property {string} password_confirm='' - 确认密码（需与密码一致）
 * @property {string} email='' - 邮箱地址
 * @property {number|null} role=null - 角色 ID
 * @property {boolean} is_staff=false - 是否允许后台访问
 * @property {boolean} is_active=true - 是否启用账号
 */
let form = reactive({
    username: '',
    password: '',
    password_confirm: '',
    email: '',
    role: null,
    is_staff: false,
    is_active: true,
})

/**
 * 密码自定义校验器
 *
 * 仅在创建模式（非编辑）下强制校验密码：
 *   - 创建时：密码为必填，且长度 ≥ 6
 *   - 编辑时：密码字段不显示，跳过校验
 *
 * @param {Object} rule - 规则对象（Element Plus 传入）
 * @param {string} value - 输入值
 * @param {Function} callback - 校验结果回调
 */
const validatePassword = (rule, value, callback) => {
    if (!formSubmit.isEdit.value && !value) {
        callback(new Error('请输入密码'))
    } else if (value && value.length < 6) {
        callback(new Error('密码长度不能少于6位'))
    } else {
        callback()
    }
}

/**
 * 确认密码自定义校验器
 *
 * 验证两次输入的密码必须一致。仅在创建模式下生效。
 *
 * @param {Object} rule - 规则对象
 * @param {string} value - 输入值
 * @param {Function} callback - 校验结果回调
 */
const validatePasswordConfirm = (rule, value, callback) => {
    if (!formSubmit.isEdit.value && !value) {
        callback(new Error('请确认密码'))
    } else if (value !== form.password) {
        callback(new Error('两次输入的密码不一致'))
    } else {
        callback()
    }
}

/**
 * Element Plus 表单验证规则
 *
 * @type {Object.<string, Array>}
 */
const rules = {
    /** 用户名：必填，长度 3-150 字符 */
    username: [
        {required: true, message: '请输入用户名', trigger: 'blur'},
        {min: 3, max: 150, message: '用户名长度在 3 到 150 个字符', trigger: 'blur'},
    ],
    /** 密码：自定义校验器（创建时必填且 ≥6 位） */
    password: [{validator: validatePassword, trigger: 'blur'}],
    /** 确认密码：需与密码一致 */
    password_confirm: [{validator: validatePasswordConfirm, trigger: 'blur'}],
    /** 邮箱：格式校验 */
    email: [
        {type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur'},
    ],
    /** 角色：必选 */
    role: [{required: true, message: '请选择角色', trigger: 'change'}],
}

// ============================================================================
// 【5】计算属性（派生数据）
// ============================================================================

/**
 * 判断当前正在编辑的用户是否是当前登录的管理员本人
 *
 * 用途：限制管理员不能修改自己的角色和账号状态，
 *       避免误操作导致自己无法登录或失去管理权限。
 *
 * @returns {boolean} 如果编辑的是当前用户则返回 true
 */
const isEditingSelf = computed(() => {
    return formSubmit.editingId.value === userStore.user?.id
})

/**
 * 根据角色代码获取对应的 Tag 类型颜色
 *
 * @param {string} roleCode - 角色代码（admin/editor/user 等）
 * @returns {string} Element Plus el-tag 的 type 属性值
 */
const getRoleType = (roleCode) => {
    const typeMap = {
        admin: 'danger',    // 管理员 → 红色
        editor: 'warning',  // 编辑者 → 黄色
        user: 'info',      // 普通用户 → 灰色
    }
    return typeMap[roleCode] || 'info'
}


// ============================================================================
// 【6】事件处理函数（连接模板与 Composables）
// ============================================================================

/**
 * 打开"新建用户"弹窗
 *
 * 执行步骤：
 *   1. 将 form 所有字段重置为初始值（清空上次填写的内容）
 *   2. 调用 formSubmit.openCreate() 设置模式为"创建"并显示弹窗
 *
 * @returns {void}
 */
const openCreateDialog = () => {
    Object.assign(form, {
        username: '', password: '', password_confirm: '',
        email: '', role: null, is_staff: false, is_active: true,
    })
    formSubmit.openCreate()
}

/**
 * 打开"编辑用户"弹窗
 *
 * 从行数据填充表单。注意：编辑时不回填密码字段，
 * 因为密码修改需要单独的流程（当前版本不支持编辑密码）。
 *
 * @param {Object} row - 表格中被点击的那一行数据
 * @param {number} row.id - 用户 ID
 * @param {string} row.username - 用户名
 * @param {string} row.email - 邮箱
 * @param {number} row.role - 角色 ID
 * @param {boolean} row.is_staff - 后台权限
 * @param {boolean} row.is_active - 账号状态
 * @returns {void}
 */
const openEditDialog = (row) => {
    Object.assign(form, {
        username: row.username,
        password: '',
        password_confirm: '',
        email: row.email,
        role: row.role,
        is_staff: row.is_staff,
        is_active: row.is_active,
    })
    formSubmit.openEdit(row.id)
}

/**
 * 处理表单提交（新建或更新）
 *
 * 这是 FormDialog @submit 事件的处理器。
 *
 * 特殊业务逻辑（编辑自身时）：
 *   如果管理员修改了自己的信息（特别是移除了后台权限），
 *   需要重新获取用户 Profile，检查是否还有后台访问权限。
 *   如果没有，则强制登出并跳转到登录页。
 *
 * 执行流程：
 *   1. 根据模式组装不同的提交数据
 *   2. 调用 formSubmit.submit()，传入自定义成功回调
 *   3. 成功回调中处理"编辑自身"的特殊逻辑
 *
 * @async
 * @returns {Promise<void>}
 */
const handleSubmit = async () => {
    if (formSubmit.isEdit.value) {
        // 编辑模式：只提交可变字段（不含 username/password）
        const editData = {
            email: form.email,
            role: form.role,
            is_staff: form.is_staff,
            is_active: form.is_active,
        }

        await formSubmit.submit(editData, async () => {
            // 特殊逻辑：如果修改的是当前登录用户
            if (formSubmit.editingId.value === userStore.user?.id) {
                // 重新获取最新的用户信息
                await userStore.fetchProfile()

                // 检查是否失去了后台访问权限
                if (!userStore.canAccessBackend()) {
                    // 强制登出并跳转登录页
                    await userStore.logout()
                    ElMessage.error('您的后台访问权限已被移除')
                    await router.push({name: 'Login', query: {error: 'no_permission'}})
                    return false  // 返回 false 表示不需要刷新列表（因为要跳转了）
                }
            }
            refreshData()  // 正常刷新列表
        })
    } else {
        // 创建模式：提交完整数据（含密码）
        const createData = {
            username: form.username,
            password: form.password,
            password_confirm: form.password_confirm,
            email: form.email,
            role: form.role,
            is_staff: form.is_staff,
            is_active: form.is_active,
        }

        await formSubmit.submit(createData, refreshData)
    }
}


// ============================================================================
// 【7】分页变化监听
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


// ============================================================================
// 【8】生命周期
// ============================================================================

/**
 * 组件挂载完成后加载初始数据
 *
 * 同时加载两个独立的数据源：
 *   1. 用户列表（分页数据）
 *   2. 角色列表（用于表单下拉选择，只需加载一次）
 */
onMounted(() => {
    refreshData()
    fetchRoles()
})
</script>

<style scoped>
/**
 * 用户页面样式
 * padding: 0 确保 TablePage 占满容器空间
 */
.user-page {
    padding: 0;
}

/**
 * 表单项下方的小提示文字
 * 用于说明字段的用途或操作限制
 */
.form-tip {
    font-size: 12px;
    color: var(--text-tertiary);
    margin-top: 4px;
    line-height: 1.5;
    padding-left: 4px;
    display: flex;
    align-items: center;
}
</style>
