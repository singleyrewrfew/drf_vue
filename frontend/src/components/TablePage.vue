<template>
    <div class="table-page">
        <el-card>
            <!-- 卡片头部：支持自定义插槽或默认标题+新建按钮 -->
            <template v-if="$slots.header" #header>
                <slot name="header" />
            </template>
            <template v-else #header>
                <div class="card-header">
                    <span class="title">{{ title }}</span>
                    <ActionButton
                        v-if="showCreate"
                        :text="createText"
                        icon="plus"
                        size="normal"
                        spin-icon
                        @click="$emit('create')"
                    />
                </div>
            </template>

            <!-- 批量操作栏（多选列开启时默认显示） -->
            <div v-if="showBatchActions" class="batch-actions-bar">
                <span class="batch-info">已选 {{ selectedRows.length }} 项</span>
                <div class="batch-buttons">
                    <slot name="batch-actions" :rows="selectedRows">
                        <ActionButton
                            type="danger"
                            text="批量删除"
                            icon="delete"
                            :disabled="selectedRows.length === 0"
                            @click="handleBatchAction"
                        />
                    </slot>
                </div>
                <button class="batch-clear" @click="clearSelection">取消选择</button>
            </div>

            <!-- 表格区域 -->
            <el-table
                ref="tableRef"
                :data="tableData"
                :row-key="resolvedRowKey"
                v-loading="tableLoading"
                v-bind="$attrs"
                element-loading-text="加载中..."
                :element-loading-background="loadingBg"
                @selection-change="handleSelectionChange"
            >
                <!-- 多选列（可选，默认显示） -->
                <el-table-column
                    v-if="showSelection"
                    type="selection"
                    width="50"
                    :selectable="props.selectable"
                    reserve-selection
                />

                <!-- 默认插槽：由父组件定义表格列 -->
                <slot />

                <!-- 操作列（可选显示） -->
                <el-table-column
                    v-if="showActions"
                    label="操作"
                    :width="actionsWidth"
                    fixed="right"
                    class-name="action-column"
                >
                    <template #default="{ row }">
                        <div class="actions">
                            <!-- 内置编辑按钮 -->
                            <ActionButton
                                v-if="showEdit && !editDisabled(row)"
                                icon="edit"
                                text="编辑"
                                @click="$emit('edit', row)"
                            />
                            <!-- 自定义操作按钮插槽（在删除按钮之前） -->
                            <slot name="row-actions" :row="row" />
                            <!-- 内置删除按钮（放最后） -->
                            <ActionButton
                                v-if="showDelete && !deleteDisabled(row)"
                                type="danger"
                                icon="delete"
                                text="删除"
                                @click="$emit('delete', row)"
                            />
                        </div>
                    </template>
                </el-table-column>

                <!-- 空状态提示 -->
                <template #empty>
                    <slot name="empty">
                        <el-empty description="暂无数据" />
                    </slot>
                </template>
            </el-table>

            <!-- 分页器（可选显示） -->
            <div v-if="showPagination && resolvedTotal > 0" class="pagination-wrapper">
                <el-pagination
                    v-model:current-page="innerPage"
                    v-model:page-size="innerPageSize"
                    :page-sizes="pageSizes"
                    :total="resolvedTotal"
                    layout="total, sizes, prev, pager, next, jumper"
                />
            </div>
        </el-card>
    </div>
</template>

