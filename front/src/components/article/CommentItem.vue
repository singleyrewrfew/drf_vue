<template>
    <div class="comment-item">
        <el-avatar :size="40" :src="comment.user_avatar" class="user-avatar">
            {{ userInitial }}
        </el-avatar>
        
        <div class="comment-body">
            <div class="comment-main">
                <div class="comment-header">
                    <span class="comment-author">{{ comment.user_name }}</span>
                    <span class="comment-time">{{ formattedTime }}</span>
                </div>
                
                <p class="comment-text" v-html="sanitizedContent"></p>
                
                <div class="comment-actions">
                    <span
                        class="action-btn"
                        :class="{ liked: isLiked }"
                        @click="handleLike"
                    >
                        <el-icon><Pointer/></el-icon>
                        <span>{{ likeCount }}</span>
                    </span>
                    
                    <span class="action-btn" @click="handleReply">
                        <el-icon><ChatDotRound/></el-icon>
                        <span>回复</span>
                    </span>
                </div>
            </div>
            
            <!-- 回复表单 -->
            <div v-if="isReplying" class="reply-form">
                <div class="reply-form-header">
                    <span>回复 <span class="reply-target">@{{ replyToName }}</span></span>
                    <el-button link size="small" @click="$emit('close-reply')">取消</el-button>
                </div>
                
                <el-input
                    v-model="replyContentLocal"
                    type="textarea"
                    :rows="2"
                    placeholder="写下你的回复..."
                    :autosize="{ minRows: 2, maxRows: 6 }"
                    resize="none"
                    @keyup.ctrl.enter="handleSubmit"
                />
                
                <div class="reply-form-actions">
                    <span class="reply-tip">Ctrl + Enter 发送</span>
                    <el-button 
                        type="primary" 
                        size="small" 
                        @click="handleSubmit"
                        :loading="submittingReply"
                    >
                        发送
                    </el-button>
                </div>
            </div>
            
            <!-- 回复列表 -->
            <div v-if="hasReplies" class="reply-section">
                <div
                    class="reply-toggle"
                    @click="handleToggleReplies"
                >
                    <span>{{ toggleText }}</span>
                    <el-icon :class="{ rotated: isExpanded }">
                        <ArrowRight/>
                    </el-icon>
                </div>
                
                <div v-if="isExpanded && comment.replies?.length" class="reply-list">
                    <div 
                        v-for="reply in comment.replies" 
                        :key="reply.id"
                        class="reply-item"
                    >
                        <el-avatar :size="24" :src="reply.user_avatar" class="reply-avatar">
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
                                
                                <span class="reply-time">{{ formatRelativeTime(reply.created_at) }}</span>
                            </div>
                            
                            <p class="reply-text" v-html="sanitizeReplyContent(reply.content)"></p>
                            
                            <div class="reply-actions">
                                <span
                                    class="action-btn small"
                                    :class="{ liked: reply.is_liked }"
                                    @click.stop="$emit('like', reply)"
                                >
                                    <el-icon><Pointer/></el-icon>
                                    <span>{{ reply.like_count || '' }}</span>
                                </span>
                                
                                <span 
                                    class="action-btn small"
                                    @click.stop="handleReplyToReply(reply)"
                                >
                                    <el-icon><ChatDotRound/></el-icon>
                                    <span>回复</span>
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { Pointer, ChatDotRound, ArrowRight } from '@element-plus/icons-vue'
import { sanitizeHtml, formatRelativeTime } from '@/utils'
import { useCommentAuth } from '@/composables/useCommentAuth'

const { requireAuth } = useCommentAuth()

const props = defineProps({
    comment: {
        type: Object,
        required: true,
        default: () => ({})
    },
    isReplying: {
        type: Boolean,
        default: false
    },
    isExpanded: {
        type: Boolean,
        default: false
    },
    replyContent: {
        type: String,
        default: ''
    },
    replyToName: {
        type: String,
        default: ''
    }
})

const emit = defineEmits(['like', 'reply', 'submit-reply', 'toggle-replies', 'close-reply', 'update:reply-content'])

const replyContentLocal = computed({
    get: () => props.replyContent,
    set: (value) => emit('update:reply-content', value)
})

const userInitial = computed(() => {
    return props.comment.user_name?.charAt(0)?.toUpperCase() || 'U'
})

const formattedTime = computed(() => {
    return formatRelativeTime(props.comment.created_at)
})

const sanitizedContent = computed(() => {
    return sanitizeHtml(props.comment.content)
})

const sanitizeReplyContent = (content) => {
    return sanitizeHtml(content)
}

const isLiked = computed(() => props.comment.is_liked)
const likeCount = computed(() => props.comment.like_count || 0)
const hasReplies = computed(() => props.comment.reply_count > 0)
const toggleText = computed(() => {
    return props.isExpanded ? '收起回复' : `${props.comment.reply_count} 条回复`
})

const handleLike = () => {
    if (!requireAuth('点赞')) return
    emit('like', props.comment)
}

