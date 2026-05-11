<template>
  <div class="custom-editor">
    <div
      ref="editorRef"
      class="editor-content"
      contenteditable="true"
      :placeholder="placeholder"
      @input="onInput"
      @focus="onFocus"
      @keyup="onCursorChange"
      @mouseup="onMouseUp"
      @mousedown="onMouseDown"
    ></div>

    <span v-if="showPlaceholder" class="editor-placeholder">{{ placeholder }}</span>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '写下你的想法...'
  }
})

const emit = defineEmits(['update:modelValue', 'update:cursor'])

const editorRef = ref(null)
const hasContent = ref(false)
const savedSelectionText = ref('')

const showPlaceholder = computed(() => !hasContent.value)

const checkEmpty = () => {
  if (!editorRef.value) return
  const text = editorRef.value.innerText.trim()
  hasContent.value = !!text && text !== '\n'
}

watch(
  () => props.modelValue,
  val => {
    if (editorRef.value && editorRef.value.innerHTML !== val) {
      editorRef.value.innerHTML = val
    }
    checkEmpty()
  },
  { immediate: true }
)

const onMouseDown = () => {
  savedSelectionText.value = ''
}

const onMouseUp = () => {
  const selection = window.getSelection()
  savedSelectionText.value = selection ? selection.toString() : ''
  emit('update:cursor')
}

const onInput = () => {
  const html = editorRef.value.innerHTML
  emit('update:modelValue', html)
  checkEmpty()
  emit('update:cursor')
}

const onFocus = () => {
  emit('update:cursor')
}

const onCursorChange = () => {
  emit('update:cursor')
}

const getHTML = () => {
  return editorRef.value?.innerHTML || ''
}

const getText = () => {
  return editorRef.value?.innerText || ''
}

const getSelectedText = () => {
  return savedSelectionText.value
}

const restoreSelection = () => {
  editorRef.value?.focus()
}

const clear = () => {
  if (editorRef.value) {
    editorRef.value.innerHTML = ''
    emit('update:modelValue', '')
  }
}

defineExpose({ getHTML, getText, getSelectedText, restoreSelection, clear })
</script>

<style scoped>
.custom-editor {
  position: relative;
}

.editor-content {
  display: block;
  padding: 10px 12px;
  min-height: 72px;
  max-height: 200px;
  overflow-y: auto;
  outline: none;
  font-size: 14px;
  line-height: 1.55;
  color: var(--text-primary);
  word-wrap: break-word;
}

.editor-content:focus {
  outline: none;
}

.editor-placeholder {
  position: absolute;
  top: 12px;
  left: 14px;
  font-size: 14px;
  color: var(--text-placeholder);
  pointer-events: none;
  user-select: none;
  line-height: 1.55;
}

/* 编辑器内基础样式 */
.editor-content :deep(p) {
  margin: 0 0 6px 0;
}

.editor-content :deep(p:last-child) {
  margin-bottom: 0;
}

.editor-content :deep(strong) {
  font-weight: 600;
}

.editor-content :deep(em) {
  font-style: italic;
}

.editor-content :deep(a) {
  color: var(--primary-color);
  text-decoration: underline;
  cursor: pointer;
}

.editor-content :deep(div.code-block) {
  display: block;
  margin: 8px 0;
  padding: 10px 12px;
  background: #f5f5f5;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color, rgba(0,0,0,0.1));
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.45;
  overflow-x: auto;
  white-space: pre-wrap !important;
  word-wrap: break-word !important;
  word-break: break-all !important;
}

.editor-content :deep(div.code-block code) {
  background: none;
  padding: 0;
  border: none;
  font-family: inherit;
  font-size: inherit;
  color: var(--text-primary);
  white-space: pre-wrap !important;
  word-wrap: break-word !important;
}

/* 暗色模式 */
[data-theme='dark'] .editor-content {
  color: var(--dark-text, #e4e4e7);
}

[data-theme='dark'] .editor-placeholder {
  color: #52525b;
}

[data-theme='dark'] .editor-content :deep(div.code-block) {
  background: #1e1e1e;
  border-color: #3f3f46;
}

[data-theme='dark'] .editor-content :deep(div.code-block code) {
  color: #d4d4d8;
}
</style>
