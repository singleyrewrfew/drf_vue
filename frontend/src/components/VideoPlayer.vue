<template>
    <div class="video-player" :class="{ 'is-dark': isDark }">
        <!-- 加载态（覆盖层） -->
        <div v-if="!ready && !hasError" class="vp-loading">
            <span class="vp-spinner"/>
        </div>

        <!-- 错误态 -->
        <div v-if="hasError" class="vp-error">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <line x1="15" y1="9" x2="9" y2="15"/>
                <line x1="9" y1="9" x2="15" y2="15"/>
            </svg>
            <p>视频加载失败</p>
            <button v-if="src" class="vp-retry" @click="retry">重试</button>
        </div>

        <!-- 播放器容器：Artplayer 会在此渲染 video 元素 -->
        <div ref="containerRef" class="vp-container"/>
    </div>
</template>

<script setup>
import { ref, shallowRef, computed, onBeforeUnmount, onMounted, watch, nextTick } from 'vue'
import Artplayer from 'artplayer'
import { getMediaUrl } from '@/utils'
import { useThemeStore } from '@/stores/theme'

const props = defineProps({
    src:              { type: String, default: '' },
    poster:           { type: String, default: '' },
    thumbnails:       { type: String, default: '' },
    thumbnailsCount:  { type: Number, default: 0 },
    /** 最大高度 (px)，默认自适应 */
    maxHeight:        { type: [Number, String], default: undefined },
    /** 是否自动播放 */
    autoplay:         { type: Boolean, default: false },
})

const emit = defineEmits(['ready', 'error'])

const themeStore = useThemeStore()

/* ---- 响应式状态 ---- */

/** 使用 shallowRef 存储 Artplayer 实例，避免 Vue 对复杂对象做深度响应式代理 */
const art = shallowRef(null)

const isDark = computed(() => themeStore.theme === 'dark')
const containerRef = ref(null)

/** 组件内部展示状态 */
const ready    = ref(false)
const hasError = ref(false)

/* ---- 计时器 ---- */
let initTimer = null

/* ---- 可见性检测 (IntersectionObserver) ---- */
let visibilityObserver = null

/* ---- 构建 ---- */

/**
 * 解析缩略图配置
 * @returns {Object|undefined}
 */
const buildThumbnailsConfig = () => {
    const url   = getMediaUrl(props.thumbnails)
    const count = props.thumbnailsCount
    if (!url || count <= 0) return undefined
    return { url, number: count, width: 160, height: 90, column: 10 }
}

/** 从 CSS 变量读取主色（降级到 #0078D4） */
const readPrimaryColor = () =>
    getComputedStyle(document.documentElement).getPropertyValue('--primary-color').trim()
    || '#0078D4'

/**
 * 等待容器具有有效尺寸
 *
 * 处理 el-dialog 等延迟渲染场景：
 *   - el-dialog 打开时有 CSS 过渡动画
 *   - destroy-on-close 导致每次打开都重新 mount
 *   - onMounted 触发时容器可能仍为 display:none 或尺寸 0
 *
 * @param {number} retries - 最大重试次数（默认 20 次）
 * @param {number} interval - 重试间隔 ms（默认 100ms）
 * @returns {Promise<boolean>} 容器是否有有效尺寸
 */
const waitForContainer = (retries = 20, interval = 100) => new Promise((resolve) => {
    const check = (attempt = 0) => {
        if (!containerRef.value) return resolve(false)
        const rect = containerRef.value.getBoundingClientRect()
        if (rect.width > 0 && rect.height > 0) return resolve(true)
        if (attempt >= retries) return resolve(false)
        setTimeout(() => check(attempt + 1), interval)
    }
    check()
})

/**
 * 创建 / 重建播放器实例
 *
 * 核心流程：
 *   1. 销毁旧实例（destroy(false) 保留 DOM 容器）
 *   2. 重置内部状态
 *   3. 等待容器具有有效尺寸
 *   4. 创建新 Artplayer 实例并绑定事件
 */
