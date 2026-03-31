<template>
    <div class="article-page">
        <div class="container">
            <el-row :gutter="24">
                <el-col :span="17">
                    <div class="article-main">
                        <template v-if="loading">
                            <div class="article-skeleton">
                                <el-skeleton animated>
                                    <template #template>
                                        <el-skeleton-item variant="h1" style="width: 80%; margin-bottom: 24px;"/>
                                        <div style="display: flex; gap: 16px; margin-bottom: 24px;">
                                            <el-skeleton-item variant="circle" style="width: 40px; height: 40px;"/>
                                            <div style="flex: 1;">
                                                <el-skeleton-item variant="text"
                                                                  style="width: 30%; margin-bottom: 8px;"/>
                                                <el-skeleton-item variant="text" style="width: 20%;"/>
                                            </div>
                                        </div>
                                        <el-skeleton-item variant="image"
                                                          style="width: 100%; height: 300px; margin-bottom: 24px;"/>
                                        <el-skeleton-item variant="text" style="width: 100%; margin-bottom: 12px;"/>
                                        <el-skeleton-item variant="text" style="width: 100%; margin-bottom: 12px;"/>
                                        <el-skeleton-item variant="text" style="width: 80%;"/>
                                    </template>
                                </el-skeleton>
                            </div>
                        </template>
                        <template v-else>
                            <!-- 文章头部 -->
                            <ArticleHeader 
                                :article="article"
                                @category-click="handleCategoryClick"
                                @tag-click="(tag) => $router.push(`/tag/${tag.slug || tag.id}`)"
                            />
                            
                            <!-- 文章内容 -->
                            <ArticleContent
                                :content="article.content"
                                :cover-image="getCoverUrl(article.cover_image)"
                                :title="article.title"
                                :is-loading="!fullContentLoaded"
                            />
                        </template>

                        <!-- 文章导航 -->
                        <ArticleNav
                            :prev-article="prevArticle"
                            :next-article="nextArticle"
                        />

                        <!-- 评论区 -->
                        <CommentsSection
                            v-if="article.id"
                            ref="commentsSectionRef"
                            :comments="comments"
                            :article-id="article.id"
                            @submit="handleCommentSubmit"
                            @like="handleLikeComment"
                            @reply="handleReply"
                        />
                    </div><!-- /.article-main -->
                </el-col>

                <el-col :span="7">
                    <div class="sidebar">
                        <div class="sidebar-card">
                            <div class="sidebar-title">
                                <el-icon>
                                    <Document/>
                                </el-icon>
                                <span>相关文章</span>
                            </div>
                            <div class="related-list">
                                <div
                                    v-for="item in relatedArticles"
                                    :key="item.id"
                                    class="related-item"
                                    @click="$router.push(getArticleUrl(item))"
                                >
                                    <div class="related-cover" v-if="item.cover_image">
                                        <img :src="getCoverUrl(item.cover_image)"/>
                                    </div>
                                    <div class="related-info">
                                        <span class="related-title">{{ item.title }}</span>
                                        <span class="related-views">{{ item.view_count }} 阅读</span>
                                    </div>
                                </div>
                                <el-empty v-if="relatedArticles.length === 0" description="暂无相关文章"
                                          :image-size="60"/>
                            </div>
                        </div>

                        <div class="sidebar-card toc-card desktop-toc">
                            <div class="sidebar-title">
                                <el-icon>
                                    <List/>
                                </el-icon>
                                <span>目录</span>
                            </div>
                            <div class="toc-list" v-if="headings.length">
                                <div
                                    v-for="(heading, index) in headings"
                                    :key="index"
                                    v-show="heading.level <= 3"
                                    :class="['toc-item', 'toc-' + heading.level]"
                                    @click="scrollToHeading(heading.id)"
                                >
                                    {{ heading.text }}
                                </div>
                            </div>
                            <el-empty v-else description="暂无目录" :image-size="60"/>
                        </div>
                    </div>
                </el-col>
            </el-row>
        </div>

        <!-- 移动端目录抽屉 -->
        <Teleport to="body">
            <!-- 移动端目录按钮 -->
            <button v-if="headings.length" class="mobile-toc-btn" @click="showTocDrawer = true">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="3" y1="6" x2="21" y2="6"/>
                    <line x1="3" y1="12" x2="15" y2="12"/>
                    <line x1="3" y1="18" x2="18" y2="18"/>
                </svg>
            </button>

            <Transition name="toc-drawer">
                <div v-if="showTocDrawer" class="toc-drawer-overlay" @click="showTocDrawer = false">
                    <div class="toc-drawer" @click.stop>
                        <div class="toc-drawer-header">
                            <span>目录</span>
                            <button class="toc-drawer-close" @click="showTocDrawer = false">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <line x1="18" y1="6" x2="6" y2="18"/>
                                    <line x1="6" y1="6" x2="18" y2="18"/>
                                </svg>
                            </button>
                        </div>
                        <div class="toc-drawer-content">
                            <div
                                v-for="(heading, index) in headings"
                                :key="index"
                                v-show="heading.level <= 3"
                                :class="['toc-drawer-item', 'toc-level-' + heading.level, { active: activeHeadingId === heading.id }]"
                                @click="handleTocClick(heading.id)"
                            >
                                {{ heading.text }}
                            </div>
                        </div>
                    </div>
                </div>
            </Transition>
        </Teleport>
    </div>
</template>

<script setup>
import {ref, computed, watch, onUnmounted, nextTick} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {
    Document,
    List
} from '@element-plus/icons-vue'
import {ElMessage} from 'element-plus'
import {marked} from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'
import {useUserStore} from '@/stores/user'
import {getContent, getContents, getComments, createComment, likeComment} from '@/api/content'
import {
    ArticleHeader,
    ArticleContent,
    ArticleNav,
    CommentsSection
} from '@/components/article'
import {getCoverUrl, getAvatarUrl, formatDate, getArticleUrl} from '@/utils'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const article = ref({})
const fullContentLoaded = ref(false)
const comments = ref([])
const commentContent = ref('')
const submitting = ref(false)
const prevArticle = ref(null)
const nextArticle = ref(null)
const relatedArticles = ref([])
const showAllComments = ref(false)
const imageInput = ref(null)

const emojis = ['😀', '😂', '😍', '🥰', '😎', '🤔', '👍', '👎', '❤️', '💔', '🎉', '🔥', '✨', '🌟', '⭐', '💯', '💪', '🙏', '😭', '😱', '🤣', '😊', '🥺', '👏', '🙄', '😴'] // 精简到 25 个常用表情

const displayComments = computed(() => {
    if (showAllComments.value) {
        return comments.value
    }
    return comments.value.slice(0, 2)
})
const showTocDrawer = ref(false)
const activeHeadingId = ref('')

const handleCategoryClick = () => {
    const idOrSlug = article.value.category_slug || article.value.category
    if (idOrSlug) {
        router.push(`/category/${idOrSlug}`)
    }
}

// 处理评论相关 - 已委托给 CommentsSection 组件
const commentsSectionRef = ref(null)

