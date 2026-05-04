<template>
    <div class="category-page">
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
            title="分类管理"
            create-text="新建分类"
            :data="categoryList"
            :loading="loading"
            v-model:page="page"
            v-model:page-size="pageSize"
            :total="total"
            @create="openCreateDialog"
            @edit="openEditDialog"
            @delete="(row) => delOp.handleDelete(row.id, refreshData)"
        >
            <!-- 表格列定义：展示分类的各字段信息 -->
            <el-table-column prop="name" label="分类名称"/>
            <el-table-column prop="slug" label="URL别名"/>
            <el-table-column prop="parent_name" label="父分类"/>
            <el-table-column prop="sort_order" label="排序" width="80"/>
            <el-table-column prop="created_at" label="创建时间" width="180"/>
        </TablePage>

        <!--
            FormDialog: 通用表单弹窗组件
            - v-model 双向绑定表单数据对象
            - v-model:show 控制弹窗显示/隐藏（绑定 formSubmit.visible）
            - :rules Element Plus 表单验证规则
            - :loading 提交按钮的加载状态（防止重复提交）
            - @submit 用户点击确定时触发
        -->
        <FormDialog
            v-model="form"
            v-model:show="dialogVisible"
            create-title="新建分类"
            edit-title="编辑分类"
            width="500px"
            label-width="80px"
            :rules="rules"
            :loading="submitLoading"
            @submit="handleSubmit"
        >
            <!-- 分类名称：必填字段，用于显示和识别分类 -->
            <el-form-item label="名称" prop="name">
                <el-input v-model="form.name" placeholder="请输入分类名称"/>
            </el-form-item>
            <!-- URL别名：可选，用于生成 SEO 友好的 URL，留空则后端自动生成 -->
            <el-form-item label="别名" prop="slug">
                <el-input v-model="form.slug" placeholder="URL别名，留空自动生成"/>
            </el-form-item>
            <!-- 父分类：支持树形层级结构，clearable 允许清空选择 -->
            <el-form-item label="父分类">
                <el-select v-model="form.parent" placeholder="请选择父分类" clearable>
                    <!-- 过滤掉当前正在编辑的分类自身，避免形成自引用循环 -->
                    <el-option
                        v-for="cat in parentCategories"
                        :key="cat.id"
                        :label="cat.name"
                        :value="cat.id"
                    />
                </el-select>
            </el-form-item>
            <!-- 分类描述：辅助说明信息，非必填 -->
            <el-form-item label="描述">
                <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入描述"/>
            </el-form-item>
            <!-- 排序值：数值越小越靠前，默认为 0 -->
            <el-form-item label="排序">
                <el-input-number v-model="form.sort_order" :min="0"/>
            </el-form-item>
        </FormDialog>
    </div>
</template>

<script setup>
/**
 * @file 分类管理页面 (Category Index)
 * @description 管理文章分类的 CRUD 操作界面。
 *              本页面展示了如何使用 Composables（组合式函数）来消除重复代码，
 *              是所有 CRUD 页面的标准参考模板。
 *
 * 使用的技术：
 *   - usePagination: 处理分页逻辑（数据加载、页码切换、offset/limit 计算）
 *   - useFormSubmit: 处理表单提交（创建/编辑模式切换、提交状态、成功/失败提示）
 *   - useDelete: 处理删除操作（确认对话框、删除请求、结果提示）
 *
 * 页面功能：
 *   1. 展示分类列表（分页表格）
 *   2. 新建分类（弹窗表单）
 *   3. 编辑分类（复用新建表单，预填数据）
 *   4. 删除分类（二次确认后执行）
 *
 * @requires vue - Vue 3 核心库（reactive, computed, onMounted）
 * @requires @/api/category - 分类相关的 API 接口
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
 * - computed: 创建计算属性（用于派生数据，如过滤后的父分类列表）
 * - onMounted: 生命周期钩子（组件挂载后自动加载数据）
 */
