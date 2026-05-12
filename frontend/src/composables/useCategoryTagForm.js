import {reactive, ref} from 'vue'
import {ElMessage} from 'element-plus'
import api from '@/api'

export function useCategoryTagForm(onCategoryCreated, onTagCreated) {
    const showCategoryDialog = ref(false)
    const showTagDialog = ref(false)
    const creatingCategory = ref(false)
    const creatingTag = ref(false)

    const categoryForm = reactive({name: '', slug: ''})
    const tagForm = reactive({name: '', slug: ''})

    const categoryRules = {
        name: [{required: true, message: '请输入分类名称', trigger: 'blur'}]
    }

    const tagRules = {
        name: [{required: true, message: '请输入标签名称', trigger: 'blur'}]
    }

    const handleCreateCategory = async (categories) => {
        if (!categoryForm.name.trim()) {
            ElMessage.warning('请输入分类名称')
            return
        }
        creatingCategory.value = true
        try {
            const payload = {name: categoryForm.name.trim(), slug: categoryForm.slug.trim() || undefined}
            const {data} = await api.post('/categories/', payload)
            ElMessage.success('分类创建成功')
            showCategoryDialog.value = false
            categoryForm.name = ''
            categoryForm.slug = ''
            categories.push(data)
            if (onCategoryCreated) onCategoryCreated(data.id)
        } catch (error) {
            ElMessage.error('创建分类失败')
        } finally {
            creatingCategory.value = false
        }
    }

    const handleCreateTag = async (tags) => {
        if (!tagForm.name.trim()) {
            ElMessage.warning('请输入标签名称')
            return
        }
        creatingTag.value = true
        try {
            const payload = {name: tagForm.name.trim(), slug: tagForm.slug.trim() || undefined}
            const {data} = await api.post('/tags/', payload)
            ElMessage.success('标签创建成功')
            showTagDialog.value = false
            tagForm.name = ''
            tagForm.slug = ''
            tags.push(data)
            if (onTagCreated) onTagCreated(data.id)
        } catch (error) {
            ElMessage.error('创建标签失败')
        } finally {
            creatingTag.value = false
        }
    }

    return {
        showCategoryDialog,
        showTagDialog,
        creatingCategory,
        creatingTag,
        categoryForm,
        tagForm,
        categoryRules,
        tagRules,
        handleCreateCategory,
        handleCreateTag,
    }
}
