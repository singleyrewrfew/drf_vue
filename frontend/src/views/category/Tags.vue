<template>
    <div class="tags-page">
        <el-card>
            <template #header>
                <div class="card-header">
                    <span>标签管理</span>
                    <CreateButton text="新建标签" @click="handleAdd"/>
                </div>
            </template>
            <el-table :data="tagList" v-loading="loading" stripe>
                <el-table-column prop="name" label="标签名称"/>
                <el-table-column prop="slug" label="URL 别名"/>
                <el-table-column prop="content_count" label="文章数量" width="100"/>
                <el-table-column prop="created_at" label="创建时间" width="180"/>
                <el-table-column label="操作" width="150" fixed="right">
                    <template #default="{ row }">
                        <div class="action-buttons">
                            <EditButton @click="handleEdit(row)"/>
                            <DeleteButton @click="handleDelete(row)"/>
                        </div>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination
                v-model:current-page="page"
                v-model:page-size="pageSize"
                :page-sizes="[10, 20, 50, 100]"
                :total="total"
                layout="total, sizes, prev, pager, next, jumper"
                @current-change="fetchTags"
                @size-change="handleSizeChange"
            />
        </el-card>

        <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑标签' : '新建标签'" width="400px">
            <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="名称" prop="name">
                    <el-input v-model="form.name" placeholder="请输入标签名称"/>
                </el-form-item>
                <el-form-item label="别名">
                    <el-input v-model="form.slug" placeholder="URL别名，留空自动生成"/>
                </el-form-item>
            </el-form>
            <template #footer>
                <ResetButton text="取消" @click="dialogVisible = false"/>
                <ConfirmButton text="确定" @click="handleSubmit" :disabled="submitLoading"/>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
import {ref, reactive, computed, onMounted} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {getTags, createTag, updateTag, deleteTag} from '@/api/category'
import EditButton from '@/components/EditButton.vue'
import DeleteButton from '@/components/DeleteButton.vue'
import CreateButton from '@/components/CreateButton.vue'
import ResetButton from '@/components/ResetButton.vue'
import ConfirmButton from '@/components/ConfirmButton.vue'

const loading = ref(false)
const submitLoading = ref(false)
const tagList = ref([])
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const dialogVisible = ref(false)
const editingId = ref(null)
const formRef = ref()

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
        const offset = (page.value - 1) * pageSize.value
        const {data} = await getTags({
            limit: pageSize.value,
            offset: offset
        })
        tagList.value = data.results || data
        total.value = data.count || tagList.value.length
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
    await formRef.value.validate()
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
        fetchTags()
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
        fetchTags()
    } catch (error) {
        ElMessage.error('删除失败')
    }
}

const handleSizeChange = () => {
    page.value = 1
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

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.action-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    align-items: center;
}
</style>
