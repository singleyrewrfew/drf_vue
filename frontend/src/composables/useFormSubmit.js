/**
 * 表单提交和删除操作组合式函数
 *
 * 作用：提供可复用的表单提交（创建/更新）和删除操作逻辑
 * 使用：在 Vue 组件中导入并调用 useFormSubmit 或 useDelete
 *
 * 主要功能：
 *   1. useFormSubmit - 表单提交管理（支持创建和编辑模式、加载状态、错误处理）
 *   2. useDelete - 删除操作管理（带确认对话框、加载状态、错误处理）
 *
 * 适用场景：
 *   - CRUD 操作的表单提交
 *   - 数据项的删除操作
 *   - 需要统一错误处理和用户反馈的场景
 */
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

/**
 * 表单提交管理组合式函数
 *
 * 封装表单的创建和编辑逻辑，自动处理加载状态、成功/失败提示和对话框控制。
 * 支持自定义成功/失败消息，提供统一的错误处理机制。
 *
 * @param {Function} createFn - 创建数据的异步函数
 *   - 接收 formData 作为参数
 *   - 示例：(formData) => api.createItem(formData)
 *
 * @param {Function} updateFn - 更新数据的异步函数
 *   - 接收 id 和 formData 作为参数
 *   - 示例：(id, formData) => api.updateItem(id, formData)
 *
 * @param {Object} [options={}] - 配置选项
 * @param {string} [options.createMessage='创建成功'] - 创建成功的提示消息
 * @param {string} [options.updateMessage='更新成功'] - 更新成功的提示消息
 * @param {string} [options.createErrorMessage='创建失败'] - 创建失败的提示消息
 * @param {string} [options.updateErrorMessage='更新失败'] - 更新失败的提示消息
 *
 * @returns {Object} 表单提交控制对象
 * @returns {Ref<boolean>} returns.isEdit - 是否为编辑模式
 * @returns {Ref<number|null>} returns.editingId - 当前编辑的项目 ID
 * @returns {Ref<boolean>} returns.loading - 加载状态
 * @returns {Ref<boolean>} returns.visible - 对话框可见性
 * @returns {Ref<Object|null>} returns.formRef - 表单引用（用于验证）
 * @returns {Function} returns.openCreate - 打开创建对话框
 * @returns {Function} returns.openEdit - 打开编辑对话框
 * @returns {Function} returns.submit - 提交表单数据
 * @returns {Function} returns.close - 关闭对话框并重置状态
 * @returns {Function} returns.validate - 验证表单
 *
 * @example
 * // 基本用法
 * import { useFormSubmit } from '@/composables/useFormSubmit'
 *
 * const { visible, isEdit, loading, openCreate, openEdit, submit, close } = useFormSubmit(
 *   (formData) => api.createUser(formData),
 *   (id, formData) => api.updateUser(id, formData),
 *   {
 *     createMessage: '用户创建成功',
 *     updateMessage: '用户更新成功'
 *   }
 * )
 *
 * // 在模板中使用
 * <el-dialog v-model="visible" :title="isEdit ? '编辑' : '创建'">
 *   <el-form ref="formRef" :model="formData">
 *     <!-- 表单字段 -->
 *   </el-form>
 *   <template #footer>
 *     <el-button @click="close">取消</el-button>
 *     <el-button type="primary" :loading="loading" @click="handleSubmit">
 *       确定
 *     </el-button>
 *   </template>
 * </el-dialog>
 *
 * @example
 * // 提交处理
 * const handleSubmit = async () => {
 *   const valid = await validate()
 *   if (!valid) return
 *
 *   await submit(formData, () => {
 *     // 成功后的回调，如刷新列表
 *     fetchList()
 *   })
 * }
 */
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

  /**
   * 打开创建对话框
   *
   * 将模式设置为创建，清空编辑 ID，显示对话框
   */
  const openCreate = () => {
    isEdit.value = false
    editingId.value = null
    visible.value = true
  }

  /**
   * 打开编辑对话框
   *
   * 将模式设置为编辑，设置编辑 ID，显示对话框
   *
   * @param {number|string} id - 要编辑的项目 ID
   */
  const openEdit = (id) => {
    isEdit.value = true
    editingId.value = id
    visible.value = true
  }

  /**
   * 提交表单数据
   *
   * 根据当前模式（创建/编辑）调用相应的 API，
   * 自动处理加载状态、成功/失败提示和对话框关闭。
   *
   * @param {Object} formData - 表单数据对象
   * @param {Function} [onSuccess] - 成功后的回调函数（可选）
   *   - 通常用于刷新列表或执行其他后续操作
   *
   * @returns {Promise} 返回 API 调用的 Promise
   *
   * @throws {Error} 如果 API 调用失败，抛出原始错误
   *
   * @example
   * const handleSubmit = async () => {
   *   const valid = await validate()
   *   if (!valid) return
   *
   *   await submit(formData, () => {
   *     fetchList() // 刷新列表
   *   })
   * }
   *
   * 工作流程：
   *   1. 设置 loading 为 true
   *   2. 根据 isEdit 判断调用 createFn 或 updateFn
   *   3. 成功时显示成功消息，关闭对话框，执行 onSuccess 回调
   *   4. 失败时从错误响应中提取消息并显示错误提示
   *   5. 无论成功失败，finally 中重置 loading 为 false
   *
   * 错误处理：
   *   - 优先使用 error.response.data.message
   *   - 其次使用 error.response.data.detail
   *   - 最后使用配置的默认错误消息
   */
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

  /**
   * 关闭对话框并重置状态
   *
   * 隐藏对话框，重置编辑模式和 ID，清除加载状态
   */
  const close = () => {
    visible.value = false
    isEdit.value = false
    editingId.value = null
    loading.value = false
  }

  /**
   * 验证表单
   *
   * 调用 Element Plus 表单的 validate 方法进行表单验证
   *
   * @returns {Promise<boolean>} 返回验证结果
   *   - true: 验证通过
   *   - false: 验证失败
   *
   * @example
   * const handleSubmit = async () => {
   *   const valid = await validate()
   *   if (!valid) {
   *     ElMessage.warning('请检查表单填写')
   *     return
   *   }
   *   await submit(formData)
   * }
   *
   * 注意：
   *   - 如果 formRef 未设置，直接返回 true（跳过验证）
   *   - 应该在提交前调用此方法确保数据有效性
   */
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

