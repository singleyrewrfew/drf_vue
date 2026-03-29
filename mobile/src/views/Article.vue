<template>
    <div class="page">
        <PageHeader title="详情">
            <template #right>
                <button class="btn-icon" @click="shareArticle">
                    <el-icon><Share /></el-icon>
                </button>
            </template>
        </PageHeader>

        <div v-if="loading" class="page-content" style="padding: 0">
            <Skeleton type="article" />
        </div>

        <div v-else-if="article" class="page-content" style="padding: 0; position: relative">
            <!-- 调试信息 -->
            <div v-if="0" style="padding: 20px; background: #f00; color: #fff">
                Debug: article = {{ article }}
            </div>

            <!-- 文章头部 -->
            <ArticleHeader :article="article" />

            <!-- 文章内容 -->
            <ArticleContent
                ref="articleContentRef"
                :content="article.content"
                :tags="article.tags"
            />

            <!-- 评论区 -->
            <CommentSection
                v-model:comments="comments"
                :article-id="article.id"
                :is-logged-in="userStore.isLoggedIn"
                :user-avatar="userStore.user?.avatar"
                @submit="handleCommentSubmit"
                @like="handleCommentLike"
            />

            <!-- 目录浮动按钮 -->
            <button v-if="tocItems.length" class="toc-fab" title="目录" @click="showToc = true">
                <el-icon><List /></el-icon>
            </button>
        </div>

        <div v-else class="page-content">
            <div class="empty-state">
                <el-icon class="empty-state-icon"><Document /></el-icon>
                <p class="empty-state-text">内容不存在或已删除</p>
            </div>
        </div>
    </div>

    <!-- 目录抽屉 -->
    <el-drawer v-model="showToc" direction="rtl" size="70%" title="目录" :with-header="true">
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
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Share, Document, List, ChatDotRound } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { marked } from 'marked'
import hljs from 'highlight.js'
import {
    getContent,
    getComments,
    createComment,
    likeComment as likeCommentApi,
} from '@/api/content'
import { getCoverUrl, getAvatarUrl, formatRelativeTime } from '@/utils'
import { useUserStore } from '@/stores/user'
import Skeleton from '@/components/Skeleton.vue'
import PageHeader from '@/components/PageHeader.vue'
import ArticleHeader from '@/components/article/ArticleHeader.vue'
import ArticleContent from '@/components/article/ArticleContent.vue'
import CommentSection from '@/components/article/CommentSection.vue'
import { useCommentAuth } from '@/composables/useCommentAuth'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const { requireAuth } = useCommentAuth()

const loading = ref(true)
const article = ref(null)
const comments = ref([])
const showToc = ref(false)
const activeTocId = ref('')
const articleContentRef = ref(null)

// 从子组件获取目录项
const tocItems = computed(() => {
    return articleContentRef.value?.tocItems || []
})

// 配置 marked 渲染器（保持原有逻辑）
let headingIdCounter = 0
const renderer = new marked.Renderer()
renderer.image = ({ href, title, text }) =>
    `<img src="${href}" alt="${text || ''}" loading="lazy" />`
renderer.code = ({ text, lang }) => {
    const code = text || ''
    let language = lang || ''
    let highlighted
    if (language && hljs.getLanguage(language)) {
        highlighted = hljs.highlight(code, { language }).value
    } else {
        highlighted = hljs.highlightAuto(code).value
    }
    return `<pre class="code-block"><code class="hljs language-${language}">${highlighted}</code></pre>`
}
renderer.heading = ({ text, depth }) => {
    const id = `heading-${headingIdCounter++}`
    return `<h${depth} id="${id}">${text}</h${depth}>`
}
marked.setOptions({ renderer })

// 获取文章详情
const fetchArticle = async () => {
    try {
        const { data } = await getContent(route.params.id)
        console.log('API 返回数据:', data)
        // 统一响应格式：data.data 才是实际数据
        article.value = data.data || data
        console.log('解析后的 article:', article.value)

        if (!article.value) {
            ElMessage.error('文章不存在')
        }
    } catch (e) {
        console.error(e)
        ElMessage.error('文章加载失败')
    } finally {
        loading.value = false
    }
}

// 获取评论列表
const fetchComments = async () => {
    try {
        const { data } = await getComments({ article: route.params.id })
        console.log('评论 API 返回:', data)
        // 如果是分页格式，取 results；如果是数组，直接使用
        comments.value = data.results || data || []
        console.log('解析后的评论:', comments.value)
        if (comments.value.length > 0) {
            console.log('第一条评论详情:', comments.value[0])
        }
    } catch (e) {
        console.error('评论加载失败:', e)
    }
}

// 处理评论提交
const handleCommentSubmit = async ({ article, content, parent, reply_to_id }) => {
    try {
        const { data } = await createComment({
            article,
            content,
            parent_comment: parent,
            reply_to: reply_to_id,
        })

        if (parent) {
            // 添加回复
            const parentComment = comments.value.find(c => c.id === parent)
            if (parentComment) {
                if (!parentComment.replies) parentComment.replies = []
                parentComment.replies.unshift(data.data)
                parentComment.reply_count++
            }
        } else {
            // 添加主评论
            comments.value.unshift(data.data)
        }

        ElMessage.success('评论成功')
    } catch (e) {
        console.error(e)
        ElMessage.error('评论失败，请重试')
    }
}

// 处理点赞
const handleCommentLike = async (commentId, parentId = null) => {
    if (!requireAuth('点赞')) return

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

// 分享文章
const shareArticle = () => {
    ElMessage.info('分享功能开发中')
}

// 滚动到指定标题
const scrollToHeading = id => {
    const element = document.getElementById(id)
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' })
        activeTocId.value = id
        showToc.value = false
    }
}

onMounted(() => {
    fetchArticle()
    fetchComments()
})
</script>

<style scoped>
/* 保持原有样式 */
.toc-fab {
    position: fixed;
    top: 50%;
    right: 20px;
    transform: translateY(-50%);
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--primary-color);
    color: white;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    z-index: 10;
    transition: all 0.3s;
}

.toc-fab:hover {
    transform: translateY(-50%) scale(1.1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.toc-list {
    padding: 8px 0;
}

.toc-item {
    display: block;
    padding: 8px 16px;
    color: var(--text-primary);
    text-decoration: none;
    font-size: 14px;
    line-height: 1.6;
    transition: all 0.2s;
    cursor: pointer;
}

.toc-item:hover {
    background: var(--bg-secondary);
}

.toc-item.active {
    color: var(--primary-color);
    font-weight: 500;
}

.empty-state {
    text-align: center;
    padding: 60px 20px;
}

.empty-state-icon {
    font-size: 64px;
    color: var(--text-tertiary);
    margin-bottom: 16px;
}

.empty-state-text {
    color: var(--text-secondary);
    font-size: 15px;
}
</style>