const handleCommentSubmit = ({ content, parentId }) => {
    if (parentId === null) {
        submitCommentMain(content)
    } else {
        submitReplyMain(parentId, content)
    }
}

const submitCommentMain = async (content) => {
    if (!content.trim()) return
    
    try {
        await createComment({
            article: route.params.id,
            content: content
        })
        
        await loadComments()
        ElMessage.success('评论成功')
    } catch (error) {
        console.error('Failed to submit comment:', error)
        ElMessage.error('评论失败')
    }
}

const submitReplyMain = async (parentId, content) => {
    if (!content.trim()) return
    
    try {
        await createComment({
            article: route.params.id,
            content: content,
            parent: parentId
        })
        
        await loadComments()
        ElMessage.success('回复成功')
    } catch (error) {
        console.error('Failed to submit reply:', error)
        ElMessage.error('回复失败')
    }
}

const handleLikeComment = async (comment) => {
    try {
        await likeComment(comment.id)
        comment.is_liked = !comment.is_liked
        comment.like_count = (comment.like_count || 0) + (comment.is_liked ? 1 : -1)
    } catch (error) {
        console.error('Failed to like comment:', error)
    }
}

const handleReply = (commentId, userName, userId) => {
    if (commentsSectionRef.value) {
        commentsSectionRef.value.openReplyForm(commentId, userName, userId)
    }
}

const scrollToHeading = (id) => {
    const element = document.getElementById(id)
    if (element) {
        const headerHeight = 72
        const elementPosition = element.getBoundingClientRect().top + window.pageYOffset
        window.scrollTo({
            top: elementPosition - headerHeight - 16,
            behavior: 'smooth'
        })
    }
}

const handleTocClick = (id) => {
    showTocDrawer.value = false
    activeHeadingId.value = id
    scrollToHeading(id)
}

const headings = ref([])

const extractHeadings = (content) => {
    if (!content) return []
    
    marked.setOptions({
        highlight: function (code, lang) {
            if (lang && hljs.getLanguage(lang)) {
                try {
                    return hljs.highlight(code, {language: lang}).value
                } catch (e) {
                    console.error(e)
                }
            }
            return hljs.highlightAuto(code).value
        },
        breaks: true,
        gfm: true,
    })
    
    const html = marked.parse(content)
    const tempDiv = document.createElement('div')
    tempDiv.innerHTML = html
    
    const headingElements = tempDiv.querySelectorAll('h1, h2, h3, h4, h5, h6')
    const result = []
    headingElements.forEach((el, index) => {
        result.push({
            id: `heading-${index}`,
            level: parseInt(el.tagName.charAt(1)),
            text: el.textContent,
        })
    })
    return result
}

const initArticleContent = () => {
    if (!article.value.content) return

    // 提取标题用于目录
    headings.value = extractHeadings(article.value.content)

    // 如果当前是预览内容且内容长度等于 5000，异步加载完整内容
    if (article.value.content === article.value.content_preview &&
        article.value.content.length === 5000 &&
        !fullContentLoaded.value) {
        loadFullContent()
    } else {
        // 否则标记为已加载完成
        fullContentLoaded.value = true
    }
}

const loadFullContent = async () => {
    try {
        const {data} = await getContent(route.params.id)
        if (data.content && data.content !== article.value.content) {
            article.value.content = data.content
            fullContentLoaded.value = true

            // 重新渲染完整内容
            nextTick(() => {
                initArticleContent()
            })
        }
    } catch (e) {
        console.error('加载完整内容失败:', e)
    }
}

const fetchArticle = async () => {
    loading.value = true
    fullContentLoaded.value = false
    try {
        // 支持通过 slug 或 ID 获取文章
        const articleId = route.params.slug || route.params.id
        const {data} = await getContent(articleId)
        article.value = data

        // 如果有 preview 字段且内容超过 preview，先使用 preview
        if (data.content_preview && data.content.length > data.content_preview.length) {
            article.value.content = data.content_preview
        }

        // 文章加载成功后，初始化内容渲染
        initArticleContent()

        // 并行加载评论和相关文章（失败不影响文章显示）
        Promise.all([
            fetchComments(),
            fetchRelatedArticles(),
        ]).catch(e => {
            console.error('加载评论或相关文章失败:', e)
        })
    } catch (e) {
        console.error(e)
        ElMessage.error('文章不存在')
    } finally {
        loading.value = false
    }
}

const fetchComments = async () => {
    try {
        const articleId = route.params.slug || route.params.id
        const {data} = await getComments({article: articleId})
        comments.value = data.results || data
    } catch (e) {
        console.error(e)
    }
}

// 别名，用于 CommentsSection 组件
const loadComments = fetchComments

const fetchRelatedArticles = async () => {
    try {
        const params = {status: 'published', page_size: 5}
        if (article.value.category) {
            params.category = article.value.category
        }
        const {data} = await getContents(params)
        const results = data.results || data
        relatedArticles.value = results.filter(item => item.id !== article.value.id).slice(0, 5)
    } catch (e) {
        console.error(e)
    }
}

const triggerImageUpload = () => {
    imageInput.value?.click()
}

const handleImageUpload = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    if (file.size > 5 * 1024 * 1024) {
        ElMessage.error('图片大小不能超过 5MB')
        return
    }

    try {
        // 这里需要调用上传接口，暂时只显示图片
        const reader = new FileReader()
        reader.onload = (e) => {
            const imgMarkdown = `![图片](${e.target.result})`
            commentContent.value += imgMarkdown
        }
        reader.readAsDataURL(file)
    } catch (e) {
        ElMessage.error('图片上传失败')
    }

    // 清空 input，确保同一文件可以再次选择
    event.target.value = ''
}

const insertLink = () => {
    const url = prompt('请输入链接地址：')
    if (!url) return

    const text = prompt('请输入链接文本：', url)
    if (!text) return

    const linkMarkdown = `[${text}](${url})`
    commentContent.value += linkMarkdown
}

const showTooltip = (message) => {
    ElMessage.info(message)
}

const insertEmoji = (emoji) => {
    commentContent.value += emoji
}

// 图片懒加载和文章内容渲染已在 initArticleContent 中处理

const submitComment = async () => {
    if (!commentContent.value.trim()) {
        ElMessage.warning('请输入评论内容')
        return
    }
    submitting.value = true
    try {
        await createComment({
            article: route.params.id,
            content: commentContent.value,
        })
        ElMessage.success('评论成功')
        commentContent.value = ''
        fetchComments()
    } catch (e) {
        ElMessage.error('评论失败')
    } finally {
        submitting.value = false
    }
}

watch(() => route.params.id, () => {
    if (route.params.id) {
        fetchArticle()
    }
}, {immediate: true})

// 注意：图片懒加载功能已移除，使用浏览器原生懒加载
</script>

<style scoped>
.article-page {
    padding: 32px 0;
    background: var(--bg-color);
    min-height: calc(100vh - var(--header-height));
}

.container {
    max-width: var(--container-max);
    margin: 0 auto;
    padding: 0 24px;
}

.article-main {
    background: var(--card-bg);
    border-radius: var(--radius-lg);
    padding: 40px;
    border: 1px solid var(--border-light);
    animation: fadeInUp 0.15s ease-out;
}

