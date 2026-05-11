<template>
  <div class="comments-section">
    <div class="section-title">
      <el-icon><ChatDotRound /></el-icon>
      <span>评论 ({{ commentCount }})</span>
    </div>

    <!-- 评论表单 -->
    <CommentForm
      v-if="isLoggedIn"
      v-model:content="commentContent"
      :user="userStore.user"
      :emojis="emojis"
      :loading="submitting"
      @submit="handleSubmit"
    />

    <!-- 登录提示 -->
    <div v-else class="login-tip">
      <p>登录后才能评论</p>
      <el-button type="primary" @click="$router.push('/login')">立即登录</el-button>
    </div>

    <!-- 评论列表 -->
    <div class="comment-list">
      <CommentItem
        v-for="comment in displayComments"
        :key="comment.id"
        :comment="getCommentWithReplies(comment)"
        :is-replying="replyToParent === comment.id"
        :is-expanded="expandedReplies.includes(comment.id)"
        :reply-content="replyContent"
        :reply-to-name="replyToName"
        @like="handleLike"
        @reply="openReplyForm"
        @submit-reply="submitReply"
        @toggle-replies="toggleReplies"
        @close-reply="closeReplyForm"
        @update:reply-content="val => replyContent = val"
      />

      <!-- 加载更多 -->
      <div v-if="hasMore" class="load-more" @click="loadMore">
        <span class="load-more-text">展开剩余 {{ remainingCount }} 条评论</span>
        <svg class="load-more-icon" viewBox="0 0 24 24" fill="none">
          <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>

      <!-- 已加载全部 -->
      <div v-if="!hasMore && comments.length > initialDisplayCount" class="all-loaded">
        <span class="loaded-line"></span>
        <span class="loaded-text">已展示全部 {{ comments.length }} 条评论</span>
        <span class="loaded-line"></span>
      </div>

      <!-- 空状态 -->
      <el-empty v-if="comments.length === 0" description="暂无评论，快来抢沙发吧~" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ChatDotRound } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import CommentForm from './CommentForm.vue'
import CommentItem from './CommentItem.vue'
import { getComments } from '@/api/content'

const props = defineProps({
  comments: {
    type: Array,
    default: () => []
  },
  articleId: {
    type: [Number, String],
    required: true
  }
})

const emit = defineEmits(['submit', 'like', 'reply'])

const userStore = useUserStore()

const commentContent = ref('')
const replyContent = ref('')
const replyToParent = ref(null)
const replyToName = ref('')
const replyToUser = ref(null)
const submitting = ref(false)
const expandedReplies = ref([])
const repliesData = ref({})
const loadingReplies = ref(new Set())

const initialDisplayCount = 5
const loadStep = 5
const displayCount = ref(initialDisplayCount)

const isLoggedIn = computed(() => userStore.isLoggedIn)
const commentCount = computed(() => props.comments.length)
const displayComments = computed(() => props.comments.slice(0, displayCount.value))
const hasMore = computed(() => displayCount.value < props.comments.length)
const remainingCount = computed(() => Math.max(0, props.comments.length - displayCount.value))

// Emoji 列表
const emojis = ['😀', '😂', '😍', '🤔', '👍', '🎉', '❤️', '🔥', '👏', '💯']

const openReplyForm = (commentId, userName, userId) => {
  replyToParent.value = commentId
  replyToName.value = userName
  replyToUser.value = userId
  replyContent.value = ''
}

const closeReplyForm = () => {
  replyToParent.value = null
  replyToName.value = ''
  replyToUser.value = null
  replyContent.value = ''
}

const handleSubmit = content => {
  emit('submit', { content, parentId: null })
  commentContent.value = ''
}

const submitReply = parentId => {
  if (!replyContent.value.trim()) return

  emit('reply', {
    content: replyContent.value,
    parentId,
    replyToUser: replyToUser.value
  })

  delete repliesData.value[parentId]
  closeReplyForm()
}

const handleLike = comment => {
  emit('like', comment)
}

const toggleReplies = async commentId => {
  const index = expandedReplies.value.indexOf(commentId)
  if (index > -1) {
    expandedReplies.value.splice(index, 1)
  } else {
    expandedReplies.value.push(commentId)
    if (!repliesData.value[commentId]) {
      await loadRepliesForComment(commentId)
    }
  }
}