const initPlayer = async () => {
    // 1. 销毁旧实例（false = 保留容器 div，不移除 DOM）
    destroyPlayer()

    // 2. 重置状态
    ready.value = false
    hasError.value = false

    await nextTick()

    if (!containerRef.value || !props.src) {
        console.warn('[VideoPlayer] 缺少容器或 src，跳过初始化')
        return
    }

    // 3. 等待容器可见且有尺寸（关键！Artplayer 要求容器必须有尺寸）
    const hasSize = await waitForContainer()
    if (!hasSize) {
        console.warn('[VideoPlayer] 容器尺寸仍为 0，跳过初始化', {
            src: props.src,
            rect: containerRef.value?.getBoundingClientRect(),
        })
        // 不设 error 态，让 IntersectionObserver 后续重试
        return
    }

    // 4. 超时保护（15 秒）
    clearTimeout(initTimer)
    initTimer = setTimeout(() => {
        if (!ready.value && !hasError.value) {
            hasError.value = true
            emit('error', new Error('视频加载超时'))
        }
    }, 15000)

    // 5. 构建配置并创建实例
    const options = {
        container:      containerRef.value,
        url:            props.src,
        autoplay:       props.autoplay,

        /* 布局 */
        pip:            true,
        autoSize:       true,
        autoMini:       true,
        fullscreen:     true,
        playsInline:    true,
        mutex:          true,
        backdrop:       true,
        miniProgressBar: true,

        /* 功能开关 */
        screenshot:     true,
        setting:        true,
        loop:           false,
        flip:           true,
        playbackRate:   true,
        aspectRatio:    true,
        subtitleOffset: true,
        airplay:        true,
        fastForward:    true,
        lock:           false,

        /* 外观 */
        theme:          readPrimaryColor(),
        lang:           navigator.language.toLowerCase(),
        moreVideoAttr:  { crossOrigin: 'anonymous' },

        /* 缩略图 */
        thumbnails:     buildThumbnailsConfig(),
    }

    // Artplayer 5.4+ 要求 poster 必须是字符串类型，不传则省略该字段
    if (props.poster) {
        options.poster = props.poster
    }

    try {
        art.value = new Artplayer(options)

        // 就绪事件
        art.value.on('ready', () => {
            clearTimeout(initTimer)
            ready.value = true
            emit('ready')
        })

        // 错误事件
        art.value.on('error', (err) => {
            clearTimeout(initTimer)
            hasError.value = true
            emit('error', err)
        })

        // 开始加载新资源 → 清除之前的错误态
        art.value.on('video:loadstart', () => { hasError.value = false })

    } catch (err) {
        console.error('[VideoPlayer] 创建实例异常:', err)
        clearTimeout(initTimer)
        hasError.value = true
        emit('error', err)
    }
}

/**
 * 销毁播放器实例
 *
 * 使用 destroy(false) 参数：
 *   - false = 仅解绑事件、释放内存，**保留容器 DOM 节点**
 *   - 这样后续可以重新在同一容器上创建新实例
 *   - 如果用 destroy() 或 destroy(true)，容器会被移除，导致无法重建
 */
const destroyPlayer = () => {
    clearTimeout(initTimer)
    if (art.value) {
        try {
            art.value.destroy(false)
        } catch (_) {
            // ignore: 容器可能已被外部移除
        }
        art.value = null
    }
}

/** 手动重试 */
const retry = () => initPlayer()

/* ---- Watchers ---- */

// src 变化 → 重建播放器
watch(() => props.src, async (newSrc, oldSrc) => {
    if (newSrc && newSrc !== oldSrc) {
        await initPlayer()
    }
})

// 主题切换 → 动态更新 Artplayer 内部配色和 CSS 类
watch(isDark, (dark) => {
    if (!art.value) return
    // 更新 Artplayer 内部 theme 色值
    art.value.option.theme = readPrimaryColor()
    // 切换容器深色类 → 触发 :deep() 样式重新匹配
    const el = containerRef.value?.closest('.video-player')
    if (el) el.classList.toggle('is-dark', dark)
}, { immediate: false })

// 缩略图变化 → 热更新（不重建整个播放器）
watch(
    () => [props.thumbnails, props.thumbnailsCount],
    ([url, count]) => {
        if (!art.value) return
        const config = buildThumbnailsConfig()
        if (config) art.value.thumbnails = config
    },
    { deep: false }
)

/* ---- 生命周期 ---- */

onMounted(() => {
    // 设置 IntersectionObserver 监听容器进入视口
    // 解决场景：el-dialog destroy-on-close → 组件挂载时 Dialog 可能还在动画中
    visibilityObserver = new IntersectionObserver(
        (entries) => {
            for (const entry of entries) {
                // 容器变为可见且尚未初始化且没有错误 → 自动触发
                if (
                    entry.isIntersecting &&
                    props.src &&
                    !art.value &&
                    !hasError.value
                ) {
                    initPlayer()
                }
            }
        },
        { threshold: 0.01 }
    )

    if (containerRef.value) {
        visibilityObserver.observe(containerRef.value)
    }

    // 正常场景（非 Dialog）：直接尝试初始化
    // Dialog 场景：如果容器尺寸为 0，initPlayer 内部会安全退出，
    // 等 Observer 检测到容器可见后再触发
    if (props.src) {
        initPlayer()
    }
})

/**
 * ⭐ 关键：使用 onBeforeUnload 而非 onUnmounted
 *
 * onBeforeUnmount 在 DOM 卸载之前调用，此时还能正确操作 DOM
 * onUnmounted 在卸载之后调用，此时容器可能已不存在
 */