.article-skeleton {
    padding: 24px 0;
}

.article-header {
    margin-bottom: 32px;
    padding-bottom: 24px;
    border-bottom: 2px solid var(--border-light);
}

.article-category {
    margin-bottom: 16px;
}

.article-category .el-tag {
    border-radius: var(--radius-sm);
    padding: 6px 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition-fast);
}

.article-category .el-tag:hover {
    background: var(--primary-color);
    color: #fff;
    border-color: var(--primary-color);
}

.article-header h1 {
    font-size: 32px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.4;
    margin-bottom: 24px;
    position: relative;
}

.article-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.author-info {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 10px 14px;
    background: var(--bg-secondary);
    border-radius: var(--radius-sm);
    transition: all var(--transition-fast);
}

[data-theme="dark"] .author-info {
    background: var(--bg-tertiary);
}

.author-info:hover {
    background: var(--primary-bg);
}

.author-info .el-avatar {
    border-radius: var(--radius-sm) !important;
    border: none;
}

.author-detail {
    display: flex;
    flex-direction: column;
}

.author-name {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 15px;
}

.publish-time {
    font-size: 13px;
    color: var(--text-tertiary);
}

.article-stats {
    display: flex;
    gap: 20px;
    font-size: 14px;
    color: var(--text-secondary);
}

.article-stats span {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 12px;
    background: var(--bg-secondary);
    border-radius: var(--radius-sm);
}

[data-theme="dark"] .article-stats span {
    background: var(--bg-tertiary);
}

.article-stats span .el-icon {
    color: var(--primary-color);
}

.article-tags {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.article-tags .el-tag {
    cursor: pointer;
    border-radius: var(--radius-sm);
    padding: 6px 12px;
    transition: all var(--transition-fast);
}

.article-tags .el-tag:hover {
    background: var(--primary-color) !important;
    color: #fff !important;
    border-color: transparent !important;
}

.article-cover {
    margin-bottom: 32px;
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-md);
}

.article-cover img {
    width: 100%;
    height: auto;
    transition: transform var(--transition-slow);
}

.article-cover:hover img {
    transform: scale(1.02);
}

.article-nav {
    display: flex;
    justify-content: space-between;
    margin-top: 48px;
    padding: 24px;
    background: var(--bg-secondary);
    border-radius: var(--radius-lg);
}

.article-nav .el-button {
    font-weight: 500;
    padding: 12px 20px;
    border-radius: var(--radius-md);
    transition: all var(--transition-fast);
}

.article-nav .el-button:hover {
    background: var(--primary-bg);
    color: var(--primary-color);
}

.comments-section {
    margin-top: 48px;
    padding-top: 40px;
    border-top: 2px solid var(--border-light);
}

.section-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 20px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 28px;
}

.section-title .el-icon {
    color: var(--primary-color);
    font-size: 22px;
}

.comment-form {
    margin-bottom: 32px;
}

.comment-form-wrapper {
    display: flex;
    gap: 16px;
    background: var(--bg-secondary);
    border-radius: var(--radius-lg);
    padding: 20px;
    border: 1px solid var(--border-color);
    transition: all var(--transition-fast);
}

.comment-form-wrapper .el-avatar {
    border-radius: var(--radius-md) !important;
    border: 2px solid var(--border-light);
}

.comment-form-content {
    flex: 1;
}

.comment-form-title {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
}

.comment-textarea :deep(.el-textarea__inner) {
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 14px;
    font-size: 14px;
    line-height: 1.7;
    transition: all var(--transition-fast);
}

.comment-textarea :deep(.el-textarea__inner:focus) {
    border-color: var(--primary-color);
}

.comment-form-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 14px;
}

.comment-form-tools {
    display: flex;
    gap: 8px;
}

.tool-btn {
    padding: 8px 12px;
    color: var(--text-tertiary);
    font-size: 18px;
    border-radius: var(--radius-md);
    transition: all var(--transition-fast);
}

.tool-btn:hover {
    color: var(--primary-color);
    background: var(--primary-bg);
}

.comment-form-actions {
    display: flex;
    align-items: center;
    gap: 14px;
}

.char-count {
    font-size: 12px;
    color: var(--text-tertiary);
}

.comment-form .el-button--primary {
    min-width: 90px;
    height: 36px;
    font-size: 14px;
    font-weight: 500;
}

.emoji-picker {
    max-height: 200px;
    overflow-y: auto;
}

.emoji-list {
    display: grid;
    grid-template-columns: repeat(10, 1fr);
    gap: 8px;
}

.emoji-item {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    font-size: 20px;
    cursor: pointer;
    border-radius: var(--radius-sm);
    transition: all var(--transition-fast);
}

.emoji-item:hover {
    background: var(--primary-bg);
    transform: scale(1.1);
}

.article-content img {
    transition: opacity var(--transition-normal);
}

.article-content img.lazy-loading {
    opacity: 0;
    background: var(--bg-secondary);
    min-height: 200px;
}

.article-content img[data-src] {
    opacity: 0;
}

.full-content-loading {
    margin-top: 24px;
    padding: 24px;
    background: var(--bg-secondary);
    border-radius: var(--radius-lg);
}

.comment-form .el-textarea {
    margin-bottom: 14px;
}

.login-tip {
    text-align: center;
    padding: 40px;
    background: linear-gradient(135deg, var(--primary-bg) 0%, var(--bg-secondary) 100%);
    border-radius: var(--radius-lg);
    margin-bottom: 32px;
}

.login-tip p {
    color: var(--text-secondary);
    margin-bottom: 16px;
    font-size: 15px;
}

.comment-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.comment-item {
    display: flex;
    gap: 14px;
    background: var(--bg-secondary);
    padding: 20px;
    border-radius: var(--radius-lg);
    transition: all var(--transition-fast);
    animation: fadeInUp 0.4s ease-out;
}

.comment-item:hover {
    box-shadow: var(--shadow-sm);
}

.comment-item .el-avatar {
    border-radius: var(--radius-md) !important;
    border: 2px solid var(--border-light);
}

.comment-body {
    flex: 1;
}

.comment-main {
    background: transparent;
    padding: 0;
    border-radius: 0;
}

.comment-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
}

.comment-author {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 15px;
}

.comment-time {
    font-size: 13px;
    color: var(--text-tertiary);
}

.comment-text {
    font-size: 15px;
    color: var(--text-primary);
    line-height: 1.8;
}

.comment-actions {
    margin-top: 14px;
    display: flex;
    gap: 20px;
}

.action-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: var(--text-tertiary);
    cursor: pointer;
    padding: 6px 12px;
    border-radius: var(--radius-full);
    transition: all var(--transition-fast);
}

.action-btn:hover {
    color: var(--primary-color);
    background: var(--primary-bg);
}

.action-btn.liked {
    color: var(--primary-color);
    background: var(--primary-bg);
}

.action-btn.small {
    font-size: 12px;
}

.reply-form {
    margin-top: 14px;
    padding: 18px;
    background: var(--card-bg);
    border-radius: var(--radius-md);
    border: 1px solid var(--border-color);
}