const loadMore = () => {
  displayCount.value = Math.min(displayCount.value + loadStep, props.comments.length)
}

const loadRepliesForComment = async commentId => {
  if (loadingReplies.value.has(commentId)) return
  loadingReplies.value.add(commentId)
  try {
    const response = await getComments({ parent: commentId })
    let data = response.data || response
    if (Array.isArray(data.results)) {
      repliesData.value[commentId] = data.results
    } else if (Array.isArray(data)) {
      repliesData.value[commentId] = data
    } else {
      repliesData.value[commentId] = []
    }
  } catch (e) {
    console.error('Failed to load replies:', e)
    repliesData.value[commentId] = []
  } finally {
    loadingReplies.value.delete(commentId)
  }
}

const getCommentWithReplies = comment => {
  if (!comment.replies) {
    comment.replies = repliesData.value[comment.id] || []
  }
  return comment
}

defineExpose({
  openReplyForm,
  closeReplyForm
})
</script>

<style scoped>
.comments-section {
  margin-top: 48px;
  padding-top: 32px;
  border-top: 1px solid var(--border-light);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 24px;
}

.section-title .el-icon {
  font-size: 20px;
  color: var(--primary-color);
}

.login-tip {
  text-align: center;
  padding: 40px 20px;
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  margin-bottom: 24px;
}

.login-tip p {
  color: var(--text-secondary);
  margin-bottom: 16px;
}

.load-more {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 14px 0;
  margin-top: 8px;
  cursor: pointer;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
  transition: all 0.2s ease;
}

.load-more:hover .load-more-text {
  color: var(--primary-color);
}

.load-more:hover .load-more-icon {
  transform: translateY(2px);
  color: var(--primary-color);
}

.load-more-text {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-tertiary);
  letter-spacing: 0.02em;
  transition: color 0.2s ease;
}

.load-more-icon {
  width: 16px;
  height: 16px;
  color: var(--text-placeholder);
  transition: all 0.25s cubic-bezier(0.25, 0.1, 0.25, 1);
}

.all-loaded {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 20px 0 8px;
}

.loaded-line {
  flex: 1;
  max-width: 80px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border-color), transparent);
}

.loaded-text {
  font-size: 12px;
  color: var(--text-placeholder);
  white-space: nowrap;
  letter-spacing: 0.03em;
}

@media (max-width: 768px) {
  .comments-section {
    margin-top: 32px;
    padding-top: 24px;
  }

  .section-title {
    font-size: 16px;
  }
}

/* 暗色模式适配 */
[data-theme='dark'] .comments-section {
  border-color: #3f3f46;
}

[data-theme='dark'] .section-title {
  color: var(--dark-text, #e4e4e7);
}

[data-theme='dark'] .section-title .el-icon {
  color: var(--dark-vermilion-light, #ef4444);
}

[data-theme='dark'] .login-tip {
  background: #27272a;
}

[data-theme='dark'] .login-tip p {
  color: var(--dark-text-muted, #a1a1aa);
}

[data-theme='dark'] .load-more:hover .load-more-text {
  color: #5db396;
}

[data-theme='dark'] .load-more:hover .load-more-icon {
  color: #5db396;
}

[data-theme='dark'] .loaded-text {
  color: #52525b;
}

[data-theme='dark'] .loaded-line {
  background: linear-gradient(90deg, transparent, #3f3f46, transparent);
}

/* el-empty 空状态暗色适配 */
[data-theme='dark'] :deep(.el-empty) {
  --el-empty-fill-color-0: #3f3f46;
  --el-empty-fill-color-1: #3f3f46;
  --el-empty-fill-color-2: #52525b;
  --el-empty-fill-color-3: #3f3f46;
  --el-empty-fill-color-4: #52525b;
  --el-empty-fill-color-5: #71717a;
  --el-empty-fill-color-6: #52525b;
  --el-empty-fill-color-7: #71717a;
  --el-empty-fill-color-8: #52525b;
  --el-empty-fill-color-9: #71717a;
}

[data-theme='dark'] :deep(.el-empty__description p) {
  color: #71717a;
}
</style>
