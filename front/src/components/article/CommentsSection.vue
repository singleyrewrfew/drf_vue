<template>
    <div class="comments-section">
        <div class="section-title">
            <el-icon><ChatDotRound/></el-icon>
            <span>评论 ({{ commentCount }})</span>
        </div>
        
        <!-- 评论表单 -->
        <CommentForm 
            v-if="isLoggedIn"
            v-model:content="commentContent"
            :user-avatar="userAvatar"
            :emojis="emojis"
            :loading="submitting"
            @submit="handleSubmit"
            @emoji-insert="insertEmoji"
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
                :comment="comment"
                :is-replying="replyToParent === comment.id"
                :reply-content="replyContent"
                :reply-to-name="replyToName"
                @like="handleLike"
                @reply="openReplyForm"
                @submit-reply="submitReply"
                @toggle-replies="toggleReplies"
                @close-reply="closeReplyForm"
            />
            
            <!-- 查看更多 -->
            <div v-if="comments.length > 2" class="show-more">
                <el-button
                    type="primary"
                    plain
                    @click="showDialog = true"
                >
                    查看全部 {{ comments.length }} 条评论
                </el-button>
            </div>
            
            <!-- 空状态 -->
            <el-empty v-if="comments.length === 0" description="暂无评论，快来抢沙发吧~"/>
        </div>
        
        <!-- 全部评论对话框 -->
        <el-dialog
            v-model="showDialog"
            title="全部评论"
            width="800px"
            destroy-on-close
        >
            <div class="dialog-comment-list">
                <CommentItem
                    v-for="comment in comments"
                    :key="comment.id"
                    :comment="comment"
                    :is-replying="replyToParent === comment.id"
                    :reply-content="replyContent"
                    :reply-to-name="replyToName"
                    @like="handleLike"
                    @reply="openReplyForm"
                    @submit-reply="submitReply"
                    @toggle-replies="toggleReplies"
                    @close-reply="closeReplyForm"
                />
            </div>
        </el-dialog>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ChatDotRound } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import CommentForm from './CommentForm.vue'
import CommentItem from './CommentItem.vue'

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

const router = useRouter()
const userStore = useUserStore()

const commentContent = ref('')
const replyContent = ref('')
const replyToParent = ref(null)
const replyToName = ref('')
const replyToUser = ref(null)
const submitting = ref(false)
const submittingReply = ref(false)
const expandedReplies = ref([])
const showDialog = ref(false)

const isLoggedIn = computed(() => userStore.isLoggedIn)
const userAvatar = computed(() => userStore.user?.avatar)
const commentCount = computed(() => props.comments.length)
const displayComments = computed(() => props.comments.slice(0, 2))

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

const handleSubmit = (content) => {
    emit('submit', { content, parentId: null })
    commentContent.value = ''
}

const submitReply = (parentId) => {
    if (!replyContent.value.trim()) return
    
    emit('reply', {
        content: replyContent.value,
        parentId,
        replyToUser: replyToUser.value
    })
    
    closeReplyForm()
}

const handleLike = (comment) => {
    emit('like', comment)
}

const toggleReplies = (commentId) => {
    const index = expandedReplies.value.indexOf(commentId)
    if (index > -1) {
        expandedReplies.value.splice(index, 1)
    } else {
        expandedReplies.value.push(commentId)
    }
}

const insertEmoji = (emoji) => {
    commentContent.value += emoji
}

defineExpose({
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

.show-more {
    text-align: center;
    margin-top: 24px;
    padding-top: 24px;
    border-top: 1px solid var(--border-light);
}

.dialog-comment-list {
    max-height: 600px;
    overflow-y: auto;
}

@media (max-width: 768px) {
    .comments-section {
        margin-top: 32px;
        padding-top: 24px;
    }
    
    .section-title {
        font-size: 16px;
    }
    
    .el-dialog {
        margin: 16px;
        width: calc(100% - 32px) !important;
    }
}
</style>
