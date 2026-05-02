<template>
    <div class="comment-form">
        <div class="comment-form-wrapper">
            <el-avatar :size="36" :src="user?.avatar" class="user-avatar">
                {{ userInitial }}
            </el-avatar>
            
            <div class="comment-form-content">
                <div v-if="editor" class="rich-toolbar">
                    <el-tooltip content="加粗 (Ctrl+B)" placement="top">
                        <el-button 
                            link 
                            class="tool-btn" 
                            :class="{ 'is-active': editor.isActive('bold') }"
                            @click="editor.chain().focus().toggleBold().run()"
                        >
                            <svg width="1.1em" height="1.1em" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M15.6 10.79c.97-.67 1.65-1.77 1.65-2.79 0-2.26-1.75-4-4-4H7v14h7.04c2.09 0 3.71-1.7 3.71-3.79 0-1.52-.86-2.82-2.15-3.42zM10 6.5h3c.83 0 1.5.67 1.5 1.5s-.67 1.5-1.5 1.5h-3v-3zm3.5 9H10v-3h3.5c.83 0 1.5.67 1.5 1.5s-.67 1.5-1.5 1.5z"/>
                            </svg>
                        </el-button>
                    </el-tooltip>
                    
                    <el-tooltip content="斜体 (Ctrl+I)" placement="top">
                        <el-button 
                            link 
                            class="tool-btn"
                            :class="{ 'is-active': editor.isActive('italic') }"
                            @click="editor.chain().focus().toggleItalic().run()"
                        >
                            <svg width="1.1em" height="1.1em" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M10 4v3h2.21l-3.42 8H6v3h8v-3h-2.21l3.42-8H18V4z"/>
                            </svg>
                        </el-button>
                    </el-tooltip>
                    
                    <div class="toolbar-divider"></div>
                    
                    <el-tooltip content="代码块" placement="top">
                        <el-button 
                            link 
                            class="tool-btn"
                            :class="{ 'is-active': editor.isActive('codeBlock') }"
                            @click="editor.chain().focus().toggleCodeBlock().run()"
                        >
                            <svg width="1.1em" height="1.1em" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/>
                            </svg>
                        </el-button>
                    </el-tooltip>
                    
                    <el-tooltip content="链接" placement="top">
                        <el-button 
                            link 
                            class="tool-btn"
                            :class="{ 'is-active': editor.isActive('link') }"
                            @click="showLinkDialog"
                        >
                            <svg width="1.1em" height="1.1em" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"/>
                            </svg>
                        </el-button>
                    </el-tooltip>
                    
                    <el-tooltip content="移除链接" placement="top" v-if="editor.isActive('link')">
                        <el-button 
                            link 
                            class="tool-btn"
                            @click="editor.chain().focus().unsetLink().run()"
                        >
                            <svg width="1.1em" height="1.1em" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M17 7h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1 0 1.43-.98 2.63-2.31 3l1.46 1.44C20.88 15.61 22 13.95 22 12c0-2.76-2.24-5-5-5zm-1 4h-2.19l2 2H16zM2 4.27l3.11 3.11C3.29 8.12 2 9.91 2 12c0 2.76 2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1 0-1.59 1.21-2.9 2.76-3.07L8.73 11H8v2h2.73L13 15.27V17h1.73l4.01 4L20 19.74 3.27 3 2 4.27z"/>
                            </svg>
                        </el-button>
                    </el-tooltip>
                    
                    <div class="toolbar-divider"></div>
                    
                    <el-popover placement="top-start" :width="300" trigger="click">
                        <template #reference>
                            <el-button link class="tool-btn" title="选择表情">
                                <svg width="1.1em" height="1.1em" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M14.413 14.223a.785.785 0 0 1 1.45.601A4.174 4.174 0 0 1 12 17.4a4.19 4.19 0 0 1-2.957-1.221 4.174 4.174 0 0 1-.906-1.355.785.785 0 1 1 1.449-.601 2.604 2.604 0 0 0 1.413 1.41 2.621 2.621 0 0 0 2.849-.566c.242-.242.434-.529.565-.844ZM8.6 8.77a1.308 1.308 0 1 1 0 2.615 1.308 1.308 0 0 1 0-2.615ZM15.4 8.77a1.308 1.308 0 1 1 0 2.615 1.308 1.308 0 0 1 0-2.615Z"/>
                                    <path fill-rule="evenodd" d="M12 1.573c5.758 0 10.427 4.669 10.427 10.427S17.758 22.427 12 22.427 1.573 17.758 1.573 12 6.242 1.573 12 1.573Zm0 1.746a8.681 8.681 0 1 0 .001 17.362A8.681 8.681 0 0 0 12 3.32Z" clip-rule="evenodd"/>
                                </svg>
                            </el-button>
                        </template>
                        
                        <div class="emoji-picker">
                            <div class="emoji-list">
                                <span 
                                    v-for="emoji in emojis" 
                                    :key="emoji" 
                                    class="emoji-item"
                                    @click="insertEmoji(emoji)"
                                >
                                    {{ emoji }}
                                </span>
                            </div>
                        </div>
                    </el-popover>
                </div>
                
                <div class="editor-wrapper">
                    <editor-content :editor="editor" class="comment-editor" />
                </div>
                
                <div class="comment-form-footer">
                    <div class="format-hint">
                        支持 <strong>加粗</strong>、<em>斜体</em>、代码块、链接
                    </div>
                    
                    <div class="comment-form-actions">
                        <span class="char-count" :class="{ 'is-exceed': contentLength > 2000 }">{{ contentLength }}/2000</span>
                        <el-button 
                            type="primary" 
                            @click="handleSubmit"
                            :loading="loading"
                            :disabled="!canSubmit"
                        >
                            发布
                        </el-button>
                    </div>
                </div>
            </div>
        </div>
        
        <el-dialog v-model="linkDialogVisible" title="插入链接" width="400px">
            <el-form label-width="80px">
                <el-form-item label="链接地址">
                    <el-input v-model="linkUrl" placeholder="https://example.com" />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="linkDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="insertLink">插入</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
