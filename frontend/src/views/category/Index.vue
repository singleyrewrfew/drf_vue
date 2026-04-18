<template>
    <div class="category-page">
        <el-card>
            <template #header>
                <div class="card-header">
                    <span>分类管理</span>
                    <CreateButton text="新建分类" @click="handleAdd"/>
                </div>
            </template>
            <el-table :data="categoryList" v-loading="loading" stripe row-key="id">
                <el-table-column prop="name" label="分类名称"/>
                <el-table-column prop="slug" label="URL别名"/>
                <el-table-column prop="parent_name" label="父分类"/>
                <el-table-column prop="sort_order" label="排序" width="80"/>
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
                @current-change="fetchCategories"
                @size-change="handleSizeChange"
            />
        </el-card>

        <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑分类' : '新建分类'" width="500px">
            <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
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
import {getCategories, createCategory, updateCategory, deleteCategory} from '@/api/category'
import EditButton from '@/components/EditButton.vue'
import DeleteButton from '@/components/DeleteButton.vue'
import CreateButton from '@/components/CreateButton.vue'
import ResetButton from '@/components/ResetButton.vue'
import ConfirmButton from '@/components/ConfirmButton.vue'

const loading = ref(false)
const submitLoading = ref(false)
const categoryList = ref([])
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const dialogVisible = ref(false)
const editingId = ref(null)
const formRef = ref()

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
        const offset = (page.value - 1) * pageSize.value
        const {data} = await getCategories({
            limit: pageSize.value,
            offset: offset
        })
        categoryList.value = data.results || data
        total.value = data.count || categoryList.value.length
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
    await formRef.value.validate()
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

const handleSizeChange = () => {
    page.value = 1
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