<script setup>
/**
 * @file TablePage.vue - 通用表格分页组件
 *
 * @description 高频使用的 CRUD 页面核心组件。封装了 Element Plus 的 el-table + 分页 + 工具栏，
 *              提供统一的表格页面布局。设计原则：简单、可复用、可扩展。
 *
 * 核心特性：
 *   - Ref 兼容：所有 props 都支持传入 Vue Ref 对象（composable 返回值可直接绑定）
 *   - 灵活的操作列：内置编辑/删除按钮 + 可通过 slot 自定义额外操作
 *   - 多选支持：可选的多选列，支持行级禁用选择、跨页保留选中状态
 *   - 自动空状态：无数据时自动展示空状态提示
 *   - 主题自适应：暗色/亮色模式下的 loading 遮罩自动适配
 *   - 完整的事件透传：create/edit/delete/selection-change 覆盖完整 CRUD 流程
 *
 * 使用示例（配合 composables）：
 * ```vue
 * <TablePage
 *     title="分类管理"
 *     :data="categoryList"        // usePagination.data 解构后的顶层 Ref
 *     :loading="loading"           // 同上
 *     :page="page"
 *     :page-size="pageSize"
 *     :total="total"
 *     @create="openCreateDialog"
 *     @edit="openEditDialog"
 *     @delete="(row) => delOp.handleDelete(row.id, refresh)"
 *     @page-change="handlePageChange"
 * >
 *     <el-table-column prop="name" label="名称" />
 *     <el-table-column prop="slug" label="别名" />
 * </TablePage>
 * ```
 *
 * @requires vue - Vue 3 响应式 API
 * @requires @/components/CreateButton.vue - 新建按钮组件
 * @requires @/components/EditButton.vue - 编辑按钮组件
 * @requires @/components/DeleteButton.vue - 删除按钮组件
 * @requires @/stores/theme.ts - 主题状态管理
 */

import { ref, computed, watch, unref } from 'vue'
import ActionButton from '@/components/ActionButton.vue'
import { useThemeStore } from '@/stores/theme.ts'


// ============================================================================
// 【1】Props 定义
// ============================================================================

/**
 * 组件属性（全部支持 Ref 传入）
 */
const props = defineProps({
    // ---- 基础信息 ----

    /** 卡片标题文字（showCreate=false 且未使用 header 插槽时显示） */
    title: {
        type: String,
        default: '数据列表',
    },

    /** 是否显示新建按钮 */
    showCreate: {
        type: Boolean,
        default: true,
    },

    /** 新建按钮的文字 */
    createText: {
        type: String,
        default: '新建',
    },

    // ---- 表格数据 ----

    /**
     * 表格数据源
     * 支持 Array 或 Ref<Array>（composable 返回的 data 可直接传入）
     * @type {Array | import('vue').Ref<Array>}
     */
    data: {
        type: [Array, Object],
        default: () => [],
    },

    /**
     * 加载状态
     * 支持 Boolean 或 Ref<Boolean>（composable 返回的 loading 可直接传入）
     * @type {Boolean | import('vue').Ref<Boolean>}
     */
    loading: {
        type: [Boolean, Object],
        default: false,
    },

    // ---- 多选功能 ----

    /** 是否显示多选列（默认开启） */
    showSelection: {
        type: Boolean,
        default: true,
    },

    /**
     * 行数据的唯一标识字段名（多选开启时必须）
     *
     * Element Plus 的 reserve-selection 功能依赖此属性来跨页保留选中状态
     * 默认值 'id' 适用于大多数后端返回的数据结构
     * 如果数据的主键不是 'id'，请传入对应的字段名（如 'uuid'、'code' 等）
     *
     * @type {string | Function}
     * @example
     * <!-- 默认使用 id 字段 -->
     * <TablePage :data="list" />
     *
     * <!-- 自定义主键字段 -->
     * <TablePage :data="list" row-key="uuid" />
     */
    rowKey: {
        type: [String, Function],
        default: 'id',
    },

    /**
     * 行级选择禁用判断函数（仅 showSelection=true 时生效）
     *
     * @param {Object} row - 当前行数据
     * @param {number} index - 当前行索引
     * @returns {boolean} 返回 false 则该行不可勾选
     *
     * @example
     * // 禁用"已发布"状态的行被选中
     * :selectable="(row) => row.status !== 'published'"
     */
    selectable: {
        type: Function,
        default: undefined,
    },

    // ---- 操作列控制 ----

    /** 是否显示操作列 */
    showActions: {
        type: Boolean,
        default: true,
    },

    /** 操作列宽度（px 或 auto） */
    actionsWidth: {
        type: [String, Number],
        default: 150,
    },

    /** 是否显示编辑按钮 */
    showEdit: {
        type: Boolean,
        default: true,
    },

    /** 是否显示删除按钮 */
    showDelete: {
        type: Boolean,
        default: true,
    },

    /**
     * 编辑按钮禁用判断函数
     * @param {Object} row - 当前行数据
     * @returns {boolean} 是否禁用该行的编辑按钮
     */
    editDisabled: {
        type: Function,
        default: () => false,
    },

    /**
     * 删除按钮禁用判断函数
     * @param {Object} row - 当前行数据
     * @returns {boolean} 是否禁用该行的删除按钮
     */
    deleteDisabled: {
        type: Function,
        default: () => false,
    },

    // ---- 分页器配置 ----

    /** 是否显示分页器 */
    showPagination: {
        type: Boolean,
        default: true,
    },

    /**
     * 当前页码（支持 v-model 双向绑定）
     * 支持 Number 或 Ref<number>
     */
    page: {
        type: [Number, Object],
        default: 1,
    },

    /**
     * 每页条数（支持 v-model 双向绑定）
     * 支持 Number 或 Ref<number>
     */
    pageSize: {
        type: [Number, Object],
        default: 10,
    },

    /** 分页器每页条数选项列表 */
    pageSizes: {
        type: Array,
        default: () => [10, 20, 50, 100],
    },

    /**
     * 数据总条数（支持 Number 或 Ref<number>）
     */
    total: {
        type: [Number, Object],
        default: 0,
    },
})


