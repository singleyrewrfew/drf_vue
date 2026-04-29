/**
 * 对话框组合式函数
 *
 * 作用：提供可复用的对话框状态管理和操作逻辑
 * 使用：在 Vue 组件中导入并调用 useDialog 或 useConfirmDialog
 *
 * 主要功能：
 *   1. useDialog - 基础对话框管理（打开、关闭、切换、加载状态）
 *   2. useConfirmDialog - 确认对话框管理（支持 Promise 异步确认）
 *
 * 适用场景：
 *   - 表单提交对话框
 *   - 删除确认对话框
 *   - 操作提示对话框
 *   - 任何需要用户确认的场景
 */
import {ref} from 'vue'

/**
 * 基础对话框管理组合式函数
 *
 * 提供对话框的显示/隐藏控制和加载状态管理。
 * 适用于简单的模态框、抽屉等 UI 组件的状态管理。
 *
 * @param {boolean} initialState - 对话框的初始显示状态，默认为 false（隐藏）
 *
 * @returns {Object} 对话框控制对象
 * @returns {Ref<boolean>} returns.visible - 对话框可见性状态（响应式引用）
 * @returns {Ref<boolean>} returns.loading - 加载状态（响应式引用）
 * @returns {Function} returns.open - 打开对话框的方法
 * @returns {Function} returns.close - 关闭对话框的方法（同时重置加载状态）
 * @returns {Function} returns.toggle - 切换对话框显示/隐藏状态的方法
 * @returns {Function} returns.withLoading - 执行异步操作时自动管理加载状态的包装器
 *
 * @example
 * // 基本用法
 * import { useDialog } from '@/composables/useDialog'
 *
 * const { visible, open, close } = useDialog()
 *
 * // 在模板中使用
 * <el-dialog v-model="visible">
 *   <span>对话框内容</span>
 * </el-dialog>
 * <button @click="open">打开对话框</button>
 *
 * @example
 * // 带加载状态的用法
 * const { visible, loading, withLoading, close } = useDialog()
 *
 * const handleSubmit = async () => {
 *   await withLoading(async () => {
 *     await api.submitForm(formData)
 *     close()
 *   })
 * }
 */