import {reactive, computed, watch, ref, onMounted} from 'vue'

/**
 * 分类 API 接口
 * - getCategories: 获取分类列表（支持分页参数 limit/offset）
 * - createCategory: 创建新分类
 * - updateCategory: 更新指定分类
 * - deleteCategory: 删除指定分类
 */
import {getCategories, createCategory, updateCategory, deleteCategory} from '@/api/category'

/**
 * Composables（组合式函数）
 * 这些函数封装了可复用的业务逻辑，避免了在每个 CRUD 页面中重复编写相同代码。
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
 *  封装删除操作的完整流程：
 *   - 自动弹出 ElMessageBox.confirm 二次确认框
 *   - 管理 loading 防止重复点击
 *   - 统一处理成功/失败消息提示
 *   - 提供 handleDelete(id, onSuccessCallback) 方法
 */
import {usePagination} from '@/composables/usePagination'
import {useFormSubmit, useDelete} from '@/composables/useFormSubmit'

/**
 * 业务组件
 * TablePage: 封装了 el-table + 分页 + 工具栏（新建按钮）的复合组件
 * FormDialog: 封装了 el-dialog + el-form + footer 按钮（确定/取消）的复合组件
 */
import TablePage from '@/components/TablePage.vue'
import FormDialog from '@/components/FormDialog.vue'


// ============================================================================
// 【2】Composables 初始化（核心业务逻辑）
// ============================================================================

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
 * 调用方式：pagination.fetchData() 即可获取第一页数据
 * 切换页面时：先调用 handleCurrentChange/handleSizeChange 更新状态，再调 fetchData()
 *
 * @type {Object} usePagination 的返回值
 * @property {Ref<number>} page - 当前页码（从 1 开始）
 * @property {Ref<number>} pageSize - 每页条数（默认 10）
 * @property {Ref<number>} total - 总记录数
 * @property {Ref<boolean>} loading - 是否正在加载
 * @property {Ref<Array>} data - 当前页的数据列表（直接用于 :data 绑定）
 * @property {Function} fetchData(params?) - 发起请求获取数据，可传额外查询参数
 * @property {Function} handleCurrentChange(page) - 更新当前页码
 * @property {Function} handleSizeChange(size) - 更新每页条数并重置到第 1 页
 */
const pagination = usePagination(
    /**
     * 数据获取函数
     * usePagination 会在每次 fetchData 时调用此函数，
     * 自动传入 {limit, offset, ...extraParams} 参数。
     *
     * @param {Object} params - 分页参数（由 usePagination 自动组装）
     * @param {number} params.limit - 每页条数
     * @param {number} params.offset - 偏移量
     * @returns {Promise<Object>} DRF 格式的响应数据 { results: Array, count: number }
     */
    async (params) => {
        const {data} = await getCategories(params)
        return data
    },
    /**
     * 分页配置选项
     * @type {Object}
     * @property {number} defaultPageSize=10 - 默认每页显示 10 条记录
     */
    {defaultPageSize: 10}
)

// ============================================================================
// 【2.1】从 pagination 解构出顶层 Ref（模板自动解包必需）
// ============================================================================
//
// ⚠️ 关键知识点：Vue 3 模板中的 Ref 自动解包
//
// Vue 3 的模板编译器会对 <script setup> 中定义的顶层 Ref 进行自动解包，
// 即：模板中使用 ref 变量时不需要写 .value，Vue 会自动读取 .value。
//
// 但是！这种自动解包只对"顶层" Ref 生效。如果 Ref 嵌套在普通对象内部
// （例如 pagination.data、pagination.loading），模板不会自动解包，
// 传递给子组件的 props 会是整个 Ref 对象而非其内部的值。
//
// 这就是报错的根因：
//   ❌ :data="pagination.data"     → TablePage 收到的是 Ref<Array> 对象
//   ❌ :loading="pagination.loading" → TablePage 收到的是 Ref<Boolean> 对象
//   ✅ :data="categoryList"        → TablePage 直接收到了 Array 值
//
// 解决方法：用解构把 Ref 提取到 <script setup> 的顶层作用域。
// 注意：解构后的变量仍然保持响应式（因为解构的是 ref 本身，不是 .value）。
//
// 参考：https://vuejs.org/guide/essentials/reactivity-fundamentals.html#ref-unwrapping-in-templates

