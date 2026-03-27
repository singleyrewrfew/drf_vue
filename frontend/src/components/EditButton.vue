<template>
    <button class="edit-btn" @click="$emit('click')" :disabled="disabled">
        <svg class="edit-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
        </svg>
        <span class="edit-text">编辑</span>
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
.edit-btn {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border: none;
    border-radius: var(--radius-xs);
    background: var(--primary-color);
    color: #fff;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
    vertical-align: middle;
    position: relative;
    z-index: 1;
}

.edit-btn:hover {
    background: var(--primary-hover);
}

.edit-btn:active {
    background: var(--primary-active);
}

.edit-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.edit-icon {
    width: 12px;
    height: 12px;
}
</style>