export function useDialog(initialState = false) {
    const visible = ref(initialState)
    const loading = ref(false)

    /**
     * 打开对话框
     *
     * 将对话框的可见性状态设置为 true
     */
    const open = () => {
        visible.value = true
    }

    /**
     * 关闭对话框
     *
     * 将对话框的可见性状态设置为 false，
     * 同时重置加载状态为 false
     */
    const close = () => {
        visible.value = false
        loading.value = false
    }

    /**
     * 切换对话框显示状态
     *
     * 如果对话框当前是显示的则隐藏，反之则显示
     */
    const toggle = () => {
        visible.value = !visible.value
    }

    /**
     * 带加载状态的异步操作包装器
     *
     * 在执行异步函数时自动管理加载状态：
     * - 函数开始前设置 loading 为 true
     * - 函数结束后（无论成功或失败）设置 loading 为 false
     *
     * @param {Function} fn - 要执行的异步函数
     *
     * @returns {Promise} 返回异步函数的执行结果
     *
     * @example
     * const handleSubmit = async () => {
     *   await withLoading(async () => {
     *     await api.saveData(data)
     *     ElMessage.success('保存成功')
     *     close()
     *   })
     * }
     *
     * 注意：
     *   - 如果异步函数抛出异常，loading 仍会被重置为 false
     *   - 适合用于表单提交、数据加载等需要显示加载状态的场景
     */
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

/**
 * 确认对话框管理组合式函数
 *
 * 提供基于 Promise 的确认对话框，支持自定义标题、消息和类型。
 * 通过 Promise 机制实现异步的用户确认/取消操作。
 *
 * @returns {Object} 确认对话框控制对象
 * @returns {Ref<boolean>} returns.visible - 对话框可见性状态
 * @returns {Ref<boolean>} returns.loading - 加载状态
 * @returns {Ref<string>} returns.title - 对话框标题
 * @returns {Ref<string>} returns.message - 对话框消息内容
 * @returns {Ref<string>} returns.type - 对话框类型（warning/success/error/info）
 * @returns {Function} returns.show - 显示确认对话框并返回 Promise
 * @returns {Function} returns.confirm - 用户点击确认按钮的处理方法
 * @returns {Function} returns.cancel - 用户点击取消按钮的处理方法
 *
 * @example
 * // 基本用法
 * import { useConfirmDialog } from '@/composables/useDialog'
 *
 * const { show, confirm, cancel } = useConfirmDialog()
 *
 * // 在模板中使用
 * <el-dialog v-model="visible" :title="title">
 *   <span>{{ message }}</span>
 *   <template #footer>
 *     <el-button @click="cancel">取消</el-button>
 *     <el-button type="primary" @click="confirm">确定</el-button>
 *   </template>
 * </el-dialog>
 *
 * @example
 * // 在业务逻辑中使用
 * const handleDelete = async () => {
 *   const confirmed = await show({
 *     title: '删除确认',
 *     message: '确定要删除这条记录吗？此操作不可恢复。',
 *     type: 'warning'
 *   })
 *
 *   if (confirmed) {
 *     await api.deleteRecord(id)
 *     ElMessage.success('删除成功')
 *   }
 * }
 *
 * 工作流程：
 *   1. 调用 show() 显示对话框，返回一个 Promise
 *   2. 用户点击“确认”或“取消”按钮
 *   3. 调用 confirm() 或 cancel() 解析 Promise
 *   4. Promise 返回 true（确认）或 false（取消）
 *   5. 根据返回值执行相应的业务逻辑
 */
export function useConfirmDialog() {
    const visible = ref(false)
    const loading = ref(false)
    const title = ref('')
    const message = ref('')
    const type = ref('warning')
    let resolvePromise = null

    /**
     * 显示确认对话框
     *
     * 配置并显示确认对话框，返回一个 Promise，
     * 该 Promise 会在用户点击确认或取消后被解析。
     *
     * @param {Object} [options={}] - 对话框配置选项
     * @param {string} [options.title='提示'] - 对话框标题
     * @param {string} [options.message='确定执行此操作？'] - 对话框消息内容
     * @param {string} [options.type='warning'] - 对话框类型
     *   - 'warning': 警告类型（默认）
     *   - 'success': 成功类型
     *   - 'error': 错误类型
     *   - 'info': 信息类型
     *
     * @returns {Promise<boolean>} 返回一个 Promise
     *   - 用户点击确认时解析为 true
     *   - 用户点击取消时解析为 false
     *
     * @example
     * const result = await show({
     *   title: '重要提示',
     *   message: '此操作将清空所有数据，是否继续？',
     *   type: 'error'
     * })
     *
     * if (result) {
     *   console.log('用户点击了确认')
     * } else {
     *   console.log('用户点击了取消')
     * }
     *
     * 注意：
     *   - 每次调用 show() 都会创建一个新的 Promise
     *   - 如果在前一个对话框未关闭时再次调用，前一个 Promise 将永远不会被解析
     *   - 建议确保同一时间只显示一个确认对话框
     */
    const show = (options = {}) => {
        title.value = options.title || '提示'
        message.value = options.message || '确定执行此操作？'
        type.value = options.type || 'warning'
        visible.value = true

        return new Promise((resolve) => {
            resolvePromise = resolve
        })
    }

    /**
     * 用户点击确认按钮
     *
     * 关闭对话框并将 Promise 解析为 true，
     * 表示用户确认执行操作
     */
    const confirm = () => {
        visible.value = false
        resolvePromise?.(true)
    }

    /**
     * 用户点击取消按钮
     *
     * 关闭对话框并将 Promise 解析为 false，
     * 表示用户取消操作
     */
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
