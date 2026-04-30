<template>
    <div class="artplayer-wrapper">
        <div ref="artRef" class="artplayer-container"></div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import Artplayer from 'artplayer'
import { getMediaUrl } from '@/utils'

const props = defineProps({
    src: { type: String, required: true },
    poster: { type: String, default: '' },
    thumbnails: { type: String, default: '' },
    thumbnailsCount: { type: Number, default: 0 },
})

const emit = defineEmits(['ready', 'error'])

const artRef = ref(null)
let artInstance = null
let initTimeout = null

const buildThumbnailsConfig = (url, count) => {
    const resolved = getMediaUrl(url)
    if (!resolved || count <= 0) return undefined
    return { url: resolved, number: count, width: 160, height: 90, column: 10 }
}

const initPlayer = async () => {
    if (artInstance) {
        artInstance.destroy()
        artInstance = null
    }

    await nextTick()

    if (!artRef.value || !props.src) return

    clearTimeout(initTimeout)
    initTimeout = setTimeout(() => {
        emit('error', new Error('视频加载超时'))
    }, 10000)

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
        moreVideoAttr: { crossOrigin: 'anonymous' },
        lock: false,
        fastForward: true,
        thumbnails: buildThumbnailsConfig(props.thumbnails, props.thumbnailsCount),
    }

    try {
        artInstance = new Artplayer(options)

        artInstance.on('ready', () => {
            clearTimeout(initTimeout)
            emit('ready')
        })

        artInstance.on('error', (error) => {
            clearTimeout(initTimeout)
            emit('error', error)
        })
    } catch (error) {
        clearTimeout(initTimeout)
        emit('error', error)
    }
}

watch(() => props.src, async (newSrc, oldSrc) => {
    if (artRef.value && newSrc && newSrc !== oldSrc) {
        await initPlayer()
    }
})

watch(() => props.thumbnails, (newVal, oldVal) => {
    if (newVal === oldVal || !artInstance) return
    const config = buildThumbnailsConfig(newVal, props.thumbnailsCount)
    if (config) {
        artInstance.thumbnails = config
    }
})

onMounted(() => {
    if (props.src) initPlayer()
})

onUnmounted(() => {
    clearTimeout(initTimeout)
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
</style>
