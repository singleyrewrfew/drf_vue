<template>
    <div class="page">
        <PageHeader title="详情">
            <template #right>
                <button class="btn-icon" @click="shareArticle">
                    <el-icon>
                        <Share/>
                    </el-icon>
                </button>
            </template>
        </PageHeader>

        <div v-if="loading" class="page-content" style="padding: 0;">
            <Skeleton type="article"/>
        </div>

        <div v-else-if="article" class="page-content" style="padding: 0;">
            <div class="article-header">
                <h1 class="article-title">{{ article.title }}</h1>

                <div class="article-author">
                    <el-avatar :size="40" :src="getAvatarUrl(article.author_avatar)">
                        {{ article.author_name?.charAt(0) }}
                    </el-avatar>
                    <div class="author-info">
                        <span class="author-name">{{ article.author_name || '匿名用户' }}</span>
                        <span class="article-time">{{ formatRelativeTime(article.created_at) }}</span>
                    </div>
                </div>
            </div>

            <div v-if="article.cover_image" class="article-cover">
                <img :src="getCoverUrl(article.cover_image)" alt="" loading="lazy"/>
            </div>

            <div class="article-body markdown-body" v-html="renderedContent"></div>

            <div v-if="article.tags?.length" class="article-tags">
                <router-link
                    v-for="tag in article.tags"
                    :key="tag.id || tag"
                    :to="`/tag/${tag.slug || tag.id || tag}`"
                    class="tag"
                >
                    {{ tag.name || tag }}
                </router-link>
            </div>

            <div class="comment-section">
                <div class="section-title">
                    <el-icon>
                        <ChatDotRound/>
                    </el-icon>
                    <span>评论 ({{ comments.length }})</span>
                </div>

                <div v-if="userStore.isLoggedIn" class="comment-form">
                    <div class="comment-form-wrapper">
                        <el-avatar :size="36" :src="getAvatarUrl(userStore.user?.avatar)">
                            {{ userStore.user?.username?.charAt(0)?.toUpperCase() }}
                        </el-avatar>
                        <div class="comment-form-content">
              <textarea
                  v-model="newCommentText"
                  class="comment-textarea"
                  placeholder="理性发言，友善互动..."
                  rows="3"
              ></textarea>
                            <div class="comment-form-footer">
                                <div class="comment-form-tools">
                                    <el-popover placement="top-start" :width="280" trigger="click">
                                        <template #reference>
                                            <button class="tool-btn">
                                                <svg width="1.2em" height="1.2em" viewBox="0 0 24 24"
                                                     fill="currentColor">
                                                    <path
                                                        d="M14.413 14.223a.785.785 0 0 1 1.45.601A4.174 4.174 0 0 1 12 17.4a4.19 4.19 0 0 1-2.957-1.221 4.174 4.174 0 0 1-.906-1.355.785.785 0 1 1 1.449-.601 2.604 2.604 0 0 0 1.413 1.41 2.621 2.621 0 0 0 2.849-.566c.242-.242.434-.529.565-.844ZM8.6 8.77a1.308 1.308 0 1 1 0 2.615 1.308 1.308 0 0 1 0-2.615ZM15.4 8.77a1.308 1.308 0 1 1 0 2.615 1.308 1.308 0 0 1 0-2.615Z"></path>
                                                    <path fill-rule="evenodd"
                                                          d="M12 1.573c5.758 0 10.427 4.669 10.427 10.427S17.758 22.427 12 22.427 1.573 17.758 1.573 12 6.242 1.573 12 1.573Zm0 1.746a8.681 8.681 0 1 0 .001 17.362A8.681 8.681 0 0 0 12 3.32Z"
                                                          clip-rule="evenodd"></path>
                                                </svg>
                                            </button>
                                        </template>
                                        <div class="emoji-picker">
                                            <div class="emoji-list">
                        <span v-for="emoji in emojis" :key="emoji" class="emoji-item" @click="insertEmoji(emoji)">
                          {{ emoji }}
                        </span>
                                            </div>
                                        </div>
                                    </el-popover>
                                </div>
                                <div class="comment-form-actions">
                                    <span class="char-count">{{ newCommentText.length }}/500</span>
                                    <button
                                        class="submit-btn"
                                        :disabled="!newCommentText.trim() || submitting"
                                        @click="submitComment"
                                    >
                                        发布
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-else class="login-tip">
                    <p>登录后才能评论</p>
                    <button class="btn btn-primary" @click="$router.push('/login')">立即登录</button>
                </div>

                <div class="comment-list">
                    <div
                        v-for="comment in comments"
                        :key="comment.id"
                        class="comment-item"
                    >
                        <el-avatar :size="40" :src="getAvatarUrl(comment.user_avatar)">
                            {{ comment.user_name?.charAt(0)?.toUpperCase() }}
                        </el-avatar>
                        <div class="comment-body">
                            <div class="comment-main">
                                <div class="comment-header">
                                    <span class="comment-author">{{ comment.user_name }}</span>
                                    <span class="comment-time">{{ formatRelativeTime(comment.created_at) }}</span>
                                </div>
                                <p class="comment-text">{{ comment.content }}</p>
                                <div class="comment-actions">
                                    <button
                                        class="action-btn"
                                        :class="{ liked: comment.is_liked }"
                                        @click="likeComment(comment.id)"
                                    >
                                        <el-icon>
                                            <Star/>
                                        </el-icon>
                                        <span>{{ comment.like_count || '' }}</span>
                                    </button>
                                    <button class="action-btn"
                                            @click="openReplyForm(comment.id, comment.user_name, comment.user_id)">
                                        <el-icon>
                                            <ChatDotRound/>
                                        </el-icon>
                                        <span>回复</span>
                                    </button>
                                </div>

                                <div v-if="replyToParent === comment.id" class="reply-form">
                                    <div class="reply-form-header">
                                        <span>回复 <span class="reply-target">@{{ replyToName }}</span></span>
                                        <button class="cancel-btn" @click="closeReplyForm">取消</button>
                                    </div>
                                    <textarea
                                        v-model="replyContent"
                                        class="reply-textarea"
                                        placeholder="写下你的回复..."
                                        rows="2"
                                    ></textarea>
                                    <div class="reply-form-footer">
                                        <span class="char-count">{{ replyContent.length }}/500</span>
                                        <button
                                            class="submit-btn small"
                                            :disabled="!replyContent.trim() || submittingReply"
                                            @click="submitReply(comment.id)"
                                        >
                                            发送
                                        </button>
                                    </div>
                                </div>

                                <div v-if="comment.reply_count > 0" class="reply-section">
                                    <div
                                        class="reply-toggle"
                                        @click="toggleReplies(comment.id)"
                                    >
                                        <span>{{
                                                expandedReplies.includes(comment.id) ? '收起回复' : `${comment.reply_count} 条回复`
                                            }}</span>
                                        <el-icon :class="{ rotated: expandedReplies.includes(comment.id) }">
                                            <ArrowRight/>
                                        </el-icon>
                                    </div>

                                    <div v-if="expandedReplies.includes(comment.id) && comment.replies?.length"
                                         class="reply-list">
                                        <div v-for="reply in comment.replies" :key="reply.id" class="reply-item">
                                            <el-avatar :size="28" :src="getAvatarUrl(reply.user_avatar)">
                                                {{ reply.user_name?.charAt(0)?.toUpperCase() }}
                                            </el-avatar>
                                            <div class="reply-body">
                                                <div class="reply-header">
                                                    <span class="reply-author">{{ reply.user_name }}</span>
                                                    <template v-if="reply.reply_to_name">
                                                        <el-icon class="reply-arrow">
                                                            <ArrowRight/>
                                                        </el-icon>
                                                        <span class="reply-to-user">{{ reply.reply_to_name }}</span>
                                                    </template>
                                                    <span class="reply-time">{{
                                                            formatRelativeTime(reply.created_at)
                                                        }}</span>
                                                </div>
                                                <p class="reply-text">{{ reply.content }}</p>
                                                <div class="reply-actions">
                                                    <button
                                                        class="action-btn small"
                                                        :class="{ liked: reply.is_liked }"
                                                        @click="likeComment(reply.id, comment.id)"
                                                    >
                                                        <el-icon>
                                                            <Star/>
                                                        </el-icon>
                                                        <span>{{ reply.like_count || '' }}</span>
                                                    </button>
                                                    <button class="action-btn small"
                                                            @click="openReplyForm(comment.id, reply.user_name, reply.user_id)">
                                                        <el-icon>
                                                            <ChatDotRound/>
                                                        </el-icon>
                                                        <span>回复</span>
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-if="comments.length === 0" class="empty-comments">
                        暂无评论，快来抢沙发吧~
                    </div>

                    <div v-if="comments.length > 3" class="show-more-comments">
                        <button class="more-btn" @click="showCommentsDialog = true">
                            查看全部 {{ comments.length }} 条评论
                        </button>
                    </div>
                </div>
            </div>

            <button
                v-if="tocItems.length"
                class="toc-fab"
                @click="showToc = true"
                title="目录"
            >
                <el-icon>
                    <List/>
                </el-icon>
            </button>
        </div>

        <div v-else class="page-content">
            <div class="empty-state">
                <el-icon class="empty-state-icon">
                    <Document/>
                </el-icon>
                <p class="empty-state-text">内容不存在或已删除</p>
            </div>
        </div>

        <el-drawer
            v-model="showToc"
            direction="rtl"
            size="70%"
            title="目录"
            :with-header="true"
        >
            <div class="toc-list">
                <a
                    v-for="item in tocItems"
                    :key="item.id"
                    class="toc-item"
                    :class="{ active: activeTocId === item.id }"
                    :style="{ paddingLeft: (item.level - 1) * 12 + 16 + 'px' }"
                    @click="scrollToHeading(item.id)"
                >
                    {{ item.text }}
                </a>
            </div>
        </el-drawer>

        <el-drawer
            v-model="showCommentsDialog"
            direction="btt"
            size="90%"
            title="全部评论"
            :with-header="true"
        >
            <div class="all-comments">
                <div
                    v-for="comment in comments"
                    :key="comment.id"
                    class="comment-item"
                >
                    <el-avatar :size="40" :src="getAvatarUrl(comment.user_avatar)">
                        {{ comment.user_name?.charAt(0)?.toUpperCase() }}
                    </el-avatar>
                    <div class="comment-body">
                        <div class="comment-main">
                            <div class="comment-header">
                                <span class="comment-author">{{ comment.user_name }}</span>
                                <span class="comment-time">{{ formatRelativeTime(comment.created_at) }}</span>
                            </div>
                            <p class="comment-text">{{ comment.content }}</p>
                            <div class="comment-actions">
                                <button
                                    class="action-btn"
                                    :class="{ liked: comment.is_liked }"
                                    @click="likeComment(comment.id)"
                                >
                                    <el-icon>
                                        <Star/>
                                    </el-icon>
                                    <span>{{ comment.like_count || '' }}</span>
                                </button>
                                <button class="action-btn"
                                        @click="openReplyForm(comment.id, comment.user_name, comment.user_id); showCommentsDialog = false">
                                    <el-icon>
                                        <ChatDotRound/>
                                    </el-icon>
                                    <span>回复</span>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </el-drawer>
    </div>
