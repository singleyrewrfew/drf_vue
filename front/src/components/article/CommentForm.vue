<template>
  <div class="comment-form">
    <div class="comment-form-wrapper">
      <el-avatar :size="32" :src="user?.avatar" class="user-avatar">
        {{ userInitial }}
      </el-avatar>

      <div class="comment-form-content">
        <div class="rich-toolbar">
          <el-tooltip content="加粗 (Ctrl+B)" placement="top">
            <button
              type="button"
              class="tool-btn"
              :class="{ 'is-active': isBold }"
              @click="execCommand('bold')"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M6 4h8a4 4 0 0 1 4 4 4 4 0 0 1-4 4H6z"/>
                <path d="M6 12h9a4 4 0 0 1 4 4 4 4 0 0 1-4 4H6z"/>
              </svg>
            </button>
          </el-tooltip>

          <el-tooltip content="斜体 (Ctrl+I)" placement="top">
            <button
              type="button"
              class="tool-btn"
              :class="{ 'is-active': isItalic }"
              @click="execCommand('italic')"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="19" y1="4" x2="10" y2="4"/>
                <line x1="14" y1="20" x2="5" y2="20"/>
                <line x1="15" y1="4" x2="9" y2="20"/>
              </svg>
            </button>
          </el-tooltip>

          <span class="toolbar-divider"></span>

          <el-tooltip content="代码块" placement="top">
            <button type="button" class="tool-btn" @click="insertCodeBlock">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="16 18 22 12 16 6"/>
                <polyline points="8 6 2 12 8 18"/>
              </svg>
            </button>
          </el-tooltip>

          <el-tooltip content="链接" placement="top">
            <button type="button" class="tool-btn" @click="showLinkDialog">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
              </svg>
            </button>
          </el-tooltip>

          <span class="toolbar-divider"></span>

          <EmojiPicker :emojis="emojis" @select="insertEmoji" />
        </div>

        <div class="editor-wrapper">
          <CustomEditor ref="editorRef" v-model="contentValue" placeholder="写下你的想法..." @update:cursor="updateCursorState" />
        </div>

        <div class="comment-form-footer">
          <span class="char-count" :class="{ 'is-exceed': contentLength > 2000 }">{{ contentLength }}/2000</span>
          <button
            type="button"
            class="submit-btn"
            :class="{ disabled: !canSubmit, loading: loading }"
            :disabled="!canSubmit || loading"
            @click="handleSubmit"
          >
            <span v-if="!loading">发布</span>
            <span v-else>发送中...</span>
          </button>
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

    <el-dialog v-model="codeDialogVisible" title="插入代码块" width="500px">
      <div class="code-dialog-content">
        <el-input
          v-model="codeContent"
          type="textarea"
          :rows="6"
          placeholder="请输入代码内容..."
          class="code-textarea"
        />
      </div>
      <template #footer>
        <el-button @click="codeDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmCodeBlock">插入</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import EmojiPicker from './EmojiPicker.vue'
import CustomEditor from './CustomEditor.vue'

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
const codeDialogVisible = ref(false)
const codeContent = ref('')
const contentValue = ref(props.content)
const editorRef = ref(null)
const isBold = ref(false)
const isItalic = ref(false)

const updateCursorState = () => {
  setTimeout(() => {
    isBold.value = document.queryCommandState('bold')
    isItalic.value = document.queryCommandState('italic')
  }, 0)
}

watch(
  () => props.content,
  val => {
    if (val !== contentValue.value) {
      contentValue.value = val
    }
  }
)

watch(contentValue, val => {
  emit('update:content', val)
})

const userInitial = computed(() => {
  return props.user?.username?.charAt(0)?.toUpperCase() || 'U'
})

const contentLength = computed(() => {
  const html = contentValue.value || ''
  const div = document.createElement('div')
  div.innerHTML = html
  return (div.textContent || '').length
})

