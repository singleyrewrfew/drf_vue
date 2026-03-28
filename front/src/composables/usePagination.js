import { ref, computed } from 'vue'

export function usePagination(options = {}) {
  const {
    defaultPage = 1,
    defaultPageSize = 10,
    pageSizes = [10, 20, 50, 100]
  } = options

  const currentPage = ref(defaultPage)
  const pageSize = ref(defaultPageSize)
  const total = ref(0)

  const offset = computed(() => (currentPage.value - 1) * pageSize.value)
  const totalPages = computed(() => Math.ceil(total.value / pageSize.value))
  const hasNextPage = computed(() => currentPage.value < totalPages.value)
  const hasPrevPage = computed(() => currentPage.value > 1)

  const setPage = (page) => {
    currentPage.value = Math.max(1, Math.min(page, totalPages.value))
  }

  const setPageSize = (size) => {
    pageSize.value = size
    currentPage.value = 1
  }

  const setTotal = (newTotal) => {
    total.value = newTotal
  }

  const nextPage = () => {
    if (hasNextPage.value) {
      currentPage.value++
    }
  }

  const prevPage = () => {
    if (hasPrevPage.value) {
      currentPage.value--
    }
  }

  const reset = () => {
    currentPage.value = defaultPage
    pageSize.value = defaultPageSize
    total.value = 0
  }

  return {
    currentPage,
    pageSize,
    total,
    offset,
    totalPages,
    hasNextPage,
    hasPrevPage,
    pageSizes,
    setPage,
    setPageSize,
    setTotal,
    nextPage,
    prevPage,
    reset
  }
}
