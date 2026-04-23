<template>
    <div class="tags-page">
        <TablePage
            title="标签管理"
            create-text="新建标签"
            :data="tagList"
            :loading="loading"
            :page="pagination.page"
            :page-size="pagination.page_size"
            :total="pagination.total"
            @create="handleAdd"
            @edit="handleEdit"
            @delete="handleDelete"
            @page-change="handlePageChange"
        >
            <el-table-column prop="name" label="标签名称"/>
            <el-table-column prop="slug" label="URL 别名"/>
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
import {ref, reactive, computed, onMounted} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {getTags, createTag, updateTag, deleteTag} from '@/api/category'
import TablePage from '@/components/TablePage.vue'
import FormDialog from '@/components/FormDialog.vue'


const loading = ref(false)
const submitLoading = ref(false)
const tagList = ref([])
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
})

const rules = {
    name: [{required: true, message: '请输入标签名称', trigger: 'blur'}],
}

const isEdit = computed(() => !!editingId.value)

const fetchTags = async () => {
    loading.value = true
    try {
        const offset = (pagination.page - 1) * pagination.page_size
        const {data} = await getTags({
            limit: pagination.page_size,
            offset: offset
        })
        tagList.value = data.results || data
        pagination.total = data.count || tagList.value.length
    } catch (error) {
        ElMessage.error('获取标签列表失败')
    } finally {
        loading.value = false
    }
}

const resetForm = () => {
    Object.assign(form, {name: '', slug: ''})
    editingId.value = null
}

const handleAdd = () => {
    resetForm()
    dialogVisible.value = true
}

const handleEdit = (row) => {
    editingId.value = row.id
    Object.assign(form, {name: row.name, slug: row.slug})
    dialogVisible.value = true
}

const handleSubmit = async () => {
    submitLoading.value = true
    try {
        const submitData = {...form}
        if (!submitData.slug) {
            delete submitData.slug
        }
        if (isEdit.value) {
            await updateTag(editingId.value, submitData)
            ElMessage.success('更新成功')
        } else {
            await createTag(submitData)
            ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        await fetchTags()
    } catch (error) {
        ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
    } finally {
        submitLoading.value = false
    }
}

const handleDelete = async (row) => {
    await ElMessageBox.confirm('确定删除该标签？', '提示', {type: 'warning'})
    try {
        await deleteTag(row.id)
        ElMessage.success('删除成功')
        await fetchTags()
    } catch (error) {
        ElMessage.error('删除失败')
    }
}

const handlePageChange = ({page, pageSize}) => {
    pagination.page = page
    pagination.page_size = pageSize
    fetchTags()
}

onMounted(() => {
    fetchTags()
})
</script>

<style scoped>
.tags-page {
    padding: 0;
}
</style>
