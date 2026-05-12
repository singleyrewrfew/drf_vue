<template>
    <el-card shadow="hover" class="system-info-card">
        <template #header>
            <div class="card-header">
                <span>系统信息</span>
                <el-button text size="small" @click="$emit('refresh')" :loading="loading">
                    刷新
                </el-button>
            </div>
        </template>
        <div class="system-info">
            <div class="info-item">
                <div class="info-content">
                    <el-icon class="info-icon" color="#409EFF">
                        <Picture/>
                    </el-icon>
                    <span class="info-label">媒体文件</span>
                </div>
                <span class="info-value">{{ stats.media }} 个</span>
            </div>
            <div class="info-item">
                <div class="info-content">
                    <el-icon class="info-icon" color="#67C23A">
                        <InfoFilled/>
                    </el-icon>
                    <span class="info-label">系统版本</span>
                </div>
                <span class="info-value">v1.0.0</span>
            </div>
            <div class="info-item">
                <div class="info-content">
                    <el-icon class="info-icon" color="#E6A23C">
                        <Platform/>
                    </el-icon>
                    <span class="info-label">框架</span>
                </div>
                <span class="info-value">Django + Vue 3</span>
            </div>

            <div class="info-divider"></div>

            <div class="info-item">
                <div class="info-content">
                    <span class="status-dot" :class="serviceStatusClass('database')"></span>
                    <span class="info-label">数据库</span>
                </div>
                <span class="info-value">{{ serviceStatusText('database') }}</span>
            </div>
            <div class="info-item">
                <div class="info-content">
                    <span class="status-dot" :class="serviceStatusClass('redis')"></span>
                    <span class="info-label">Redis</span>
                </div>
                <span class="info-value">{{ serviceStatusText('redis') }}</span>
            </div>
            <div class="info-item">
                <div class="info-content">
                    <span class="status-dot" :class="serviceStatusClass('celery')"></span>
                    <span class="info-label">Celery</span>
                </div>
                <span class="info-value">{{ serviceStatusText('celery') }}</span>
            </div>
        </div>
    </el-card>
</template>

<script setup>
import {Picture, InfoFilled, Platform} from '@element-plus/icons-vue'

const props = defineProps({
    stats: {
        type: Object,
        required: true
    },
    healthData: {
        type: Object,
        default: null
    },
    loading: {
        type: Boolean,
        default: false
    }
})

defineEmits(['refresh'])

const serviceStatusClass = (service) => {
    const status = props.healthData?.services?.[service]?.status
    return status === 'healthy' ? 'dot-healthy' : status === 'unhealthy' ? 'dot-unhealthy' : 'dot-unknown'
}

const serviceStatusText = (service) => {
    const info = props.healthData?.services?.[service]
    if (props.loading) return '检测中...'
    if (!info) return '未检测'
    if (info.status === 'healthy') {
        if (service === 'celery') return `${info.workers} Worker`
        if (service === 'redis') return info.used_memory_human || '正常'
        return `${info.response_time_ms}ms`
    }
    return '异常'
}
</script>

<style scoped>
.system-info-card {
    margin-top: 20px;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.system-info {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.info-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 16px;
    border-radius: 8px;
    background: var(--bg-secondary);
    transition: all 0.2s ease;
}

.info-item:hover {
    background: var(--bg-tertiary);
    transform: translateX(4px);
}

.info-content {
    display: flex;
    align-items: center;
    gap: 10px;
}

.info-icon {
    font-size: 18px;
}

.info-label {
    color: var(--text-secondary);
    font-size: 14px;
    font-weight: 500;
}

.info-value {
    color: var(--text-primary);
    font-size: 14px;
    font-weight: 600;
    background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.info-divider {
    height: 1px;
    background: var(--border-light);
    margin: 8px 0;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

.dot-healthy {
    background: var(--success-color, #67C23A);
    box-shadow: 0 0 4px var(--success-color, #67C23A);
}

.dot-unhealthy {
    background: var(--danger-color, #F56C6C);
    box-shadow: 0 0 4px var(--danger-color, #F56C6C);
}

.dot-unknown {
    background: var(--text-tertiary, #C0C4CC);
}
</style>
