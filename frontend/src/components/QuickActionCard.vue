<template>
    <div class="quick-action-card" :class="[type]" @click="$emit('click')">
        <div class="action-icon">
            <el-icon :size="20">
                <slot></slot>
            </el-icon>
        </div>
        <span class="action-title">{{ title }}</span>
    </div>
</template>

<script setup>
defineEmits(['click'])
defineProps({
    title: {
        type: String,
        required: true
    },
    description: {
        type: String,
        default: ''
    },
    type: {
        type: String,
        default: 'primary',
        validator: (v) => ['primary', 'success', 'warning', 'danger', 'info'].includes(v)
    }
})
</script>

<style scoped>
.quick-action-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 16px 12px;
    background: var(--card-bg);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all 0.15s ease;
    border: 1px solid var(--border-color);
    min-height: 80px;
}

.quick-action-card:hover {
    background: var(--bg-secondary);
    border-color: var(--primary-color);
}

.quick-action-card:active {
    background: var(--bg-tertiary);
}

.action-icon {
    width: 36px;
    height: 36px;
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--icon-bg);
    color: var(--icon-color);
    transition: transform 0.15s ease;
}

.quick-action-card:hover .action-icon {
    transform: scale(1.05);
}

.action-title {
    font-size: 13px;
    font-weight: 500;
    color: var(--text-primary);
    text-align: center;
}

.quick-action-card.primary {
    --icon-bg: var(--primary-bg);
    --icon-color: var(--primary-color);
}

.quick-action-card.success {
    --icon-bg: var(--success-bg);
    --icon-color: var(--success-color);
}

.quick-action-card.warning {
    --icon-bg: var(--warning-bg);
    --icon-color: var(--warning-color);
}

.quick-action-card.danger {
    --icon-bg: var(--danger-bg);
    --icon-color: var(--danger-color);
}

.quick-action-card.info {
    --icon-bg: var(--info-bg);
    --icon-color: var(--info-color);
}
</style>