const canSubmit = computed(() => {
  const text = (contentValue.value || '').replace(/<[^>]*>/g, '').trim()
  return text.length > 0 && contentLength.value <= 2000
})

const execCommand = command => {
  editorRef.value?.restoreSelection()

  setTimeout(() => {
    document.execCommand(command, false, null)

    isBold.value = document.queryCommandState('bold')
    isItalic.value = document.queryCommandState('italic')

    syncContent()
  }, 10)
}

const insertCodeBlock = () => {
  const selection = window.getSelection()
  const selectedText = selection ? selection.toString() : ''
  codeContent.value = selectedText
  codeDialogVisible.value = true
}

const confirmCodeBlock = () => {
  if (!codeContent.value.trim()) return

  editorRef.value?.restoreSelection()

  setTimeout(() => {
    const codeHtml = `<div class="code-block"><code>${escapeHtml(codeContent.value)}</code></div>`
    document.execCommand('insertHTML', false, codeHtml)

    codeDialogVisible.value = false
    codeContent.value = ''
    syncContent()
  }, 10)
}

const escapeHtml = text => {
  const div = document.createElement('div')
  div.textContent = text
  return div.innerHTML
}

const showLinkDialog = () => {
  linkUrl.value = ''
  linkDialogVisible.value = true
}

const insertLink = () => {
  if (!linkUrl.value.trim()) return

  editorRef.value?.restoreSelection()

  setTimeout(() => {
    const selection = window.getSelection()
    if (selection && selection.rangeCount) {
      const selectedText = selection.toString() || linkUrl.value
      const linkEl = `<a href="${linkUrl.value}" target="_blank" rel="noopener noreferrer">${selectedText}</a>`
      document.execCommand('insertHTML', false, linkEl)
    }

    linkDialogVisible.value = false
    linkUrl.value = ''
    syncContent()
  }, 10)
}

const insertEmoji = emoji => {
  editorRef.value?.restoreSelection()

  setTimeout(() => {
    document.execCommand('insertText', false, emoji)
    syncContent()
  }, 10)
}

const syncContent = () => {
  if (editorRef.value) {
    contentValue.value = editorRef.value.getHTML()
  }
}

const handleSubmit = () => {
  if (!canSubmit.value) return
  const html = editorRef.value?.getHTML() || ''
  emit('submit', html)
}
</script>

<style scoped>
.comment-form {
  margin-bottom: 24px;
}

.comment-form-wrapper {
  display: flex;
  gap: 10px;
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-light, transparent);
}

.user-avatar {
  flex-shrink: 0;
  border-radius: var(--radius-sm) !important;
}

.comment-form-content {
  flex: 1;
  min-width: 0;
}

.rich-toolbar {
  display: flex;
  align-items: center;
  gap: 2px;
  margin-bottom: 8px;
  padding: 4px 6px;
  background: transparent;
  border-radius: var(--radius-sm);
}

.tool-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 28px;
  color: var(--text-placeholder);
  cursor: pointer;
  border: none;
  border-radius: var(--radius-sm);
  background: transparent;
  transition: all 0.15s ease;
}

.tool-btn:hover {
  color: var(--primary-color);
  background: var(--primary-bg, rgba(45, 90, 74, 0.08));
}

.tool-btn.is-active {
  color: var(--primary-color);
  background: var(--primary-bg, rgba(45, 90, 74, 0.12));
}

.toolbar-divider {
  width: 1px;
  height: 16px;
  background: var(--border-color, rgba(0,0,0,0.08));
  margin: 0 4px;
}

.editor-wrapper {
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  background: var(--card-bg);
  margin-bottom: 10px;
  transition: border-color 0.2s ease;
}

.editor-wrapper:focus-within {
  border-color: var(--primary-color);
}

.comment-form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 2px;
}

.char-count {
  font-size: 12px;
  color: var(--text-placeholder);
  letter-spacing: -0.02em;
}

