import { ref, computed } from 'vue'

export function useAsync(asyncFunction, options = {}) {
  const {
    immediate = false,
    initialData = null,
    onSuccess = null,
    onError = null
  } = options

  const data = ref(initialData)
  const error = ref(null)
  const loading = ref(false)

  const isReady = computed(() => data.value !== null && !error.value)
  const hasError = computed(() => error.value !== null)

  const execute = async (...args) => {
    loading.value = true
    error.value = null

    try {
      const result = await asyncFunction(...args)
      data.value = result
      if (onSuccess) {
        onSuccess(result)
      }
      return result
    } catch (e) {
      error.value = e
      if (onError) {
        onError(e)
      }
      throw e
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    data.value = initialData
    error.value = null
    loading.value = false
  }

  if (immediate) {
    execute()
  }

  return {
    data,
    error,
    loading,
    isReady,
    hasError,
    execute,
    reset
  }
}