/** @type {Ref<Array>} 分类列表数据（由 usePagination 管理，模板中自动解包为 Array） */
const categoryList = pagination.data

/** @type {Ref<boolean>} 加载状态（true=正在请求数据） */
const loading = pagination.loading

/** @type {Ref<number>} 当前页码（从 1 开始） */
const page = pagination.page

/** @type {Ref<number>} 每页显示条数 */
const pageSize = pagination.pageSize

/** @type {Ref<number>} 总记录数 */
const total = pagination.total

/**
 * 刷新数据（封装了 fetchData 调用的快捷方法）
 * 用于删除/创建/编辑成功后重新获取当前页数据。
 *
 * @returns {Promise<void>}
 */
const refreshData = () => pagination.fetchData()

/**
 *
 * 通过 useFormSubmit 封装，自动处理以下内容：
 *   ✅ 对话框开关控制（visible）
 *   ✅ 创建/编辑模式切换（isEdit / editingId）
 *   ✅ 提交按钮防重复点击（loading）
 *   ✅ 成功/失败消息提示（ElMessage）
 *   ✅ 提交成功后自动关闭对话框
 *
 * 工作流程：
 *   1. 用户点"新建" → 调用 openCreateDialog() → 重置 form → formSubmit.openCreate()
 *   2. 用户点某行"编辑" → 调用 openEditDialog(row) → 填充 form → formSubmit.openEdit(id)
 *   3. 用户在弹窗点"确定" → 触发 @submit → handleSubmit() → formSubmit.submit(formData)
 *   4. formSubmit 内部根据 isEdit 决定调 createFn 还是 updateFn
 *
 * @type {Object} useFormSubmit 的返回值
 * @property {Ref<boolean>} isEdit - 当前是否为编辑模式
 * @property {Ref<number|null>} editingId - 正在编辑的分类 ID（创建时为 null）
 * @property {Ref<boolean>} loading - 提交按钮是否显示加载中
 * @property {Ref<boolean>} visible - 弹窗是否可见（双向绑定到 FormDialog）
 * @property {Function} openCreate() - 打开创建模式的弹窗
 * @property {Function} openEdit(id) - 打开编辑模式的弹窗
 * @property {Function} submit(formData, onSuccess?) - 执行提交（内部判断创建/更新）
 * @property {Function} close() - 关闭弹窗并重置状态
 */
const formSubmit = useFormSubmit(
    /**
     * 创建函数
     * 当 isEdit === false 时，formSubmit.submit() 会调用此函数。
     *
     * @param {Object} formData - 表单数据（经过 handleSubmit 预处理后的）
     * @param {string} formData.name - 分类名称
     * @param {string} [formData.slug] - URL 别名（可能被删除）
     * @param {number|string} [formData.parent] - 父分类 ID（可能被删除）
     * @param {string} [formData.description] - 描述
     * @param {number} [formData.sort_order=0] - 排序值
     * @returns {Promise<Object>} 后端返回的创建结果
     */
    async (formData) => await createCategory(formData),

    /**
     * 更新函数
     * 当 isEdit === true 时，formSubmit.submit() 会调用此函数。
     * 第一个参数 id 来自 formSubmit.editingId（openEdit 时设置）。
     *
     * @param {number|string} id - 要更新的分类 ID
     * @param {Object} formData - 表单数据（与 createFn 相同结构）
     * @returns {Promise<Object>} 后端返回的更新结果
     */
    async (id, formData) => await updateCategory(id, formData),

    {
        /** @type {string} 创建成功后 ElMessage 显示的文字 */
        createMessage: '创建成功',
        /** @type {string} 更新成功后 ElMessage 显示的文字 */
        updateMessage: '更新成功',
    }
)

