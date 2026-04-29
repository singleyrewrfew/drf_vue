/**
 * 分页管理组合式函数
 *
 * 作用：提供可复用的分页逻辑，包括数据获取、页码控制和状态管理
 * 使用：在 Vue 组件中导入并调用 usePagination
 *
 * 主要功能：
 *   1. 自动计算偏移量（offset）和限制（limit）
 *   2. 管理分页状态（当前页、每页大小、总条数、总页数）
 *   3. 提供页码跳转方法（首页、末页、上一页、下一页）
 *   4. 处理加载状态和错误信息
 *   5. 支持重置分页状态
 *
 * 适用场景：
 *   - 列表数据的分页展示
 *   - 表格数据的分页加载
 *   - 任何需要 offset/limit 分页的 API 接口
 */
import { ref, computed } from 'vue'

/**
 * 分页管理组合式函数
 *
 * 封装分页逻辑，自动处理 offset/limit 计算、数据获取和状态管理。
 * 适用于 Django REST Framework 的分页格式（results/count）或其他类似格式。
 *
 * @param {Function} fetchFn - 获取数据的异步函数
 *   - 接收包含 limit、offset 和其他参数的对象
 *   - 应返回包含 results（或数组）和 count（或总数）的对象
 *   - 示例：(params) => api.getUsers(params)
 *
 * @param {Object} [options={}] - 配置选项
 * @param {number} [options.defaultPageSize=20] - 默认每页显示条数
 *
 * @returns {Object} 分页控制对象
 * @returns {Ref<number>} returns.page - 当前页码（从 1 开始）
 * @returns {Ref<number>} returns.pageSize - 每页显示条数
 * @returns {Ref<number>} returns.total - 总数据条数
 * @returns {Ref<boolean>} returns.loading - 加载状态
 * @returns {Ref<Array>} returns.data - 当前页的数据列表
 * @returns {Ref<Error|null>} returns.error - 错误信息
 * @returns {ComputedRef<number>} returns.totalPages - 总页数（计算属性）
 * @returns {Function} returns.fetchData - 获取数据的方法
 * @returns {Function} returns.handleSizeChange - 处理每页条数变化
 * @returns {Function} returns.handleCurrentChange - 处理当前页变化
 * @returns {Function} returns.reset - 重置分页状态
 * @returns {Function} returns.goToFirst - 跳转到首页
 * @returns {Function} returns.goToLast - 跳转到末页
 * @returns {Function} returns.goToPrev - 跳转到上一页
 * @returns {Function} returns.goToNext - 跳转到下一页
 *
 * @example
 * // 基本用法
 * import { usePagination } from '@/composables/usePagination'
 *
 * const {
 *   page,
 *   pageSize,
 *   total,
 *   loading,
 *   data,
 *   totalPages,
 *   fetchData,
 *   handleSizeChange,
 *   handleCurrentChange
 * } = usePagination(
 *   (params) => api.getUsers(params),
 *   { defaultPageSize: 10 }
 * )
 *
 * // 在模板中使用
 * <el-table :data="data" v-loading="loading">
 *   <!-- 表格列 -->
 * </el-table>
 *
 * <el-pagination
 *   v-model:current-page="page"
 *   v-model:page-size="pageSize"
 *   :total="total"
 *   :page-sizes="[10, 20, 50, 100]"
 *   @size-change="handleSizeChange"
 *   @current-change="handleCurrentChange"
 * />
 *
 * @example
 * // 在生命周期中获取数据
 * import { onMounted, watch } from 'vue'
 *
 * onMounted(() => {
 *   fetchData()
 * })
 *
 * // 监听页码变化，自动重新获取数据
 * watch([page, pageSize], () => {
 *   fetchData()
 * })
 *
 * @example
 * // 带额外参数的查询
 * const searchUsers = async (keyword) => {
 *   await fetchData({ search: keyword })
 * }
 */
