import { ref } from 'vue'
import { ElMessage } from 'element-plus'

export function useFormSubmit(createFn, updateFn, options = {}) {
  const isEdit = ref(false)
  const editingId = ref(null)
  const loading = ref(false)
  const visible = ref(false)
  const formRef = ref(null)

  const createMessage = options.createMessage || '创建成功'
  const updateMessage = options.updateMessage || '更新成功'
  const createErrorMessage = options.createErrorMessage || '创建失败'
  const updateErrorMessage = options.updateErrorMessage || '更新失败'

  const openCreate = () => {
    isEdit.value = false
    editingId.value = null
    visible.value = true
  }

  const openEdit = (id) => {
    isEdit.value = true
    editingId.value = id
    visible.value = true
  }

  const submit = async (formData, onSuccess) => {
    loading.value = true
    try {
      if (isEdit.value && editingId.value) {
        await updateFn(editingId.value, formData)
        ElMessage.success(updateMessage)
      } else {
        await createFn(formData)
        ElMessage.success(createMessage)
      }
      visible.value = false
      onSuccess?.()
    } catch (error) {
      const message = error.response?.data?.message || 
        error.response?.data?.detail ||
        (isEdit.value ? updateErrorMessage : createErrorMessage)
      ElMessage.error(message)
      throw error
    } finally {
      loading.value = false
    }
  }

  const close = () => {
    visible.value = false
    isEdit.value = false
    editingId.value = null
    loading.value = false
  }

  const validate = async () => {
    if (!formRef.value) return true
    return await formRef.value.validate()
  }

  return {
    isEdit,
    editingId,
    loading,
    visible,
    formRef,
    openCreate,
    openEdit,
    submit,
    close,
    validate
  }
}

export function useDelete(deleteFn, options = {}) {
  const loading = ref(false)
  const message = options.message || '确定删除该项？'
  const successMessage = options.successMessage || '删除成功'
  const errorMessage = options.errorMessage || '删除失败'

  const handleDelete = async (id, onSuccess) => {
    const { ElMessageBox } = await import('element-plus')
    await ElMessageBox.confirm(message, '提示', { type: 'warning' })
    
    loading.value = true
    try {
      await deleteFn(id)
      ElMessage.success(successMessage)
      onSuccess?.()
    } catch (error) {
      const msg = error.response?.data?.message || 
        error.response?.data?.detail || 
        errorMessage
      ElMessage.error(msg)
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    handleDelete
  }
}
