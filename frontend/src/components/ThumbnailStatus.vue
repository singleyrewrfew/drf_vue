<template>
    <div class="thumbnail-status">
        <el-tag v-if="status === 'pending'" type="info" size="small">
            <span class="status-content">
                <el-icon class="is-loading"><Loading/></el-icon>
                <span>等待中</span>
            </span>
        </el-tag>
        <el-tag v-else-if="status === 'processing'" type="warning" size="small">
            <span class="status-content">
                <el-icon class="is-loading"><Loading/></el-icon>
                <span>生成中</span>
            </span>
        </el-tag>
        <el-tag v-else-if="status === 'completed'" type="success" size="small">
            已完成
        </el-tag>
        <div v-else-if="status === 'failed'" class="failed-status">
            <el-tag type="danger" size="small">失败</el-tag>
            <RetryButton @click="$emit('retry')"/>
        </div>
    </div>
</template>

<script setup>
import { Loading } from '@element-plus/icons-vue'
import RetryButton from '@/components/RetryButton.vue'

defineProps({
    status: {
        type: String,
        default: 'pending',
        validator: (value) => ['pending', 'processing', 'completed', 'failed'].includes(value)
    }
})

defineEmits(['retry'])
</script>

<style scoped>
.thumbnail-status {
    display: inline-flex;
    align-items: center;
}

.status-content {
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.failed-status {
    display: flex;
    align-items: center;
    gap: 8px;
}
</style>
