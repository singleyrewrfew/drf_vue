<template>
    <div class="table-page">
        <el-card>
            <!-- #header 是 el-card 组件提供的插槽, 流程:子组件挖个坑 → 父组件填内容 → Vue 自动把填的内容放到坑里 -->
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
                :element-loading-background="loadingBackground()"
            >
                <slot></slot>
                <el-table-column v-if="showActions" label="操作" :width="actionsWidth" fixed="right">
                    <template #default="{ row }">
                        <div class="action-buttons">
                            <EditButton v-if="showEdit" @click="$emit('edit', row)" :disabled="editDisabled?.(row)" />
                            <DeleteButton v-if="showDelete" @click="$emit('delete', row)"
                                :disabled="deleteDisabled?.(row)" />
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
import { ref, watch } from 'vue'
import CreateButton from '@/components/CreateButton.vue'
import EditButton from '@/components/EditButton.vue'
import DeleteButton from '@/components/DeleteButton.vue'
import {useThemeStore} from '@/stores/theme.ts'

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
const loadingBackground = () => {
    if (themeStore.theme === 'light') {
        return 'rgba(136,135,135,0.8)'
    }else {
        return 'rgba(53,48,48,0.8)'
    }
}

const props = defineProps({
    title: {
        type: String,
        default: '数据列表'
    },
    data: {
        type: Array,
        default: () => []
    },
    loading: {
        type: Boolean,
        default: false
    },
    showCreate: {
        type: Boolean,
        default: true
    },
    createText: {
        type: String,
        default: '新建'
    },
    showActions: {
        type: Boolean,
        default: true
    },
    actionsWidth: {
        type: [String, Number],
        default: 150
    },
    showEdit: {
        type: Boolean,
        default: true
    },
    showDelete: {
        type: Boolean,
        default: true
    },
    editDisabled: {
        type: Function,
        default: null
    },
    deleteDisabled: {
        type: Function,
        default: null
    },
    showPagination: {
        type: Boolean,
        default: true
    },
    page: {
        type: Number,
        default: 1
    },
    pageSize: {
        type: Number,
        default: 20
    },
    pageSizes: {
        type: Array,
        default: () => [10, 20, 50, 100]
    },
    total: {
        type: Number,
        default: 0
    }
})
// 'update:page', 'update:pageSize' 这两个目前没有使用
const emit = defineEmits(['create', 'edit', 'delete', 'update:page', 'update:pageSize', 'page-change'])

const currentPage = ref(props.page)
const currentPageSize = ref(props.pageSize)

watch(
    () => props.page, // 监听来源
    // 监听回调函数
    (val) => {
        currentPage.value = val
    }
)

watch(
    () => props.pageSize, // 监听来源
    // 监听回调函数
    (val) => {
        currentPageSize.value = val
    }
)

const handleSizeChange = (size) => {
    // 1. 重置页码：用户切换每页显示条数（如从 10 条改成 20 条）时，必须把页码重置为 1。
    // 这是行业标准行为，避免出现 “新 pageSize 下页码超出范围” 的 BUG。
    currentPage.value = 1
    // 2. 触发 v-model:page 双向绑定更新（父组件同步 page）
    emit('update:page', 1)
    // 3. 触发 v-model:pageSize 双向绑定更新（父组件同步 pageSize）
    emit('update:pageSize', size)
    // 4. 触发自定义事件，向父组件传递完整分页参数
    emit('page-change', { page: 1, pageSize: size })
}

const handleCurrentChange = (page) => {
    // 1. 同步更新父组件的页码（v-model:page）
    emit('update:page', page)
    // 2. 通知父组件：页码变了，带上当前页+每页条数去请求数据
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
