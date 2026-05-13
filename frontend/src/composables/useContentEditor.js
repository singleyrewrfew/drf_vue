import {ref, watch, onUnmounted, computed} from 'vue'
import {useThemeStore} from '@/stores/theme'
import {useRoute} from 'vue-router'
import {logger} from '@/utils/logger.js'

const DRAFT_KEY_PREFIX = 'content_draft_'

function getDraftKey(route) {
    return route.params.id ? `${DRAFT_KEY_PREFIX}${route.params.id}` : `${DRAFT_KEY_PREFIX}new`
}

function saveDraftToStorage(key, data) {
    try { 
        const jsonStr = JSON.stringify({...data, savedAt: Date.now()})
        localStorage.setItem(key, jsonStr)
        return true
    } catch (e) {
        logger.warn('草稿保存失败', e.message || e)
        if (e.name === 'QuotaExceededError') {
            logger.error('本地存储空间已满，建议清理旧草稿或减少内容长度')
        }
        return false
    }
}

function loadDraftFromStorage(key) {
    try {
        const raw = localStorage.getItem(key)
        if (!raw) return null
        const data = JSON.parse(raw)
        if (Date.now() - data.savedAt > 7 * 24 * 60 * 60 * 1000) { localStorage.removeItem(key); return null }
        return data
    } catch { return null }
}

export function useContentEditor(formRef) {
    const route = useRoute()
    const themeStore = useThemeStore()

    const editorLoaded = ref(false)
    const showPreview = ref(false)
    const previewTheme = ref('github')
    const codeTheme = ref('github')
    const editorHeight = ref('500px')
    const autoSaveStatus = ref('')
    const autoSaveTimer = ref(null)
    const lastSaveContent = ref('')
    const hasDraft = ref(false)
    const draftData = ref(null)
    const saveVersion = ref(0)

    const draftKey = computed(() => getDraftKey(route))

    const editorThemeClass = () => ({'md-editor-dark': themeStore.theme === 'dark'})

    const toolbars = [
        'bold', 'underline', 'italic', '-', 'title', 'strikeThrough', 'quote',
        'unorderedList', 'orderedList', '-', 'codeRow', 'code', 'link', 'image',
        'table', '-', 'revoke', 'next', '=', 'pageFullscreen', 'fullscreen', 'preview',
    ]

    const updateEditorTheme = () => {
        const isDark = themeStore.theme === 'dark'
        previewTheme.value = isDark ? 'mk-cute' : 'github'
        codeTheme.value = isDark ? 'one-dark' : 'github'
    }

    const getFormValue = () => {
        if (!formRef) return {}
        const f = typeof formRef === 'object' && 'value' in formRef ? formRef.value : formRef
        return f || {}
    }

    const triggerAutoSave = () => {
        if (autoSaveTimer.value) clearTimeout(autoSaveTimer.value)
        
        const currentVersion = ++saveVersion.value
        
        const executeSave = () => {
            const f = getFormValue()
            const content = f.content || ''
            
            if (!content || content.length < 10) {
                if (currentVersion === saveVersion.value) {
                    autoSaveTimer.value = setTimeout(executeSave, 5000)
                }
                return
            }

            if (currentVersion !== saveVersion.value) {
                return
            }

            if (content === lastSaveContent.value) {
                if (currentVersion === saveVersion.value) {
                    autoSaveTimer.value = setTimeout(executeSave, 5000)
                }
                return
            }

            autoSaveStatus.value = 'saving'

            let title = f.title || ''
            if (!title && content) {
                title = content.substring(0, 50).replace(/\n/g, ' ').trim()
            }

            const draftDataToSave = {
                title,
                slug: f.slug || '',
                summary: f.summary || '',
                content,
                category: f.category || null,
                tags: f.tags || [],
                cover_image: f.cover_image || '',
                status: f.status || 'draft',
                is_top: f.is_top || false,
            }

            const saved = saveDraftToStorage(draftKey.value, draftDataToSave)
            if (!saved) {
                autoSaveStatus.value = ''
                logger.warn('草稿自动保存失败，内容可能过大')
                return
            }
            
            lastSaveContent.value = content
            autoSaveStatus.value = 'local'
            
            setTimeout(() => {
                if (autoSaveStatus.value === 'local') {
                    autoSaveStatus.value = ''
                }
            }, 3000)

            if (currentVersion === saveVersion.value) {
                autoSaveTimer.value = setTimeout(executeSave, 5000)
            }
        }
        
        autoSaveTimer.value = setTimeout(executeSave, 5000)
    }

    const handleContentChange = (value) => {
        if (!autoSaveTimer.value) {
            const content = value || getFormValue().content || ''
            if (content && content.length >= 10) {
                triggerAutoSave()
            }
        }
    }

    const initLastContent = (content) => {
        lastSaveContent.value = content || ''
    }

    const checkLocalDraft = () => {
        const data = loadDraftFromStorage(draftKey.value)
        if (data && !route.params.id) {
            hasDraft.value = true
            draftData.value = data
            return true
        }
        hasDraft.value = false
        draftData.value = null
        return false
    }

    const restoreDraft = () => {
        if (!draftData.value) return
        const f = getFormValue()
        Object.assign(f, {
            title: draftData.value.title || '',
            slug: draftData.value.slug || '',
            summary: draftData.value.summary || '',
            content: draftData.value.content || '',
            category: draftData.value.category || null,
            tags: draftData.value.tags || [],
            cover_image: draftData.value.cover_image || '',
            status: draftData.value.status || 'draft',
            is_top: draftData.value.is_top || false,
        })
        initLastContent(f.content || '')
        hasDraft.value = false
        draftData.value = null
    }

    const discardDraft = () => {
        localStorage.removeItem(draftKey.value)
        hasDraft.value = false
        draftData.value = null
    }

    const clearDraftStorage = () => {
        localStorage.removeItem(draftKey.value)
    }

    watch(() => themeStore.theme, updateEditorTheme)

    onUnmounted(() => {
        if (autoSaveTimer.value) clearTimeout(autoSaveTimer.value)
    })

    return {
        editorLoaded,
        showPreview,
        previewTheme,
        codeTheme,
        editorHeight,
        autoSaveStatus,
        toolbars,
        editorThemeClass,
        handleContentChange,
        triggerAutoSave,
        initLastContent,
        hasDraft,
        draftData,
        checkLocalDraft,
        restoreDraft,
        discardDraft,
        clearDraftStorage,
    }
}