// ============================================================================
// 【2.2】从 formSubmit 解构出顶层 Ref（模板自动解包必需）
// ============================================================================
//
// 与 pagination 同理，formSubmit 的属性（visible、loading）也是嵌套在对象内的
// Ref，模板中直接使用 formSubmit.visible / formSubmit.loading 不会自动解包。
//
// ❌ v-model:show="formSubmit.visible"   → FormDialog 收到 Ref<Boolean>，视为 truthy → 弹窗立即打开！
// ✅ v-model:show="dialogVisible"         → FormDialog 直接收到了 Boolean 值

/** @type {Ref<boolean>} 弹窗显示状态（双向绑定到 FormDialog 的 v-model:show） */
const dialogVisible = formSubmit.visible

/** @type {Ref<boolean>} 表单提交按钮的加载状态 */
const submitLoading = formSubmit.loading

/**
 * 删除操作管理实例
 *
 * 通过 useDelete 封装，自动处理以下内容：
 *   ✅ 弹出确认对话框（ElMessageBox.confirm）
 *   ✅ 用户取消时不执行任何操作
 *   ✅ 删除中的 loading 状态
 *   ✅ 成功/失败消息提示
 *
 * 在模板中的用法：
 *   @delete="(row) => delOp.handleDelete(row.id, () => pagination.fetchData())"
 *   解释：点击删除按钮时 → 调用 handleDelete(row.id, 回调)
 *         → 弹出确认框 → 用户确认 → 执行 deleteCategory(id)
 *         → 成功 → 显示提示 → 执行回调（刷新列表）
 *
 * @type {Object} useDelete 的返回值
 * @property {Ref<boolean>} loading - 删除操作是否进行中
 * @property {Function} handleDelete(id, onSuccess?) - 执行带确认的删除操作
 */
const delOp = useDelete(
    /**
     * 删除函数
     * handleDelete 内部会先弹出确认框，用户确认后才调用此函数。
     *
     * @param {number|string} id - 要删除的分类 ID
     * @returns {Promise<void>}
     */
    async (id) => await deleteCategory(id),

    {
        /** @type {string} 确认对话框中显示的提示文字 */
        message: '确定删除该分类？',
    }
)


// ============================================================================
// 【3】表单数据定义
// ============================================================================

/**
 * 分类表单数据对象（响应式）
 *
 * 使用 reactive 而非 ref，因为表单是一个包含多个字段的对象，
 * reactive 可以直接修改属性而无需 .value，更适合表单场景。
 *
 * 注意：这里使用 let 而非 const，是因为 Object.assign 需要
 * 直接修改 reactive 对象的属性。实际上 Vue 3 中 const 也可以，
 * 但 let 更符合语义（表示这个引用本身不变，只是内容变化）。
 *
 * @type {Object} 响应式表单数据
 * @property {string} name='' - 分类名称（必填）
 * @property {string} slug='' - URL 别名（选填，留空后端自动生成）
 * @property {string|number} parent='' - 父分类 ID（选填，空字符串表示无父级）
 * @property {string} description='' - 分类描述（选填）
 * @property {number} sort_order=0 - 排序值（越小越靠前，默认 0）
 */
let form = reactive({
    name: '',
    slug: '',
    parent: '',
    description: '',
    sort_order: 0,
})