</template>

<script setup>
import {ref, computed, onMounted, nextTick, watch} from 'vue'
import {useRoute} from 'vue-router'
import {ElMessage} from 'element-plus'
import {Share, Document, List, Star, ChatDotRound, ArrowRight} from '@element-plus/icons-vue'
import {marked} from 'marked'
import hljs from 'highlight.js'
import {getContent, getComments, createComment, likeComment as likeCommentApi} from '@/api/content'
import {getCoverUrl, getAvatarUrl, formatRelativeTime} from '@/utils'
import {useUserStore} from '@/stores/user'
import Skeleton from '@/components/Skeleton.vue'
import PageHeader from '@/components/PageHeader.vue'

const route = useRoute()
const userStore = useUserStore()
const loading = ref(true)
const article = ref(null)
const showToc = ref(false)
const tocItems = ref([])
const activeTocId = ref('')
const comments = ref([])
const newCommentText = ref('')
const submitting = ref(false)
const showCommentsDialog = ref(false)
const expandedReplies = ref([])
const replyToParent = ref(null)
const replyToName = ref('')
const replyToUserId = ref(null)
const replyContent = ref('')
const submittingReply = ref(false)

const emojis = ['😀', '😂', '😍', '🥰', '😎', '🤔', '👍', '👎', '❤️', '💔', '🎉', '🔥', '✨', '🌟', '⭐', '💯', '💪', '🙏', '😭', '😱', '🤣', '😊', '🥺', '👏', '🙄', '😴', '😋', '😜', '🤪', '😇']

