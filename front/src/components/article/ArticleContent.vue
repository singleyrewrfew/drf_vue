<template>
  <div class="article-content-wrapper">
    <div v-if="coverImage" class="article-cover">
      <img :src="coverImage" :alt="title" loading="lazy" />
    </div>

    <div ref="contentRef" class="article-body markdown-body" v-html="renderedContent"></div>

    <div v-if="isLoading" class="content-loading">
      <el-skeleton :rows="10" animated />
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, nextTick } from 'vue'
import { renderMarkdown } from '@/utils/markdown'

const props = defineProps({
  content: {
    type: String,
    default: ''
  },
  coverImage: {
    type: String,
    default: ''
  },
  title: {
    type: String,
    default: ''
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

const contentRef = ref(null)

const renderedContent = computed(() => {
  if (!props.content) return ''
  return renderMarkdown(props.content)
})

onMounted(() => {
  nextTick(() => {
    addCopyButtons()
  })
})

function addCopyButtons() {
  if (!contentRef.value) return

  const codeBlocks = contentRef.value.querySelectorAll('pre code')

  codeBlocks.forEach(codeBlock => {
    const pre = codeBlock.parentElement
    if (pre && !pre.querySelector('.copy-button')) {
      const button = document.createElement('button')
      button.className = 'copy-button'
      button.textContent = '复制'
      button.addEventListener('click', () => handleCopy(codeBlock, button))
      pre.style.position = 'relative'
      pre.appendChild(button)
    }
  })
}

async function handleCopy(codeElement, button) {
  try {
    const code = codeElement.textContent

    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(code)
    } else {
      const textarea = document.createElement('textarea')
      textarea.value = code
      textarea.style.position = 'fixed'
      textarea.style.left = '-9999px'
      textarea.style.top = '-9999px'
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
    }

    button.textContent = '已复制!'
    button.classList.add('copied')

    setTimeout(() => {
      button.textContent = '复制'
      button.classList.remove('copied')
    }, 2000)
  } catch (err) {
    console.error('复制失败:', err)
    button.textContent = '复制失败'
    setTimeout(() => {
      button.textContent = '复制'
    }, 2000)
  }
}
</script>

<style scoped>
.article-content-wrapper {
  margin-top: 32px;
}

.article-cover {
  width: 100%;
  height: 400px;
  margin-bottom: 32px;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
}

.article-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
}

.article-cover:hover img {
  transform: scale(1.05);
}

@media (max-width: 768px) {
  .article-cover {
    height: 240px;
  }
}

.article-body {
  font-size: 16px;
  line-height: 1.8;
  color: var(--text-primary);
}

.markdown-body {
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4),
.markdown-body :deep(h5),
.markdown-body :deep(h6) {
  margin-top: 32px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
  color: var(--text-primary);
}

.markdown-body :deep(h1) {
  font-size: 32px;
  padding-bottom: 0.3em;
  border-bottom: 2px solid var(--border-light);
}

.markdown-body :deep(h2) {
  font-size: 24px;
  padding-bottom: 0.25em;
  border-bottom: 1px solid var(--border-light);
}

.markdown-body :deep(h3) {
  font-size: 20px;
}

.markdown-body :deep(p) {
  margin-bottom: 16px;
  line-height: 1.8;
}

.markdown-body :deep(a) {
  color: var(--primary-color);
  text-decoration: none;
  transition: all var(--transition-fast);
}

.markdown-body :deep(a:hover) {
  text-decoration: underline;
}

.markdown-body :deep(pre) {
  margin: 24px 0;
  padding: 28px 32px 20px 32px;
  background: var(--bg-secondary, #f8f9fa);
  border-radius: var(--radius-md, 8px);
  overflow-x: auto;
  position: relative;
  border: 1px solid var(--border-light, #e5e7eb);
  box-shadow:
    inset 0 1px 3px rgba(0, 0, 0, 0.04),
    0 1px 3px rgba(0, 0, 0, 0.06);
}

[data-theme='dark'] .markdown-body :deep(pre) {
  background: rgba(30, 31, 35, 0.8);
  border-color: rgba(255, 255, 255, 0.08);
}

.markdown-body :deep(pre code) {
  display: block;
  padding: 0;
  margin: 0;
  font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, 'Liberation Mono', Menlo, monospace;
  font-size: 13.5px;
  line-height: 1.7;
  color: var(--text-primary, #1f2328);
  tab-size: 2;
  word-break: normal;
  white-space: pre;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
}

[data-theme='dark'] .markdown-body :deep(pre code) {
  color: #e6edf3;
}

.markdown-body :deep(code) {
  font-family: var(--font-mono);
  font-size: 14px;
}

.markdown-body :deep(:not(pre) > code) {
  padding: 4px 8px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-xs);
}

.markdown-body :deep(blockquote) {
  margin: 16px 0;
  padding: 12px 16px;
  border-left: 4px solid var(--primary-color);
  background: var(--bg-secondary);
  color: var(--text-secondary);
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  margin: 16px 0;
  padding-left: 24px;
}

.markdown-body :deep(li) {
  margin-bottom: 8px;
}

.markdown-body :deep(table) {
  width: 100%;
  margin: 16px 0;
  border-collapse: separate;
  border-spacing: 0;
  border-radius: var(--radius-md, 8px);
  overflow: hidden;
  border: 1px solid var(--border-color);
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  padding: 12px;
  border: 1px solid var(--border-color);
  text-align: left;
}

.markdown-body :deep(th) {
  background: var(--bg-secondary);
  font-weight: 600;
  color: var(--text-primary);
}

.markdown-body :deep(tr:nth-child(even)) {
  background: var(--bg-secondary);
}

.markdown-body :deep(img) {
  max-width: 100%;
  height: auto;
  margin: 16px 0;
  border-radius: var(--radius-md);
}

.markdown-body :deep(hr) {
  margin: 32px 0;
  border: none;
  border-top: 2px solid var(--border-light);
}

.markdown-body :deep(.copy-button) {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 6px 14px;
  font-size: 12px;
  font-weight: 500;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: var(--text-secondary, #6b7280);
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid var(--border-light, #e5e7eb);
  border-radius: 6px;
  cursor: pointer;
  opacity: 0;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 10;
  backdrop-filter: blur(8px);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

[data-theme='dark'] .markdown-body :deep(.copy-button) {
  color: rgba(255, 255, 255, 0.6);
  background: rgba(39, 42, 48, 0.9);
  border-color: rgba(255, 255, 255, 0.1);
}

.markdown-body :deep(pre:hover .copy-button) {
  opacity: 1;
}

.markdown-body :deep(.copy-button:hover) {
  color: var(--primary-color);
  background: white;
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow:
    0 4px 12px rgba(var(--primary-rgb), 0.15),
    0 2px 4px rgba(0, 0, 0, 0.06);
}

.markdown-body :deep(.copy-button.copied) {
  color: #16a34a;
  border-color: #16a34a;
  background: #f0fdf4;
}

[data-theme='dark'] .markdown-body :deep(.copy-button.copied) {
  color: #4ade80;
  border-color: #4ade80;
  background: rgba(22, 163, 74, 0.15);
}

.markdown-body :deep(.copy-button.copied) {
  background: #67c23a;
}

.content-loading {
  margin-top: 32px;
}
</style>
