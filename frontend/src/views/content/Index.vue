<template>
    <div class="content-page">
        <TablePage
            ref="tableRef"
            title="内容管理"
            :show-create="false"
            :show-edit="false"
            :data="contentList"
            :loading="loading"
            v-model:page="page"
            v-model:page-size="pageSize"
            :total="total"
            :default-page-size="10"
            @delete="(row) => delOp.handleDelete(row.id, refreshData)"
        >
            <template #header>
                <ContentSearchBar
                    v-model:search-form="searchForm"
                    :categories="categories"
                    @search="handleSearch"
                    @reset="handleReset"
                />
            </template>

            <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip/>
            <el-table-column prop="author_name" label="作者" width="120"/>
            <el-table-column prop="category_name" label="分类" width="120"/>
            <el-table-column label="标签" width="200">
                <template #default="{ row }">
                    <div class="tag-list">
                        <el-tag
                            v-for="tag in row.tags"
                            :key="tag.id"
                            size="small"
                            effect="plain"
                            class="content-tag"
                        >
                            {{ tag.name }}
                        </el-tag>
                        <span v-if="!row.tags || row.tags.length === 0" class="no-tags">-</span>
                    </div>
                </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
                <template #default="{ row }">
                    <StatusTag :type="CONTENT_STATUS_MAP[row.status]?.type" :text="CONTENT_STATUS_MAP[row.status]?.label"/>
                </template>
            </el-table-column>
            <el-table-column prop="view_count" label="浏览量" width="100"/>
            <el-table-column prop="created_at" label="创建时间" width="180"/>

            <template #row-actions="{ row }">
                <ActionButton
                    v-if="row.status === 'published'"
                    icon="eye"
                    text="查看"
                    type="info"
                    @click="handleView(row)"
                />
                <ActionButton icon="edit" text="编辑" @click="handleEdit(row)"/>
                <ActionButton
                    v-if="row.status === 'draft'"
                    icon="publish"
                    text="发布"
                    type="success"
                    @click="handlePublish(row)"
                />
            </template>
        </TablePage>
    </div>
</template>

<script setup>
import {reactive, ref, onMounted} from 'vue'
import {useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'
import {getContents, deleteContent, publishContent} from '@/api/content'
import api from '@/api'
import {useCrudPage} from '@/composables/useCrudPage'
import {CONTENT_STATUS_MAP} from '@/constants/contentConfig.js'
import TablePage from '@/components/TablePage.vue'
import ActionButton from '@/components/ActionButton.vue'
import StatusTag from '@/components/StatusTag.vue'
import ContentSearchBar from './components/ContentSearchBar.vue'

const router = useRouter()

const searchForm = reactive({
    status: null,
    category: null,
    search: '',
})

const {
    data: contentList,
    loading,
    page,
    pageSize,
    total,
    refreshData,
    delOp,
    tableRef
} = useCrudPage(
    async (params) => {
        if (searchForm.status) params.status = searchForm.status
        if (searchForm.category) params.category = searchForm.category
        if (searchForm.search) params.search = searchForm.search.trim()
        const {data} = await getContents(params)
        return data
    },
    {
        deleteFn: async (id) => await deleteContent(id),
        deleteOptions: {message: '确定删除该内容？'},
        paginationOptions: {defaultPageSize: 10}
    }
)

const categories = ref([])

const handleSearch = () => {
    page.value = 1
    refreshData()
}

const handleReset = () => {
    searchForm.status = null
    searchForm.category = null
    searchForm.search = ''
    page.value = 1
    refreshData()
}

const handleEdit = (row) => {
    router.push(`/contents/${row.id}/edit`)
}

const handleView = (row) => {
    const frontUrl = import.meta.env.VITE_FRONT_URL || window.location.origin
    window.open(`${frontUrl}/article/${row.id}`, '_blank')
}

const handlePublish = async (row) => {
    try {
        await publishContent(row.id)
        ElMessage.success('发布成功')
        await refreshData()
    } catch (error) {
        ElMessage.error('发布失败')
    }
}

onMounted(() => {
    fetchCategories()
})

const fetchCategories = async () => {
    try {
        const {data} = await api.get('/categories/')
        categories.value = data.results || data
    } catch (error) {
        console.error('获取分类列表失败:', error)
    }
}
</script>

<style scoped>
.content-page {
    padding: 20px;
}

.tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    align-items: center;
    min-height: 24px;
}

.content-tag {
    margin: 2px;
}

.no-tags {
    color: #909399;
    font-size: 14px;
}
</style>

<style>
.content-select-popper {
    z-index: 9999 !important;
}
</style>