const insertEmoji = (emoji) => {
    newCommentText.value += emoji
}

const openReplyForm = (parentId, userName, userId) => {
    replyToParent.value = parentId
    replyToName.value = userName
    replyToUserId.value = userId
    replyContent.value = ''
}

const closeReplyForm = () => {
    replyToParent.value = null
    replyToName.value = ''
    replyToUserId.value = null
    replyContent.value = ''
}

const toggleReplies = async (commentId) => {
    const index = expandedReplies.value.indexOf(commentId)
    if (index > -1) {
        expandedReplies.value.splice(index, 1)
    } else {
        expandedReplies.value.push(commentId)
    }
}

const submitReply = async (parentId) => {
    if (!replyContent.value.trim() || submittingReply.value) return

    if (!userStore.isLoggedIn) {
        ElMessage.warning('请先登录')
        return
    }

    submittingReply.value = true
    try {
        const {data} = await createComment({
            article: article.value.id,
            content: replyContent.value.trim(),
            parent: parentId,
            reply_to_id: replyToUserId.value
        })

        // 补充用户信息
        const newReply = {
            ...data,
            user_id: userStore.user?.id,
            user_name: userStore.user?.username,
            user_avatar: userStore.user?.avatar,
            reply_to_name: replyToName.value,
            like_count: data.like_count || 0,
            replies: []
        }

        const parentComment = comments.value.find(c => c.id === parentId)
        if (parentComment) {
            if (!parentComment.replies) parentComment.replies = []
            parentComment.replies.push(newReply)
            parentComment.reply_count = (parentComment.reply_count || 0) + 1
            if (!expandedReplies.value.includes(parentId)) {
                expandedReplies.value.push(parentId)
            }
        }

        closeReplyForm()
        ElMessage.success('回复成功')
    } catch (e) {
        console.error(e)
        ElMessage.error('回复失败')
    } finally {
        submittingReply.value = false
    }
}

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
    if (!article.value?.content) return ''
    headingIdCounter = 0
    tocItems.value = []

    const html = marked(article.value.content)

    const headingRegex = /<h([1-6]) id="([^"]+)">([^<]+)<\/h\1>/g
    let match
    while ((match = headingRegex.exec(html)) !== null) {
        tocItems.value.push({
            level: parseInt(match[1]),
            id: match[2],
            text: match[3]
        })
    }

    return html
})

