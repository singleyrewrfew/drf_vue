<template>
    <button class="view-btn" @click="$emit('click')" :disabled="disabled">
        <svg class="view-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
            <circle cx="12" cy="12" r="3"/>
        </svg>
        <span class="view-text">查看</span>
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
.view-btn {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border: none;
    border-radius: var(--radius-xs);
    background: var(--info-color);
    color: #fff;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
    vertical-align: middle;
    position: relative;
    z-index: 1;
}

.view-btn:hover {
    filter: brightness(1.1);
}

.view-btn:active {
    filter: brightness(0.95);
}

.view-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.view-icon {
    width: 12px;
    height: 12px;
}
</style>