.reply-form-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    color: var(--text-primary);
}

.reply-target {
    color: var(--primary-color);
    font-weight: 600;
}

.reply-form .el-textarea {
    margin-bottom: 10px;
}

.reply-form :deep(.el-textarea__inner) {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    padding: 12px !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
    transition: all var(--transition-fast) !important;
}

.reply-form :deep(.el-textarea__inner:focus) {
    border-color: var(--primary-color) !important;
}

.reply-form :deep(.el-textarea__inner::placeholder) {
    color: var(--text-tertiary) !important;
}

[data-theme="dark"] .reply-form {
    background: var(--bg-secondary);
}

[data-theme="dark"] .reply-form :deep(.el-textarea__inner) {
    background: var(--bg-tertiary) !important;
}

.reply-form-actions {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 10px;
}

.reply-form-actions .el-button--primary {
    background: var(--primary-color);
    border-color: var(--primary-color);
}

.reply-form-actions .el-button--primary:hover {
    background: var(--primary-hover);
    border-color: var(--primary-hover);
}

.reply-form-header .el-button.is-link {
    color: var(--text-secondary);
}

.reply-form-header .el-button.is-link:hover {
    color: var(--primary-color);
}

.reply-tip {
    font-size: 12px;
    color: var(--text-tertiary);
}

.reply-section {
    margin-top: 10px;
}

.reply-toggle {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    background: var(--bg-tertiary);
    color: var(--text-secondary);
    font-size: 12px;
    cursor: pointer;
    border-radius: var(--radius-full);
    transition: all var(--transition-fast);
    font-weight: 500;
}

.reply-toggle:hover {
    background: var(--primary-bg);
    color: var(--primary-color);
}

.reply-toggle .el-icon {
    font-size: 14px;
    transition: transform var(--transition-normal);
}

.reply-toggle .el-icon.rotated {
    transform: rotate(90deg);
}

.reply-list {
    margin-top: 14px;
    padding-left: 24px;
    border-left: 2px solid var(--border-light);
}

.reply-item {
    display: flex;
    gap: 12px;
    padding: 14px;
    margin-bottom: 10px;
    background: var(--card-bg);
    border-radius: var(--radius-md);
    border: 1px solid var(--border-light);
    transition: all var(--transition-fast);
}

.reply-item:hover {
    border-color: var(--primary-light);
}

.reply-item .el-avatar {
    border-radius: var(--radius-sm) !important;
}

.reply-item:last-child {
    margin-bottom: 0;
}

.reply-body {
    flex: 1;
}

.reply-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
}

.reply-arrow {
    color: var(--text-tertiary);
    font-size: 12px;
}

.reply-author {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 14px;
}

.reply-time {
    font-size: 12px;
    color: var(--text-tertiary);
}

.reply-text {
    font-size: 14px;
    color: var(--text-primary);
    line-height: 1.7;
}

.reply-actions {
    margin-top: 10px;
    display: flex;
    gap: 16px;
}

.sidebar {
    display: flex;
    flex-direction: column;
    gap: 24px;
    align-self: flex-start;
    position: sticky;
    top: 96px;
    max-height: calc(100vh - 116px);
    overflow-y: auto;
    scrollbar-width: none;
    -ms-overflow-style: none;
}

.sidebar::-webkit-scrollbar {
    display: none;
}

.sidebar-card {
    background: var(--card-bg);
    border-radius: var(--radius-lg);
    padding: 24px;
    border: 1px solid var(--border-light);
    transition: all var(--transition-fast);
}

.sidebar-card:hover {
    border-color: rgba(0, 120, 212, 0.2);
    box-shadow: var(--shadow-sm);
}

.sidebar-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 17px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 18px;
    padding-bottom: 14px;
    border-bottom: 2px solid var(--border-light);
}

.sidebar-title .el-icon {
    color: var(--primary-color);
    font-size: 20px;
}

.toc-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
    max-height: 400px;
    overflow-y: auto;
    padding-right: 8px;
}

.toc-list::-webkit-scrollbar {
    width: 4px;
}

.toc-list::-webkit-scrollbar-track {
    background: var(--bg-secondary);
    border-radius: 2px;
}

.toc-list::-webkit-scrollbar-thumb {
    background: var(--border-dark);
    border-radius: 2px;
}

.toc-item {
    font-size: 13px;
    color: var(--text-secondary);
    text-decoration: none;
    padding: 8px 12px;
    display: block;
    border-radius: var(--radius-sm);
    transition: all var(--transition-fast);
    cursor: pointer;
    border-left: 2px solid transparent;
}

.toc-item:hover {
    color: var(--primary-color);
    background: var(--primary-bg);
    border-left-color: var(--primary-color);
}

.toc-2 {
    padding-left: 0;
}

.toc-3 {
    padding-left: 16px;
}

.toc-4 {
    padding-left: 32px;
}

.related-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.related-item {
    display: flex;
    gap: 14px;
    padding: 14px;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all var(--transition-fast);
    border: 1px solid transparent;
}

.related-item:hover {
    background: var(--primary-bg);
    border-color: var(--primary-light);
    transform: translateX(4px);
}

.related-cover {
    width: 80px;
    height: 60px;
    border-radius: var(--radius-md);
    overflow: hidden;
    flex-shrink: 0;
}

.related-cover img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform var(--transition-normal);
}

.related-item:hover .related-cover img {
    transform: scale(1.1);
}

.related-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-width: 0;
}

.related-title {
    font-size: 14px;
    color: var(--text-primary);
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    margin-bottom: 6px;
    font-weight: 500;
    transition: color var(--transition-fast);
}

.related-item:hover .related-title {
    color: var(--primary-color);
}

.related-views {
    font-size: 12px;
    color: var(--text-tertiary);
}

.show-more-comments {
    margin-top: 24px;
    text-align: center;
}

.show-more-comments .el-button {
    border-radius: var(--radius-full);
    padding: 12px 32px;
}

/* 对话框评论样式 */
.dialog-comment-list {
    height: 100%;
    max-height: calc(80vh - 120px);
    overflow-y: auto;
    padding-right: 8px;
}

.dialog-comment-item {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
    background: var(--bg-secondary);
    padding: 16px;
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
}

[data-theme="dark"] .dialog-comment-item {
    background: var(--bg-tertiary);
}

.dialog-comment-item .el-avatar {
    border-radius: var(--radius-sm) !important;
}

.dialog-comment-body {
    flex: 1;
}

.dialog-comment-main {
    background: transparent;
    padding: 0;
    border-radius: 0;
}

.dialog-comment-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
}

.dialog-comment-author {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 15px;
}

.dialog-comment-time {
    font-size: 13px;
    color: var(--text-tertiary);
}

.dialog-comment-text {
    font-size: 15px;
    color: var(--text-primary);
    line-height: 1.7;
}

.dialog-comment-actions {
    margin-top: 12px;
    display: flex;
    gap: 20px;
}

.dialog-action-btn {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 13px;
    color: var(--text-tertiary);
    cursor: pointer;
    transition: color var(--transition-fast);
}

.dialog-action-btn:hover {
    color: var(--primary-color);
}