const scrollToHeading = (id) => {
    showToc.value = false
    const el = document.getElementById(id)
    if (el) {
        const pageContent = document.querySelector('.page-content')
        const headerOffset = 60
        const elementPosition = el.offsetTop

        if (pageContent) {
            pageContent.scrollTo({
                top: elementPosition - headerOffset,
                behavior: 'smooth'
            })
        }
        activeTocId.value = id
    }
}

const updateActiveToc = () => {
    const pageContent = document.querySelector('.page-content')
    if (!pageContent) return

    const scrollTop = pageContent.scrollTop + 80
    let currentId = ''

    for (const item of tocItems.value) {
        const el = document.getElementById(item.id)
        if (el && el.offsetTop <= scrollTop) {
            currentId = item.id
        }
    }

    activeTocId.value = currentId
}

const fetchComments = async () => {
    if (!article.value?.id) return
    try {
        const {data} = await getComments({content: article.value.id})
        comments.value = data.results || data
    } catch (e) {
        console.error(e)
    }
}

const submitComment = async () => {
    if (!newCommentText.value.trim() || submitting.value) return

    if (!userStore.isLoggedIn) {
        ElMessage.warning('请先登录')
        return
    }

    submitting.value = true
    try {
        const {data} = await createComment({
            article: article.value.id,
            content: newCommentText.value.trim()
        })

        // 补充用户信息
        const newComment = {
            ...data,
            user_id: userStore.user?.id,
            user_name: userStore.user?.username,
            user_avatar: userStore.user?.avatar,
            like_count: data.like_count || 0,
            reply_count: 0,
            replies: []
        }

        comments.value.unshift(newComment)
        newCommentText.value = ''
        ElMessage.success('评论成功')
    } catch (e) {
        console.error(e)
        ElMessage.error('评论失败')
    } finally {
        submitting.value = false
    }
}

