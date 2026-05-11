<template>
  <div class="comment-item">
    <el-avatar :size="32" :src="comment.user_avatar" class="user-avatar">
      {{ userInitial }}
    </el-avatar>

    <div class="comment-body">
      <div class="comment-main">
        <div class="comment-header">
          <span class="comment-author">{{ comment.user_name }}</span>
        </div>

        <p class="comment-text" v-html="sanitizedContent"></p>

        <div class="comment-actions">
          <button type="button" class="like-btn" :class="{ 'is-liked': isLiked }" @click="handleLike">
            <svg class="like-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
            </svg>
            <span v-if="likeCount" class="like-count">{{ likeCount }}</span>
          </button>

          <button type="button" class="reply-btn" @click="handleReply">
            <svg class="reply-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
            </svg>
            <span>回复</span>
          </button>

          <button v-if="hasReplies" type="button" class="reply-toggle-inline" @click="handleToggleReplies">
            <span class="toggle-count">{{ comment.reply_count }}</span>
            <span class="toggle-label">{{ isExpanded ? '收起' : '条回复' }}</span>
            <svg class="toggle-icon" :class="{ expanded: isExpanded }" viewBox="0 0 16 16" fill="none">
              <path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>

          <span class="action-time">{{ formattedTime }}</span>
        </div>
      </div>

      <!-- 回复表单 -->
      <div v-if="isReplying" class="reply-form">
        <div class="reply-form-header">
          <span
            >回复 <span class="reply-target">@{{ replyToName }}</span></span
          >
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
          <el-button type="primary" size="small" @click="handleSubmit" :loading="submittingReply">
            发送
          </el-button>
        </div>
      </div>

      <!-- 回复列表 -->
      <div v-if="hasReplies && isExpanded" class="reply-section">
        <div v-if="comment.replies?.length" class="reply-list">
          <div v-for="reply in comment.replies" :key="reply.id" class="reply-item">
            <el-avatar :size="24" :src="reply.user_avatar" class="reply-avatar">
              {{ reply.user_name?.charAt(0)?.toUpperCase() }}
            </el-avatar>

            <div class="reply-body">
              <div class="reply-meta">
                <span class="reply-author">{{ reply.user_name }}</span>
                <span v-if="reply.reply_to_name" class="reply-target-tag">
                  <svg class="reply-arrow-icon" viewBox="0 0 16 16" fill="none">
                    <path d="M6 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  回复 <span class="reply-target-name">@{{ reply.reply_to_name }}</span>
                </span>
                <span class="reply-time">{{ formatRelativeTime(reply.created_at) }}</span>
              </div>

              <p class="reply-text" v-html="sanitizeReplyContent(reply.content)"></p>

              <div class="reply-actions">
                <button
                  type="button"
                  class="like-btn like-btn--sm"
                  :class="{ 'is-liked': reply.is_liked }"
                  @click.stop="$emit('like', reply)"
                >
                  <svg class="like-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                  </svg>
                  <span v-if="reply.like_count" class="like-count">{{ reply.like_count }}</span>
                </button>

                <button type="button" class="reply-btn reply-btn--sm" @click.stop="handleReplyToReply(reply)">
                  <svg class="reply-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
                  </svg>
                  <span>回复</span>
                </button>
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

const emit = defineEmits([
  'like',
  'reply',
  'submit-reply',
  'toggle-replies',
  'close-reply',
  'update:reply-content'
])

const replyContentLocal = computed({
  get: () => props.replyContent,
  set: value => emit('update:reply-content', value)
})

const userInitial = computed(() => {
  return props.comment.user_name?.charAt(0)?.toUpperCase() || 'U'
})

const formattedTime = computed(() => {
  return formatRelativeTime(props.comment.created_at)
})

const sanitizedContent = computed(() => {
  let html = props.comment.content || ''
  html = sanitizeHtml(html)
  html = html.replace(/<div>(<code>[\s\S]*?<\/code>)<\/div>/gi, '<div class="code-block">$1</div>')
  return html
})

const sanitizeReplyContent = content => {
  return sanitizeHtml(content)
}

const isLiked = computed(() => props.comment.is_liked)
const likeCount = computed(() => props.comment.like_count || '')
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

