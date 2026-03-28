<template>
    <div class="comment-form">
        <div class="comment-form-wrapper">
            <el-avatar :size="36" :src="userAvatar" class="user-avatar">
                {{ userInitial }}
            </el-avatar>
            
            <div class="comment-form-content">
                <el-input
                    v-model="contentLocal"
                    type="textarea"
                    :rows="3"
                    placeholder="理性发言，友善互动..."
                    :autosize="{ minRows: 3, maxRows: 8 }"
                    resize="none"
                    class="comment-textarea"
                    @input="handleInput"
                />
                
                <div class="comment-form-footer">
                    <div class="comment-form-tools">
                        <el-popover placement="top-start" :width="300" trigger="click">
                            <template #reference>
                                <el-button link class="tool-btn" title="选择表情">
                                    <svg width="1.2em" height="1.2em" viewBox="0 0 24 24" fill="currentColor">
                                        <path d="M14.413 14.223a.785.785 0 0 1 1.45.601A4.174 4.174 0 0 1 12 17.4a4.19 4.19 0 0 1-2.957-1.221 4.174 4.174 0 0 1-.906-1.355.785.785 0 1 1 1.449-.601 2.604 2.604 0 0 0 1.413 1.41 2.621 2.621 0 0 0 2.849-.566c.242-.242.434-.529.565-.844ZM8.6 8.77a1.308 1.308 0 1 1 0 2.615 1.308 1.308 0 0 1 0-2.615ZM15.4 8.77a1.308 1.308 0 1 1 0 2.615 1.308 1.308 0 0 1 0-2.615Z"/>
                                        <path fill-rule="evenodd" d="M12 1.573c5.758 0 10.427 4.669 10.427 10.427S17.758 22.427 12 22.427 1.573 17.758 1.573 12 6.242 1.573 12 1.573Zm0 1.746a8.681 8.681 0 1 0 .001 17.362A8.681 8.681 0 0 0 12 3.32Z" clip-rule="evenodd"/>
                                    </svg>
                                </el-button>
                            </template>
                            
                            <div class="emoji-picker">
                                <div class="emoji-list">
                                    <span 
                                        v-for="emoji in emojis" 
                                        :key="emoji" 
                                        class="emoji-item"
                                        @click="handleEmojiClick(emoji)"
                                    >
                                        {{ emoji }}
                                    </span>
                                </div>
                            </div>
                        </el-popover>
                    </div>
                    
                    <div class="comment-form-actions">
                        <span class="char-count">{{ contentLength }}/500</span>
                        <el-button 
                            type="primary" 
                            @click="handleSubmit"
                            :loading="loading"
                            :disabled="!canSubmit"
                        >
                            发布
                        </el-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    content: {
        type: String,
        default: ''
    },
    userAvatar: {
        type: String,
        default: ''
    },
    emojis: {
        type: Array,
        default: () => []
    },
    loading: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['update:content', 'submit', 'emoji-insert'])

const contentLocal = computed({
    get: () => props.content,
    set: (value) => emit('update:content', value)
})

const userInitial = computed(() => {
    const username = props.userAvatar?.username || 'U'
    return username.charAt(0).toUpperCase()
})

const contentLength = computed(() => props.content.length)
const canSubmit = computed(() => props.content.trim().length > 0 && props.content.length <= 500)

const handleInput = (value) => {
    // 可以在这里添加输入处理逻辑
}

const handleSubmit = () => {
    if (!canSubmit.value) return
    emit('submit', props.content)
}

const handleEmojiClick = (emoji) => {
    emit('emoji-insert', emoji)
}
</script>

<style scoped>
.comment-form {
    margin-bottom: 32px;
}

.comment-form-wrapper {
    display: flex;
    gap: 12px;
    padding: 20px;
    background: var(--bg-secondary);
    border-radius: var(--radius-lg);
}

.user-avatar {
    flex-shrink: 0;
    border-radius: var(--radius-sm) !important;
    border: 2px solid var(--border-light);
}

.comment-form-content {
    flex: 1;
    min-width: 0;
}

.comment-textarea {
    margin-bottom: 12px;
}

.comment-textarea :deep(.el-textarea__inner) {
    background: var(--card-bg) !important;
    border-color: var(--border-color) !important;
}

.comment-form-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.comment-form-tools {
    display: flex;
    gap: 8px;
}

.tool-btn {
    padding: 6px 10px;
    color: var(--text-tertiary);
    transition: all var(--transition-fast);
}

.tool-btn:hover {
    color: var(--primary-color);
}

.emoji-picker {
    padding: 12px;
}

.emoji-list {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 8px;
}

.emoji-item {
    font-size: 20px;
    cursor: pointer;
    padding: 6px;
    border-radius: var(--radius-xs);
    transition: all var(--transition-fast);
    display: flex;
    align-items: center;
    justify-content: center;
}

.emoji-item:hover {
    background: var(--bg-tertiary);
    transform: scale(1.2);
}

.comment-form-actions {
    display: flex;
    align-items: center;
    gap: 12px;
}

.char-count {
    font-size: 13px;
    color: var(--text-tertiary);
}

@media (max-width: 768px) {
    .comment-form-wrapper {
        padding: 16px;
        gap: 8px;
    }
    
    .comment-form-footer {
        flex-wrap: wrap;
        gap: 8px;
    }
}
</style>
