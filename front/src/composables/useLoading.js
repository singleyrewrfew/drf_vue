import { ref } from 'vue'

export function useLoading(initialState = false) {
  const loading = ref(initialState)
  const loadingText = ref('加载中...')

  const startLoading = (text = '加载中...') => {
    loading.value = true
    loadingText.value = text
  }

  const stopLoading = () => {
    loading.value = false
  }

  const withLoading = async (fn, text = '加载中...') => {
    startLoading(text)
    try {
      return await fn()
    } finally {
      stopLoading()
    }
  }

  return {
    loading,
    loadingText,
    startLoading,
    stopLoading,
    withLoading
  }
}