/**
 * 删除操作管理组合式函数
 *
 * 封装删除操作的完整流程，包括确认对话框、加载状态、成功/失败提示。
 * 使用 Element Plus 的 ElMessageBox 实现二次确认，防止误删。
 *
 * @param {Function} deleteFn - 删除数据的异步函数
 *   - 接收 id 作为参数
 *   - 示例：(id) => api.deleteItem(id)
 *
 * @param {Object} [options={}] - 配置选项
 * @param {string} [options.message='确定删除该项？'] - 确认对话框的提示消息
 * @param {string} [options.successMessage='删除成功'] - 删除成功的提示消息
 * @param {string} [options.errorMessage='删除失败'] - 删除失败的提示消息
 *
 * @returns {Object} 删除操作控制对象
 * @returns {Ref<boolean>} returns.loading - 加载状态
 * @returns {Function} returns.handleDelete - 执行删除操作的方法
 *
 * @example
 * // 基本用法
 * import { useDelete } from '@/composables/useFormSubmit'
 *
 * const { loading, handleDelete } = useDelete(
 *   (id) => api.deleteUser(id),
 *   {
 *     message: '确定要删除这个用户吗？',
 *     successMessage: '用户已删除',
 *     errorMessage: '删除用户失败'
 *   }
 * )
 *
 * // 在模板中使用
 * <el-button
 *   type="danger"
 *   :loading="loading"
 *   @click="handleDelete(item.id, () => fetchList())"
 * >
 *   删除
 * </el-button>
 *
 * @example
 * // 在业务逻辑中使用
 * const handleItemClick = (item) => {
 *   handleDelete(item.id, () => {
 *     // 删除成功后的回调，如刷新列表
 *     fetchList()
 *   })
 * }
 *
 * 工作流程：
 *   1. 动态导入 ElMessageBox（按需加载）
 *   2. 显示确认对话框，等待用户选择
 *   3. 用户点击确认后，设置 loading 为 true
 *   4. 调用 deleteFn 执行删除
 *   5. 成功时显示成功消息，执行 onSuccess 回调
 *   6. 失败时显示错误消息
 *   7. finally 中重置 loading 为 false
 *
 * 注意：
 *   - 如果用户点击取消，ElMessageBox.confirm 会抛出异常，后续代码不会执行
 *   - 使用动态导入减少初始包体积
 */
export function useDelete(deleteFn, options = {}) {
  const loading = ref(false)
  const message = options.message || '确定删除该项？'
  const successMessage = options.successMessage || '删除成功'
  const errorMessage = options.errorMessage || '删除失败'

  /**
   * 执行删除操作
   *
   * 显示确认对话框，用户确认后执行删除操作，
   * 自动处理加载状态、成功/失败提示。
   *
   * @param {number|string} id - 要删除的项目 ID
   * @param {Function} [onSuccess] - 成功后的回调函数（可选）
   *   - 通常用于刷新列表或执行其他后续操作
   *
   * @returns {Promise} 返回删除操作的 Promise
   *
   * @throws {Error} 如果用户取消或删除失败，抛出错误
   *
   * @example
   * const handleDeleteClick = (item) => {
   *   handleDelete(item.id, () => {
   *     fetchList() // 刷新列表
   *   })
   * }
   *
   * 错误处理：
   *   - 优先使用 error.response.data.message
   *   - 其次使用 error.response.data.detail
   *   - 最后使用配置的默认错误消息
   *
   * 注意：
   *   - 如果用户在确认对话框中点击取消，函数会提前退出
   *   - onSuccess 只在删除成功时执行
   */
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
