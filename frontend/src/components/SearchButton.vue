<template>
    <button type="button" class="search-btn" @click.stop="$emit('click')" :disabled="disabled">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <span class="search-text">{{ text }}</span>
    </button>
</template>

<script setup>
defineEmits(['click'])
defineProps({
    text: {
        type: String,
        default: '搜索'
    },
    disabled: {
        type: Boolean,
        default: false
    }
})
</script>

<style scoped>
.search-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 8px 16px;
    border: none;
    border-radius: var(--radius-sm);
    background: var(--primary-color);
    color: #fff;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
    user-select: none;
    position: relative;
    z-index: 1;
}

.search-btn:hover {
    background: var(--primary-hover);
}

.search-btn:active {
    background: var(--primary-active);
}

.search-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.search-btn:disabled:hover {
    background: var(--primary-color);
}

.search-icon {
    width: 14px;
    height: 14px;
}
</style>