onBeforeUnmount(() => {
    // 断开可见性观察
    if (visibilityObserver) {
        visibilityObserver.disconnect()
        visibilityObserver = null
    }
    // 销毁播放器（false = 保留容器 DOM）
    destroyPlayer()
})

/* ---- 暴露方法给父组件 ---- */

defineExpose({
    /** 播放 */
    play:    () => art.value?.play?.(),
    /** 暂停 */
    pause:   () => art.value?.pause?.(),
    /** 跳转 (秒) */
    seek:    (time) => art.value?.seek?.(time),
    /** 切换播放/暂停 */
    toggle:  () => art.value?.toggle?.(),
    /** 销毁并重新初始化 */
    refresh: () => initPlayer(),
    /** 当前播放器实例（高级用法） */
    instance: () => art.value,
})
</script>

<style scoped>
.video-player {
    position: relative;
    width: 100%;
    background: #000;
    border-radius: var(--radius-md, 8px);
    overflow: hidden;

    /* 默认 16:9，可被 maxHeight 覆盖 */
    --vp-height: min(70vh, 520px);
    aspect-ratio: 16 / 9;
    max-height: v-bind("typeof props.maxHeight === 'number' ? props.maxHeight + 'px' : (props.maxHeight || 'var(--vp-height)')");
}

.vp-container {
    width: 100%;
    height: 100%;
    display: block;
}

/* ---- 加载态 ---- */
.vp-loading {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #000;
    z-index: 10;
}

.vp-spinner {
    width: 36px; height: 36px;
    border: 3px solid rgba(255,255,255,0.12);
    border-top-color: var(--primary-color, #0078D4);
    border-radius: 50%;
    animation: vp-spin 0.75s linear infinite;
}

@keyframes vp-spin { to { transform: rotate(360deg); } }

/* ---- 错误态 ---- */
.vp-error {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    background: #000;
    color: var(--text-secondary, #909399);
    z-index: 10;
}

.vp-error svg { width: 48px; height: 48px; opacity: 0.5; }

.vp-error p {
    margin: 0; font-size: 14px;
}

.vp-retry {
    margin-top: 4px;
    padding: 6px 18px;
    border: none;
    border-radius: var(--radius-sm, 6px);
    background: var(--primary-color, #0078D4);
    color: #fff; font-size: 13px;
    cursor: pointer;
    transition: background 0.2s ease;
}
.vp-retry:hover { background: var(--primary-hover, #106EBE); }

/* ---- Artplayer 深度样式覆盖 ---- */

/* ===== 通用控件配色（浅色默认） ===== */

/* 底部控制栏 */
.video-player :deep(.art-bottom) {
    background: linear-gradient(transparent, rgba(0,0,0,0.65));
}

/* 进度条轨道 */
.video-player :deep(.art-progress .art-progress-outer) {
    background: rgba(255,255,255,0.18);
}
/* 已播放 / 缓冲 */
.video-player :deep(.art-progress .art-progress-inner),
.video-player :deep(.art-progress .art-progress-buffer) {}

/* 控制按钮图标 + 文字 */
.video-player :deep(.art-icon path),
.video-player :deep(.art-icon svg),
.video-player :deep(.art-time),
.video-player :deep(.art-subtitle-url) {
    color: #fff;
    fill: #fff;
}

/* 右键菜单 + 设置面板 */
.video-player :deep(.art-contextmenu),
.video-player :deep(.art-setting) {
    background: var(--card-bg, #fff);
    border-color: var(--border-color, #e5e5e5);
}

.video-player :deep(.art-contextmenu a),
.video-player :deep(.art-setting .art-setting-item) {
    color: var(--text-primary, #1a1a1a);
}

.video-player :deep(.art-contextmenu a:hover),
.video-player :deep(.art-setting .art-setting-item:hover) {
    background: var(--primary-bg, rgba(0,120,212,0.08));
    color: var(--primary-color, #0078d4);
}

.video-player :deep(.art-setting .art-setting-item-right) {
    color: var(--text-secondary, #616161);
}

/* ===== 深色模式适配 ===== */
.is-dark :deep(.art-bottom) {
    background: linear-gradient(transparent, rgba(0,0,0,0.82));
}

.is-dark :deep(.art-contextmenu),
.is-dark :deep(.art-setting) {
    background: var(--card-bg);
    border-color: var(--border-color);
}
.is-dark :deep(.art-contextmenu a),
.is-dark :deep(.art-setting .art-setting-item) {
    color: var(--text-primary);
}
.is-dark :deep(.art-setting .art-setting-item-right) {
    color: var(--text-secondary);
}
</style>
