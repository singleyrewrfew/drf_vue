import {ref, watch, onUnmounted} from 'vue'

/**
 * 表单草稿自动持久化 Composable
 *
 * 功能：
 *   - watch 表单字段变化 → 防抖写入 localStorage
 *   - 提供 loadDraft / clearDraft / hasDraft 方法
 *   - 仅在非编辑模式下生效（由调用方控制）
 *   - 提交成功后调用 clearDraft() 清除
 *
 * @param {Object} options
 * @param {string} options.storageKey - localStorage 的 key
 * @param {Object} options.formData - reactive 表单对象（watch 目标）
 * @param {number} [options.debounceMs=1500] - 防抖毫秒数
 * @param {boolean} [options.enabled=true] - 是否启用持久化
 *
 * @returns {{ saveDraft: Function, loadDraft: Function, clearDraft: Function, hasDraft: Function }}
 */
export function useDraftPersistence({storageKey, formData, debounceMs = 1500, enabled = true}) {
    let _timer = null

    /** 将当前表单快照写入 localStorage */
    const saveDraft = () => {
        const snapshot = {...formData, savedAt: Date.now()}
        try {
            localStorage.setItem(storageKey, JSON.stringify(snapshot))
        } catch {
            /* 静默失败：localStorage 满 / 不可用 */
        }
    }

    /** 读取草稿快照，无则 null */
    const loadDraft = () => {
        try {
            const raw = localStorage.getItem(storageKey)
            return raw ? JSON.parse(raw) : null
        } catch { return null }
    }

    /** 删除草稿 */
    const clearDraft = () => localStorage.removeItem(storageKey)

    /** 是否存在有效草稿 */
    const hasDraft = (() => {
        const d = loadDraft()
        // 至少有一个有意义的字段才算有效草稿
        if (!d || !d.savedAt) return false
        const keys = Object.keys(d).filter(k =>
            !['savedAt'].includes(k)
        )
        return keys.some(k => {
            const val = d[k]
            if (typeof val === 'string') return !!val.trim()
            if (Array.isArray(val)) return val.length > 0
            return val != null && val !== '' && val !== false
        })
    })()

    // 防抖自动保存
    if (enabled) {
        watch(
            () => ({...formData}),
            () => {
                if (_timer) clearTimeout(_timer)
                _timer = setTimeout(saveDraft, debounceMs)
            },
            { deep: true },
        )
    }

    onUnmounted(() => { if (_timer) clearTimeout(_timer) })

    return {saveDraft, loadDraft, clearDraft, hasDraft}
}
