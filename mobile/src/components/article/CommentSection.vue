<template>
    <div class="comment-section">
        <div class="section-title">
            <el-icon><ChatDotRound/></el-icon>
            <span>评论 ({{ comments.length }})</span>
        </div>

        <!-- 评论表单 -->
        <div v-if="isLoggedIn" class="comment-form">
            <div class="comment-form-wrapper">
                <el-avatar :size="36" :src="getAvatarUrl(userAvatar)">
                    {{ userInitial }}
                </el-avatar>
                <div class="comment-form-content">
                    <textarea
                        v-model="newCommentText"
                        class="comment-textarea"
                        placeholder="理性发言，友善互动...（最多 500 字）"
                        rows="3"
                        maxlength="500"
                    ></textarea>
                    <div class="comment-form-footer">
                        <div class="comment-form-tools">
                            <el-popover placement="top-start" :width="280" trigger="click">
                                <template #reference>
                                    <button class="tool-btn">
                                        <svg width="1.2em" height="1.2em" viewBox="0 0 24 24" fill="currentColor">
                                            <path d="M14.413 14.223a.785.785 0 0 1 1.45.601A4.174 4.174 0 0 1 12 17.4a4.19 4.19 0 0 1-2.957-1.221 4.174 4.174 0 0 1-.906-1.355.785.785 0 1 1 1.449-.601 2.604 2.604 0 0 0 1.413 1.41 2.621 2.621 0 0 0 2.849-.566c.242-.242.434-.529.565-.844ZM8.6 8.77a1.308 1.308 0 1 1 0 2.615 1.308 1.308 0 0 1 0-2.615ZM15.4 8.77a1.308 1.308 0 1 1 0 2.615 1.308 1.308 0 0 1 0-2.615Z"></path>
                                            <path fill-rule="evenodd" d="M12 1.573c5.758 0 10.427 4.669 10.427 10.427S17.758 22.427 12 22.427 1.573 17.758 1.573 12 6.242 1.573 12 1.573Zm0 1.746a8.681 8.681 0 1 0 .001 17.362A8.681 8.681 0 0 0 12 3.32Z" clip-rule="evenodd"></path>
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

        <!-- 评论列表 -->
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
                            <!-- 调试：输出评论数据 -->
                            <div v-if="0">Comment: {{ comment }}</div>
                            <button
                                class="action-btn"
                                :class="{ liked: comment.is_liked }"
                                @click="$emit('like', comment.id)"
                            >
                                <el-icon><Star/></el-icon>
                                <span>{{ comment.like_count ?? '赞' }}</span>
                            </button>
                            <button class="action-btn" @click="openReplyForm(comment)">
                                <el-icon><ChatDotRound/></el-icon>
                                <span>回复</span>
                            </button>
                        </div>

                        <!-- 回复表单 -->
                        <div v-if="replyToParent === comment.id" class="reply-form">
                            <div class="reply-form-header">
                                <span>回复 <span class="reply-target">@{{ replyToName }}</span></span>
                                <button class="cancel-btn" @click="closeReplyForm">取消</button>
                            </div>
                            <textarea
                                v-model="replyContent"
                                class="reply-textarea"
                                placeholder="写下你的回复...（最多 500 字）"
                                rows="2"
                                maxlength="500"
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

                        <!-- 回复列表 -->
                        <div v-if="comment.reply_count > 0" class="reply-section">
                            <div class="reply-toggle" @click="toggleReplies(comment.id)">
                                <span>{{ expandedReplies.includes(comment.id) ? '收起回复' : `${comment.reply_count} 条回复` }}</span>
                                <el-icon :class="{ rotated: expandedReplies.includes(comment.id) }">
                                    <ArrowRight/>
                                </el-icon>
                            </div>

                            <div v-if="expandedReplies.includes(comment.id) && comment.replies?.length" class="reply-list">
                                <div v-for="reply in comment.replies" :key="reply.id" class="reply-item">
                                    <el-avatar :size="28" :src="getAvatarUrl(reply.user_avatar)">
                                        {{ reply.user_name?.charAt(0)?.toUpperCase() }}
                                    </el-avatar>
                                    <div class="reply-body">
                                        <div class="reply-header">
                                            <span class="reply-author">{{ reply.user_name }}</span>
                                            <template v-if="reply.reply_to_name">
                                                <el-icon class="reply-arrow"><ArrowRight/></el-icon>
                                                <span class="reply-to-user">{{ reply.reply_to_name }}</span>
                                            </template>
                                            <span class="reply-time">{{ formatRelativeTime(reply.created_at) }}</span>
                                        </div>
                                        <p class="reply-text">{{ reply.content }}</p>
                                        <div class="reply-actions">
                                            <button
                                                class="action-btn small"
                                                :class="{ liked: reply.is_liked }"
                                                @click="$emit('like', reply.id, comment.id)"
                                            >
                                                <el-icon><Star/></el-icon>
                                                <span>{{ reply.like_count || '' }}</span>
                                            </button>
                                            <button class="action-btn small" @click="openReplyForm(reply, comment.id)">
                                                <el-icon><ChatDotRound/></el-icon>
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
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Star, ChatDotRound, ArrowRight } from '@element-plus/icons-vue'
import { getAvatarUrl, formatRelativeTime } from '@/utils'
import { useCommentAuth } from '@/composables/useCommentAuth'