// ============================================================================
// 【2】Emits 定义
// ============================================================================

/**
 * 组件事件列表
 *
 * | 事件名 | 参数 | 说明 |
 * |--------|------|------|
 * | create | 无 | 点击新建按钮 |
 * | edit | row (Object) | 点击某行的编辑按钮 |
 * | delete | row (Object) | 点击某行的删除按钮 |
 * | batch-delete | rows (Array) | 批量删除（选中 ≥ 2 行时触发） |
 * | update:page | page (number) | 页码变化（v-model 支持） |
 * | update:pageSize | size (number) | 每页条数变化（v-model 支持） |
 * | selection-change | rows (Array) | 多选选中行变化（showSelection=true 时） |
 */
const emit = defineEmits(['create', 'edit', 'delete', 'batch-delete', 'update:page', 'update:pageSize', 'selection-change'])


// ============================================================================
// 【3】内部状态与计算属性（Ref 兼容层）
// ============================================================================

/**
 * ⭐ 关键设计：unref() 实现 Ref 兼容
 *
 * 问题背景：
 *   当使用 composables 时，返回值是 Ref 对象（如 pagination.data = Ref<Array>）。
 *   如果直接将 Ref 赋值给 props，Vue 的 prop 类型校验会报错：
 *     "Expected Array, got Object"
 *
 * 解决方案：
 *   props 类型声明为 [Array, Object]（同时接受数组或对象），
 *   内部使用 unref() 提取实际值。
 *   这样既兼容普通值也兼容 Ref。
 *
 *   unref(x) 等价于：x 是 Ref ? x.value : x
 */

/** @type {import('vue').ComputedRef<Array>} 经过 unref 处理的实际表格数据 */
const tableData = computed(() => unref(props.data))

/** @type {import('vue').ComputedRef<boolean>} 经过 unref 处理的实际加载状态 */
const tableLoading = computed(() => unref(props.loading))

/**
 * 解析后的 row-key 值
 * 支持字符串（字段名）或函数（取值函数），直接透传给 el-table 的 row-key prop
 *
 * @type {import('vue').ComputedRef<string | Function>}
 */
const resolvedRowKey = computed(() => props.rowKey)

/** @type {import('vue').ComputedRef<number>} 经过 unref 处理的实际总条数 */
const resolvedTotal = computed(() => unref(props.total))


// ============================================================================
// 【4】分页器内部状态管理
// ============================================================================

/** 表格 DOM 引用（暴露给父组件） */
const tableRef = ref(null)

/** 内部页码状态（用于 el-pagination 的 v-model 双向绑定） */
const innerPage = ref(unref(props.page))

/** 内部每页条数状态 */
const innerPageSize = ref(unref(props.pageSize))

/**
 * 监听外部 page 变化 → 同步到内部状态
 * 场景：父组件切换搜索条件后重置页码
 */
