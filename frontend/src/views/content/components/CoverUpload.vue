<template>
    <div class="cover-wrapper">
        <div class="cover-uploader" @click="triggerSelect">
            <img v-if="previewUrl" :src="previewUrl" class="cover-image"/>
            <div v-else class="cover-placeholder">
                <el-icon class="cover-uploader-icon"><Plus/></el-icon>
                <span>点击上传封面</span>
            </div>
        </div>
        <div class="cover-toolbar">
            <ActionButton icon="upload" text="上传文件" size="small" stop @click="triggerSelect"/>
            <ActionButton icon="preview" text="媒体库" size="small" stop @click="$emit('open-media')"/>
            <ActionButton v-if="previewUrl || modelValue" variant="outline" type="text" icon="delete" text="移除" size="small" stop @click="handleClear"/>
        </div>
        <div v-if="pendingFile" class="cover-status-bar">
            <el-icon class="status-icon"><Clock/></el-icon>
            <span>封面图将在提交时上传</span>
        </div>
        <input ref="inputRef" :id="id" type="file" accept="image/jpeg,image/png,image/gif,image/webp" style="display: none"
               @change="handleFileChange"/>
        <div class="cover-tip">支持 JPG/PNG/GIF/WEBP，建议尺寸 1920x1080</div>
    </div>
</template>

<script setup>
import {ref, watch} from 'vue'
import {ElMessage} from 'element-plus'
import {Plus, Clock} from '@element-plus/icons-vue'
import ActionButton from '@/components/ActionButton.vue'

const props = defineProps({
    modelValue: {type: String, default: ''},
    id: {type: String, default: ''},
})

const emit = defineEmits(['update:modelValue', 'select-file', 'open-media', 'file-ready'])

const inputRef = ref(null)
const pendingFile = ref(null)
const previewUrl = ref('')

watch(() => props.modelValue, (val) => {
    if (val && val !== previewUrl.value) previewUrl.value = val
}, {immediate: true})

const triggerSelect = () => inputRef.value?.click()

const handleFileChange = (event) => {
    const file = event.target.files?.[0]
    if (!file) return
    const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if (!validTypes.includes(file.type)) {
        ElMessage.error('只能上传 JPG/PNG/GIF/WEBP 格式的图片')
        event.target.value = ''
        return
    }
    if (file.size / 1024 / 1024 >= 10) {
        ElMessage.error('图片大小不能超过 10MB')
        event.target.value = ''
        return
    }
    if (previewUrl.value && previewUrl.value.startsWith('blob:')) URL.revokeObjectURL(previewUrl.value)
    pendingFile.value = file
    previewUrl.value = URL.createObjectURL(file)
    emit('update:modelValue', '')
    emit('file-ready', file)
    event.target.value = ''
}

const handleClear = () => {
    if (previewUrl.value && previewUrl.value.startsWith('blob:')) URL.revokeObjectURL(previewUrl.value)
    pendingFile.value = null
    previewUrl.value = ''
    emit('update:modelValue', '')
}

const setFromMedia = (url) => {
    if (previewUrl.value && previewUrl.value.startsWith('blob:')) URL.revokeObjectURL(previewUrl.value)
    pendingFile.value = null
    previewUrl.value = url
    emit('update:modelValue', url)
}

defineExpose({setFromMedia, pendingFile, previewUrl})
</script>

<style scoped>
.cover-wrapper {width: 100%}
.cover-uploader {width: 100%; aspect-ratio: 16/9; border: 2px dashed var(--border-color); border-radius: var(--radius-md); cursor: pointer; overflow: hidden; transition: border-color 0.2s ease}
.cover-uploader:hover {border-color: var(--primary-color)}
.cover-image {width: 100%; height: 100%; object-fit: cover; display: block}
.cover-placeholder {width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; color: var(--text-tertiary)}
.cover-uploader-icon {font-size: 32px}
.cover-toolbar {display: flex; gap: 8px; margin-top: 8px; align-items: center}
.cover-status-bar {margin-top: 8px; padding: 6px 10px; background: rgba(64, 158, 255, 0.1); border-radius: var(--radius-sm); display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--primary-color)}
.status-icon {font-size: 14px}
.cover-tip {margin-top: 4px; font-size: 12px; color: var(--text-tertiary)}
</style>
