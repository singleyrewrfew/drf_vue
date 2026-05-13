<template>
    <div class="stat-card"
         :class="[`stat-card--${type}`, `stat-card--${size}`, { 'stat-card--clickable': clickable }]"
         :role="clickable ? 'button' : undefined"
         :tabindex="clickable ? 0 : undefined"
         @click="handleClick"
         @keydown.enter="handleClick">
        <div class="stat-content">
            <div class="stat-icon">
                <slot name="icon">
                    <el-icon :size="iconSize" v-if="iconComponent">
                        <component :is="iconComponent" />
                    </el-icon>
                </slot>
            </div>
            <div class="stat-info">
                <span class="stat-value">{{ animated && animationStarted ? displayValue : formattedValue }}</span>
                <span class="stat-label">{{ label }}</span>
            </div>
            <slot name="extra" />
        </div>
        <div class="stat-footer" v-if="$slots.footer || footer">
            <slot name="footer">{{ footer }}</slot>
        </div>
    </div>
</template>

<script setup>
import { computed, watch, onMounted, ref } from 'vue'
import {
    Document, ChatDotRound, User, View,
    VideoPlay, Picture, Setting, Star, Message
} from '@element-plus/icons-vue'
import { useCountUp } from '@/composables/useCountUp.js'

const props = defineProps({
    value: {
        type: [String, Number],
        required: true
    },
    label: {
        type: String,
        required: true
    },
    /** 主题色 */
    type: {
        type: String,
        default: 'primary',
        validator: (v) => ['primary', 'success', 'warning', 'danger', 'info'].includes(v)
    },
    /**
     * 内置图标名（字符串）
     * 支持值: Document / ChatDotRound / User / View / VideoPlay /
     *         Picture / Setting / Star / Message
     *
     * 也可通过 #icon slot 自定义任意内容
     */
    icon: {
        type: String,
        default: ''
    },
    /** 底部文字 */
    footer: {
        type: String,
        default: ''
    },
    /** 是否可点击（启用后触发 @click） */
    clickable: {
        type: Boolean,
        default: false
    },
    /** 尺寸变体：large(主卡片) / normal(默认) / wide(全宽) */
    size: {
        type: String,
        default: 'normal',
        validator: (v) => ['large', 'normal', 'wide'].includes(v)
    },
    /** 是否启用数字动画 */
    animated: {
        type: Boolean,
        default: true
    }
})

const emit = defineEmits(['click'])

/** 内置图标映射表 */
const iconMap = {
    Document, ChatDotRound, User, View,
    VideoPlay, Picture, Setting, Star, Message
}

/** 根据 icon 名称查找对应组件 */
const iconComponent = computed(() => iconMap[props.icon] || null)

/** 根据尺寸动态调整图标大小 */
const iconSize = computed(() => {
    const sizes = { large: 28, normal: 22, wide: 24 }
    return sizes[props.size] || 22
})

/** 格式化静态数值（非动画模式）*/
const formattedValue = computed(() => {
    const num = Number(props.value) || 0
    return num.toLocaleString('en-US')
})

/** CountUp 动画 Hook - 简化版 */
const targetNum = computed(() => Number(props.value) || 0)
const { displayValue, startAnimation } = useCountUp(0)

/** 动画是否已启动 */
const animationStarted = ref(false)

/** 启动动画的统一方法 */
const triggerAnimation = (value) => {
    if (animationStarted.value) {
        startAnimation(value, {
            duration: props.size === 'wide' ? 1200 : 1000,
            easing: 'easeOutQuart',
            startFromCurrent: true
        })
    } else {
        animationStarted.value = true
        startAnimation(value, {
            duration: props.size === 'wide' ? 1800 : 1400,
            easing: 'easeOutExpo'
        })
    }
}

onMounted(() => {
    if (props.animated && targetNum.value > 0) {
        requestAnimationFrame(() => {
            setTimeout(() => triggerAnimation(targetNum.value), 100)
        })
    }
})

watch(targetNum, (newValue, oldValue) => {
    if (!props.animated) return
    if (newValue !== oldValue) {
        triggerAnimation(newValue)
    }
})

const handleClick = () => {
    if (props.clickable) emit('click')
}
</script>

<style scoped>
.stat-card {
    position: relative;
    padding: 16px;
    border-radius: var(--radius-md);
    background: var(--card-bg);
    transition:
        transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1),
        box-shadow 0.3s ease,
        border-color 0.25s ease,
        background 0.3s ease;
    border: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    justify-content: space-between; /* 让内容在等高容器中均匀分布 */
    height: 100%; /* 填满 grid 单元格高度 */
    min-width: 0; /* 允许在 grid 中收缩 */
    overflow: hidden; /* 防止内容溢出 */
}

/* 键盘焦点可见状态（可点击卡片）*/
.stat-card--clickable:focus-visible {
    outline: none;
    box-shadow:
        0 4px 20px -6px rgba(0, 0, 0, 0.15),
        0 0 0 3px var(--primary-bg),
        0 0 0 5px var(--primary-color);
}

