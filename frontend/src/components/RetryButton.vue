<template>
    <button class="retry-btn" @click="$emit('click')" :disabled="disabled">
        <svg class="retry-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="23 4 23 10 17 10"/>
            <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
        </svg>
        <span class="retry-text">重试</span>
    </button>
</template>

<script setup>
defineEmits(['click'])
defineProps({
    disabled: {
        type: Boolean,
        default: false
    }
})
</script>

<style scoped>
.retry-btn {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border: none;
    border-radius: var(--radius-xs);
    background: var(--warning-color);
    color: #fff;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
    vertical-align: middle;
    position: relative;
    z-index: 1;
}

.retry-btn:hover {
    background: var(--warning-hover);
}

.retry-btn:active {
    filter: brightness(0.95);
}

.retry-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.retry-icon {
    width: 12px;
    height: 12px;
}
</style>
