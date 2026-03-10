<template>
  <div ref="artRef" class="artplayer-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import Artplayer from 'artplayer'

const props = defineProps({
  src: {
    type: String,
    required: true
  },
  poster: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['ready', 'error'])

const artRef = ref(null)
let artInstance = null

const initPlayer = () => {
  if (artInstance) {
    artInstance.destroy()
  }

  if (!artRef.value) {
    console.error('VideoPlayer: artRef is null')
    return
  }
  
  if (!props.src) {
    console.error('VideoPlayer: src is empty')
    return
  }

  console.log('VideoPlayer: initializing with src =', props.src)

  artInstance = new Artplayer({
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
    }
  })

  artInstance.on('ready', () => {
    console.log('VideoPlayer: ready')
    emit('ready')
  })

  artInstance.on('error', (error) => {
    console.error('VideoPlayer: error', error)
    emit('error', error)
  })
  
  artInstance.on('play', () => {
    console.log('VideoPlayer: playing')
  })
  
  artInstance.on('pause', () => {
    console.log('VideoPlayer: paused')
  })
}

watch(() => props.src, () => {
  if (props.src) {
    initPlayer()
  }
})

onMounted(() => {
  initPlayer()
})

onUnmounted(() => {
  if (artInstance) {
    artInstance.destroy()
    artInstance = null
  }
})
</script>

<style scoped>
.artplayer-container {
  width: 100%;
  height: 450px;
}
</style>
