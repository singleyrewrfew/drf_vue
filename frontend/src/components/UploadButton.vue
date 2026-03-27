<template>
    <div class="upload-btn" :class="{ 'is-loading': loading }">
        <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
        <span class="upload-text">{{ loading ? `${loadingText} ${progress}%` : text }}</span>
        <div v-if="loading" class="upload-progress">
            <div class="upload-progress-bar" :style="{ width: progress + '%' }"></div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    text: {
        type: String,
        default: '上传文件'
    },
    loadingText: {
        type: String,
        default: '上传中'
    },
    loading: {
        type: Boolean,
        default: false
    },
    progress: {
        type: Number,
        default: 0
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
    user-select: none;
    z-index: 1;
}

.upload-btn:hover {
    background: var(--primary-hover);
}

.upload-btn:active {
    background: var(--primary-active);
}

.upload-btn.is-loading {
    pointer-events: none;
    opacity: 0.9;
}

.upload-icon {
    width: 14px;
    height: 14px;
}

.upload-text {
    position: relative;
    z-index: 1;
}

.upload-progress {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 0 0 var(--radius-sm) var(--radius-sm);
    overflow: hidden;
}

.upload-progress-bar {
    height: 100%;
    background: #fff;
    transition: width 0.3s ease;
}
</style>