const likeComment = async (commentId, parentId = null) => {
    try {
        await likeCommentApi(commentId)

        if (parentId) {
            const parentComment = comments.value.find(c => c.id === parentId)
            if (parentComment?.replies) {
                const reply = parentComment.replies.find(r => r.id === commentId)
                if (reply) {
                    reply.like_count = (reply.like_count || 0) + 1
                    reply.is_liked = true
                }
            }
        } else {
            const comment = comments.value.find(c => c.id === commentId)
            if (comment) {
                comment.like_count = (comment.like_count || 0) + 1
                comment.is_liked = true
            }
        }
    } catch (e) {
        console.error(e)
    }
}

watch(() => article.value, async () => {
    if (article.value) {
        await nextTick()
        const pageContent = document.querySelector('.page-content')
        if (pageContent) {
            pageContent.addEventListener('scroll', updateActiveToc)
        }
        fetchComments()
    }
})

const fetchArticle = async () => {
    loading.value = true
    try {
        const {data} = await getContent(route.params.id)
        article.value = data
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
}

const shareArticle = async () => {
    if (navigator.share) {
        try {
            await navigator.share({
                title: article.value?.title,
                url: window.location.href
            })
        } catch (e) {
        }
    } else {
        await navigator.clipboard.writeText(window.location.href)
        ElMessage.success('链接已复制')
    }
}

onMounted(fetchArticle)
</script>

<style scoped>
.article-header {
    padding: 16px;
    padding-bottom: 0;
}

.article-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.5;
    margin: 0 0 16px;
}

.article-author {
    display: flex;
    align-items: center;
    gap: 12px;
}

