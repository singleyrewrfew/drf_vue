<template>
    <div class="table-page">
        <el-card>
            <template #header v-if="$slots.header">
                <slot name="header"></slot>
            </template>
            <template #header v-else>
                <div class="card-header">
                    <span>{{ title }}</span>
                    <CreateButton v-if="showCreate" :text="createText" @click="$emit('create')" />
                </div>
            </template>
            <el-table
                :data="data"
                v-loading="loading"
                v-bind="$attrs"
                element-loading-text="Loading..."
                element-loading-svg-view-box="-10, -10, 50, 50"
                :element-loading-spinner="svg"
                :element-loading-background="loadingBackground"
            >
                <slot></slot>
                <el-table-column v-if="showActions" label="操作" :width="actionsWidth" fixed="right">
                    <template #default="{ row }">
                        <div class="action-buttons">
                            <EditButton v-if="showEdit" @click="$emit('edit', row)" :disabled="isEditDisabled(row)" />
                            <DeleteButton v-if="showDelete" @click="$emit('delete', row)"
                                :disabled="isDeleteDisabled(row)" />
                            <slot name="actions" :row="row"></slot>
                        </div>
                    </template>
                </el-table-column>
            </el-table>
            <div v-if="showPagination" class="pagination-wrapper">
                <el-pagination v-model:current-page="currentPage" v-model:page-size="currentPageSize"
                    :page-sizes="pageSizes" :total="total" layout="total, sizes, prev, pager, next, jumper"
                    @size-change="handleSizeChange" @current-change="handleCurrentChange" />
            </div>
        </el-card>
    </div>
</template>

<script setup>
/**
 * 通用表格分页组件
 *
 * 封装了 Element Plus 的 el-table 和 el-pagination，提供统一的表格展示、操作按钮和分页功能。
 * 支持自定义表头、操作列显示/隐藏、加载状态、主题适配等。
 */
import { ref, watch, computed } from 'vue'
import CreateButton from '@/components/CreateButton.vue'
import EditButton from '@/components/EditButton.vue'
import DeleteButton from '@/components/DeleteButton.vue'
import {useThemeStore} from '@/stores/theme.ts'

/**
 * 自定义 SVG 加载动画
 */
const svg = `
        <path class="path" d="
          M 30 15
          L 28 17
          M 25.61 25.61
          A 15 15, 0, 0, 1, 15 30
          A 15 15, 0, 1, 1, 27.99 7.5
          L 15 15
        " style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"/>
      `

const themeStore = useThemeStore()

/**
 * 根据主题动态计算加载遮罩背景色
 *
 * @type {import('vue').ComputedRef<string>}
 */
const loadingBackground = computed(() => {
    return themeStore.theme === 'light' ? 'rgba(136,135,135,0.8)' : 'rgba(53,48,48,0.8)'
})

/**
 * 组件属性定义
 */
const props = defineProps({
    /** 卡片标题 */
    title: {
        type: String,
        default: '数据列表'
    },
    /** 表格数据 */
    data: {
        type: Array,
        default: () => []
    },
    /** 加载状态 */
    loading: {
        type: Boolean,
        default: false
    },
    /** 是否显示新建按钮 */
    showCreate: {
        type: Boolean,
        default: true
    },
    /** 新建按钮文本 */
    createText: {
        type: String,
        default: '新建'
    },
    /** 是否显示操作列 */
    showActions: {
        type: Boolean,
        default: true
    },
    /** 操作列宽度 */
    actionsWidth: {
        type: [String, Number],
        default: 150
    },
    /** 是否显示编辑按钮 */
    showEdit: {
        type: Boolean,
        default: true
    },
    /** 是否显示删除按钮 */
    showDelete: {
        type: Boolean,
        default: true
    },
    /** 编辑按钮禁用判断函数 */
    editDisabled: {
        type: Function,
        default: () => false
    },
    /** 删除按钮禁用判断函数 */
    deleteDisabled: {
        type: Function,
        default: () => false
    },
    /** 是否显示分页器 */
    showPagination: {
        type: Boolean,
        default: true
    },
    /** 当前页码 */
    page: {
        type: Number,
        default: 1
    },
    /** 每页显示条数 */
    pageSize: {
        type: Number,
        default: 20
    },
    /** 每页显示条数选项 */
    pageSizes: {
        type: Array,
        default: () => [10, 20, 50, 100]
    },
    /** 数据总数 */
    total: {
        type: Number,
        default: 0
    }
})

/**
 * 组件事件定义
 */
const emit = defineEmits(['create', 'edit', 'delete', 'update:page', 'update:pageSize', 'page-change'])

/**
 * 本地页码状态（用于 v-model 双向绑定）
 * @type {import('vue').Ref<number>}
 */
const currentPage = ref(props.page)

/**
 * 本地每页条数状态（用于 v-model 双向绑定）
 * @type {import('vue').Ref<number>}
 */
const currentPageSize = ref(props.pageSize)

/**
 * 监听父组件传入的页码变化，同步到本地状态
 */
watch(
    () => props.page,
    (val) => {
        currentPage.value = val
    }
)

/**
 * 监听父组件传入的每页条数变化，同步到本地状态
 */
watch(
    () => props.pageSize,
    (val) => {
        currentPageSize.value = val
    }
)

/**
 * 判断编辑按钮是否禁用
 *
 * @param {Object} row - 当前行数据
 * @returns {boolean} 是否禁用
 */
const isEditDisabled = (row) => {
    return props.editDisabled(row)
}

/**
 * 判断删除按钮是否禁用
 *
 * @param {Object} row - 当前行数据
 * @returns {boolean} 是否禁用
 */
const isDeleteDisabled = (row) => {
    return props.deleteDisabled(row)
}

/**
 * 处理每页显示条数变化
 *
 * 当用户切换每页显示条数时，重置页码为 1 并通知父组件。
 *
 * @param {number} size - 新的每页显示条数
 */
const handleSizeChange = (size) => {
    currentPage.value = 1
    emit('update:page', 1)
    emit('update:pageSize', size)
    emit('page-change', { page: 1, pageSize: size })
}

/**
 * 处理页码变化
 *
 * 当用户切换页码时，通知父组件更新数据。
 *
 * @param {number} page - 新的页码
 */
const handleCurrentChange = (page) => {
    emit('update:page', page)
    emit('page-change', { page, pageSize: currentPageSize.value })
}
</script>

<style scoped>
.table-page {
    padding: 0;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.pagination-wrapper {
    display: flex;
    justify-content: center;
    margin-top: 16px;
}

.action-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    align-items: center;
}

/* 暗色主题下的 loading 遮罩适配 */
[data-theme="dark"] .el-loading-mask {
    background-color: rgba(0, 0, 0, 0.7) !important;
}

[data-theme="dark"] .el-loading-spinner {
    color: var(--primary-color) !important;
}

[data-theme="dark"] .el-loading-spinner .path {
    stroke: var(--primary-color) !important;
}

[data-theme="dark"] .el-loading-spinner .circular {
    stroke: var(--primary-color) !important;
}

[data-theme="dark"] .el-loading-text {
    color: var(--text-primary) !important;
}
</style>