/* ---- 底部光晕装饰线（hover 时亮起） ---- */
.stat-card::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 10%;
    right: 10%;
    height: 2px;
    border-radius: 2px;
    opacity: 0;
    transform: scaleX(0.5);
    transition: all 0.3s ease;
}

/* 可点击态 */
.stat-card--clickable {
    cursor: pointer;
}

/* ================================================================
   尺寸变体 — Bento Grid 适配
   ================================================================ */

/* ---- Large（主卡片，占据 2x1 空间） ---- */
.stat-card--large {
    padding: 20px 24px;
}

.stat-card--large .stat-content {
    gap: 20px;
}

.stat-card--large .stat-icon {
    width: 56px;
    height: 56px;
}

.stat-card--large .stat-value {
    font-size: 36px;
}

.stat-card--large .stat-label {
    font-size: 15px;
}

/* ---- Normal（标准卡片，默认尺寸） ---- */
.stat-card--normal {
    padding: 16px;
}

/* ---- Wide（全宽数据流卡片） ---- */
.stat-card--wide {
    padding: 24px 32px;
    background: linear-gradient(135deg, var(--card-bg) 0%, var(--bg-secondary) 100%);
}

.stat-card--wide .stat-content {
    justify-content: center;
    text-align: center;
    flex-direction: column;
    gap: 16px;
}

.stat-card--wide .stat-icon {
    width: 56px;
    height: 56px;
    border-radius: var(--radius-md);
}

.stat-card--wide .stat-value {
    font-size: 42px;
    font-weight: 700;
    letter-spacing: -0.02em;
}

.stat-card--wide .stat-label {
    font-size: 15px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    opacity: 0.8;
}

/* ---- 统一 hover 效果 ---- */
.stat-card:hover {
    transform: translateY(-4px);
    box-shadow:
        0 8px 24px -6px rgba(0, 0, 0, 0.12),
        0 4px 8px -4px rgba(0, 0, 0, 0.06);
    border-color: transparent;
}

.stat-card:hover::after {
    opacity: 1;
    transform: scaleX(1);
}

/* 各主题光晕颜色 */
.stat-card--primary:hover::after { background: var(--primary-color); box-shadow: 0 0 12px var(--primary-color); }
.stat-card--success:hover::after { background: var(--success-color); box-shadow: 0 0 12px var(--success-color); }
.stat-card--warning:hover::after { background: var(--warning-color); box-shadow: 0 0 12px var(--warning-color); }
.stat-card--danger:hover::after { background: var(--danger-color); box-shadow: 0 0 12px var(--danger-color); }
.stat-card--info:hover::after { background: var(--info-color); box-shadow: 0 0 12px var(--info-color); }

/* ---- 内容区 ---- */
.stat-content {
    display: flex;
    align-items: center;
    gap: 16px;
    flex: 1; /* 自动填充可用空间 */
}

/* ---- 图标容器 ---- */
.stat-icon {
    width: 44px;
    height: 44px;
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* hover 图标弹跳 */
.stat-card:hover .stat-icon {
    transform: rotate(-8deg) scale(1.15);
}

/* ---- 图标背景/前景色跟随主题 ---- */
.stat-card--primary .stat-icon { background: var(--primary-bg); color: var(--primary-color); }
.stat-card--success .stat-icon { background: var(--success-bg); color: var(--success-color); }
.stat-card--warning .stat-icon { background: var(--warning-bg); color: var(--warning-color); }
.stat-card--danger .stat-icon { background: var(--danger-bg); color: var(--danger-color); }
.stat-card--info .stat-icon { background: var(--info-bg); color: var(--info-color); }

/* ---- 文字区域 ---- */
.stat-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0; /* 允许收缩 */
    flex: 1;
    overflow: hidden; /* 防止内容溢出 */
}

.stat-value {
    font-size: 28px;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.2;
    transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), color 0.3s ease;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* hover 数值微微上移 + 变色 */
.stat-card:hover .stat-value {
    transform: translateY(-2px);
}

.stat-card--primary:hover .stat-value { color: var(--primary-color); }
.stat-card--success:hover .stat-value { color: var(--success-color); }
.stat-card--warning:hover .stat-value { color: var(--warning-color); }
.stat-card--danger:hover .stat-value { color: var(--danger-color); }
.stat-card--info:hover .stat-value { color: var(--info-color); }

.stat-label {
    font-size: 13px;
    color: var(--text-secondary);
    font-weight: 400;
    transition: color 0.3s ease;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.stat-card:hover .stat-label {
    color: var(--text-primary);
}

/* ---- 底部 ---- */
.stat-footer {
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid var(--border-light);
    font-size: 12px;
    color: var(--text-tertiary);
    transition: color 0.3s ease;
    overflow: hidden;
    flex-shrink: 0; /* 防止 footer 被压缩 */
}

.stat-card:hover .stat-footer {
    color: var(--text-secondary);
}
</style>