.dialog-action-btn.liked {
    color: var(--primary-color);
}

.dialog-action-btn.small {
    font-size: 12px;
}

.dialog-reply-form {
    margin-top: 12px;
    padding: 16px;
    background: var(--bg-secondary);
    border-radius: var(--radius-md);
    border: 1px solid var(--border-color);
}

.dialog-reply-form-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.dialog-reply-target {
    color: var(--primary-color);
    font-weight: 500;
}

.dialog-reply-form .el-textarea {
    margin-bottom: 8px;
}

.dialog-reply-form :deep(.el-textarea__inner) {
    background: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    padding: 12px !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
    transition: all var(--transition-fast) !important;
}

.dialog-reply-form :deep(.el-textarea__inner:focus) {
    border-color: var(--primary-color) !important;
}

.dialog-reply-form :deep(.el-textarea__inner::placeholder) {
    color: var(--text-tertiary) !important;
}

[data-theme="dark"] .dialog-reply-form {
    background: var(--bg-tertiary);
}

[data-theme="dark"] .dialog-reply-form :deep(.el-textarea__inner) {
    background: var(--bg-secondary) !important;
}

.dialog-reply-form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
}

.dialog-reply-tip {
    font-size: 12px;
    color: var(--text-tertiary);
}

.dialog-reply-section {
    margin-top: 8px;
}

.dialog-reply-toggle {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    background: var(--bg-secondary);
    color: var(--text-secondary);
    font-size: 12px;
    cursor: pointer;
    border-radius: var(--radius-sm);
    transition: all var(--transition-fast);
    border: 1px solid var(--border-color);
    font-weight: 500;
}

.dialog-reply-toggle:hover {
    background: var(--primary-bg);
    border-color: var(--primary-color);
    color: var(--primary-color);
}

.dialog-reply-toggle .el-icon {
    font-size: 16px;
    color: var(--text-secondary);
    transition: transform var(--transition-normal);
}

[data-theme="dark"] .dialog-reply-toggle {
    background: var(--bg-tertiary);
}

.dialog-reply-toggle .el-icon.rotated {
    transform: rotate(90deg);
}

.dialog-reply-list {
    margin-top: 12px;
    padding-left: 24px;
}

.dialog-reply-item {
    display: flex;
    gap: 10px;
    padding: 12px;
    margin-bottom: 8px;
    background: var(--bg-secondary);
    border-radius: var(--radius-sm);
    border: 1px solid var(--border-light);
}

[data-theme="dark"] .dialog-reply-item {
    background: var(--bg-tertiary);
}

.dialog-reply-item .el-avatar {
    border-radius: 3px !important;
}

.dialog-reply-item:last-child {
    margin-bottom: 0;
}

.dialog-reply-body {
    flex: 1;
}

.dialog-reply-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;
}

.dialog-reply-author {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 14px;
}

.dialog-reply-time {
    font-size: 12px;
    color: var(--text-tertiary);
}

.dialog-reply-text {
    font-size: 14px;
    color: var(--text-primary);
    line-height: 1.6;
}

.dialog-reply-actions {
    margin-top: 8px;
    display: flex;
    gap: 16px;
}

.dialog-reply-arrow {
    color: var(--text-tertiary);
    font-size: 12px;
}
</style>

<style>
.markdown-body {
    font-size: 16px;
    line-height: 1.9;
    color: var(--text-primary);
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4,
.markdown-body h5,
.markdown-body h6 {
    margin-top: 32px;
    margin-bottom: 16px;
    font-weight: 700;
    line-height: 1.4;
    color: var(--text-primary);
}

.markdown-body h1 {
    font-size: 30px;
    padding-bottom: 14px;
    border-bottom: 2px solid var(--border-light);
    position: relative;
}

.markdown-body h1::before {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 60px;
    height: 3px;
    background: var(--primary-color);
    border-radius: 2px;
}

.markdown-body h2 {
    font-size: 26px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--border-light);
    position: relative;
}

.markdown-body h2::before {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 40px;
    height: 3px;
    background: var(--primary-color);
    border-radius: 2px;
}

.markdown-body h3 {
    font-size: 22px;
}

.markdown-body h4 {
    font-size: 19px;
}

.markdown-body p {
    margin-bottom: 18px;
}

.markdown-body a {
    color: var(--primary-color);
    text-decoration: none;
    border-bottom: 1px dashed var(--primary-light);
    transition: all var(--transition-fast);
}

.markdown-body a:hover {
    color: var(--primary-dark);
    border-bottom-style: solid;
}

.markdown-body img {
    max-width: 100%;
    border-radius: var(--radius-lg);
    margin: 20px 0;
    box-shadow: var(--shadow-md);
    transition: all var(--transition-normal);
}

.markdown-body img:hover {
    box-shadow: var(--shadow-lg);
}

.markdown-body pre {
    background: var(--bg-secondary);
    padding: 16px;
    border-radius: var(--radius-md);
    overflow-x: auto;
    margin: 16px 0;
    border: 1px solid var(--border-light);
}

.markdown-body code {
    font-family: var(--font-mono);
    font-size: 14px;
}

.markdown-body pre code {
    color: var(--text-primary);
    padding-top: 16px;
    display: block;
}

[data-theme="dark"] .markdown-body pre code {
    color: #e0e0e0;
}

.markdown-body p code {
    background: var(--primary-bg);
    padding: 3px 8px;
    border-radius: var(--radius-sm);
    color: var(--primary-color);
    font-size: 14px;
    font-weight: 500;
}

.markdown-body blockquote {
    border-left: 4px solid var(--primary-color);
    padding: 16px 20px;
    margin: 20px 0;
    background: linear-gradient(135deg, var(--primary-bg) 0%, var(--bg-secondary) 100%);
    color: var(--text-secondary);
    border-radius: 0 var(--radius-lg) var(--radius-lg) 0;
    position: relative;
}

.markdown-body blockquote::before {
    content: '"';
    position: absolute;
    top: -10px;
    left: 20px;
    font-size: 48px;
    color: var(--primary-light);
    opacity: 0.3;
    font-family: Georgia, serif;
}

.markdown-body ul,
.markdown-body ol {
    padding-left: 28px;
    margin-bottom: 18px;
}

.markdown-body li {
    margin-bottom: 10px;
    line-height: 1.7;
}

.markdown-body li::marker {
    color: var(--primary-color);
}

.markdown-body table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

.markdown-body th,
.markdown-body td {
    border: 1px solid var(--border-color);
    padding: 14px 16px;
    text-align: left;
}

.markdown-body th {
    background: var(--primary-color);
    color: #fff;
    font-weight: 600;
}

.markdown-body tr:nth-child(even) {
    background: var(--bg-secondary);
}

.markdown-body tr:hover {
    background: var(--primary-bg);
}

.markdown-body hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--border-color), transparent);
    margin: 32px 0;
}

.markdown-body .hljs {
    background: transparent;
}

.markdown-body .highlight {
    margin: 20px 0;
}

/* 确保所有 textarea 不能调整大小 */
textarea {
    resize: none !important;
    scrollbar-width: none; /* Firefox */
}

textarea::-webkit-scrollbar {
    display: none; /* Chrome/Safari */
}