const handleReplyToReply = reply => {
  if (!requireAuth('回复')) return
  emit('reply', props.comment.id, reply.user_name, reply.user_id)
}
</script>

<style scoped>
.comment-item {
  display: flex;
  gap: 10px;
  padding: 14px 0;
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
  margin-bottom: 10px;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.comment-author {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 14px;
}

.action-time {
  font-size: 12px;
  color: var(--text-placeholder);
  margin-left: auto;
  padding-left: 8px;
}

.comment-text {
  font-size: 14px;
  line-height: 1.5;
  color: var(--text-primary);
  margin: 6px 0;
  word-wrap: break-word;
}

.comment-text :deep(pre),
.comment-text :deep(div.code-block),
.reply-text :deep(pre),
.reply-text :deep(div.code-block) {
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
.comment-text :deep(div.code-block code),
.reply-text :deep(pre code),
.reply-text :deep(div.code-block code) {
  background: transparent;
  padding: 0;
  white-space: pre-wrap;
  word-break: break-all;
}

[data-theme='dark'] .comment-text :deep(pre),
[data-theme='dark'] .reply-text :deep(pre) {
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
  align-items: center;
  gap: 4px;
  margin-top: 6px;
  padding-top: 6px;
}

.like-btn,
.reply-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-placeholder);
  cursor: pointer;
  border: none;
  border-radius: var(--radius-full);
  background: transparent;
  transition: all 0.25s cubic-bezier(0.25, 0.1, 0.25, 1);
  -webkit-tap-highlight-color: transparent;
  user-select: none;
}

.like-btn:hover,
.reply-btn:hover {
  background: var(--primary-bg);
  color: var(--primary-color);
}

.like-btn:active {
  transform: scale(0.92);
}

.like-icon {
  width: 16px;
  height: 16px;
  stroke: currentColor;
  stroke-width: 1.8;
  fill: none;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.like-btn.is-liked .like-icon {
  fill: var(--vermilion-color);
  stroke: var(--vermilion-color);
  transform: scale(1.08);
}

.like-btn.is-liked {
  color: var(--vermilion-color);
}

.like-count {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: -0.02em;
  min-width: 8px;
  text-align: center;
}

.reply-icon {
  width: 15px;
  height: 15px;
  stroke: currentColor;
  stroke-width: 1.6;
  fill: none;
}

.like-btn--sm,
.reply-btn--sm {
  padding: 4px 8px;
  font-size: 12px;
  gap: 4px;
}

.like-btn--sm .like-icon,
.reply-btn--sm .reply-icon {
  width: 14px;
  height: 14px;
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
  margin-top: 12px;
  padding-left: 44px;
  position: relative;
}

.reply-section::before {
  content: '';
  position: absolute;
  left: 20px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(180deg, var(--border-light) 0%, transparent 100%);
  border-radius: 1px;
}

.reply-toggle-inline {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 10px;
  margin-left: 2px;
  font-size: 12px;
  color: var(--text-placeholder);
  cursor: pointer;
  border: none;
  border-radius: var(--radius-full);
  background: transparent;
  transition: all 0.2s ease;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
}

.reply-toggle-inline:hover {
  color: var(--primary-color);
  background: var(--primary-bg, rgba(45, 90, 74, 0.06));
}

.reply-toggle-inline:active {
  transform: scale(0.96);
}

.toggle-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 4px;
  font-size: 11px;
  font-weight: 600;
  color: var(--primary-color);
  background: var(--primary-bg, rgba(45, 90, 74, 0.1));
  border-radius: var(--radius-full);
  line-height: 1;
}

.toggle-label {
  font-weight: 500;
  font-size: 12px;
  letter-spacing: 0.02em;
}