export function usePagination(fetchFn, options = {}) {
  const page = ref(1)
  const pageSize = ref(options.defaultPageSize || 20)
  const total = ref(0)
  const loading = ref(false)
  const data = ref([])
  const error = ref(null)

  /**
   * 计算总页数
   *
   * 根据总数据条数和每页显示条数计算总页数
   * 使用 Math.ceil 向上取整，确保最后一页即使不满也能显示
   *
   * 计算公式：总页数 = ceil(总条数 / 每页条数)
   *
   * 示例：
   *   - total=100, pageSize=20 -> totalPages=5
   *   - total=101, pageSize=20 -> totalPages=6
   *   - total=0, pageSize=20 -> totalPages=0
   */
  const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

  /**
   * 获取分页数据
   *
   * 根据当前页码和每页条数计算 offset，调用 fetchFn 获取数据，
   * 并更新 data、total、loading、error 等状态。
   *
   * @param {Object} [params={}] - 额外的查询参数
   *   - 会与 limit、offset 合并后传递给 fetchFn
   *   - 示例：{ search: 'keyword', status: 'active' }
   *
   * @returns {Promise<Object>} 返回 API 响应的原始数据
   *
   * @throws {Error} 如果 API 调用失败，抛出原始错误
   *
   * @example
   * // 基本调用
   * await fetchData()
   *
   * @example
   * // 带搜索参数
   * await fetchData({ search: '张三' })
   *
   * @example
   * // 带筛选参数
   * await fetchData({ status: 'published', category: 1 })
   *
   * 工作流程：
   *   1. 设置 loading 为 true，清除之前的错误
   *   2. 计算 offset = (page - 1) * pageSize
   *   3. 调用 fetchFn，传入 limit、offset 和额外参数
   *   4. 更新 data（从 result.results 或 result 本身）
   *   5. 更新 total（从 result.count 或 data.length）
   *   6. 成功时返回 result，失败时设置 error 并抛出异常
   *   7. finally 中重置 loading 为 false
   *
   * 数据格式兼容：
   *   - DRF 格式：{ results: [...], count: 100 }
   *   - 简单数组：[...] （此时 total = data.length）
   *
   * 注意：
   *   - 每次调用都会重新获取数据，不会缓存
   *   - 应该在页码或每页条数变化时调用此方法
   */
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

  /**
   * 处理每页显示条数变化
   *
   * 当用户改变每页显示条数时调用，会自动将页码重置为第 1 页，
   * 避免因为每页条数增加导致当前页超出范围。
   *
   * @param {number} size - 新的每页显示条数
   *
   * @example
   * // Element Plus 分页组件使用
   * <el-pagination
   *   @size-change="handleSizeChange"
   *   :page-sizes="[10, 20, 50, 100]"
   * />
   *
   * 注意：
   *   - 调用此方法后需要手动调用 fetchData() 重新获取数据
   *   - 页码会被重置为 1，因为每页条数变化后原页码可能无效
   */
  const handleSizeChange = (size) => {
    pageSize.value = size
    page.value = 1
  }

  /**
   * 处理当前页码变化
   *
   * 当用户切换页码时调用，更新当前页码。
   *
   * @param {number} newPage - 新的页码
   *
   * @example
   * // Element Plus 分页组件使用
   * <el-pagination
   *   @current-change="handleCurrentChange"
   * />
   *
   * 注意：
   *   - 调用此方法后需要手动调用 fetchData() 重新获取数据
   *   - 此方法只更新页码状态，不自动获取数据
   */
  const handleCurrentChange = (newPage) => {
    page.value = newPage
  }

  /**
   * 重置分页状态
   *
   * 将所有分页相关状态重置为初始值，
   * 通常在切换数据源或清除筛选条件时调用。
   *
   * 重置的内容：
   *   - page: 重置为 1
   *   - pageSize: 重置为配置的默认值（或 20）
   *   - total: 重置为 0
   *   - data: 重置为空数组
   *   - error: 重置为 null
   *
   * @example
   * // 清除搜索条件时重置分页
   * const clearSearch = () => {
   *   searchKeyword.value = ''
   *   reset()
   *   fetchData()
   * }
   *
   * 注意：
   *   - 此方法不会自动调用 fetchData()
   *   - 如果需要重新获取数据，应在调用 reset() 后手动调用 fetchData()
   */
  const reset = () => {
    page.value = 1
    pageSize.value = options.defaultPageSize || 20
    total.value = 0
    data.value = []
    error.value = null
  }

  /**
   * 跳转到首页
   *
   * 将当前页码设置为 1
   */
  const goToFirst = () => { page.value = 1 }

  /**
   * 跳转到末页
   *
   * 将当前页码设置为最后一页
   * 如果总页数为 0，则页码保持为 0
   */
  const goToLast = () => { page.value = totalPages.value }

  /**
   * 跳转到上一页
   *
   * 如果当前页大于 1，则页码减 1
   * 如果已经在首页，则不做任何操作
   */
  const goToPrev = () => { if (page.value > 1) page.value-- }

  /**
   * 跳转到下一页
   *
   * 如果当前页小于总页数，则页码加 1
   * 如果已经在末页，则不做任何操作
   */
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