/* 确保 Element Plus 的 textarea 不能调整大小 */
.el-textarea__inner {
    resize: none !important;
    scrollbar-width: none; /* Firefox */
}

.el-textarea__inner::-webkit-scrollbar {
    display: none; /* Chrome/Safari */
}

/* 确保评论和回复的 textarea 不能调整大小 */
.comment-form .el-textarea__inner,
.reply-form .el-textarea__inner,
.dialog-reply-form .el-textarea__inner {
    resize: none !important;
    scrollbar-width: none; /* Firefox */
}

.comment-form .el-textarea__inner::-webkit-scrollbar,
.reply-form .el-textarea__inner::-webkit-scrollbar,
.dialog-reply-form .el-textarea__inner::-webkit-scrollbar {
    display: none; /* Chrome/Safari */
}

/* 评论对话框固定位置样式 */
.article-page .el-dialog {
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    margin: 0 !important;
    max-height: 80vh !important;
    display: flex !important;
    flex-direction: column !important;
}

.article-page .el-dialog .el-dialog__header {
    flex-shrink: 0;
    background: var(--bg-primary);
    border-bottom: 1px solid var(--border-color);
}

[data-theme="dark"] .article-page .el-dialog .el-dialog__header {
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-color);
}

.article-page .el-dialog .el-dialog__title {
    color: var(--text-primary);
}

.article-page .el-dialog .el-dialog__headerbtn {
    color: var(--text-secondary);
}

.article-page .el-dialog .el-dialog__headerbtn:hover {
    color: var(--text-primary);
}

.article-page .el-dialog .el-dialog__body {
    overflow: hidden !important;
    flex: 1;
    min-height: 0;
    padding: 10px 20px 20px !important;
}

