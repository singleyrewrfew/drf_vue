<template>
    <div class="empty-state" :class="[`empty-state--${type}`, { 'empty-state--compact': compact }]">
        <!-- 自定义插图区域 -->
        <div class="empty-illustration">
            <slot name="illustration">
                <!-- 默认 SVG 插图（根据类型动态切换） -->
                <svg v-if="type === 'data'" class="empty-svg" viewBox="0 0 200 160" fill="none">
                    <!-- 文档/数据空状态图标 -->
                    <rect x="40" y="20" width="120" height="100" rx="8" stroke="currentColor" stroke-width="2" fill="none"/>
                    <line x1="60" y1="50" x2="140" y2="50" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    <line x1="60" y1="75" x2="120" y2="75" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    <line x1="60" y1="100" x2="100" y2="100" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    <circle cx="150" cy="130" r="25" fill="var(--primary-bg)" stroke="var(--primary-color)" stroke-width="2"/>
                    <path d="M145 130L150 135L158 125" stroke="var(--primary-color)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>

                <svg v-else-if="type === 'search'" class="empty-svg" viewBox="0 0 200 160" fill="none">
                    <!-- 搜索无结果图标 -->
                    <circle cx="85" cy="70" r="35" stroke="currentColor" stroke-width="2" fill="none"/>
                    <line x1="110" y1="95" x2="140" y2="125" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
                    <line x1="68" y1="55" x2="102" y2="89" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                    <line x1="102" y1="55" x2="68" y2="89" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                </svg>

                <svg v-else-if="type === 'error'" class="empty-svg" viewBox="0 0 200 160" fill="none">
                    <!-- 错误状态图标 -->
                    <circle cx="100" cy="75" r="45" stroke="var(--danger-color)" stroke-width="2" fill="var(--danger-bg)"/>
                    <line x1="85" y1="60" x2="115" y2="90" stroke="var(--danger-color)" stroke-width="3" stroke-linecap="round"/>
                    <line x1="115" y1="60" x2="85" y2="90" stroke="var(--danger-color)" stroke-width="3" stroke-linecap="round"/>
                    <text x="100" y="142" text-anchor="middle" font-size="13" fill="var(--text-secondary)">出错了</text>
                </svg>

                <svg v-else class="empty-svg" viewBox="0 0 200 160" fill="none">
                    <!-- 默认通用空状态 -->
                    <rect x="30" y="30" width="140" height="90" rx="10" stroke="currentColor" stroke-width="2" fill="none" stroke-dasharray="6 4"/>
                    <path d="M80 65 L95 80 L120 55" stroke="var(--primary-color)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </slot>
        </div>

        <!-- 文字内容区 -->
        <div class="empty-content">
            <h3 v-if="title || $slots.title" class="empty-title">
                <slot name="title">{{ title }}</slot>
            </h3>
            
            <p v-if="description || $slots.description" class="empty-description">
                <slot name="description">{{ description }}</slot>
            </p>

            <!-- 操作按钮区 -->
            <div v-if="$slots.action || actionText" class="empty-action">
                <slot name="action">
                    <ActionButton 
                        :icon="actionIcon"
                        :text="actionText"
                        size="normal"
                        @click="$emit('action')"
                    />
                </slot>
            </div>

            <!-- 辅助链接 -->
            <div v-if="$slots.secondary || secondaryText" class="empty-secondary">
                <slot name="secondary">
                    <button class="secondary-link" @click="$emit('secondary')">
                        {{ secondaryText }}
                    </button>
                </slot>
            </div>
        </div>
    </div>
</template>

<script setup>
import ActionButton from './ActionButton.vue'

defineProps({
    /** 空状态类型 */
    type: {
        type: String,
        default: 'data',
        validator: (v) => ['data', 'search', 'error'].includes(v)
    },
    /** 标题文字 */
    title: {
        type: String,
        default: ''
    },
    /** 描述文字 */
    description: {
        type: String,
        default: ''
    },
    /** 主操作按钮文字 */
    actionText: {
        type: String,
        default: ''
    },
    /** 主操作按钮图标 */
    actionIcon: {
        type: String,
        default: 'plus'
    },
    /** 次要操作文字（如"了解更多"） */
    secondaryText: {
        type: String,
        default: ''
    },
    /** 紧凑模式（减少间距） */
    compact: {
        type: Boolean,
        default: false
    }
})

defineEmits(['action', 'secondary'])
</script>

<style scoped>
/* ================================================================
   Empty State — 专业空状态组件
   设计标准：情感化插图 + 引导性文案 + 明确行动点
   ================================================================ */

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 48px 24px;
    text-align: center;
}

.empty-state--compact {
    padding: 32px 16px;
}

/* ---- 插图区域 ---- */
.empty-illustration {
    margin-bottom: 24px;
    color: var(--text-tertiary);
    transition: color 0.3s ease, transform 0.3s ease;
}

.empty-state:hover .empty-illustration {
    color: var(--text-secondary);
    transform: scale(1.02);
}

.empty-svg {
    width: 160px;
    height: 128px;
    max-width: 100%;
}

.empty-state--compact .empty-svg {
    width: 120px;
    height: 96px;
}

/* ---- 内容区域 ---- */
.empty-content {
    max-width: 360px;
}

.empty-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 8px 0;
    line-height: 1.4;
}

.empty-state--compact .empty-title {
    font-size: 16px;
    margin-bottom: 6px;
}

.empty-description {
    font-size: 14px;
    line-height: 1.6;
    color: var(--text-secondary);
    margin: 0 0 20px 0;
}

.empty-state--compact .empty-description {
    font-size: 13px;
    margin-bottom: 16px;
}

/* ---- 操作按钮 ---- */
.empty-action {
    margin-bottom: 12px;
}

/* ---- 辅助链接 ---- */
.empty-secondary {
    margin-top: 4px;
}

.secondary-link {
    background: none;
    border: none;
    padding: 0;
    font-size: 13px;
    color: var(--primary-color);
    cursor: pointer;
    transition: color 0.15s ease;
    font-family: inherit;
}

.secondary-link:hover {
    color: var(--primary-hover);
    text-decoration: underline;
}

/* ================================================================
   类型变体样式微调
   ================================================================ */

/* 数据为空（默认） */
.empty-state--data .empty-illustration {
    color: var(--text-tertiary);
}

/* 搜索无结果 */
.empty-state--search .empty-illustration {
    color: var(--info-color, #909399);
}

/* 错误状态 */
.empty-state--error .empty-illustration {
    color: var(--danger-color);
}
</style>
