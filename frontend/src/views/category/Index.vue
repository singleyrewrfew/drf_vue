<template>
    <div class="category-page">
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
            <el-table-column prop="name" label="分类名称"/>
            <el-table-column prop="slug" label="URL别名"/>
            <el-table-column prop="parent_name" label="父分类"/>
            <el-table-column prop="sort_order" label="排序" width="80"/>
            <el-table-column prop="created_at" label="创建时间" width="180"/>
        </TablePage>

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
            <el-form-item label="名称" prop="name">
                <el-input v-model="form.name" placeholder="请输入分类名称"/>
            </el-form-item>
            <el-form-item label="别名" prop="slug">
                <el-input v-model="form.slug" placeholder="URL别名，留空自动生成"/>
            </el-form-item>
            <el-form-item label="父分类">
                <el-select v-model="form.parent" placeholder="请选择父分类" clearable>
                    <el-option
                        v-for="cat in parentCategories"
                        :key="cat.id"
                        :label="cat.name"
                        :value="cat.id"
                    />
                </el-select>
            </el-form-item>
            <el-form-item label="描述">
                <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入描述"/>
            </el-form-item>
            <el-form-item label="排序">
                <el-input-number v-model="form.sort_order" :min="0"/>
            </el-form-item>
        </FormDialog>
    </div>
</template>

<script setup>
import {reactive, computed, ref} from 'vue'
import {getCategories, createCategory, updateCategory, deleteCategory} from '@/api/category'
import {useCrudPage} from '@/composables/useCrudPage'
import TablePage from '@/components/TablePage.vue'
import FormDialog from '@/components/FormDialog.vue'

const {
    data: categoryList,
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
        const {data} = await getCategories(params)
        return data
    },
    {
        deleteFn: async (id) => await deleteCategory(id),
        deleteOptions: {message: '确定删除该分类？'},
        createFn: async (formData) => await createCategory(formData),
        updateFn: async (id, formData) => await updateCategory(id, formData),
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
    parent: '',
    description: '',
    sort_order: 0,
})

const rules = {
    name: [{required: true, message: '请输入分类名称', trigger: 'blur'}],
}

const parentCategories = computed(() => {
    return categoryList.value.filter((cat) => cat.id !== formSubmit.editingId.value)
})

const openCreateDialog = () => {
    Object.assign(form, {
        name: '',
        slug: '',
        parent: '',
        description: '',
        sort_order: 0,
    })
    formSubmit.openCreate()
}

const openEditDialog = (row) => {
    Object.assign(form, {
        name: row.name,
        slug: row.slug,
        parent: row.parent || '',
        description: row.description,
        sort_order: row.sort_order,
    })
    formSubmit.openEdit(row.id)
}

const handleSubmit = async () => {
    const submitData = {...form}
    if (!submitData.slug) delete submitData.slug
    if (!submitData.parent) delete submitData.parent
    await formSubmit.submit(submitData, refreshData)
}
</script>

<style scoped>
.category-page {
    padding: 0;
}
</style>
