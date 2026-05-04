<template>
    <div class="stat-card" :class="[`stat-card--${type}`, { 'stat-card--clickable': clickable }]"
         :role="clickable ? 'button' : undefined"
         :tabindex="clickable ? 0 : undefined"
         @click="handleClick"
         @keydown.enter="handleClick">
        <div class="stat-content">
            <div class="stat-icon">
                <!-- slot 优先，fallback 到内置 icon -->
                <slot name="icon">
                    <el-icon :size="22" v-if="iconComponent">
                        <component :is="iconComponent" />
                    </el-icon>
                </slot>
            </div>
            <div class="stat-info">
                <span class="stat-value">{{ value }}</span>
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
import { computed } from 'vue'
import {
    Document, ChatDotRound, User, View,
    VideoPlay, Picture, Setting, Star, Message
} from '@element-plus/icons-vue'

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
    min-width: 0;
    flex: 1;
}

.stat-value {
    font-size: 28px;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.2;
    transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), color 0.3s ease;
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
}

.stat-card:hover .stat-footer {
    color: var(--text-secondary);
}
</style>
