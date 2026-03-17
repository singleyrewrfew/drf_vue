<template>
  <div class="table-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>{{ title }}</span>
          <CreateButton v-if="showCreate" :text="createText" @click="$emit('create')" />
        </div>
      </template>
      <el-table :data="data" v-loading="loading" stripe v-bind="$attrs">
        <slot></slot>
        <el-table-column v-if="showActions" label="操作" :width="actionsWidth" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <EditButton v-if="showEdit" @click="$emit('edit', row)" :disabled="editDisabled?.(row)" />
              <DeleteButton v-if="showDelete" @click="$emit('delete', row)" :disabled="deleteDisabled?.(row)" />
              <slot name="actions" :row="row"></slot>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="showPagination" class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="currentPageSize"
          :page-sizes="pageSizes"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import CreateButton from '@/components/CreateButton.vue'
import EditButton from '@/components/EditButton.vue'
import DeleteButton from '@/components/DeleteButton.vue'

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

const emit = defineEmits(['create', 'edit', 'delete', 'update:page', 'update:pageSize', 'page-change'])

const currentPage = ref(props.page)
const currentPageSize = ref(props.pageSize)

watch(() => props.page, (val) => {
  currentPage.value = val
})

watch(() => props.pageSize, (val) => {
  currentPageSize.value = val
})

const handleSizeChange = (size) => {
  currentPage.value = 1
  emit('update:page', 1)
  emit('update:pageSize', size)
  emit('page-change', { page: 1, pageSize: size })
}

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