/* 移动端 Markdown 样式适配 */
@media (max-width: 768px) {
    .markdown-body {
        font-size: 14px;
        line-height: 1.7;
    }

    .markdown-body h1 {
        font-size: 20px;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .markdown-body h2 {
        font-size: 17px;
        margin-top: 16px;
        margin-bottom: 8px;
    }

    .markdown-body h3 {
        font-size: 15px;
        margin-top: 14px;
        margin-bottom: 6px;
    }

    .markdown-body h4 {
        font-size: 14px;
        margin-top: 12px;
        margin-bottom: 6px;
    }

    .markdown-body p {
        margin-bottom: 12px;
    }

    .markdown-body pre {
        padding: 12px;
        margin: 12px 0;
        font-size: 12px;
        border-radius: 6px;
    }

    .markdown-body pre::before {
        top: 6px;
        left: 10px;
        width: 6px;
        height: 6px;
    }

    .markdown-body code {
        font-size: 12px;
    }

    .markdown-body p code {
        padding: 1px 4px;
        font-size: 12px;
    }

    .markdown-body blockquote {
        padding: 10px 12px;
        margin: 12px 0;
    }

    .markdown-body blockquote::before {
        font-size: 28px;
        left: 10px;
        top: -6px;
    }

    .markdown-body ul,
    .markdown-body ol {
        padding-left: 18px;
        margin-bottom: 12px;
    }

    .markdown-body li {
        margin-bottom: 6px;
    }

    .markdown-body table {
        margin: 12px 0;
        font-size: 13px;
    }

    .markdown-body th,
    .markdown-body td {
        padding: 8px 10px;
    }

    .markdown-body img {
        margin: 12px 0;
    }

    .markdown-body hr {
        margin: 16px 0;
    }
}

@media (max-width: 576px) {
    .markdown-body {
        font-size: 13px;
        line-height: 1.6;
    }

    .markdown-body h1 {
        font-size: 18px;
        margin-top: 16px;
        margin-bottom: 8px;
    }

    .markdown-body h2 {
        font-size: 16px;
        margin-top: 14px;
        margin-bottom: 6px;
    }

    .markdown-body h3 {
        font-size: 14px;
        margin-top: 12px;
        margin-bottom: 4px;
    }

    .markdown-body h4 {
        font-size: 13px;
        margin-top: 10px;
        margin-bottom: 4px;
    }

    .markdown-body p {
        margin-bottom: 10px;
    }

    .markdown-body pre {
        padding: 10px;
        margin: 10px 0;
        font-size: 11px;
        border-radius: 4px;
    }

    .markdown-body code {
        font-size: 11px;
    }

    .markdown-body p code {
        padding: 1px 3px;
        font-size: 11px;
    }

    .markdown-body blockquote {
        padding: 8px 10px;
        margin: 10px 0;
    }

    .markdown-body blockquote::before {
        font-size: 24px;
        left: 8px;
        top: -4px;
    }

    .markdown-body ul,
    .markdown-body ol {
        padding-left: 16px;
        margin-bottom: 10px;
    }

    .markdown-body li {
        margin-bottom: 4px;
    }

    .markdown-body table {
        margin: 10px 0;
        font-size: 12px;
        display: block;
        overflow-x: auto;
        white-space: nowrap;
    }

    .markdown-body th,
    .markdown-body td {
        padding: 6px 8px;
    }

    .markdown-body img {
        margin: 10px 0;
    }

    .markdown-body hr {
        margin: 12px 0;
    }
}

@media (max-width: 992px) {
    .el-row {
        flex-direction: column;
    }

    .el-col-17 {
        max-width: 100%;
        flex: 0 0 100%;
    }

    .el-col-7 {
        max-width: 100%;
        flex: 0 0 100%;
        margin-top: 16px;
    }

    .sidebar {
        position: static;
        max-height: none;
        flex-direction: column;
        gap: 12px;
    }

    .sidebar-card {
        padding: 16px;
    }

    .sidebar-title {
        font-size: 15px;
        margin-bottom: 12px;
        padding-bottom: 10px;
    }

    .toc-list {
        max-height: 200px;
    }

    .toc-item {
        font-size: 12px;
        padding: 6px 10px;
    }

    .related-item {
        padding: 10px;
        gap: 10px;
    }

    .related-cover {
        width: 60px;
        height: 45px;
    }

    .related-title {
        font-size: 13px;
    }

    .related-views {
        font-size: 11px;
    }
}

@media (max-width: 768px) {
    .article-page {
        padding: 12px 0;
    }

    .container {
        padding: 0 12px;
    }

    .article-main {
        padding: 16px;
        border-radius: var(--radius-md);
    }

    .article-header {
        margin-bottom: 16px;
        padding-bottom: 16px;
    }

    .article-header h1 {
        font-size: 20px;
        line-height: 1.3;
        margin-bottom: 12px;
    }

    .article-category {
        margin-bottom: 12px;
    }

    .article-category .el-tag {
        padding: 4px 10px;
        font-size: 12px;
    }

    .article-meta {
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
        margin-bottom: 12px;
    }

    .author-info {
        align-self: flex-start;
        padding: 6px 10px;
        gap: 8px;
    }

    .author-info .el-avatar {
        width: 28px !important;
        height: 28px !important;
    }

    .author-name {
        font-size: 13px;
    }

    .publish-time {
        font-size: 12px;
    }

    .article-stats {
        width: auto;
        align-self: flex-start;
    }

    .article-stats span {
        padding: 4px 8px;
        font-size: 12px;
    }

    .article-tags {
        gap: 6px;
    }

    .article-tags .el-tag {
        padding: 3px 8px;
        font-size: 11px;
    }

    .article-cover {
        margin-bottom: 16px;
    }

    .article-content {
        font-size: 15px;
    }

    .article-nav {
        flex-direction: column;
        gap: 8px;
        padding: 12px;
        margin-top: 24px;
    }

    .article-nav .el-button {
        width: 100%;
        justify-content: center;
        font-size: 13px;
    }

    .comments-section {
        margin-top: 24px;
        padding-top: 20px;
    }

    .section-title {
        font-size: 16px;
        margin-bottom: 16px;
    }

    .comment-form-wrapper {
        flex-direction: column;
        gap: 10px;
        padding: 12px;
    }

    .comment-form-wrapper .el-avatar {
        display: none;
    }

    .comment-item {
        padding: 12px;
        gap: 10px;
    }

    .comment-item .el-avatar {
        width: 28px !important;
        height: 28px !important;
    }

    .comment-header {
        margin-bottom: 6px;
    }

    .comment-author {
        font-size: 13px;
    }

    .comment-time {
        font-size: 11px;
    }

    .comment-text {
        font-size: 14px;
        line-height: 1.6;
    }

    .comment-actions {
        margin-top: 8px;
        gap: 12px;
    }

    .action-btn {
        font-size: 12px;
        padding: 4px 8px;
    }

    .reply-form {
        padding: 10px;
    }

    .reply-form-header {
        margin-bottom: 8px;
        font-size: 13px;
    }

    .reply-list {
        padding-left: 12px;
    }

    .reply-item {
        padding: 10px;
        gap: 8px;
    }

    .reply-item .el-avatar {
        width: 20px !important;
        height: 20px !important;
    }

    .reply-header {
        margin-bottom: 4px;
    }

    .reply-author {
        font-size: 12px;
    }

    .reply-time {
        font-size: 11px;
    }

    .reply-text {
        font-size: 13px;
    }

    .reply-actions {
        margin-top: 6px;
        gap: 10px;
    }

    .reply-toggle {
        padding: 6px 10px;
        font-size: 11px;
    }
}

@media (max-width: 576px) {
    .article-page {
        padding: 8px 0;
    }

    .container {
        padding: 0 10px;
    }

    .article-main {
        padding: 12px;
        border-radius: var(--radius-sm);
    }

    .article-header {
        margin-bottom: 12px;
        padding-bottom: 12px;
    }

    .article-header h1 {
        font-size: 18px;
        margin-bottom: 10px;
    }

    .article-category {
        margin-bottom: 10px;
    }

    .article-category .el-tag {
        padding: 3px 8px;
        font-size: 11px;
    }

    .article-meta {
        gap: 6px;
        margin-bottom: 10px;
    }

    .author-info {
        padding: 5px 8px;
        gap: 6px;
    }

    .author-info .el-avatar {
        width: 24px !important;
        height: 24px !important;
    }

    .author-name {
        font-size: 12px;
    }

    .publish-time {
        font-size: 11px;
    }

    .article-stats span {
        padding: 3px 6px;
        font-size: 11px;
        gap: 4px;
    }

    .article-tags {
        gap: 5px;
    }

    .article-tags .el-tag {
        padding: 2px 6px;
        font-size: 10px;
    }

    .article-cover {
        margin-bottom: 12px;
        border-radius: var(--radius-sm);
    }

    .article-nav {
        padding: 10px;
        margin-top: 20px;
    }

    .comments-section {
        margin-top: 20px;
        padding-top: 16px;
    }

    .section-title {
        font-size: 15px;
        margin-bottom: 12px;
    }

    .login-tip {
        padding: 24px 16px;
        margin-bottom: 20px;
    }

    .login-tip p {
        font-size: 13px;
        margin-bottom: 12px;
    }

    .comment-form-wrapper {
        padding: 10px;
    }

    .comment-textarea :deep(.el-textarea__inner) {
        padding: 10px;
        font-size: 13px;
    }

    .comment-form-footer {
        flex-direction: column;
        gap: 10px;
        align-items: stretch;
    }

    .comment-form-tools {
        justify-content: flex-start;
    }

    .tool-btn {
        padding: 6px 10px;
        font-size: 16px;
    }

    .comment-form-actions {
        justify-content: space-between;
    }

    .char-count {
        font-size: 11px;
    }

    .comment-form .el-button--primary {
        flex: 1;
        min-width: auto;
        height: 32px;
        font-size: 13px;
    }

    .comment-item {
        padding: 10px;
        gap: 8px;
    }

    .comment-item .el-avatar {
        width: 24px !important;
        height: 24px !important;
    }

    .comment-text {
        font-size: 13px;
    }

    .reply-form {
        padding: 8px;
    }

    .reply-form :deep(.el-textarea__inner) {
        padding: 8px !important;
        font-size: 12px !important;
    }

    .reply-item {
        padding: 8px;
        gap: 6px;
    }

    .reply-item .el-avatar {
        width: 18px !important;
        height: 18px !important;
    }

    .show-more-comments .el-button {
        width: 100%;
        font-size: 13px;
    }

    .sidebar-card {
        padding: 12px;
    }

    .sidebar-title {
        font-size: 14px;
        margin-bottom: 10px;
        padding-bottom: 8px;
    }

    .sidebar-title .el-icon {
        font-size: 16px;
    }

    .toc-list {
        max-height: 150px;
    }

    .toc-item {
        font-size: 11px;
        padding: 5px 8px;
    }

    .related-item {
        padding: 8px;
        gap: 8px;
    }

    .related-cover {
        width: 50px;
        height: 38px;
    }

    .related-title {
        font-size: 12px;
        margin-bottom: 4px;
    }

    .related-views {
        font-size: 10px;
    }

    .comments-section {
        margin-top: 16px;
        padding-top: 12px;
    }

    .section-title {
        font-size: 14px;
        margin-bottom: 10px;
    }

    .section-title .el-icon {
        font-size: 16px;
    }

    .login-tip {
        padding: 16px 12px;
        margin-bottom: 12px;
    }

    .login-tip p {
        font-size: 12px;
        margin-bottom: 8px;
    }

    .login-tip .el-button {
        padding: 6px 14px;
        font-size: 12px;
    }

    .comment-form-wrapper {
        padding: 8px;
        gap: 8px;
    }

    .comment-textarea :deep(.el-textarea__inner) {
        padding: 8px;
        font-size: 12px;
    }

    .comment-form-footer {
        gap: 8px;
    }

    .comment-form-tools {
        gap: 4px;
    }

    .tool-btn {
        padding: 4px 6px;
        font-size: 14px;
    }

    .char-count {
        font-size: 10px;
    }

    .comment-form .el-button--primary {
        height: 28px;
        font-size: 12px;
        padding: 0 10px;
    }

    .comment-item {
        padding: 8px;
        gap: 6px;
    }

    .comment-item .el-avatar {
        width: 22px !important;
        height: 22px !important;
    }

    .comment-header {
        margin-bottom: 4px;
        gap: 4px;
    }

    .comment-author {
        font-size: 12px;
    }

    .comment-time {
        font-size: 10px;
    }

    .comment-text {
        font-size: 12px;
        line-height: 1.5;
    }

    .comment-actions {
        margin-top: 4px;
        gap: 8px;
    }

    .action-btn {
        font-size: 10px;
        padding: 2px 5px;
        gap: 2px;
    }

    .action-btn .el-icon {
        font-size: 11px;
    }

    .reply-form {
        padding: 6px;
        margin-top: 6px;
    }

    .reply-form-header {
        margin-bottom: 4px;
        font-size: 11px;
    }

    .reply-form :deep(.el-textarea__inner) {
        padding: 6px !important;
        font-size: 11px !important;
    }

    .reply-form-actions {
        margin-top: 4px;
    }

    .reply-form-actions .el-button {
        height: 24px;
        font-size: 10px;
        padding: 0 8px;
    }

    .reply-list {
        padding-left: 8px;
        margin-top: 6px;
    }

    .reply-item {
        padding: 6px;
        gap: 5px;
    }

    .reply-item .el-avatar {
        width: 16px !important;
        height: 16px !important;
    }

    .reply-header {
        margin-bottom: 2px;
        gap: 3px;
    }

    .reply-author {
        font-size: 10px;
    }

    .reply-time {
        font-size: 9px;
    }

    .reply-text {
        font-size: 11px;
        line-height: 1.4;
    }

    .reply-actions {
        margin-top: 3px;
        gap: 6px;
    }

    .reply-actions .action-btn {
        font-size: 9px;
        padding: 1px 3px;
    }

    .reply-toggle {
        padding: 3px 6px;
        font-size: 9px;
        margin-top: 4px;
    }

    .show-more-comments {
        margin-top: 10px;
    }

    .show-more-comments .el-button {
        font-size: 12px;
        padding: 6px 10px;
    }
}

/* 移动端目录按钮 */
.mobile-toc-btn {
    display: none;
    position: fixed;
    right: 16px;
    bottom: 80px;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: var(--primary-color);
    color: #fff;
    border: none;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    cursor: pointer;
    z-index: 999;
    align-items: center;
    justify-content: center;
    transition: all var(--transition-fast);
}

.mobile-toc-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.mobile-toc-btn svg {
    width: 22px;
    height: 22px;
}

/* 移动端目录抽屉 */
.toc-drawer-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 2000;
    display: flex;
    justify-content: flex-end;
}

