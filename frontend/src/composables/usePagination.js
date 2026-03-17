import { ref, computed } from 'vue'

export function usePagination(fetchFn, options = {}) {
  const page = ref(1)
  const pageSize = ref(options.defaultPageSize || 20)
  const total = ref(0)
  const loading = ref(false)
  const data = ref([])
  const error = ref(null)

  const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

  const fetchData = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const offset = (page.value - 1) * pageSize.value
      const result = await fetchFn({
        limit: pageSize.value,
        offset,
        ...params
      })
      data.value = result.results || result
      total.value = result.count || data.value.length
      return result
    } catch (e) {
      error.value = e
      throw e
    } finally {
      loading.value = false
    }
  }

  const handleSizeChange = (size) => {
    pageSize.value = size
    page.value = 1
  }

  const handleCurrentChange = (newPage) => {
    page.value = newPage
  }

  const reset = () => {
    page.value = 1
    pageSize.value = options.defaultPageSize || 20
    total.value = 0
    data.value = []
    error.value = null
  }

  const goToFirst = () => { page.value = 1 }
  const goToLast = () => { page.value = totalPages.value }
  const goToPrev = () => { if (page.value > 1) page.value-- }
  const goToNext = () => { if (page.value < totalPages.value) page.value++ }

  return {
    page,
    pageSize,
    total,
    loading,
    data,
    error,
    totalPages,
    fetchData,
    handleSizeChange,
    handleCurrentChange,
    reset,
    goToFirst,
    goToLast,
    goToPrev,
    goToNext
  }
}
