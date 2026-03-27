<template>
    <div class="comment-item">
        <el-avatar :size="avatarSize" :src="getAvatarUrl(comment.user_avatar)">
            {{ comment.user_name?.charAt(0)?.toUpperCase() }}
        </el-avatar>
        <div class="comment-body">
            <div class="comment-main">
                <div class="comment-header">
                    <span class="comment-author">{{ comment.user_name }}</span>
                    <template v-if="comment.reply_to_name && showReplyTo">
                        <el-icon class="reply-arrow">
                            <ArrowRight/>
                        </el-icon>
                        <span class="reply-to-user">{{ comment.reply_to_name }}</span>
                    </template>
                    <span class="comment-time">{{ formatRelativeTime(comment.created_at) }}</span>
                </div>
                <p class="comment-text">{{ comment.content }}</p>
                <div class="comment-actions">
                    <button
                        class="action-btn"
                        :class="{ liked: comment.is_liked, small: isReply }"
                        @click="$emit('like', comment.id)"
                    >
                        <el-icon>
                            <Star/>
                        </el-icon>
                        <span>{{ comment.like_count || '' }}</span>
                    </button>
                    <button
                        class="action-btn"
                        :class="{ small: isReply }"
                        @click="$emit('reply', comment)"
                    >
                        <el-icon>
                            <ChatDotRound/>
                        </el-icon>
                        <span>回复</span>
                    </button>
                </div>
                <slot name="reply-form"/>
                <slot name="replies"/>
            </div>
        </div>
    </div>
</template>

<script setup>
import {Star, ChatDotRound, ArrowRight} from '@element-plus/icons-vue'
import {getAvatarUrl, formatRelativeTime} from '@/utils'

const props = defineProps({
    comment: {type: Object, required: true},
    isReply: {type: Boolean, default: false},
    showReplyTo: {type: Boolean, default: false}
})

const emit = defineEmits(['like', 'reply'])

const avatarSize = props.isReply ? 28 : 40
</script>

<style scoped>
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
    flex-shrink: 0;
}

.comment-body {
    flex: 1;
    min-width: 0;
}

.comment-main {
    background: transparent;
    padding: 0;
}

.comment-header {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 8px;
    flex-wrap: wrap;
}

.comment-author {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 14px;
}

.reply-arrow {
    font-size: 10px;
    color: var(--text-tertiary);
}

.reply-to-user {
    font-size: 13px;
    color: var(--primary-color);
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

.action-btn.small {
    font-size: 11px;
    padding: 2px 8px;
}
</style>