import { computed, ref, watch, onBeforeUnmount } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Link from '@tiptap/extension-link'

const props = defineProps({
    content: {
        type: String,
        default: ''
    },
    user: {
        type: Object,
        default: () => ({})
    },
    emojis: {
        type: Array,
        default: () => []
    },
    loading: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['update:content', 'submit'])

const linkDialogVisible = ref(false)
const linkUrl = ref('')

const editor = useEditor({
    content: props.content,
    extensions: [
        StarterKit.configure({
            heading: false,
            bulletList: false,
            orderedList: false,
            blockquote: false,
            horizontalRule: false,
            code: false,
        }),
        Link.configure({
            openOnClick: false,
            HTMLAttributes: {
                target: '_blank',
                rel: 'noopener noreferrer',
            },
        }),
    ],
    onUpdate: ({ editor }) => {
        const html = editor.getHTML()
        emit('update:content', html)
    },
})

watch(() => props.content, (newValue) => {
    if (editor.value && editor.value.getHTML() !== newValue) {
        editor.value.commands.setContent(newValue, false)
    }
})

const userInitial = computed(() => {
    return props.user?.username?.charAt(0)?.toUpperCase() || 'U'
})

const contentLength = computed(() => {
    if (!editor.value) return 0
    return editor.value.getText().length
})

const canSubmit = computed(() => {
    if (!editor.value) return false
    const text = editor.value.getText().trim()
    return text.length > 0 && contentLength.value <= 2000
})

const showLinkDialog = () => {
    linkUrl.value = ''
    linkDialogVisible.value = true
}

const insertLink = () => {
    if (!linkUrl.value.trim()) return
    
    editor.value
        .chain()
        .focus()
        .extendMarkRange('link')
        .setLink({ href: linkUrl.value })
        .run()
    
    linkDialogVisible.value = false
    linkUrl.value = ''
}

const insertEmoji = (emoji) => {
    editor.value
        .chain()
        .focus()
        .insertContent(emoji)
        .run()
}

const handleSubmit = () => {
    if (!canSubmit.value) return
    const html = editor.value.getHTML()
    emit('submit', html)
}

onBeforeUnmount(() => {
    editor.value?.destroy()
})
</script>

<style scoped>
.comment-form {
    margin-bottom: 32px;
}

.comment-form-wrapper {
    display: flex;
    gap: 12px;
    padding: 20px;
    background: var(--bg-secondary);
    border-radius: var(--radius-lg);
}

.user-avatar {
    flex-shrink: 0;
    border-radius: var(--radius-sm) !important;
    border: 2px solid var(--border-light);
}

.comment-form-content {
    flex: 1;
    min-width: 0;
}

.rich-toolbar {
    display: flex;
    align-items: center;
    gap: 4px;
    margin-bottom: 8px;
    padding: 6px 8px;
    background: var(--bg-tertiary);
    border-radius: var(--radius-sm);
}

.tool-btn {
    padding: 6px 8px;
    color: var(--text-tertiary);
    transition: all var(--transition-fast);
    border-radius: var(--radius-xs);
}

.tool-btn:hover {
    color: var(--primary-color);
    background: var(--bg-secondary);
}

.tool-btn.is-active {
    color: var(--primary-color);
    background: var(--bg-secondary);
}

.toolbar-divider {
    width: 1px;
    height: 16px;
    background: var(--border-color);
    margin: 0 4px;
}

.editor-wrapper {
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    background: var(--card-bg);
    margin-bottom: 12px;
}

.comment-editor {
    padding: 12px;
    min-height: 80px;
    max-height: 240px;
    overflow-y: auto;
}

.comment-editor :deep(.tiptap) {
    outline: none;
    min-height: 56px;
    color: var(--text-primary);
}

.comment-editor :deep(.tiptap p) {
    margin: 0 0 8px 0;
    color: var(--text-primary);
}

.comment-editor :deep(.tiptap p:last-child) {
    margin-bottom: 0;
}

.comment-editor :deep(.tiptap strong) {
    font-weight: 600;
}

.comment-editor :deep(.tiptap em) {
    font-style: italic;
}

.comment-editor :deep(.tiptap a) {
    color: var(--primary-color);
    text-decoration: underline;
    cursor: pointer;
}

.comment-editor :deep(.tiptap a:hover) {
    text-decoration: none;
}

.comment-editor :deep(.tiptap pre) {
    background: var(--bg-tertiary);
    border-radius: var(--radius-sm);
    padding: 12px 16px;
    overflow-x: auto;
    margin: 8px 0;
    border: 1px solid var(--border-color);
}

.comment-editor :deep(.tiptap pre code) {
    font-family: 'Fira Code', 'Consolas', monospace;
    font-size: 13px;
    background: transparent;
    padding: 0;
    color: var(--text-primary);
}

.comment-editor :deep(.tiptap p.is-editor-empty:first-child::before) {
    color: var(--text-placeholder);
    content: attr(data-placeholder);
    float: left;
    height: 0;
    pointer-events: none;
}

[data-theme="dark"] .editor-wrapper {
    border-color: var(--border-color);
}

[data-theme="dark"] .comment-editor :deep(.tiptap pre) {
    background: var(--bg-tertiary);
    border-color: var(--border-dark);
}

[data-theme="dark"] .rich-toolbar {
    background: var(--bg-tertiary);
}

[data-theme="dark"] .tool-btn:hover,
[data-theme="dark"] .tool-btn.is-active {
    background: var(--bg-secondary);
}

[data-theme="dark"] .emoji-item:hover {
    background: var(--bg-secondary);
}

[data-theme="dark"] .el-dialog {
    --el-dialog-bg-color: var(--card-bg);
    --el-dialog-title-font-size: 16px;
}

[data-theme="dark"] .el-dialog .el-input__wrapper {
    background: var(--bg-secondary);
    box-shadow: 0 0 0 1px var(--border-color) inset;
}

[data-theme="dark"] .el-dialog .el-input__inner {
    color: var(--text-primary);
}

[data-theme="dark"] .el-dialog .el-form-item__label {
    color: var(--text-secondary);
}

.comment-form-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.format-hint {
    font-size: 12px;
    color: var(--text-tertiary);
}

.format-hint strong {
    font-weight: 600;
}

.comment-form-actions {
    display: flex;
    align-items: center;
    gap: 12px;
}

.char-count {
    font-size: 13px;
    color: var(--text-tertiary);
}

.char-count.is-exceed {
    color: var(--danger-color);
}

.emoji-picker {
    padding: 12px;
}

.emoji-list {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 8px;
}

.emoji-item {
    font-size: 20px;
    cursor: pointer;
    padding: 6px;
    border-radius: var(--radius-xs);
    transition: all var(--transition-fast);
    display: flex;
    align-items: center;
    justify-content: center;
}

.emoji-item:hover {
    background: var(--bg-tertiary);
    transform: scale(1.2);
}

@media (max-width: 768px) {
    .comment-form-wrapper {
        padding: 16px;
        gap: 8px;
    }
    
    .comment-form-footer {
        flex-wrap: wrap;
        gap: 8px;
    }
    
    .format-hint {
        display: none;
    }
}
</style>
