<template>
    <div class="article-content-wrapper">
        <!-- 封面图 -->
        <div v-if="coverImage" class="article-cover">
            <img :src="coverImage" :alt="title" loading="lazy"/>
        </div>
        
        <!-- Markdown 内容 -->
        <div 
            class="article-body markdown-body" 
            v-html="renderedContent"
        ></div>
        
        <!-- 加载占位符 -->
        <div v-if="isLoading" class="content-loading">
            <el-skeleton :rows="10" animated/>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'

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

// 配置 marked
marked.setOptions({
    gfm: true,
    breaks: true,
    highlight: function(code, lang) {
        if (lang && hljs.getLanguage(lang)) {
            try {
                return hljs.highlight(code, { language: lang }).value
            } catch (e) {
                console.error('Highlight error:', e)
            }
        }
        return code
    }
})

const renderedContent = computed(() => {
    if (!props.content) return ''
    return marked.parse(props.content)
})
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

/* Markdown 样式 */
.markdown-body {
    /* 标题 */
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

/* 段落 */
.markdown-body :deep(p) {
    margin-bottom: 16px;
    line-height: 1.8;
}

/* 链接 */
.markdown-body :deep(a) {
    color: var(--primary-color);
    text-decoration: none;
    transition: all var(--transition-fast);
}

.markdown-body :deep(a:hover) {
    text-decoration: underline;
}

/* 代码块 */
.markdown-body :deep(pre) {
    margin: 16px 0;
    padding: 16px;
    background: var(--bg-secondary);
    border-radius: var(--radius-md);
    overflow: auto;
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

/* 引用 */
.markdown-body :deep(blockquote) {
    margin: 16px 0;
    padding: 12px 16px;
    border-left: 4px solid var(--primary-color);
    background: var(--bg-secondary);
    color: var(--text-secondary);
}

/* 列表 */
.markdown-body :deep(ul),
.markdown-body :deep(ol) {
    margin: 16px 0;
    padding-left: 24px;
}

.markdown-body :deep(li) {
    margin-bottom: 8px;
}

/* 表格 */
.markdown-body :deep(table) {
    width: 100%;
    margin: 16px 0;
    border-collapse: collapse;
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
}

.markdown-body :deep(tr:nth-child(even)) {
    background: var(--bg-secondary);
}

/* 图片 */
.markdown-body :deep(img) {
    max-width: 100%;
    height: auto;
    margin: 16px 0;
    border-radius: var(--radius-md);
}

/* 分割线 */
.markdown-body :deep(hr) {
    margin: 32px 0;
    border: none;
    border-top: 2px solid var(--border-light);
}

.content-loading {
    margin-top: 32px;
}
</style>
