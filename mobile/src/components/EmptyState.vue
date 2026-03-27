<template>
    <div class="empty-state">
        <el-icon class="empty-state-icon">
            <component :is="icon"/>
        </el-icon>
        <p class="empty-state-text">{{ text }}</p>
        <p v-if="hint" class="empty-state-hint">{{ hint }}</p>
        <slot/>
    </div>
</template>

<script setup>
import {Document} from '@element-plus/icons-vue'

defineProps({
    icon: {type: [Object, String], default: Document},
    text: {type: String, default: '暂无内容'},
    hint: {type: String, default: ''}
})
</script>

<style scoped>
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 20px;
    color: var(--text-tertiary);
}

.empty-state-icon {
    font-size: 48px;
    margin-bottom: 16px;
    color: var(--text-placeholder);
}

.empty-state-text {
    font-size: 14px;
    margin: 0;
}

.empty-state-hint {
    font-size: 12px;
    color: var(--text-placeholder);
    margin-top: 8px;
}
</style>