const handleReply = () => {
    if (!requireAuth('评论')) return
    emit('reply', props.comment.id, props.comment.user_name, props.comment.user)
}

const handleSubmit = () => {
    if (!replyContentLocal.value.trim()) return
    emit('submit-reply', props.comment.id)
}

const handleToggleReplies = () => {
    emit('toggle-replies', props.comment.id)
}

const handleReplyToReply = (reply) => {
    if (!requireAuth('回复')) return
    emit('reply', props.comment.id, reply.user_name, reply.user_id)
}
</script>

<style scoped>
.comment-item {
    display: flex;
    gap: 12px;
    padding: 20px 0;
    border-bottom: 1px solid var(--border-light);
}

.comment-item:last-child {
    border-bottom: none;
}

.user-avatar {
    flex-shrink: 0;
    border-radius: var(--radius-sm) !important;
}

.comment-body {
    flex: 1;
    min-width: 0;
}

.comment-main {
    margin-bottom: 16px;
}

.comment-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
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
    font-size: 14px;
    line-height: 1.6;
    color: var(--text-primary);
    margin: 12px 0;
    word-wrap: break-word;
}

.comment-text :deep(pre),
.reply-text :deep(pre) {
    background: var(--bg-tertiary);
    padding: 12px 16px;
    border-radius: var(--radius-sm);
    overflow-x: auto;
    margin: 12px 0;
    font-size: 13px;
    line-height: 1.5;
    border: 1px solid var(--border-color);
}

.comment-text :deep(code),
.reply-text :deep(code) {
    font-family: 'Fira Code', 'Consolas', monospace;
    font-size: 13px;
    color: var(--text-primary);
}

.comment-text :deep(pre code),
.reply-text :deep(pre code) {
    background: transparent;
    padding: 0;
}

[data-theme="dark"] .comment-text :deep(pre),
[data-theme="dark"] .reply-text :deep(pre) {
    background: var(--bg-tertiary);
    border-color: var(--border-dark);
}

.comment-text :deep(p),
.reply-text :deep(p) {
    margin: 8px 0;
}

.comment-text :deep(strong),
.reply-text :deep(strong) {
    font-weight: 600;
}

.comment-text :deep(a),
.reply-text :deep(a) {
    color: var(--primary-color);
    text-decoration: none;
}

.comment-text :deep(a:hover),
.reply-text :deep(a:hover) {
    text-decoration: underline;
}

.comment-actions {
    display: flex;
    gap: 16px;
    margin-top: 12px;
}

.action-btn {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 8px;
    font-size: 13px;
    color: var(--text-tertiary);
    cursor: pointer;
    border-radius: var(--radius-xs);
    transition: all var(--transition-fast);
}

.action-btn:hover {
    background: var(--bg-secondary);
    color: var(--primary-color);
}

.action-btn.liked {
    color: var(--danger-color);
}

.action-btn .el-icon {
    font-size: 14px;
}

.action-btn.small {
    padding: 2px 6px;
    font-size: 12px;
}

/* 回复表单 */
.reply-form {
    margin: 16px 0;
    padding: 16px;
    background: var(--bg-secondary);
    border-radius: var(--radius-md);
}

.reply-form-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    font-size: 13px;
    color: var(--text-secondary);
}

.reply-target {
    color: var(--primary-color);
    font-weight: 500;
}

.reply-form-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 12px;
}

.reply-tip {
    font-size: 12px;
    color: var(--text-tertiary);
}

/* 回复区域 */
.reply-section {
    margin-top: 16px;
    padding-left: 48px;
}

.reply-toggle {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 0;
    font-size: 13px;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all var(--transition-fast);
}

.reply-toggle:hover {
    color: var(--primary-color);
}

.reply-toggle .el-icon {
    font-size: 14px;
    transition: transform var(--transition-fast);
}

.reply-toggle .el-icon.rotated {
    transform: rotate(90deg);
}

.reply-list {
    margin-top: 12px;
}

.reply-item {
    display: flex;
    gap: 8px;
    padding: 12px 0;
}

.reply-avatar {
    flex-shrink: 0;
}

.reply-body {
    flex: 1;
    min-width: 0;
}

.reply-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
    font-size: 13px;
}

.reply-author {
    font-weight: 600;
    color: var(--text-primary);
}

.reply-to-user {
    color: var(--primary-color);
}

.reply-arrow {
    font-size: 12px;
    color: var(--text-tertiary);
}

.reply-time {
    color: var(--text-tertiary);
    font-size: 12px;
}

.reply-text {
    font-size: 14px;
    line-height: 1.5;
    color: var(--text-primary);
    margin: 8px 0;
}

.reply-actions {
    display: flex;
    gap: 12px;
    margin-top: 8px;
}

@media (max-width: 768px) {
    .comment-item {
        padding: 16px 0;
    }
    
    .reply-section {
        padding-left: 32px;
    }
}
</style>
