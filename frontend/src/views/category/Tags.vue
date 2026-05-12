<template>
    <div class="tags-page">
        <TablePage
            ref="tableRef"
            title="标签管理"
            create-text="新建标签"
            :data="tagList"
            :loading="loading"
            v-model:page="page"
            v-model:page-size="pageSize"
            :total="total"
            @create="openCreateDialog"
            @edit="openEditDialog"
            @delete="(row) => delOp.handleDelete(row.id, refreshData)"
        >
            <el-table-column prop="name" label="标签名称"/>
            <el-table-column prop="slug" label="URL别名"/>
            <el-table-column prop="content_count" label="文章数量" width="100"/>
            <el-table-column prop="created_at" label="创建时间" width="180"/>
        </TablePage>

        <FormDialog
            v-model="form"
            v-model:show="dialogVisible"
            create-title="新建标签"
            edit-title="编辑标签"
            width="400px"
            label-width="80px"
            :rules="rules"
            :loading="submitLoading"
            @submit="handleSubmit"
        >
            <el-form-item label="名称" prop="name">
                <el-input v-model="form.name" placeholder="请输入标签名称"/>
            </el-form-item>
            <el-form-item label="别名">
                <el-input v-model="form.slug" placeholder="URL别名，留空自动生成"/>
            </el-form-item>
        </FormDialog>
    </div>
</template>

<script setup>
import {reactive} from 'vue'
import {getTags, createTag, updateTag, deleteTag} from '@/api/category'
import {useCrudPage} from '@/composables/useCrudPage'
import TablePage from '@/components/TablePage.vue'
import FormDialog from '@/components/FormDialog.vue'

const {
    data: tagList,
    loading,
    page,
    pageSize,
    total,
    refreshData,
    formSubmit,
    dialogVisible,
    submitLoading,
    delOp,
    tableRef
} = useCrudPage(
    async (params) => {
        const {data} = await getTags(params)
        return data
    },
    {
        deleteFn: async (id) => await deleteTag(id),
        deleteOptions: {message: '确定删除该标签？'},
        createFn: async (formData) => await createTag(formData),
        updateFn: async (id, formData) => await updateTag(id, formData),
        formOptions: {
            createMessage: '创建成功',
            updateMessage: '更新成功',
        },
        paginationOptions: {defaultPageSize: 10}
    }
)

let form = reactive({
    name: '',
    slug: '',
})

const rules = {
    name: [{required: true, message: '请输入标签名称', trigger: 'blur'}],
}

const openCreateDialog = () => {
    Object.assign(form, {name: '', slug: ''})
    formSubmit.openCreate()
}

const openEditDialog = (row) => {
    Object.assign(form, {name: row.name, slug: row.slug})
    formSubmit.openEdit(row.id)
}

const handleSubmit = async () => {
    const submitData = {...form}
    if (!submitData.slug) delete submitData.slug
    await formSubmit.submit(submitData, refreshData)
}
</script>

<style scoped>
.tags-page {
    padding: 0;
}
</style>