.author-info {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.author-name {
    font-size: 15px;
    font-weight: 500;
    color: var(--text-primary);
}

.article-time {
    font-size: 12px;
    color: var(--text-tertiary);
    margin-top: 2px;
}

.article-cover {
    margin: 16px 0;
}

.article-cover img {
    width: 100%;
    display: block;
}

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

.markdown-body :deep(h1) {
    font-size: 20px;
}

.markdown-body :deep(h2) {
    font-size: 18px;
}

.markdown-body :deep(h3) {
    font-size: 16px;
}

.markdown-body :deep(h4) {
    font-size: 15px;
}

.markdown-body :deep(p) {
    margin-bottom: 16px;
}

.markdown-body :deep(a) {
    color: var(--primary-color);
}

.markdown-body :deep(img) {
    max-width: 100%;
    border-radius: var(--radius-md);
    margin: 12px 0;
}

.markdown-body :deep(.code-block) {
    background: #282c34;
    padding: 16px;
    border-radius: var(--radius-md);
    overflow-x: auto;
    margin: 16px 0;
    -webkit-overflow-scrolling: touch;
}

.markdown-body :deep(.code-block code) {
    font-family: var(--font-mono);
    font-size: 13px;
    line-height: 1.6;
    color: #abb2bf;
    background: transparent;
    padding: 0;
}

.markdown-body :deep(pre) {
    background: var(--bg-secondary);
    padding: 12px;
    border-radius: var(--radius-md);
    overflow-x: auto;
    margin: 12px 0;
}

.markdown-body :deep(code) {
    font-family: var(--font-mono);
    font-size: 13px;
}

.markdown-body :deep(p code) {
    background: var(--bg-secondary);
    padding: 2px 6px;
    border-radius: var(--radius-sm);
}

.markdown-body :deep(blockquote) {
    border-left: 3px solid var(--primary-color);
    padding-left: 12px;
    margin: 12px 0;
    color: var(--text-secondary);
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
    padding-left: 20px;
    margin: 12px 0;
}

.markdown-body :deep(li) {
    margin-bottom: 6px;
}

.markdown-body :deep(table) {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    display: block;
    overflow-x: auto;
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
    border: 1px solid var(--border-color);
    padding: 8px 12px;
    text-align: left;
}

.markdown-body :deep(th) {
    background: var(--bg-secondary);
    font-weight: 500;
}

.markdown-body :deep(hr) {
    border: none;
    height: 1px;
    background: var(--border-color);
    margin: 20px 0;
}

.markdown-body :deep(strong),
.markdown-body :deep(b) {
    font-weight: 600;
    color: var(--text-primary);
}

.markdown-body :deep(em),
.markdown-body :deep(i) {
    font-style: italic;
}

.markdown-body :deep(del),
.markdown-body :deep(s) {
    text-decoration: line-through;
    color: var(--text-tertiary);
}

.markdown-body :deep(mark) {
    background: #fff3b0;
    padding: 2px 4px;
    border-radius: 2px;
}

:global(.dark) .markdown-body :deep(mark),
:global([data-theme="dark"]) .markdown-body :deep(mark) {
    background: #5c4a00;
}

.markdown-body :deep(kbd) {
    display: inline-block;
    padding: 2px 6px;
    font-size: 12px;
    font-family: var(--font-mono);
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    box-shadow: inset 0 -1px 0 var(--border-color);
}

.markdown-body :deep(sup),
.markdown-body :deep(sub) {
    font-size: 0.75em;
    vertical-align: baseline;
    position: relative;
    top: -0.5em;
}

.markdown-body :deep(sub) {
    top: 0.2em;
}

.markdown-body :deep(details) {
    margin: 12px 0;
    padding: 12px;
    background: var(--bg-secondary);
    border-radius: var(--radius-md);
}

.markdown-body :deep(summary) {
    cursor: pointer;
    font-weight: 500;
    color: var(--text-primary);
}

.markdown-body :deep(details[open] summary) {
    margin-bottom: 12px;
}

.markdown-body :deep(ul) {
    list-style-type: disc;
}

.markdown-body :deep(ol) {
    list-style-type: decimal;
}

.markdown-body :deep(ul ul) {
    list-style-type: circle;
}

.markdown-body :deep(ul ul ul) {
    list-style-type: square;
}

.markdown-body :deep(.task-list-item) {
    list-style: none;
    margin-left: -20px;
}

.markdown-body :deep(.task-list-item input) {
    margin-right: 8px;
    vertical-align: middle;
}

.markdown-body :deep(abbr) {
    border-bottom: 1px dotted var(--text-tertiary);
    cursor: help;
}

.markdown-body :deep(pre code) {
    background: transparent;
    padding: 0;
}

.markdown-body :deep(figure) {
    margin: 16px 0;
}

.markdown-body :deep(figcaption) {
    font-size: 12px;
    color: var(--text-tertiary);
    text-align: center;
    margin-top: 8px;
}

.markdown-body :deep(.hljs-keyword),
.markdown-body :deep(.hljs-selector-tag),
.markdown-body :deep(.hljs-built_in) {
    color: #c678dd;
}

.markdown-body :deep(.hljs-string),
.markdown-body :deep(.hljs-title),
.markdown-body :deep(.hljs-section),
.markdown-body :deep(.hljs-attribute) {
    color: #98c379;
}

.markdown-body :deep(.hljs-number),
.markdown-body :deep(.hljs-literal),
.markdown-body :deep(.hljs-variable) {
    color: #d19a66;
}

.markdown-body :deep(.hljs-comment),
.markdown-body :deep(.hljs-quote) {
    color: #5c6370;
    font-style: italic;
}

.markdown-body :deep(.hljs-function) {
    color: #61afef;
}

.markdown-body :deep(.hljs-params) {
    color: #abb2bf;
}

.markdown-body :deep(.hljs-class .hljs-title),
.markdown-body :deep(.hljs-type) {
    color: #e5c07b;
}

.markdown-body :deep(.hljs-tag),
.markdown-body :deep(.hljs-name) {
    color: #e06c75;
}

.markdown-body :deep(.hljs-attr) {
    color: #d19a66;
}

.markdown-body :deep(.hljs-symbol),
.markdown-body :deep(.hljs-bullet) {
    color: #61afef;
}

.markdown-body :deep(.hljs-meta) {
    color: #61afef;
}

.markdown-body :deep(.hljs-addition) {
    background: rgba(152, 195, 121, 0.15);
    color: #98c379;
}

.markdown-body :deep(.hljs-deletion) {
    background: rgba(224, 108, 117, 0.15);
    color: #e06c75;
}

.markdown-body :deep(.hljs-emphasis) {
    font-style: italic;
}

.markdown-body :deep(.hljs-strong) {
    font-weight: bold;
}

.toc-list {
    padding: 0;
}

.toc-item {
    display: block;
    padding: 12px 16px;
    font-size: 14px;
    color: var(--text-secondary);
    text-decoration: none;
    border-left: 2px solid transparent;
    transition: all var(--transition-fast);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.toc-item:active {
    background: var(--bg-secondary);
}

.toc-item.active {
    color: var(--primary-color);
    border-left-color: var(--primary-color);
    background: var(--primary-bg);
}

.toc-fab {
    position: fixed;
    right: 16px;
    top: 50%;
    transform: translateY(-50%);
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--card-bg);
    box-shadow: var(--shadow-md);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-secondary);
    z-index: var(--z-sticky);
    transition: all var(--transition-fast);
}

