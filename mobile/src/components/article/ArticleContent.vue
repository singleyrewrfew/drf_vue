<template>
    <div class="article-body markdown-body" v-html="renderedContent"></div>

    <div v-if="tags?.length" class="article-tags">
        <router-link
            v-for="tag in tags"
            :key="tag.id || tag"
            :to="`/tag/${tag.slug || tag.id || tag}`"
            class="tag"
        >
            {{ tag.name || tag }}
        </router-link>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'

const props = defineProps({
    content: {
        type: String,
        required: true
    },
    tags: {
        type: Array,
        default: () => []
    }
})

// 配置 marked 渲染器
let headingIdCounter = 0
const renderer = new marked.Renderer()

renderer.image = ({href, title, text}) => {
    return `<img src="${href}" alt="${text || ''}" loading="lazy" />`
}

renderer.code = ({text, lang}) => {
    const code = text || ''
    let language = lang || ''
    let highlighted

    if (language && hljs.getLanguage(language)) {
        highlighted = hljs.highlight(code, {language}).value
    } else {
        highlighted = hljs.highlightAuto(code).value
        language = highlighted.language || 'plaintext'
    }

    return `<pre class="code-block"><code class="hljs language-${language}">${highlighted}</code></pre>`
}

renderer.heading = ({text, depth}) => {
    const id = `heading-${headingIdCounter++}`
    return `<h${depth} id="${id}">${text}</h${depth}>`
}

marked.setOptions({renderer})

const renderedContent = computed(() => {
    if (!props.content) {
        console.warn('ArticleContent: content is empty')
        return '<p>暂无内容</p>'
    }
    headingIdCounter = 0
    return marked(props.content)
})

// 暴露 tocItems 给父组件
const tocItems = computed(() => {
    const items = []
    const html = renderedContent.value
    const headingRegex = /<h([1-6]) id="([^"]+)">([^<]+)<\/h\1>/g
    let match
    while ((match = headingRegex.exec(html)) !== null) {
        items.push({
            level: parseInt(match[1]),
            id: match[2],
            text: match[3]
        })
    }
    return items
})

defineExpose({
    tocItems
})
</script>

<style scoped>
.article-body {
    padding: 16px;
    padding-bottom: 0;
}

.article-tags {
    padding: 16px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.markdown-body {
    font-size: 15px;
    line-height: 1.8;
    color: var(--text-primary);
    word-break: break-word;
}

/* Markdown 样式保持不变... */
.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4),
.markdown-body :deep(h5),
.markdown-body :deep(h6) {
    margin-top: 24px;
    margin-bottom: 12px;
    font-weight: 600;
    line-height: 1.4;
    color: var(--text-primary);
}

.markdown-body :deep(h1) { font-size: 20px; }
.markdown-body :deep(h2) { font-size: 18px; }
.markdown-body :deep(h3) { font-size: 16px; }
.markdown-body :deep(h4) { font-size: 15px; }

.markdown-body :deep(p) { margin-bottom: 16px; }
.markdown-body :deep(a) { color: var(--primary-color); }
.markdown-body :deep(img) { max-width: 100%; border-radius: var(--radius-md); margin: 12px 0; }

.markdown-body :deep(.code-block) {
    background: #282c34;
    padding: 16px;
    border-radius: var(--radius-md);
    overflow-x: auto;
    margin: 16px 0;
}

.markdown-body :deep(.code-block code) {
    font-family: var(--font-mono);
    font-size: 13px;
    line-height: 1.6;
    color: #abb2bf;
}
</style>