const props = defineProps({
    comments: {
        type: Array,
        default: () => []
    },
    articleId: {
        type: [String, Number],
        required: true
    },
    isLoggedIn: {
        type: Boolean,
        default: false
    },
    userAvatar: {
        type: String,
        default: ''
    }
})

const emit = defineEmits(['submit', 'like', 'update:comments'])

const { requireAuth } = useCommentAuth()

const newCommentText = ref('')
const submitting = ref(false)
const replyToParent = ref(null)
const replyToName = ref('')
const replyToUserId = ref(null)
const replyContent = ref('')
const submittingReply = ref(false)
const expandedReplies = ref([])

const emojis = ['😀', '😂', '😍', '🤔', '👍', '🎉', '❤️', '🔥', '👏', '💯']

const userInitial = computed(() => props.userAvatar?.charAt(0)?.toUpperCase() || 'U')

const insertEmoji = (emoji) => {
    newCommentText.value += emoji
}

const openReplyForm = (target, parentCommentId = null) => {
    if (parentCommentId) {
        // 回复回复
        replyToParent.value = parentCommentId
        replyToName.value = target.user_name
        replyToUserId.value = target.user_id
    } else {
        // 回复主评论
        replyToParent.value = target.id
        replyToName.value = target.user_name
        replyToUserId.value = target.user_id
    }
    replyContent.value = ''
}

const closeReplyForm = () => {
    replyToParent.value = null
    replyToName.value = ''
    replyToUserId.value = null
    replyContent.value = ''
}

const toggleReplies = (commentId) => {
    const index = expandedReplies.value.indexOf(commentId)
    if (index > -1) {
        expandedReplies.value.splice(index, 1)
    } else {
        expandedReplies.value.push(commentId)
    }
}

const submitComment = async () => {
    if (!newCommentText.value.trim() || submitting.value) return
    
    if (!props.isLoggedIn) {
        requireAuth('评论')
        return
    }
    
    submitting.value = true
    try {
        emit('submit', {
            article: props.articleId,
            content: newCommentText.value.trim(),
            parent: null
        })
        newCommentText.value = ''
    } catch (e) {
        console.error(e)
    } finally {
        submitting.value = false
    }
}

const submitReply = async (parentId) => {
    if (!replyContent.value.trim() || submittingReply.value) return
    
    if (!props.isLoggedIn) {
        requireAuth('回复')
        return
    }
    
    submittingReply.value = true
    try {
        emit('submit', {
            article: props.articleId,
            content: replyContent.value.trim(),
            parent: parentId,
            reply_to_id: replyToUserId.value
        })
        closeReplyForm()
    } catch (e) {
        console.error(e)
    } finally {
        submittingReply.value = false
    }
}

watch(() => props.comments, () => {
    // 监听评论变化
}, { deep: true })
</script>

<style scoped>
.comment-section {
    padding: 16px;
    padding-bottom: 80px; /* 防止被底部导航栏遮挡 */
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

/* 完整的评论区样式 */
.comment-form {
    margin-bottom: 24px;
}

.comment-form-wrapper {
    display: flex;
    gap: 12px;
}

.comment-form-content {
    flex: 1;
}

.comment-textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    resize: vertical;
    font-family: inherit;
    font-size: 14px;
    line-height: 1.6;
    background: var(--bg-secondary);
}

.comment-textarea:focus {
    outline: none;
    border-color: var(--primary-color);
    background: var(--bg-primary);
}

