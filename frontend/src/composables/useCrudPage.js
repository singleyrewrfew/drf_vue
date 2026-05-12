import { ref, watch, onMounted } from 'vue'
import { usePagination } from './usePagination'
import { useFormSubmit, useDelete } from './useFormSubmit'

export function useCrudPage(fetchFn, options = {}) {
  const {
    deleteFn,
    createFn,
    updateFn,
    formOptions = {},
    paginationOptions = {},
    deleteOptions = {},
    autoLoad = true
  } = options

  const pagination = usePagination(fetchFn, paginationOptions)

  const data = pagination.data
  const loading = pagination.loading
  const page = pagination.page
  const pageSize = pagination.pageSize
  const total = pagination.total
  const refreshData = () => pagination.fetchData()

  let formSubmit = null
  let dialogVisible = ref(false)
  let submitLoading = ref(false)

  if (createFn && updateFn) {
    formSubmit = useFormSubmit(createFn, updateFn, formOptions)
    dialogVisible = formSubmit.visible
    submitLoading = formSubmit.loading
  }

  let delOp = null
  if (deleteFn) {
    delOp = useDelete(deleteFn, deleteOptions)
  }

  const tableRef = ref(null)

  watch([page, pageSize], () => {
    refreshData()
  })

  if (autoLoad) {
    onMounted(() => {
      refreshData()
    })
  }

  return {
    data,
    loading,
    page,
    pageSize,
    total,
    refreshData,
    fetchData: pagination.fetchData,
    formSubmit,
    dialogVisible,
    submitLoading,
    delOp,
    tableRef,
    pagination
  }
}
