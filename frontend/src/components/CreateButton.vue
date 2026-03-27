<template>
    <button class="create-btn" @click="$emit('click')" :disabled="disabled">
        <svg class="create-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        <span class="create-text">{{ text }}</span>
    </button>
</template>

<script setup>
defineEmits(['click'])
defineProps({
    text: {
        type: String,
        default: '新建'
    },
    disabled: {
        type: Boolean,
        default: false
    }
})
</script>

<style scoped>
.create-btn {
    display: inline-flex;
    align-items: center;
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

.create-btn:hover {
    background: var(--primary-hover);
}

.create-btn:active {
    background: var(--primary-active);
}

.create-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.create-btn:disabled:hover {
    background: var(--primary-color);
}

.create-icon {
    width: 14px;
    height: 14px;
    transition: transform 0.15s ease;
}

.create-btn:hover .create-icon {
    transform: rotate(90deg);
}
</style>
