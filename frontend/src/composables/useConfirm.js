/**
 * 确认对话框组合式函数
 *
 * 作用：封装 Element Plus 的 MessageBox 组件，提供简化的确认、提示和输入对话框
 * 使用：在 Vue 组件中导入并调用 useConfirm
 *
 * 主要功能：
 *   1. confirm - 通用确认话框（支持自定义标题、消息和类型）
 *   2. confirmDelete - 删除确认对话框（预配置警告类型和默认消息）
 *   3. alert - 信息提示对话框（仅确认按钮）
 *   4. prompt - 输入对话框（获取用户输入）
 *
 * 适用场景：
 *   - 重要操作的二次确认（如删除、提交）
 *   - 操作结果提示（成功、失败、警告）
 *   - 需要用户输入简单信息的场景
 */
import { ElMessageBox } from 'element-plus'

/**
 * 确认对话框管理组合式函数
 *
 * 提供基于 Promise 的对话框方法，将 Element Plus 的 MessageBox API 简化为
 * 返回布尔值或结构化对象的形式，便于在业务逻辑中使用。
 *
 * @returns {Object} 对话框控制对象
 * @returns {Function} returns.confirm - 通用确认对话框
 * @returns {Function} returns.confirmDelete - 删除确认对话框
 * @returns {Function} returns.alert - 信息提示对话框
 * @returns {Function} returns.prompt - 输入对话框
 *
 * @example
 * // 基本用法
 * import { useConfirm } from '@/composables/useConfirm'
 *
 * const { confirm, confirmDelete, alert, prompt } = useConfirm()
 *
 * @example
 * // 删除确认
 * const handleDelete = async (id) => {
 *   const confirmed = await confirmDelete()
 *   if (confirmed) {
 *     await api.deleteItem(id)
 *     alert('删除成功')
 *   }
 * }
 *
 * @example
 * // 自定义确认
 * const handlePublish = async () => {
 *   const confirmed = await confirm(
 *     '确定要发布这篇文章吗？发布后将对所有用户可见。',
 *     '发布确认',
 *     { type: 'info' }
 *   )
 *   if (confirmed) {
 *     await api.publishArticle(articleId)
 *   }
 * }
 *
 * @example
 * // 输入对话框
 * const handleRename = async () => {
 *   const result = await prompt('请输入新的名称：', '重命名')
 *   if (result.confirmed && result.value) {
 *     await api.rename(item.id, result.value)
 *   }
 * }
 */