.toc-drawer {
    width: 280px;
    max-width: 80vw;
    height: 100%;
    background: var(--bg-primary);
    box-shadow: -4px 0 16px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
}

.toc-drawer-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    border-bottom: 1px solid var(--border-light);
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
}

.toc-drawer-close {
    width: 32px;
    height: 32px;
    border: none;
    background: transparent;
    color: var(--text-secondary);
    cursor: pointer;
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all var(--transition-fast);
}

.toc-drawer-close:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
}

.toc-drawer-close svg {
    width: 18px;
    height: 18px;
}

.toc-drawer-content {
    flex: 1;
    overflow-y: auto;
    padding: 12px 0;
}

.toc-drawer-item {
    padding: 12px 20px;
    font-size: 14px;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all var(--transition-fast);
    border-left: 3px solid transparent;
}

.toc-drawer-item:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
}

.toc-drawer-item.active {
    color: var(--primary-color);
    background: rgba(var(--primary-rgb), 0.08);
    border-left-color: var(--primary-color);
}

.toc-drawer-item.toc-level-2 {
    padding-left: 20px;
    font-weight: 500;
}

.toc-drawer-item.toc-level-3 {
    padding-left: 32px;
    font-size: 13px;
}

.toc-drawer-item.toc-level-4 {
    padding-left: 44px;
    font-size: 12px;
}

/* 抽屉动画 */
.toc-drawer-enter-active,
.toc-drawer-leave-active {
    transition: all 0.25s ease;
}

.toc-drawer-enter-active .toc-drawer,
.toc-drawer-leave-active .toc-drawer {
    transition: transform 0.25s ease;
}

.toc-drawer-enter-from,
.toc-drawer-leave-to {
    background: rgba(0, 0, 0, 0);
}

.toc-drawer-enter-from .toc-drawer,
.toc-drawer-leave-to .toc-drawer {
    transform: translateX(100%);
}

@media (max-width: 768px) {
    .mobile-toc-btn {
        display: flex !important;
    }

    .desktop-toc {
        display: none !important;
    }
}
</style>

<style>
/* 移动端目录按钮 - 非scoped，因为Teleport到body */
.mobile-toc-btn {
    display: flex;
    position: fixed;
    right: 16px;
    bottom: 80px;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: #0078D4;
    color: #fff;
    border: none;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    cursor: pointer;
    z-index: 999;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
}

.mobile-toc-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.mobile-toc-btn svg {
    width: 22px;
    height: 22px;
}

/* 移动端目录抽屉 */
.toc-drawer-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 2000;
    display: flex;
    justify-content: flex-end;
}

.toc-drawer {
    width: 280px;
    max-width: 80vw;
    height: 100%;
    background: var(--bg-primary);
    box-shadow: -4px 0 16px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
}

.toc-drawer-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    border-bottom: 1px solid var(--border-light);
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
}

.toc-drawer-close {
    width: 32px;
    height: 32px;
    border: none;
    background: transparent;
    color: var(--text-secondary);
    cursor: pointer;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
}

.toc-drawer-close:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
}

.toc-drawer-close svg {
    width: 18px;
    height: 18px;
}

.toc-drawer-content {
    flex: 1;
    overflow-y: auto;
    padding: 12px 0;
}

.toc-drawer-item {
    padding: 12px 20px;
    font-size: 14px;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
    border-left: 3px solid transparent;
}

.toc-drawer-item:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
}

.toc-drawer-item.active {
    color: var(--primary-color);
    background: rgba(64, 158, 255, 0.08);
    border-left-color: var(--primary-color);
}

.toc-drawer-item.toc-level-2 {
    padding-left: 20px;
    font-weight: 500;
}

.toc-drawer-item.toc-level-3 {
    padding-left: 32px;
    font-size: 13px;
}

.toc-drawer-item.toc-level-4 {
    padding-left: 44px;
    font-size: 12px;
}

/* 抽屉动画 */
.toc-drawer-enter-active,
.toc-drawer-leave-active {
    transition: all 0.25s ease;
}

.toc-drawer-enter-active .toc-drawer,
.toc-drawer-leave-active .toc-drawer {
    transition: transform 0.25s ease;
}

.toc-drawer-enter-from,
.toc-drawer-leave-to {
    background: rgba(0, 0, 0, 0);
}

.toc-drawer-enter-from .toc-drawer,
.toc-drawer-leave-to .toc-drawer {
    transform: translateX(100%);
}

@media (min-width: 769px) {
    .mobile-toc-btn {
        display: none !important;
    }
}

@media (max-width: 768px) {
    .mobile-toc-btn {
        display: flex !important;
    }
}
</style>
