import { ref } from 'vue'

export function useDialog(initialState = false) {
  const visible = ref(initialState)
  const loading = ref(false)

  const open = () => {
    visible.value = true
  }

  const close = () => {
    visible.value = false
    loading.value = false
  }

  const toggle = () => {
    visible.value = !visible.value
  }

  const withLoading = async (fn) => {
    loading.value = true
    try {
      await fn()
    } finally {
      loading.value = false
    }
  }

  return {
    visible,
    loading,
    open,
    close,
    toggle,
    withLoading
  }
}

export function useConfirmDialog() {
  const visible = ref(false)
  const loading = ref(false)
  const title = ref('')
  const message = ref('')
  const type = ref('warning')
  let resolvePromise = null

  const show = (options = {}) => {
    title.value = options.title || '提示'
    message.value = options.message || '确定执行此操作？'
    type.value = options.type || 'warning'
    visible.value = true
    
    return new Promise((resolve) => {
      resolvePromise = resolve
    })
  }

  const confirm = () => {
    visible.value = false
    resolvePromise?.(true)
  }

  const cancel = () => {
    visible.value = false
    resolvePromise?.(false)
  }

  return {
    visible,
    loading,
    title,
    message,
    type,
    show,
    confirm,
    cancel
  }
}