.toc-fab:active {
    transform: translateY(-50%) scale(0.95);
    background: var(--bg-secondary);
}

:global(.dark) .toc-fab,
:global([data-theme="dark"]) .toc-fab {
    background: var(--bg-tertiary);
}

.comment-section {
    margin-top: 24px;
    padding: 16px;
    padding-bottom: calc(var(--tab-bar-height) + var(--safe-area-bottom) + 16px);
    background: var(--card-bg);
}

.section-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 16px;
}

.section-title .el-icon {
    color: var(--primary-color);
}

.comment-form {
    margin-bottom: 20px;
}

.comment-form-wrapper {
    display: flex;
    gap: 12px;
    background: var(--bg-secondary);
    border-radius: var(--radius-md);
    padding: 14px;
}

.comment-form-wrapper .el-avatar {
    border-radius: var(--radius-sm) !important;
    border: 2px solid var(--border-color);
}

.comment-form-content {
    flex: 1;
}

.comment-textarea {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    background: var(--bg-color);
    color: var(--text-primary);
    font-size: 14px;
    line-height: 1.6;
    resize: none;
    font-family: inherit;
}

.comment-textarea::placeholder {
    color: var(--text-placeholder);
}

.comment-textarea:focus {
    outline: none;
    border-color: var(--primary-color);
}

.comment-form-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;
}

.comment-form-tools {
    display: flex;
    gap: 6px;
}

.tool-btn {
    padding: 6px 10px;
    color: var(--text-tertiary);
    font-size: 18px;
    border-radius: var(--radius-sm);
    transition: all var(--transition-fast);
}

.tool-btn:active {
    color: var(--primary-color);
    background: var(--primary-bg);
}

.comment-form-actions {
    display: flex;
    align-items: center;
    gap: 10px;
}

.char-count {
    font-size: 12px;
    color: var(--text-tertiary);
}

.submit-btn {
    padding: 6px 16px;
    background: var(--primary-color);
    color: #fff;
    border-radius: var(--radius-sm);
    font-size: 14px;
    font-weight: 500;
}

.submit-btn:disabled {
    opacity: 0.5;
}

.submit-btn:not(:disabled):active {
    opacity: 0.8;
}

.emoji-picker {
    max-height: 200px;
    overflow-y: auto;
}

.emoji-list {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 6px;
}

.emoji-item {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    font-size: 18px;
    cursor: pointer;
    border-radius: var(--radius-sm);
    transition: all var(--transition-fast);
}

.emoji-item:active {
    background: var(--primary-bg);
    transform: scale(1.1);
}

.login-tip {
    text-align: center;
    padding: 24px;
    background: linear-gradient(135deg, var(--primary-bg) 0%, var(--bg-secondary) 100%);
    border-radius: var(--radius-md);
    margin-bottom: 16px;
}

