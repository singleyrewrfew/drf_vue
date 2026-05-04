<template>
    <div class="image-uploader">
        <div class="uploader-area" :class="{ 'has-image': previewUrl }" @click="triggerSelect">
            <img v-if="previewUrl" :src="previewUrl" class="preview-image"/>
            <div v-else class="placeholder">
                <el-icon class="placeholder-icon"><Plus /></el-icon>
                <span>{{ placeholderText }}</span>
            </div>
        </div>

        <!-- 操作按钮 -->
        <div v-if="previewUrl" class="action-bar">
            <button v-if="pendingFile" type="button" class="action-btn action-btn-warning"
                    @click.stop="triggerSelect">
                <el-icon><Upload /></el-icon>
                <span>{{ replaceText }}</span>
            </button>
            <button type="button" class="action-btn action-btn-danger" @click.stop="handleClear">
                <el-icon><Delete /></el-icon>
                <span>{{ removeText }}</span>
            </button>
        </div>

        <!-- 待上传提示 -->
        <div v-if="pendingFile" class="status-hint">
            <el-icon><Clock /></el-icon>
            <span>{{ pendingText }}</span>
        </div>

        <!-- 提示文字 -->
        <div v-if="tip" class="tip-text">{{ tip }}</div>

        <!-- 隐藏 file input -->
        <input ref="inputRef" type="file" :accept="acceptTypes" style="display: none" @change="handleFileChange"/>
    </div>
</template>

<script setup>
import {ref, computed} from 'vue'
import {ElMessage} from 'element-plus'
import {Plus, Upload, Delete, Clock} from '@element-plus/icons-vue'

const props = defineProps({
    /** 当前预览 URL（已有图片或服务端返回的 URL） */
    modelValue: {type: String, default: ''},
    /** 允许的 MIME 类型，默认常见图片格式 */
    acceptTypes: {type: String, default: 'image/jpeg,image/png,image/gif,image/webp'},
    /** 最大文件大小 (MB)，默认 10MB */
    maxSizeMB: {type: Number, default: 10},
    /** 占位文字 */
    placeholderText: {type: String, default: '点击上传图片'},
    /** 替换按钮文字 */
    replaceText: {type: String, default: '更换'},
    /** 移除按钮文字 */
    removeText: {type: String, default: '移除'},
    /** 底部提示（如建议尺寸） */
    tip: {type: String, default: ''},
    /** 待上传状态栏文字 */
    pendingText: {type: String, default: '图片将在提交时上传'},
})

const emit = defineEmits(['update:modelValue', 'select', 'clear', 'file-selected'])

const inputRef = ref(null)
const pendingFile = ref(null)
const previewUrl = computed(() => props.modelValue)

/** 触发隐藏的 file input */
const triggerSelect = () => inputRef.value?.click()

/**
 * 处理文件选择：校验类型/大小 → 创建预览 → 暂存文件
 * 校验失败时静默重置 input，不 emit 任何事件
 */
const handleFileChange = (event) => {
    const file = event.target.files?.[0]
    if (!file) return

    if (!props.acceptTypes.split(',').some(t => t.trim() === file.type)) {
        ElMessage.error(`不支持 ${file.type} 格式`)
        event.target.value = ''
        return
    }

    if (file.size / 1024 / 1024 > props.maxSizeMB) {
        ElMessage.error(`图片大小不能超过 ${props.maxSizeMB}MB`)
        event.target.value = ''
        return
    }

    // 回收旧 blob
    revokeBlob()

    pendingFile.value = file
    const url = URL.createObjectURL(file)
    emit('update:modelValue', url)
    emit('file-selected', file)
    event.target.value = ''
}

/** 清除图片和待上传文件 */
const handleClear = () => {
    revokeBlob()
    pendingFile.value = null
    emit('update:modelValue', '')
    emit('clear')
}

/** 安全回收 blob URL */
const revokeBlob = () => {
    if (props.modelValue?.startsWith('blob:')) {
        URL.revokeObjectURL(props.modelValue)
    }
}

/** 获取当前暂存的待上传 File 对象（外部提交时调用） */
const getPendingFile = () => pendingFile.value

defineExpose({ triggerSelect, getPendingFile, clear: handleClear })
</script>

<style scoped>
.image-uploader {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.uploader-area {
    border: 1px dashed var(--border-color);
    border-radius: var(--radius-sm);
    cursor: pointer;
    position: relative;
    overflow: hidden;
    width: 100%;
    max-width: 320px;
    aspect-ratio: 16 / 9;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--bg-tertiary);
    transition: border-color var(--transition-fast), box-shadow 0.2s ease;
}

.uploader-area:hover {
    border-color: var(--primary-color);
    box-shadow: 0 2px 12px rgba(64, 158, 255, 0.08);
}

.uploader-area.has-image {
    border-style: solid;
}

.placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    color: var(--text-tertiary);
}

.placeholder-icon {
    font-size: 32px;
}

.preview-image {
    max-width: 100%;
    max-height: 100%;
    display: block;
    object-fit: contain;
}

.action-bar {
    display: flex;
    gap: 8px;
}

.action-btn {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border: none;
    border-radius: var(--radius-xs);
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
}

.action-btn .el-icon {
    font-size: 12px;
}

.action-btn-warning {
    background: var(--warning-color, #e6a23c);
    color: #fff;
}

.action-btn-warning:hover {
    background: var(--warning-hover, #ebb563);
}

.action-btn-danger {
    background: var(--danger-color);
    color: #fff;
}

.action-btn-danger:hover {
    background: var(--danger-hover);
}

.status-hint {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    background: var(--warning-bg, #fdf6ec);
    border-radius: var(--radius-sm);
    font-size: 12px;
    color: var(--warning-color, #e6a23c);
}

.status-hint .el-icon {
    font-size: 14px;
}

[data-theme="dark"] .status-hint {
    background: rgba(230, 162, 60, 0.1);
}

.tip-text {
    font-size: 12px;
    color: var(--text-tertiary);
}
</style>
