<template>
    <!-- 视频播放器容器 -->
    <div class="artplayer-wrapper">
        <!-- Artplayer播放器挂载节点 -->
        <div ref="artRef" class="artplayer-container"></div>
        <!-- 视频加载状态遮罩层 -->
        <div v-if="loading" class="artplayer-loading-overlay">
            <div class="loading-spinner"></div>
            <p>视频加载中...</p>
        </div>
    </div>
</template>

<script setup>
import {ref, onMounted, onUnmounted, watch, nextTick} from 'vue'
import Artplayer from 'artplayer'

/**
 * 视频播放器组件属性定义
 */
const props = defineProps({
    /** 视频源地址（必需） */
    src: {
        type: String,
        required: true
    },
    /** 视频封面图片URL */
    poster: {
        type: String,
        default: ''
    },
    /** 视频缩略图URL（用于进度条预览） */
    thumbnails: {
        type: String,
        default: ''
    },
    /** 缩略图总数量 */
    thumbnailsCount: {
        type: Number,
        default: 0
    }
})

/**
 * 组件事件定义
 * @event ready - 播放器初始化完成时触发
 * @event error - 播放器加载或初始化失败时触发，携带错误对象参数
 */
const emit = defineEmits(['ready', 'error'])

/** 播放器DOM引用 */
const artRef = ref(null)
/** Artplayer实例对象 */
let artInstance = null
/** 视频加载状态标识 */
const loading = ref(true)
/** 初始化超时定时器 */
let initTimeout = null

/**
 * 获取媒体资源的基础URL地址
 * @returns {string} 媒体资源基础URL（去除/api后缀）
 */
const getMediaBaseUrl = () => {
    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '/api'
    return apiBaseUrl.replace(/\/api\/?$/, '')
}

/**
 * 初始化Artplayer播放器实例
 * 该函数会销毁旧实例并创建新实例，配置播放器各项参数及事件监听
 * @async
 * @throws {Error} 当播放器初始化失败时会触发error事件并传递错误对象
 */
const initPlayer = async () => {
    // 销毁已存在的播放器实例，避免内存泄漏
    if (artInstance) {
        artInstance.destroy()
        artInstance = null
    }

    // 等待 DOM 更新确保 ref 存在
    await nextTick()
    
    // 验证DOM节点和视频源是否有效
    if (!artRef.value || !props.src) {
        loading.value = false
        return
    }

    // 设置10秒加载超时保护，防止视频加载卡死
    loading.value = true
    clearTimeout(initTimeout)
    initTimeout = setTimeout(() => {
        console.error('[VideoPlayer] Load timeout')
        loading.value = false
        emit('error', new Error('视频加载超时'))
    }, 10000) // 10 秒超时

    // 构建播放器配置选项
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

    // 配置视频缩略图（仅当URL有效且数量大于0时启用）
    if (props.thumbnails && props.thumbnails.trim() !== '' && props.thumbnailsCount > 0) {
        let thumbnailsUrl = props.thumbnails
        
        // 标准化缩略图URL格式，确保包含完整域名
        if (!thumbnailsUrl.startsWith('http')) {
            const baseUrl = getMediaBaseUrl()
            if (thumbnailsUrl.startsWith('/media/')) {
                thumbnailsUrl = `${baseUrl}${thumbnailsUrl}`
            } else {
                thumbnailsUrl = `${baseUrl}/media/${thumbnailsUrl}`
            }
        }

        // 输出缩略图配置信息用于调试
        console.log('[VideoPlayer] Thumbnails config:', {
            url: thumbnailsUrl,
            number: props.thumbnailsCount,
            original: props.thumbnails
        })

        // 设置缩略图详细配置参数
        options.thumbnails = {
            url: thumbnailsUrl,
            number: props.thumbnailsCount,
            width: 160,
            height: 90,
            column: 10,
        }
    } else {
        // 输出未启用缩略图的原因
        console.log('[VideoPlayer] No thumbnails:', {
            thumbnails: props.thumbnails,
            count: props.thumbnailsCount
        })
    }

    // 使用try-catch捕获播放器初始化异常
    try {
        artInstance = new Artplayer(options)

        // 监听播放器就绪事件
        artInstance.on('ready', () => {
            clearTimeout(initTimeout)
            loading.value = false
            emit('ready')
        })

        // 监听播放器错误事件
        artInstance.on('error', (error) => {
            clearTimeout(initTimeout)
            loading.value = false
            console.error('[VideoPlayer] Error:', error)
            emit('error', error)
        })
    } catch (error) {
        // 处理播放器初始化失败的异常情况
        clearTimeout(initTimeout)
        loading.value = false
        console.error('[VideoPlayer] Failed to initialize:', error)
        emit('error', error)
    }
}

/**
 * 监听视频源和缩略图变化，自动重新初始化播放器
 * @param {Array} [newSrc, newThumbnails] - 新的视频源和缩略图URL
 * @param {Array} [oldSrc, oldThumbnails] - 旧的视频源和缩略图URL
 */
watch(() => [props.src, props.thumbnails], async ([newSrc, newThumbnails], [oldSrc, oldThumbnails]) => {
    // 仅在组件挂载后且 src 或 thumbnails 发生变化时重新初始化
    if (artRef.value && newSrc && (newSrc !== oldSrc || newThumbnails !== oldThumbnails)) {
        await initPlayer()
    }
}, { deep: true })

/**
 * 组件挂载时初始化播放器（仅当有视频源时）
 */
onMounted(() => {
    if (props.src) {
        initPlayer()
    }
})

/**
 * 组件卸载时销毁播放器实例，释放资源防止内存泄漏
 */
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
