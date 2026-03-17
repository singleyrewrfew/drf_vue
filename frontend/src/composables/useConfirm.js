import { ElMessageBox } from 'element-plus'

export function useConfirm() {
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

  const confirmDelete = async (message = '确定删除该项？此操作不可恢复。') => {
    return confirm(message, '确认删除', { type: 'warning' })
  }

  const alert = async (message, title = '提示', options = {}) => {
    await ElMessageBox.alert(message, title, {
      confirmButtonText: '确定',
      ...options
    })
  }

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
