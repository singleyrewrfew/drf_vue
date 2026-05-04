<template>
    <button
        ref="btnRef"
        class="upload-btn"
        :class="{ 'is-loading': loading, 'is-disabled': disabled }"
        :style="{ width: lockedWidth }"
        type="button"
        @click="handleClick"
    >
        <!-- 进度条 -->
        <span v-if="loading" class="upload-btn__progress">
            <span class="upload-btn__progress-bar" :style="{ width: clampedProgress + '%' }"/>
        </span>

        <!-- 内容 -->
        <svg v-if="!loading || showIconWhileLoading" class="upload-btn__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
        <span class="upload-btn__label">{{ displayText }}</span>
    </button>
</template>

<script setup>
import { computed, ref, onMounted, nextTick } from 'vue'

const props = defineProps({
    /** 正常状态文字 */
    text: { type: String, default: '上传文件' },
    /** 加载状态文字 */
    loadingText: { type: String, default: '上传中...' },
    /** 是否加载中 */
    loading: { type: Boolean, default: false },
    /** 上传进度 0~100，自动钳制 */
    progress: { type: Number, default: 0 },
    /** 是否禁用 */
    disabled: { type: Boolean, default: false },
    /** 加载时是否仍显示图标 */
    showIconWhileLoading: { type: Boolean, default: false }
})

const emit = defineEmits(['click'])

const btnRef = ref(null)
const lockedWidth = ref('')

/** 锁定按钮宽度（防止状态切换时抖动） */
const lockWidth = () => {
    if (!btnRef.value || lockedWidth.value) return
    lockedWidth.value = btnRef.value.offsetWidth + 'px'
}

/** 点击事件：loading/disabled 时阻止 emit */
const handleClick = (e) => {
    if (props.disabled || props.loading) return
    emit('click', e)
}

onMounted(() => nextTick(lockWidth))

/** 钳制进度值到 [0, 100] */
const clampedProgress = computed(() => {
    const val = props.progress
    if (typeof val !== 'number' || Number.isNaN(val)) return 0
    return Math.min(100, Math.max(0, val))
})

/** 当前显示文字 */
const displayText = computed(() => {
    return (props.loading && props.loadingText)
        ? props.loadingText
        : props.text
})
</script>

<style scoped>
.upload-btn {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    height: 34px; padding: 0 16px;
    border: none;
    border-radius: var(--radius-sm);
    background: var(--primary-color);
    color: #fff;
    font-size: 13px; font-weight: 500; line-height: 1;
    cursor: pointer;
    overflow: hidden;
    user-select: none;
    white-space: nowrap;
    transition:
        background-color 0.15s ease,
        opacity 0.15s ease,
        box-shadow 0.15s ease;
}

/* ---- Hover / Active ---- */
.upload-btn:hover:not(.is-disabled):not(.is-loading) {
    background: var(--primary-hover);
}
.upload-btn:active:not(.is-disabled):not(.is-loading) {
    background: var(--primary-active);
}

/* ---- Loading / Disabled ---- */
.upload-btn.is-disabled {
    pointer-events: none;
    opacity: 0.5;
}

/* ---- 图标 ---- */
.upload-btn__icon {
    width: 14px; height: 14px;
    flex-shrink: 0;
}

/* ---- 文字（固定按钮宽度，超长文本截断） ---- */
.upload-btn__label {
    position: relative; z-index: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    min-width: 0;
}

/* ---- 底部进度条 ---- */
.upload-btn__progress {
    position: absolute; bottom: 0; left: 0;
    width: 100%; height: 2px;
    background: rgba(255, 255, 255, 0.25);
    border-radius: 0 0 var(--radius-sm) var(--radius-sm);
    overflow: hidden;
}
.upload-btn__progress-bar {
    display: block; height: 100%;
    background: #fff;
    transition: width 0.25s ease;
}
</style>