.comment-form-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
}

.comment-form-tools {
    display: flex;
    gap: 8px;
}

.tool-btn {
    padding: 4px 8px;
    background: transparent;
    border: none;
    cursor: pointer;
    color: var(--text-tertiary);
    border-radius: var(--radius-sm);
}

.tool-btn:hover {
    background: var(--bg-secondary);
    color: var(--primary-color);
}

.emoji-list {
    display: grid;
    grid-template-columns: repeat(10, 1fr);
    gap: 4px;
}

.emoji-item {
    font-size: 20px;
    cursor: pointer;
    padding: 4px;
    border-radius: var(--radius-sm);
}

.emoji-item:hover {
    background: var(--bg-secondary);
    transform: scale(1.2);
}

.comment-form-actions {
    display: flex;
    align-items: center;
    gap: 12px;
}

.char-count {
    font-size: 12px;
    color: var(--text-tertiary);
}

.submit-btn {
    padding: 8px 24px;
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: var(--radius-md);
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
}

.submit-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.submit-btn:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.submit-btn.small {
    padding: 4px 16px;
    font-size: 13px;
}

.login-tip {
    text-align: center;
    padding: 24px;
    color: var(--text-secondary);
}

.login-tip p {
    margin-bottom: 12px;
}

.comment-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.comment-item {
    display: flex;
    gap: 12px;
}

.comment-body {
    flex: 1;
}

.comment-main {
    background: var(--bg-secondary);
    padding: 12px;
    border-radius: var(--radius-md);
}

.comment-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.comment-author {
    font-weight: 500;
    color: var(--text-primary);
    font-size: 14px;
}

.comment-time {
    font-size: 12px;
    color: var(--text-tertiary);
}

.comment-text {
    color: var(--text-primary);
    font-size: 14px;
    line-height: 1.6;
    margin: 8px 0;
    word-break: break-word;
}

.comment-actions {
    display: flex;
    gap: 16px;
    margin-top: 8px;
}

.action-btn {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 4px 8px;
    background: transparent;
    border: none;
    border-radius: var(--radius-sm);
    color: var(--text-tertiary);
    font-size: 13px;
    cursor: pointer;
}

.action-btn:hover {
    background: var(--bg-primary);
    color: var(--primary-color);
}

.action-btn.liked {
    color: #f56c6c;
}

.action-btn.small {
    padding: 2px 6px;
    font-size: 12px;
}

.reply-form {
    margin-top: 12px;
    background: var(--bg-primary);
    padding: 12px;
    border-radius: var(--radius-md);
}

.reply-form-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    font-size: 13px;
}

.reply-target {
    color: var(--primary-color);
    font-weight: 500;
}

.cancel-btn {
    background: transparent;
    border: none;
    color: var(--text-tertiary);
    cursor: pointer;
    font-size: 13px;
}

.reply-textarea {
    width: 100%;
    padding: 8px;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    resize: vertical;
    font-family: inherit;
    font-size: 13px;
    line-height: 1.5;
    background: var(--bg-secondary);
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

.reply-section {
    margin-top: 12px;
}

.reply-toggle {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 8px 0;
    color: var(--text-tertiary);
    font-size: 13px;
    cursor: pointer;
}

.reply-toggle:hover {
    color: var(--primary-color);
}

.reply-toggle .el-icon {
    transition: transform 0.3s;
}

.reply-toggle .el-icon.rotated {
    transform: rotate(90deg);
}

.reply-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 12px;
}

.reply-item {
    display: flex;
    gap: 8px;
}

.reply-body {
    flex: 1;
    background: var(--bg-primary);
    padding: 10px;
    border-radius: var(--radius-md);
}

.reply-header {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 6px;
    font-size: 13px;
}

.reply-author {
    font-weight: 500;
    color: var(--text-primary);
}

.reply-arrow {
    font-size: 12px;
    color: var(--text-tertiary);
}

.reply-to-user {
    color: var(--primary-color);
}

.reply-time {
    margin-left: auto;
    font-size: 12px;
    color: var(--text-tertiary);
}

.reply-text {
    color: var(--text-primary);
    font-size: 13px;
    line-height: 1.5;
    margin-bottom: 6px;
}

.reply-actions {
    display: flex;
    gap: 12px;
}

.empty-comments {
    text-align: center;
    padding: 40px 20px;
    color: var(--text-tertiary);
    font-size: 14px;
}
</style>
