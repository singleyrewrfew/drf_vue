<template>
    <Transition name="slide-fade">
        <div v-if="visible" class="draft-restore-bar">
            <el-icon><Clock /></el-icon>
            <span>草稿已恢复 — 上次保存时间：{{ savedTimeStr }}</span>
        </div>
    </Transition>
</template>

<script setup>
import {computed} from 'vue'
import {Clock} from '@element-plus/icons-vue'

const props = defineProps({
    /** 是否显示 */
    visible: {type: Boolean, default: false},
    /** 草稿保存时间戳 (Date.now()) */
    savedAt: {type: Number, default: 0},
})

const savedTimeStr = computed(() => {
    if (!props.savedAt) return ''
    try {
        return new Date(props.savedAt).toLocaleString()
    } catch {
        return ''
    }
})
</script>

<style scoped>
.draft-restore-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    margin-bottom: 16px;
    background: var(--success-bg, #f0f9eb);
    border-radius: var(--radius-sm);
    font-size: 13px;
    color: var(--success-color, #67c23a);
}

.draft-restore-bar .el-icon {
    font-size: 16px;
}

/* 过渡动画 */
.slide-fade-enter-active {
    transition: all 0.3s ease-out;
}
.slide-fade-leave-active {
    transition: all 0.25s ease-in;
}
.slide-fade-enter-from {
    opacity: 0;
    transform: translateY(-10px);
}
.slide-fade-leave-to {
    opacity: 0;
    transform: translateY(-5px);
}

[data-theme="dark"] .draft-restore-bar {
    background: rgba(103, 194, 58, 0.1);
}
</style>