export function useConfirm() {
  /**
   * 显示通用确认对话框
   *
   * 显示一个带有“确定”和“取消”按钮的确认对话框，
   * 根据用户的选择返回 true 或 false。
   *
   * @param {string} message - 对话框显示的消息内容
   * @param {string} [title='提示'] - 对话框标题
   * @param {Object} [options={}] - 额外的配置选项
   * @param {string} [options.type='warning'] - 对话框类型
   *   - 'success': 成功类型（绿色图标）
   *   - 'warning': 警告类型（黄色图标，默认）
   *   - 'error': 错误类型（红色图标）
   *   - 'info': 信息类型（蓝色图标）
   *   - 也可以传递其他 ElMessageBox 支持的选项
   *
   * @returns {Promise<boolean>} 返回用户的选择
   *   - true: 用户点击了“确定”按钮
   *   - false: 用户点击了“取消”按钮或关闭了对话框
   *
   * @example
   * // 基本用法
   * const confirmed = await confirm('确定执行此操作？')
   * if (confirmed) {
   *   // 用户点击了确定
   * }
   *
   * @example
   * // 自定义类型
   * const confirmed = await confirm(
   *   '这是一个重要操作，请确认后再继续。',
   *   '重要提示',
   *   { type: 'error' }
   * )
   *
   * @example
   * // 在业务逻辑中使用
   * const handleSubmit = async () => {
   *   const confirmed = await confirm('确定提交表单吗？')
   *   if (!confirmed) return
   *
   *   await api.submitForm(formData)
   * }
   *
   * 注意：
   *   - 该方法会捕获 ElMessageBox 的取消异常，不会抛出错误
   *   - 适合用于需要用户确认的场景
   */
  const confirm = async (message, title = '提示', options = {}) => {
    try {
      await ElMessageBox.confirm(message, title, {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: options.type || 'warning',
        ...options
      })
      return true
    } catch {
      return false
    }
  }

  /**
   * 显示删除确认对话框
   *
   * 专门用于删除操作的确认对话框，预配置了警告类型和默认消息。
   * 强调删除操作的不可逆性，提醒用户谨慎操作。
   *
   * @param {string} [message='确定删除该项？此操作不可恢复。'] - 确认消息
   *
   * @returns {Promise<boolean>} 返回用户的选择
   *   - true: 用户确认删除
   *   - false: 用户取消删除
   *
   * @example
   * // 基本用法
   * const handleDelete = async (id) => {
   *   const confirmed = await confirmDelete()
   *   if (confirmed) {
   *     await api.deleteItem(id)
   *     ElMessage.success('删除成功')
   *   }
   * }
   *
   * @example
   * // 自定义消息
   * const confirmed = await confirmDelete(
   *   '确定要删除这个用户吗？删除后将无法恢复该用户的所有数据。'
   * )
   *
   * 注意：
   *   - 默认使用 warning 类型，显示黄色警告图标
   *   - 消息强调了操作的不可恢复性
   *   - 是 confirm 方法的便捷包装
   */
  const confirmDelete = async (message = '确定删除该项？此操作不可恢复。') => {
    return confirm(message, '确认删除', { type: 'warning' })
  }

  /**
   * 显示信息提示对话框
   *
   * 显示一个只带“确定”按钮的信息提示对话框，
   * 用于向用户展示操作结果或重要信息。
   *
   * @param {string} message - 对话框显示的消息内容
   * @param {string} [title='提示'] - 对话框标题
   * @param {Object} [options={}] - 额外的配置选项
   *   - 可以传递任何 ElMessageBox.alert 支持的选项
   *
   * @returns {Promise<void>} 当用户点击确定后解析
   *
   * @example
   * // 基本用法
   * await alert('操作已成功完成')
   *
   * @example
   * // 成功提示
   * await alert('数据保存成功！', '成功', { type: 'success' })
   *
   * @example
   * // 错误提示
   * await alert('操作失败，请稍后重试。', '错误', { type: 'error' })
   *
   * @example
   * // 在业务逻辑中使用
   * const handleSubmit = async () => {
   *   try {
   *     await api.saveData(data)
   *     await alert('保存成功', '提示', { type: 'success' })
   *   } catch (error) {
   *     await alert('保存失败：' + error.message, '错误', { type: 'error' })
   *   }
   * }
   *
   * 注意：
   *   - 与 confirm 不同，alert 只有一个“确定”按钮
   *   - 适合用于不需要用户选择的操作结果提示
   */
  const alert = async (message, title = '提示', options = {}) => {
    await ElMessageBox.alert(message, title, {
      confirmButtonText: '确定',
      ...options
    })
  }

  /**
   * 显示输入对话框
   *
   * 显示一个带有输入框的对话框，允许用户输入文本信息，
   * 返回包含确认状态和输入值的对象。
   *
   * @param {string} message - 对话框显示的提示消息
   * @param {string} [title='请输入'] - 对话框标题
   * @param {Object} [options={}] - 额外的配置选项
   *   - 可以传递任何 ElMessageBox.prompt 支持的选项
   *   - 常用选项：inputType, inputPattern, inputPlaceholder 等
   *
   * @returns {Promise<Object>} 返回包含确认状态和输入值的对象
   * @returns {boolean} returns.confirmed - 用户是否点击了“确定”
   * @returns {string|null} returns.value - 用户输入的值，如果取消则为 null
   *
   * @example
   * // 基本用法
   * const result = await prompt('请输入您的姓名：', '个人信息')
   * if (result.confirmed && result.value) {
   *   console.log('用户输入的姓名：', result.value)
   * }
   *
   * @example
   * // 带验证的输入
   * const result = await prompt('请输入邮箱地址：', '邮箱验证', {
   *   inputPattern: /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/,
   *   inputErrorMessage: '邮箱格式不正确'
   * })
   * if (result.confirmed) {
   *   await api.updateEmail(result.value)
   * }
   *
   * @example
   * // 密码输入
   * const result = await prompt('请输入密码：', '身份验证', {
   *   inputType: 'password',
   *   inputPlaceholder: '请输入您的密码'
   * })
   * if (result.confirmed && result.value) {
   *   await verifyPassword(result.value)
   * }
   *
   * @example
   * // 在业务逻辑中使用
   * const handleRename = async (item) => {
   *   const result = await prompt('请输入新的名称：', '重命名', {
   *     inputValue: item.name,
   *     inputPlaceholder: '请输入新名称'
   *   })
   *
   *   if (result.confirmed && result.value) {
   *     await api.rename(item.id, result.value)
   *     ElMessage.success('重命名成功')
   *   }
   * }
   *
   * 注意：
   *   - 如果用户点击取消，value 为 null
   *   - 应该检查 confirmed 和 value 两个字段
   *   - 可以使用 inputPattern 进行输入验证
   */
  const prompt = async (message, title = '请输入', options = {}) => {
    try {
      const { value } = await ElMessageBox.prompt(message, title, {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        ...options
      })
      return { confirmed: true, value }
    } catch {
      return { confirmed: false, value: null }
    }
  }

  return {
    confirm,
    confirmDelete,
    alert,
    prompt
  }
}