/**
 * Element Plus 表单验证规则
 *
 * rules 对象的 key 必须对应 form 中需要验证的字段名（prop）。
 * 每个规则是一个数组，支持多条验证规则（按顺序执行）。
 *
 * @type {Object.<string, Array>}
 * @property {Array} name.name - 名称字段的验证规则
 * @property {boolean} name[0].required=true - 该字段为必填
 * @property {string} name[0].message='请输入分类名称' - 验证失败时的提示文字
 * @property {string} name[0].trigger='blur' - 触发验证的事件（blur=失去焦点时验证）
 */
const rules = {
    name: [{required: true, message: '请输入分类名称', trigger: 'blur'}],
}


// ============================================================================
// 【4】计算属性（派生数据）
// ============================================================================

/**
 * 可用的父分类列表（排除当前正在编辑的分类自身）
 *
 * 这是一个计算属性（computed），会自动追踪依赖并在依赖变化时重新计算：
 *   - 当 categoryList（分类列表）变化时自动更新
 *   - 当 formSubmit.editingId（当前编辑的 ID）变化时自动更新
 *
 * 为什么需要过滤？
 *   防止用户将某个分类的父分类设为它自己，形成自引用循环，
 *   这会导致后端报错或前端渲染异常（无限递归树形结构）。
 *
 * @returns {Array} 过滤后的父分类候选列表
 */
const parentCategories = computed(() => {
    return categoryList.value.filter((cat) => cat.id !== formSubmit.editingId.value)
})


// ============================================================================
// 【5】事件处理函数（连接模板与 Composables）
// ============================================================================

/**
 * 打开"新建分类"弹窗
 *
 * 执行步骤：
 *   1. 将 form 所有字段重置为初始值（清空上次填写的内容）
 *   2. 调用 formSubmit.openCreate() 设置模式为"创建"并显示弹窗
 *
 * @returns {void}
 *
 * @example
 * // 在模板中通过 @create="openCreateDialog" 触发
 * // 点击 TablePage 的"新建分类"按钮时会自动调用
 */
const openCreateDialog = () => {
    // 重置表单为空白状态
    Object.assign(form, {
        name: '',
        slug: '',
        parent: '',
        description: '',
        sort_order: 0,
    })
    // 通知 composable：打开弹窗，进入创建模式
    formSubmit.openCreate()
}

/**
 * 打开"编辑分类"弹窗
 *
 * 执行步骤：
 *   1. 从表格行数据（row）中提取各字段值，填充到 form
 *   2. 调用 formSubmit.openEdit(row.id) 设置模式为"编辑"并显示弹窗
 *
 * @param {Object} row - 表格中被点击的那一行数据（由 TablePage 的 @edit 事件传递）
 * @param {number} row.id - 分类的主键 ID
 * @param {string} row.name - 分类名称
 * @param {string} row.slug - URL 别名
 * @param {number|undefined} row.parent - 父分类 ID（无父级时为 undefined/null）
 * @param {string} row.description - 分类描述
 * @param {number} row.sort_order - 排序值
 * @returns {void}
 *
 * @example
 * // 在模板中通过 @edit="openEditDialog" 触发
 * // 点击表格行的"编辑"按钮时，TablePage 会传递整行数据
 */
const openEditDialog = (row) => {
    // 将行数据填充到表单（注意 parent 可能是 null/undefined，转为空字符串）
    Object.assign(form, {
        name: row.name,
        slug: row.slug,
        parent: row.parent || '',
        description: row.description,
        sort_order: row.sort_order,
    })
    // 通知 composable：打开弹窗，进入编辑模式，记住正在编辑的 ID
    formSubmit.openEdit(row.id)
}

