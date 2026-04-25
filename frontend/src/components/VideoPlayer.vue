<template>
    <div class="artplayer-wrapper">
        <div ref="artRef" class="artplayer-container"></div>
        <div v-if="loading" class="artplayer-loading-overlay">
            <div class="loading-spinner"></div>
            <p>视频加载中...</p>
        </div>
    </div>
</template>

<script setup>
import {ref, onMounted, onUnmounted, watch, nextTick} from 'vue'
import Artplayer from 'artplayer'

const props = defineProps({
    src: {
        type: String,
        required: true
    },
    poster: {
        type: String,
        default: ''
    },
    thumbnails: {
        type: String,
        default: ''
    },
    thumbnailsCount: {
        type: Number,
        default: 0
    }
})

const emit = defineEmits(['ready', 'error'])

const artRef = ref(null)
let artInstance = null
const loading = ref(true)
let initTimeout = null

const getMediaBaseUrl = () => {
    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '/api'
    return apiBaseUrl.replace(/\/api\/?$/, '')
}

const initPlayer = async () => {
    if (artInstance) {
        artInstance.destroy()
        artInstance = null
    }

    // 等待 DOM 更新确保 ref 存在
    await nextTick()
    
    if (!artRef.value || !props.src) {
        loading.value = false
        return
    }

    // 设置加载超时，防止卡死
    loading.value = true
    clearTimeout(initTimeout)
    initTimeout = setTimeout(() => {
        console.error('[VideoPlayer] Load timeout')
        loading.value = false
        emit('error', new Error('视频加载超时'))
    }, 10000) // 10 秒超时

    const baseUrl = getMediaBaseUrl()
    const options = {
        container: artRef.value,
        url: props.src,
        poster: props.poster,
        autoplay: false,
        pip: true,
        autoSize: true,
        autoMini: true,
        screenshot: true,
        setting: true,
        loop: false,
        flip: true,
        playbackRate: true,
        aspectRatio: true,
        fullscreen: true,
        subtitleOffset: true,
        miniProgressBar: true,
        mutex: true,
        backdrop: true,
        playsInline: true,
        autoPlayback: true,
        airplay: true,
        theme: '#409eff',
        lang: navigator.language.toLowerCase(),
        moreVideoAttr: {
            crossOrigin: 'anonymous'
        },
        // 添加超时设置，防止加载卡死
        lock: false,
        fastForward: true
    }

    // 只有当缩略图 URL 有效且数量大于 0 时才配置缩略图
    if (props.thumbnails && props.thumbnails.trim() !== '' && props.thumbnailsCount > 0) {
        let thumbnailsUrl = props.thumbnails
        
        // 确保 URL 格式正确
        if (!thumbnailsUrl.startsWith('http')) {
            const baseUrl = getMediaBaseUrl()
            if (thumbnailsUrl.startsWith('/media/')) {
                thumbnailsUrl = `${baseUrl}${thumbnailsUrl}`
            } else {
                thumbnailsUrl = `${baseUrl}/media/${thumbnailsUrl}`
            }
        }

        console.log('[VideoPlayer] Thumbnails config:', {
            url: thumbnailsUrl,
            number: props.thumbnailsCount,
            original: props.thumbnails
        })

        options.thumbnails = {
            url: thumbnailsUrl,
            number: props.thumbnailsCount,
            width: 160,
            height: 90,
            column: 10,
        }
    } else {
        console.log('[VideoPlayer] No thumbnails:', {
            thumbnails: props.thumbnails,
            count: props.thumbnailsCount
        })
    }

    try {
        artInstance = new Artplayer(options)

        artInstance.on('ready', () => {
            clearTimeout(initTimeout)
            loading.value = false
            emit('ready')
        })

        artInstance.on('error', (error) => {
            clearTimeout(initTimeout)
            loading.value = false
            console.error('[VideoPlayer] Error:', error)
            emit('error', error)
        })
    } catch (error) {
        clearTimeout(initTimeout)
        loading.value = false
        console.error('[VideoPlayer] Failed to initialize:', error)
        emit('error', error)
    }
}

watch(() => [props.src, props.thumbnails], async ([newSrc, newThumbnails], [oldSrc, oldThumbnails]) => {
    // 仅在组件挂载后且 src 或 thumbnails 发生变化时重新初始化
    if (artRef.value && newSrc && (newSrc !== oldSrc || newThumbnails !== oldThumbnails)) {
        await initPlayer()
    }
}, { deep: true })

onMounted(() => {
    if (props.src) {
        initPlayer()
    }
})

onUnmounted(() => {
    if (artInstance) {
        artInstance.destroy()
        artInstance = null
    }
})
</script>

<style scoped>
.artplayer-wrapper {
    position: relative;
    width: 100%;
    height: 450px;
    background: #000;
}

.artplayer-container {
    width: 100%;
    height: 100%;
}

.artplayer-loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.8);
    color: #fff;
    z-index: 10;
}

.loading-spinner {
    border: 4px solid rgba(255, 255, 255, 0.3);
    border-top: 4px solid #fff;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin-bottom: 10px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
