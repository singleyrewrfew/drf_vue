<template>
    <MediaDialog :visible="visible" title="从媒体库选择" :width="800" @update:visible="$emit('update:visible', $event)" @close="handleClose">
        <div class="media-library">
            <div class="media-toolbar">
                <el-input v-model="searchText" placeholder="搜索文件名..." prefix-icon="Search" clearable size="default"
                          style="width: 240px" @input="handleSearch"/>
            </div>
            <div v-if="loading" class="media-loading">
                <el-icon class="is-loading"><Loading/></el-icon>
                <span>加载中...</span>
            </div>
            <div v-else-if="filteredItems.length === 0" class="media-empty">
                <el-icon><Picture/></el-icon>
                <span>暂无图片</span>
            </div>
            <div v-else class="media-grid">
                <div v-for="item in filteredItems" :key="item.id" class="media-item" :class="{ 'is-selected': selectedId === item.id }"
                     @click="selectItem(item)">
                    <img :src="getFullUrl(item.url)" :alt="item.filename" class="media-thumb"/>
                    <div class="media-info">
                        <span class="media-filename">{{ item.filename }}</span>
                        <span class="media-size">{{ formatSize(item.file_size) }}</span>
                    </div>
                    <div v-if="selectedId === item.id" class="media-check">
                        <el-icon><Check/></el-icon>
                    </div>
                </div>
            </div>
            <div v-if="total > pageSize" class="media-pagination">
                <el-pagination v-model:current-page="currentPage" :page-size="pageSize" :total="total" layout="prev, pager, next" small
                               @current-change="handlePageChange"/>
            </div>
        </div>
        <template #footer>
            <ActionButton variant="outline" type="text" text="取消" icon="reset" size="normal" @click="$emit('update:visible', false)"/>
            <ActionButton text="确认选择" icon="approve" size="normal" stop @click="confirmSelect" :disabled="!selectedItem"/>
        </template>
    </MediaDialog>
</template>

<script setup>
import {ref, computed, watch} from 'vue'
import {ElMessage} from 'element-plus'
import {Loading, Picture, Check, Search} from '@element-plus/icons-vue'
import MediaDialog from '@/components/MediaDialog.vue'
import ActionButton from '@/components/ActionButton.vue'
import {getMedia} from '@/api/media'

const props = defineProps({
    visible: {type: Boolean, default: false},
})

const emit = defineEmits(['update:visible', 'select'])

const loading = ref(false)
const allItems = ref([])
const searchText = ref('')
const currentPage = ref(1)
const pageSize = ref(12)
const selectedId = ref(null)
const selectedItem = ref(null)

const imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg']
const isImageFile = (item) => {
    const filename = item.filename?.toLowerCase() || item.url?.toLowerCase() || ''
    return imageExtensions.some(ext => filename.endsWith(`.${ext}`))
}

const filteredItems = computed(() => {
    let items = allItems.value
    if (searchText.value) {
        const keyword = searchText.value.toLowerCase()
        items = items.filter(item => (item.filename || '').toLowerCase().includes(keyword))
    }
    return items.slice((currentPage.value - 1) * pageSize.value, currentPage.value * pageSize.value)
})

const total = computed(() => {
    if (!searchText.value) return allItems.value.length
    const keyword = searchText.value.toLowerCase()
    return allItems.value.filter(item => (item.filename || '').toLowerCase().includes(keyword)).length
})

const getFullUrl = (url) => {
    if (!url) return ''
    if (url.startsWith('http')) return url
    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '/api'
    const mediaBaseUrl = apiBaseUrl.replace(/\/api\/?$/, '')
    return `${mediaBaseUrl}${url}`
}

const formatSize = (bytes) => {
    if (!bytes) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const fetchList = async () => {
    loading.value = true
    try {
        const params = {page: 1, page_size: 100, type: 'image'}
        const {data} = await getMedia(params)
        allItems.value = (data.results || data || []).filter(isImageFile)
    } catch (error) {
        console.error('获取媒体列表失败:', error)
        ElMessage.error('获取媒体列表失败')
    } finally {
        loading.value = false
    }
}

const selectItem = (item) => {
    selectedId.value = item.id
    selectedItem.value = item
}

const handleSearch = () => {
    currentPage.value = 1
}

const handlePageChange = (page) => {
    currentPage.value = page
}

const confirmSelect = () => {
    if (!selectedItem.value) return
    emit('select', {
        url: getFullUrl(selectedItem.value.url),
        id: selectedItem.value.id,
        ...selectedItem.value,
    })
    emit('update:visible', false)
    ElMessage.success('已选择封面图')
}

const handleClose = () => {
    searchText.value = ''
    currentPage.value = 1
    selectedId.value = null
    selectedItem.value = null
}

watch(() => props.visible, (val) => {
    if (val) fetchList()
})
</script>

<style scoped>
.media-library {padding: 0}
.media-toolbar {margin-bottom: 16px}
.media-loading, .media-empty {display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 200px; gap: 12px; color: var(--text-tertiary)}
.media-grid {display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 12px}
.media-item {position: relative; border-radius: var(--radius-md); overflow: hidden; cursor: pointer; border: 2px solid transparent; transition: all 0.2s ease; background: var(--bg-secondary)}
.media-item:hover {border-color: var(--primary-light)}
.media-item.is-selected {border-color: var(--primary-color)}
.media-thumb {width: 100%; aspect-ratio: 1; object-fit: cover; display: block}
.media-info {padding: 8px; display: flex; flex-direction: column; gap: 2px}
.media-filename {font-size: 12px; color: var(--text-primary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap}
.media-size {font-size: 11px; color: var(--text-tertiary)}
.media-check {position: absolute; top: 8px; right: 8px; width: 24px; height: 24px; background: var(--primary-color); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white}
.media-pagination {margin-top: 16px; display: flex; justify-content: center}
</style>