/**
 * 处理表单提交（新建或更新）
 *
 * 这是 FormDialog @submit 事件的处理器。当用户在弹窗中点击"确定"按钮时触发。
 *
 * 执行流程：
 *   1. 复制一份数据（避免直接修改原始 reactive 对象）
 *   2. 清理空值字段（slug 和 parent 为空时删除，让后端使用默认行为）
 *   3. 调用 formSubmit.submit()，它会根据 isEdit 自动选择 create 或 update
 *   4. 提交成功后执行回调 → 刷新分类列表
 *
 * 为什么要在提交前清理空值？
 *   - slug 为空字符串时，应该不传这个字段（后端会自动从 name 生成）
 *   - parent 为空字符串时，应该不传（表示顶级分类，而不是传空字符串给后端）
 *   - 这是一种前后端协议约定，避免后端收到无效的空字符串值
 *
 * @async
 * @returns {Promise<void>}
 * @throws {Error} 如果提交失败（已由 formSubmit 内部 catch 并显示错误提示）
 *
 * @example
 * // 由 FormDialog 的 @submit="handleSubmit" 触发
 * // FormDialog 内部会先做表单验证，验证通过后才 emit submit 事件
 */
const handleSubmit = async () => {
    // 浅拷贝表单数据，避免影响原 form 对象
    const submitData = {...form}

    // 移除空的可选字段（后端约定：不传则使用默认行为）
    if (!submitData.slug) delete submitData.slug
    if (!submitData.parent) delete submitData.parent

    // 调用 composable 的 submit 方法
    // 它会自动：设置 loading → 根据 isEdit 调用 createFn/updateFn → 显示提示 → 关闭弹窗
    // 第二个参数是成功回调：刷新列表数据
    await formSubmit.submit(submitData, refreshData)
}



// ============================================================================
// 【6】分页变化监听（v-model 双向绑定联动数据刷新）
// ============================================================================

/**
 * TablePage 组件引用
 *
 * 用于在需要时访问 el-table 的底层方法，如：
 *   - clearSelection(): 清空所有选中行
 *   - toggleRowSelection(row, selected): 切换某行选中状态
 *   - sort(prop, order): 触发排序
 *
 * @type {Ref<ComponentPublicInstance|null>}
 */
const tableRef = ref(null)

/**
 * 监听页码变化 → 自动重新请求数据
 *
 * 当用户点击分页器切换页码时：
 *   1. TablePage 内部的 innerPage 更新
 *   2. emit('update:page', newPage) 通知父组件
 *   3. v-model:page="page" 同步更新本组件的 page Ref
 *   4. 此 watch 触发 → 调用 refreshData() 获取新页数据
 */
/**
 * 监听页码或每页条数变化 → 自动重新请求数据
 *
 * 使用 watch 合并监听 page 和 pageSize，避免：
 *   1. 切换 pageSize 时同时触发两个独立 watch → 双重 API 请求
 *   2. TablePage 内部在切换 pageSize 时会自动将页码重置为 1，
 *      此时 page 和 pageSize 同时变化，合并为一个回调只触发一次 fetchData
 *
 * 数据流：
 *   用户点击翻页/切换条数
 *     → TablePage 内部 innerPage/innerPageSize 更新
 *       → emit('update:page') / emit('update:pageSize')
 *         → 父组件 page/pageSize ref 更新
 *           → 此 watch 触发（同一 tick 内多次修改只触发一次）
 *             → refreshData() → fetchData() → 单次 API 请求 ✅
 */
watch([page, pageSize], () => {
    refreshData()
})


// ============================================================================
// 【7】生命周期
// ============================================================================

/**
 * 组件挂载完成后自动加载第一页数据
 *
 * onMounted 是 Vue 3 的生命周期钩子，在组件首次渲染到 DOM 后执行。
 * 这里用它来实现"页面打开即加载"的效果。
 *
 * 为什么不用 watch？
 *   因为我们只需要在挂载时加载一次，不需要监听路由参数等变化。
 *   如果后续需要支持"从搜索页返回保持状态"，可以改用 onActivated。
 */
onMounted(() => {
    refreshData()
})
</script>

<style scoped>
/**
 * 分类页面样式
 * padding: 0 确保 TablePage 组件占满整个容器空间，
 * 不产生额外的外边距或内边距。
 */
.category-page {
    padding: 0;
}
</style>