.login-tip p {
    color: var(--text-secondary);
    margin-bottom: 12px;
    font-size: 14px;
}

.comment-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.comment-item {
    display: flex;
    gap: 12px;
    background: var(--bg-secondary);
    padding: 14px;
    border-radius: var(--radius-md);
    transition: all var(--transition-fast);
}

.comment-item .el-avatar {
    border-radius: var(--radius-sm) !important;
    border: 2px solid var(--border-color);
}

.comment-body {
    flex: 1;
}

.comment-main {
    background: transparent;
    padding: 0;
}

.comment-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
}

.comment-author {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 14px;
}

.comment-time {
    font-size: 12px;
    color: var(--text-tertiary);
}

.comment-text {
    font-size: 14px;
    color: var(--text-primary);
    line-height: 1.7;
    margin: 0;
}

.comment-actions {
    margin-top: 10px;
    display: flex;
    gap: 16px;
}

.action-btn {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    color: var(--text-tertiary);
    padding: 4px 10px;
    border-radius: var(--radius-full);
    transition: all var(--transition-fast);
}

.action-btn:active {
    color: var(--primary-color);
    background: var(--primary-bg);
}

.action-btn.liked {
    color: var(--primary-color);
    background: var(--primary-bg);
}

.empty-comments {
    text-align: center;
    padding: 32px;
    color: var(--text-tertiary);
    font-size: 14px;
}

.reply-section {
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid var(--border-color);
}

.reply-toggle {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 13px;
    color: var(--primary-color);
    cursor: pointer;
    padding: 4px 0;
}

.reply-toggle .el-icon {
    font-size: 12px;
    transition: transform var(--transition-fast);
}

.reply-toggle .el-icon.rotated {
    transform: rotate(90deg);
}

.reply-list {
    margin-top: 12px;
    padding-left: 12px;
    border-left: 2px solid var(--border-color);
}

.reply-item {
    display: flex;
    gap: 10px;
    padding: 10px 0;
}

.reply-item .el-avatar {
    border-radius: var(--radius-sm) !important;
    border: 2px solid var(--border-color);
}

.reply-body {
    flex: 1;
}

.reply-header {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 4px;
    flex-wrap: wrap;
}

.reply-author {
    font-weight: 500;
    color: var(--text-primary);
    font-size: 13px;
}

.reply-arrow {
    font-size: 10px;
    color: var(--text-tertiary);
}

.reply-to-user {
    font-size: 13px;
    color: var(--primary-color);
}

.reply-time {
    font-size: 11px;
    color: var(--text-tertiary);
}

.reply-text {
    font-size: 13px;
    color: var(--text-primary);
    line-height: 1.6;
    margin: 0;
}

.reply-actions {
    margin-top: 6px;
    display: flex;
    gap: 12px;
}

.action-btn.small {
    font-size: 11px;
    padding: 2px 8px;
}

.reply-form {
    margin-top: 12px;
    padding: 12px;
    background: var(--bg-tertiary);
    border-radius: var(--radius-md);
}

.reply-form-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    font-size: 13px;
    color: var(--text-secondary);
}

.reply-target {
    color: var(--primary-color);
    font-weight: 500;
}

.cancel-btn {
    font-size: 12px;
    color: var(--text-tertiary);
}

.reply-textarea {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    background: var(--bg-color);
    color: var(--text-primary);
    font-size: 13px;
    line-height: 1.5;
    resize: none;
    font-family: inherit;
}

.reply-textarea::placeholder {
    color: var(--text-placeholder);
}

.reply-textarea:focus {
    outline: none;
    border-color: var(--primary-color);
}

.reply-form-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
}

.submit-btn.small {
    padding: 4px 12px;
    font-size: 13px;
}

.show-more-comments {
    text-align: center;
    padding: 16px;
}

.more-btn {
    color: var(--primary-color);
    font-size: 14px;
    font-weight: 500;
}

.all-comments {
    padding: 0 16px;
    padding-bottom: calc(var(--tab-bar-height) + var(--safe-area-bottom) + 16px);
}
</style>
