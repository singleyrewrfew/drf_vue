<template>
    <div class="artplayer-wrapper" :class="{ 'artplayer-dark': isDark }">
        <div ref="artRef" class="artplayer-container"></div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import Artplayer from 'artplayer'
import { getMediaUrl } from '@/utils'
import { useThemeStore } from '@/stores/theme'

const props = defineProps({
    src: { type: String, required: true },
    poster: { type: String, default: '' },
    thumbnails: { type: String, default: '' },
    thumbnailsCount: { type: Number, default: 0 },
})

const emit = defineEmits(['ready', 'error'])

const themeStore = useThemeStore()
const isDark = ref(themeStore.theme === 'dark')
const artRef = ref(null)
let artInstance = null
let initTimeout = null

const PRIMARY_COLOR = '#0078D4'

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
        theme: PRIMARY_COLOR,
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

watch(() => themeStore.theme, (newTheme) => {
    isDark.value = newTheme === 'dark'
})

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

:deep(.art-contextmenu) {
    background: var(--card-bg, #fff);
    border-color: var(--border-color, #e5e5e5);
}

:deep(.art-contextmenu a) {
    color: var(--text-primary, #1a1a1a);
}

:deep(.art-contextmenu a:hover) {
    background: var(--primary-bg, rgba(0, 120, 212, 0.08));
    color: var(--primary-color, #0078d4);
}

:deep(.art-setting) {
    background: var(--card-bg, #fff);
}

:deep(.art-setting .art-setting-item) {
    color: var(--text-primary, #1a1a1a);
}

:deep(.art-setting .art-setting-item:hover) {
    background: var(--primary-bg, rgba(0, 120, 212, 0.08));
}

:deep(.art-setting .art-setting-item-right) {
    color: var(--text-secondary, #616161);
}
</style>
