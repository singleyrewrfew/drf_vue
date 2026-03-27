<template>
    <button type="button" class="view-all-btn" @click.stop="$emit('click')" :disabled="disabled">
        <span class="view-all-text">{{ text }}</span>
        <svg class="view-all-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="5" y1="12" x2="19" y2="12"/>
            <polyline points="12 5 19 12 12 19"/>
        </svg>
    </button>
</template>

<script setup>
defineEmits(['click'])
defineProps({
    text: {
        type: String,
        default: '查看全部'
    },
    disabled: {
        type: Boolean,
        default: false
    }
})
</script>

<style scoped>
.view-all-btn {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    background: var(--card-bg);
    color: var(--primary-color);
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
    vertical-align: middle;
    position: relative;
    z-index: 1;
}

.view-all-btn:hover {
    background: var(--primary-bg);
    border-color: var(--primary-color);
}

.view-all-btn:active {
    background: var(--bg-secondary);
}

.view-all-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.view-all-btn:disabled:hover {
    background: var(--card-bg);
    border-color: var(--border-color);
}

.view-all-icon {
    width: 12px;
    height: 12px;
    transition: transform 0.15s ease;
}

.view-all-btn:hover .view-all-icon {
    transform: translateX(2px);
}
</style>
