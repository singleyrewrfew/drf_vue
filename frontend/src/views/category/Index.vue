<template>
    <div class="category-page">
        <TablePage
            title="分类管理"
            create-text="新建分类"
            :data="categoryList"
            :loading="loading"
            :page="pagination.page"
            :page-size="pagination.page_size"
            :total="pagination.total"
            @create="handleAdd"
            @edit="handleEdit"
            @delete="handleDelete"
            @page-change="handlePageChange"
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
                    <el-option v-for="cat in parentCategories" :key="cat.id" :label="cat.name" :value="cat.id"/>
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
import {ref, reactive, computed, onMounted} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {getCategories, createCategory, updateCategory, deleteCategory} from '@/api/category'
import TablePage from '@/components/TablePage.vue'
import FormDialog from '@/components/FormDialog.vue'
const loading = ref(false)
const submitLoading = ref(false)
const categoryList = ref([])
const dialogVisible = ref(false)
const editingId = ref(null)

const pagination = reactive({
    page: 1,
    page_size: 10,
    total: 0,
})


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

const isEdit = computed(() => !!editingId.value)

const parentCategories = computed(() => {
    return categoryList.value.filter((cat) => cat.id !== editingId.value)
})

const fetchCategories = async () => {
    loading.value = true
    try {
        const offset = (pagination.page - 1) * pagination.page_size
        const {data} = await getCategories({
            limit: pagination.page_size,
            offset: offset
        })
        categoryList.value = data.results || data
        pagination.total = data.count || categoryList.value.length
    } catch (error) {
        ElMessage.error('获取分类列表失败')
    } finally {
        loading.value = false
    }
}

const resetForm = () => {
    Object.assign(form, {
        name: '',
        slug: '',
        parent: '',
        description: '',
        sort_order: 0,
    })
    editingId.value = null
}

const handleAdd = () => {
    resetForm()
    dialogVisible.value = true
}

const handleEdit = (row) => {
    editingId.value = row.id
    Object.assign(form, {
        name: row.name,
        slug: row.slug,
        parent: row.parent || '',
        description: row.description,
        sort_order: row.sort_order,
    })
    dialogVisible.value = true
}

const handleSubmit = async () => {
    submitLoading.value = true
    try {
        const submitData = {...form}
        if (!submitData.slug) {
            delete submitData.slug
        }
        if (!submitData.parent) {
            delete submitData.parent
        }
        if (isEdit.value) {
            await updateCategory(editingId.value, submitData)
            ElMessage.success('更新成功')
        } else {
            await createCategory(submitData)
            ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        await fetchCategories()
    } catch (error) {
        ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
    } finally {
        submitLoading.value = false
    }
}

const handleDelete = async (row) => {
    await ElMessageBox.confirm('确定删除该分类？', '提示', {type: 'warning'})
    try {
        await deleteCategory(row.id)
        ElMessage.success('删除成功')
        await fetchCategories()
    } catch (error) {
        ElMessage.error('删除失败')
    }
}

const handlePageChange = ({page, pageSize}) => {
    pagination.page = page
    pagination.page_size = pageSize
    fetchCategories()
}

onMounted(() => {
    fetchCategories()
})
</script>

<style scoped>
.category-page {
    padding: 0;
}
</style>