watch(
    () => unref(props.page),
    (val) => {
        if (val !== innerPage.value) {
            innerPage.value = val ?? 1
        }
    }
)

/**
 * 监听外部 pageSize 变化 → 同步到内部状态
 */
watch(
    () => unref(props.pageSize),
    (val) => {
        if (val !== innerPageSize.value) {
            innerPageSize.value = val ?? 10
        }
    }
)

/**
 * 页码变化时的统一处理（使用 post 刷新，避免同步循环触发）
 *
 * 通知父组件更新 page 值（用于 v-model 双向绑定）
 * 使用 flush: 'post' 确保在所有同步修改完成后再触发，
 * 避免在切换 pageSize 重置页码时产生重复 emit。
 */
watch(innerPage, (val) => {
    emit('update:page', val)
}, { flush: 'post' })

/**
 * 每页条数变化时的统一处理
 *
 * 注意：切换 pageSize 时自动跳回第 1 页（避免当前页超出范围）
 * 页码重置由 innerPage 的 watch 负责通知父组件，此处只设置值即可
 */
watch(innerPageSize, (val) => {
    emit('update:pageSize', val)
    // 切换每页条数时，重置页码为 1
    if (innerPage.value !== 1) {
        innerPage.value = 1  // 会触发上面的 innerPage watch（post 模式下异步执行）
    }
})


// ============================================================================
// 【5】主题相关
// ============================================================================

/** 主题 store 实例 */
const themeStore = useThemeStore()

/**
 * 加载遮罩背景色（根据当前主题动态计算）
 * @type {import('vue').ComputedRef<string>}
 */
const loadingBg = computed(() =>
    themeStore.theme === 'light' ? 'rgba(136,135,135,0.8)' : 'rgba(53,48,48,0.8)'
)


// ============================================================================
// 【6】多选功能
// ============================================================================

/**
 * 处理选中行变化事件
 *
 * 当用户勾选/取消勾选某行时，el-table 会触发 selection-change 事件。
 * 本函数将其透传给父组件，方便父组件获取当前选中的行数据。
 *
 * @param {Array} rows - 当前所有被选中的行数据
 */
const handleSelectionChange = (rows) => {
    selectedRows.value = rows
    emit('selection-change', rows)
}

/** 当前选中的行数据（内部状态） */
const selectedRows = ref([])

/** 是否显示批量操作栏：多选列开启时默认显示 */
const showBatchActions = computed(() => props.showSelection)

/** 批量操作按钮点击处理（暂无接口，alert 提示） */
const handleBatchAction = () => {
    const rows = selectedRows.value
    const ids = rows.map(r => r.id || r.name || '[未知]')
    alert(`批量操作（${rows.length} 项）：\n${ids.join('\n')}\n\n批量删除接口待实现`)
    emit('batch-delete', rows)
}

/**
 * 清空所有选中状态（通过 ref 调用 el-table 原生方法）
 *
 * @example
 * // 父组件中使用
 * // const tableRef = ref(null)
 * // tableRef.value.clearSelection()
 */
const clearSelection = () => {
    tableRef.value?.clearSelection()
}

/**
 * 切换某一行的选中状态
 *
 * @param {Object} row - 目标行数据
 * @param {boolean} [selected=true] - true=选中，false=取消选中
 */
const toggleRowSelection = (row, selected = true) => {
    tableRef.value?.toggleRowSelection(row, selected)
}

/** 切换全选 / 全不选 */
const toggleAllSelection = () => {
    tableRef.value?.toggleAllSelection()
}

/** 获取当前所有选中的行 */
const getSelectionRows = () => {
    return tableRef.value?.getSelectionRows() || []
}


// ============================================================================
// 【7】暴露给模板的方法（无需定义，直接使用 props 函数即可）
// ============================================================================

// 旧版代码中 isEditDisabled / isDeleteDisabled 是冗余包装：
//   const isEditDisabled = (row) => props.editDisabled(row)  ← 多了一层间接调用
//
// 直接在模板中使用 props.editDisabled(row) 即可，更清晰。


