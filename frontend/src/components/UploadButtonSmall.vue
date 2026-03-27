<template>
    <button class="upload-btn" @click="$emit('click')" :disabled="disabled">
        <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
        <span class="upload-text"><slot>{{ text }}</slot></span>
    </button>
</template>

<script setup>
defineEmits(['click'])
defineProps({
    text: {
        type: String,
        default: '上传'
    },
    disabled: {
        type: Boolean,
        default: false
    }
})
</script>

<style scoped>
.upload-btn {
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
    position: relative;
    overflow: hidden;
    z-index: 1;
}

.upload-btn:hover {
    background: var(--primary-hover);
}

.upload-btn:active {
    background: var(--primary-active);
}

.upload-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.upload-icon {
    width: 14px;
    height: 14px;
}

.upload-text {
    position: relative;
    z-index: 1;
}
</style>