.char-count.is-exceed {
  color: var(--vermilion-color);
}

.submit-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 7px 18px;
  font-size: 13px;
  font-weight: 500;
  color: #fff;
  cursor: pointer;
  border: none;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--vermilion-color) 0%, #d43d47 100%);
  transition: all 0.2s ease;
  -webkit-tap-highlight-color: transparent;
}

.submit-btn:hover:not(.disabled):not(.loading) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(197, 61, 67, 0.25);
}

.submit-btn:active:not(.disabled):not(.loading) {
  transform: scale(0.97);
}

.submit-btn.disabled {
  opacity: 0.45;
  cursor: not-allowed;
  pointer-events: none;
}

.submit-btn.loading {
  opacity: 0.75;
  cursor: wait;
}

/* 暗色模式适配 */
[data-theme='dark'] .comment-form-wrapper {
  background: var(--bg-tertiary, #252219);
  border-color: var(--border-dark, #3d3830);
}

[data-theme='dark'] .rich-toolbar {
  background: transparent;
}

[data-theme='dark'] .tool-btn {
  color: #71717a;
}

[data-theme='dark'] .tool-btn:hover,
[data-theme='dark'] .tool-btn.is-active {
  color: #5db396;
  background: rgba(93, 179, 150, 0.1);
}

[data-theme='dark'] .toolbar-divider {
  background: #3f3f46;
}

[data-theme='dark'] .editor-wrapper {
  border-color: #3f3f46;
  background: var(--bg-primary, #0d0d0a);
}

[data-theme='dark'] .editor-wrapper:focus-within {
  border-color: #5db396;
}

[data-theme='dark'] .char-count {
  color: #52525b;
}

[data-theme='dark'] .char-count.is-exceed {
  color: var(--dark-vermilion-light, #ef4444);
}

[data-theme='dark'] .submit-btn {
  background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
}

[data-theme='dark'] .submit-btn:hover:not(.disabled):not(.loading) {
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

@media (max-width: 768px) {
  .comment-form-wrapper {
    padding: 12px;
    gap: 8px;
  }

  .submit-btn {
    padding: 6px 16px;
    font-size: 12px;
  }
}

.code-dialog-content {
  padding: 0 4px;
}

.code-textarea :deep(textarea) {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.6;
  background: var(--bg-primary, #fafafa);
  border: 1px solid var(--border-color, #e5e5e5);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  transition: all 0.2s ease;
}

.code-textarea :deep(textarea:focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(45, 90, 74, 0.1);
}

.code-textarea :deep(textarea::placeholder) {
  color: var(--text-placeholder);
}

/* 弹窗统一样式 */
.comment-form :deep(.el-dialog) {
  border-radius: 12px;
  overflow: hidden;
  background: var(--card-bg, #fff);
}

.comment-form :deep(.el-dialog__header) {
  padding: 16px 20px;
  margin: 0;
  border-bottom: 1px solid var(--border-light, rgba(0,0,0,0.06));
  background: var(--card-bg, #fff);
}

.comment-form :deep(.el-dialog__title) {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: 0.02em;
}

.comment-form :deep(.el-dialog__body) {
  padding: 20px;
  background: var(--card-bg, #fff);
}

.comment-form :deep(.el-dialog__footer) {
  padding: 12px 20px 16px;
  border-top: 1px solid var(--border-light, rgba(0,0,0,0.06));
  background: var(--card-bg, #fff);
}

/* 表单输入框 */
.comment-form :deep(.el-input__wrapper),
.comment-form :deep(.el-textarea__inner) {
  background: var(--bg-secondary, #f7f7f7);
  border-color: transparent;
  box-shadow: none;
  transition: all 0.2s ease;
}

.comment-form :deep(.el-input__wrapper:hover),
.comment-form :deep(.el-textarea__inner:hover) {
  background: var(--bg-tertiary, #f0f0f0);
}

.comment-form :deep(.el-input__wrapper.is-focus),
.comment-form :deep(.el-textarea__inner:focus) {
  background: var(--card-bg);
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(197, 61, 67, 0.08);
}

.comment-form :deep(.el-form-item__label) {
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 13px;
}

/* 弹窗按钮 */
.comment-form :deep(.el-dialog__footer .el-button) {
  border-radius: var(--radius-full);
  padding: 8px 18px;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.25s cubic-bezier(0.25, 0.1, 0.25, 1);
}

.comment-form :deep(.el-dialog__footer .el-button--primary) {
  background: linear-gradient(135deg, var(--vermilion-color) 0%, #d43d47 100%);
  border: none;
  color: #fff;
}

.comment-form :deep(.el-dialog__footer .el-button--primary:hover) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(197, 61, 67, 0.25);
}

.comment-form :deep(.el-dialog__close) {
  color: var(--text-placeholder);
  transition: all 0.2s ease;
}

.comment-form :deep(.el-dialog__close:hover) {
  color: var(--vermilion-color);
}

/* 暗色模式 */
[data-theme='dark'] .code-textarea :deep(textarea) {
  background: #18181b;
  border-color: #3f3f46;
  color: #e4e4e7;
}

[data-theme='dark'] .code-textarea :deep(textarea:focus) {
  border-color: #5db396;
  box-shadow: 0 0 0 2px rgba(93, 179, 150, 0.15);
}

[data-theme='dark'] .code-textarea :deep(textarea::placeholder) {
  color: #52525b;
}

[data-theme='dark'] .comment-form :deep(.el-dialog) {
  background: #1a1917;
}

[data-theme='dark'] .comment-form :deep(.el-dialog__header) {
  background: #1a1917;
  border-color: #2d2c28;
}

[data-theme='dark'] .comment-form :deep(.el-dialog__body) {
  background: #1a1917;
}

[data-theme='dark'] .comment-form :deep(.el-dialog__footer) {
  background: #1a1917;
  border-color: #2d2c28;
}

[data-theme='dark'] .comment-form :deep(.el-dialog__title) {
  color: #e4e4e7;
}

[data-theme='dark'] .comment-form :deep(.el-dialog__close) {
  color: #52525b;
}

[data-theme='dark'] .comment-form :deep(.el-dialog__close:hover) {
  color: #ef4444;
}

[data-theme='dark'] .comment-form :deep(.el-input__wrapper),
[data-theme='dark'] .comment-form :deep(.el-textarea__inner) {
  background: #1e1e1c;
  border-color: #3f3f46;
  box-shadow: none;
  color: #e4e4e7;
}

[data-theme='dark'] .comment-form :deep(.el-input__wrapper:hover),
[data-theme='dark'] .comment-form :deep(.el-textarea__inner:hover) {
  background: #262523;
}

[data-theme='dark'] .comment-form :deep(.el-input__wrapper.is-focus),
[data-theme='dark'] .comment-form :deep(.el-textarea__inner:focus) {
  background: #1a1917;
  border-color: #5db396;
  box-shadow: 0 0 0 2px rgba(93, 179, 150, 0.15);
}

[data-theme='dark'] .comment-form :deep(.el-form-item__label) {
  color: #a1a1aa;
}

[data-theme='dark'] .comment-form :deep(.el-dialog__footer .el-button) {
  background: transparent;
  border-color: #3f3f46;
  color: #a1a1aa;
}

[data-theme='dark'] .comment-form :deep(.el-dialog__footer .el-button:hover) {
  border-color: #52525b;
  color: #e4e4e7;
  background: rgba(255, 255, 255, 0.05);
}

[data-theme='dark'] .comment-form :deep(.el-dialog__footer .el-button--primary) {
  background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
  border: none;
  color: #fff;
}

[data-theme='dark'] .comment-form :deep(.el-dialog__footer .el-button--primary:hover) {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(220, 38, 38, 0.35);
}
</style>