// ============================================================================
// 【8】Expose（暴露给父组件的公共方法）
// ============================================================================

/**
 * 暴露给父组件的公共方法和引用
 *
 * 使用方式（通过 ref 访问）：
 * ```js
 * const tableRef = ref(null)
 *
 * // 多选相关
 * tableRef.value.clearSelection()           // 清空选中
 * tableRef.value.toggleRowSelection(row)    // 切换单行
 * tableRef.value.toggleAllSelection()       // 切换全选
 * tableRef.value.getSelectionRows()        // 获取选中行
 *
 * // 表格底层实例
 * tableRef.value.tableRef                  // el-table 原生引用
 * ```
 */
defineExpose({
    /** el-table 实例引用 */
    tableRef,

    // ---- 多选操作方法 ----
    /** 清空所有选中状态 */
    clearSelection,
    /** 切换某行选中状态 */
    toggleRowSelection,
    /** 切换全选/全不选 */
    toggleAllSelection,
    /** 获取当前选中的行列表 */
    getSelectionRows,
    /** 当前选中的行数据（Ref，可直接访问 .value） */
    selectedRows,
})
</script>


<style scoped>
/* ============================================================
 * TablePage 组件样式
 * 设计原则：
 *   - 最小化样式侵入（不强制子元素布局）
 *   - 主题自适应（亮色/暗色模式）
 *   - 响应式友好（操作按钮自动换行）
 * ============================================================ */

.table-page {
    padding: 0;
}

/* ---- 卡片头部：标题左对齐，操作按钮右对齐 ---- */
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-header .title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

/* ---- 分页器居中显示 ---- */
.pagination-wrapper {
    display: flex;
    justify-content: center;
    margin-top: 16px;
}

/* ---- 操作列按钮组：水平排列，超出自动换行 ---- */
.actions {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    align-items: center;
    justify-content: center;
}

/* ---- 批量操作栏（多选列开启时默认显示） ---- */
.batch-actions-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 16px;
  margin-top: 0;
  margin-bottom: 12px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-xs);
  font-size: 13px;
}

.batch-actions-bar .batch-info {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--text-primary);
  font-weight: 500;
  white-space: nowrap;
  line-height: 1.4;
}

/* 已选数字高亮 */
.batch-actions-bar .batch-info::before {
    content: '';
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--primary-color, #409eff);
    flex-shrink: 0;
}

.batch-actions-bar .batch-buttons {
    display: flex;
    gap: 4px;
    flex: 1;
}

.batch-actions-bar .batch-clear {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 14px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-xs);
  background: var(--card-bg);
  color: var(--text-secondary);
  font-size: 12px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s ease;
  user-select: none;
}

.batch-actions-bar .batch-clear:hover {
  color: var(--primary-color);
  border-color: var(--primary-hover);
  background: var(--primary-bg);
}

.batch-actions-bar .batch-clear:active {
    transform: scale(0.97);
}

/* 暗色主题下的批量操作栏 */
[data-theme='dark'] .batch-actions-bar {
  background: rgba(255, 255, 255, 0.04);
}

[data-theme='dark'] .batch-actions-bar .batch-info {
  color: var(--text-primary);
}

[data-theme='dark'] .batch-actions-bar .batch-clear {
  color: var(--text-secondary);
  border-color: var(--border-color);
  background: transparent;
}

[data-theme='dark'] .batch-actions-bar .batch-clear:hover {
  color: var(--primary-color);
  border-color: var(--primary-bg-hover);
  background: var(--primary-bg);
}

/* ---- 暗色主题适配 ---- */
/*
 * 使用 CSS 选择器而非 !important 来覆盖 Element Plus 默认样式。
 * 通过 data-theme 属性选择器实现主题感知。
 */
[data-theme='dark'] .el-loading-mask {
  background-color: rgba(0, 0, 0, 0.7);
}

[data-theme='dark'] .el-loading-spinner {
  color: var(--primary-color);
}

[data-theme='dark'] .el-loading-spinner .path {
  stroke: var(--primary-color);
}

[data-theme='dark'] .el-loading-text {
  color: var(--text-primary);
}
</style>