.toggle-icon {
  width: 12px;
  height: 12px;
  opacity: 0.6;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toggle-icon.expanded {
  transform: rotate(180deg);
}

.reply-list {
  margin-top: 4px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.reply-item {
  display: flex;
  gap: 8px;
  padding: 8px 8px;
  border-radius: var(--radius-md);
  transition: background 0.15s ease;
}

.reply-item:hover {
  background: var(--bg-secondary, rgba(0,0,0,0.02));
}

.reply-avatar {
  flex-shrink: 0;
  margin-top: 2px;
}

.reply-body {
  flex: 1;
  min-width: 0;
}

.reply-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: 5px;
}

.reply-author {
  font-weight: 600;
  font-size: 13px;
  color: var(--text-primary);
}

.reply-target-tag {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  padding: 2px 8px;
  font-size: 12px;
  color: var(--primary-color);
  background: var(--primary-bg);
  border-radius: var(--radius-full);
  line-height: 1.4;
}

.reply-arrow-icon {
  width: 11px;
  height: 11px;
  opacity: 0.7;
}

.reply-target-name {
  font-weight: 500;
}

.reply-time {
  font-size: 12px;
  color: var(--text-placeholder);
  margin-left: auto;
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

/* 暗色模式适配 */
[data-theme='dark'] .comment-item {
  border-bottom-color: #3f3f46;
}

[data-theme='dark'] .comment-author,
[data-theme='dark'] .reply-author {
  color: var(--dark-text, #e4e4e7);
}

[data-theme='dark'] .action-time,
[data-theme='dark'] .reply-time {
  color: #52525b;
}

[data-theme='dark'] .comment-text,
[data-theme='dark'] .reply-text {
  color: var(--dark-text, #e4e4e7);
}

[data-theme='dark'] .comment-text :deep(pre),
[data-theme='dark'] .comment-text :deep(div.code-block),
[data-theme='dark'] .reply-text :deep(pre),
[data-theme='dark'] .reply-text :deep(div.code-block) {
  background: var(--bg-tertiary);
  border-color: var(--border-dark);
}

[data-theme='dark'] .comment-text :deep(a),
[data-theme='dark'] .reply-text :deep(a) {
  color: var(--dark-vermilion-light, #ef4444);
}

[data-theme='dark'] .like-btn,
[data-theme='dark'] .reply-btn {
  color: #71717a;
}

[data-theme='dark'] .like-btn:hover,
[data-theme='dark'] .reply-btn:hover {
  background: rgba(74, 157, 130, 0.12);
  color: #5db396;
}

[data-theme='dark'] .like-btn.is-liked {
  color: var(--dark-vermilion-light, #ef4444);
}

[data-theme='dark'] .like-btn.is-liked .like-icon {
  fill: var(--dark-vermilion-light, #ef4444);
  stroke: var(--dark-vermilion-light, #ef4444);
}

[data-theme='dark'] .reply-form {
  background: var(--bg-tertiary, #252219);
  border: 1px solid var(--border-dark, #4d463c);
}

[data-theme='dark'] .reply-form-header {
  color: var(--dark-text-muted, #a1a1aa);
}

[data-theme='dark'] .reply-target {
  color: var(--primary-color);
}

[data-theme='dark'] .reply-tip {
  color: #71717a;
}

[data-theme='dark'] .reply-section {
  border-color: #3f3f46;
}

[data-theme='dark'] .reply-toggle-inline {
  color: #71717a;
}

[data-theme='dark'] .reply-toggle-inline:hover {
  color: #5db396;
  background: rgba(93, 179, 150, 0.08);
}

[data-theme='dark'] .toggle-count {
  color: var(--primary-color);
  background: var(--primary-bg, rgba(45, 90, 74, 0.15));
}

/* 暗色模式下输入框适配 */
[data-theme='dark'] .reply-form :deep(.el-textarea__inner) {
  background-color: var(--bg-primary, #0d0d0a);
  border-color: var(--border-dark, #4d463c);
  color: var(--dark-text, #e4e4e7);
}

[data-theme='dark'] .reply-form :deep(.el-textarea__inner)::placeholder {
  color: #52525b;
}

[data-theme='dark'] .reply-form :deep(.el-textarea__inner:focus) {
  border-color: var(--primary-color);
}

[data-theme='dark'] .reply-section::before {
  background: linear-gradient(180deg, #3f3f46 0%, transparent 100%);
}

[data-theme='dark'] .reply-item:hover {
  background: rgba(74, 157, 130, 0.06);
}

[data-theme='dark'] .reply-target-tag {
  background: rgba(74, 157, 130, 0.12);
  color: #5db396;
}

@media (max-width: 768px) {
  .comment-item {
    padding: 12px 0;
  }

  .reply-section {
    padding-left: 30px;
  }

  .reply-section::before {
    left: 14px;
  }
}
</style>
