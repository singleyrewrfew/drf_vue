<template>
    <button
        class="action-btn"
        :class="[`action-btn--${type}`, `action-btn--${size}`, { 'action-btn--spin': spinIcon, 'action-btn--outline': variant === 'outline', 'action-btn--after': iconAfter }]"
        :disabled="disabled"
        :type="htmlType"
        @click="handleClick"
    >
        <!-- 图标在左侧（默认） -->
        <svg v-if="icon && !iconAfter" class="action-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" v-html="iconSvg" />
        <span class="action-text">
            <slot>{{ text }}</slot>
        </span>
        <!-- 图标在右侧 -->
        <svg v-if="icon && iconAfter" class="action-icon action-icon--after" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" v-html="iconSvg" />
    </button>
</template>

<script setup>
const emit = defineEmits(['click'])

const props = defineProps({
    /** 按钮文字（支持 slot 覆盖，不传则使用 slot 内容） */
    text: {
        type: String,
        default: ''
    },
    /** 图标名称 */
    icon: {
        type: String,
        default: ''
    },
    /** 颜色主题 */
    type: {
        type: String,
        default: 'primary',
        validator: v => ['primary', 'danger', 'info', 'success', 'warning', 'text'].includes(v)
    },
    /** 尺寸变体: normal(大号14px) / small(小号12px) */
    size: {
        type: String,
        default: 'small',
        validator: v => ['normal', 'small'].includes(v)
    },
    /** 样式变体: filled(实心默认) / outline(描边) */
    variant: {
        type: String,
        default: 'filled',
        validator: v => ['filled', 'outline'].includes(v)
    },
    disabled: {
        type: Boolean,
        default: false
    },
    /** hover时图标是否旋转90° (仅normal尺寸生效) */
    spinIcon: {
        type: Boolean,
        default: false
    },
    /** 图标是否在文字右侧 */
    iconAfter: {
        type: Boolean,
        default: false
    },
    /** 是否阻止事件冒泡 (@click.stop) */
    stop: {
        type: Boolean,
        default: false
    },
    /** HTML button type */
    htmlType: {
        type: String,
        default: 'button'
    }
})

/** 内置图标 SVG 路径 */
const icons = {
    plus: '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
    edit: '<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>',
    delete: '<polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/>',
    preview: '<rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/>',
    copy: '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>',
    approve: '<polyline points="20 6 9 17 4 12"/>',
    upload: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>',
    // 新增图标
    search: '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    reset: '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>',
    retry: '<polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>',
    eye: '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
    arrowRight: '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
    publish: '<path d="M22 2L11 13"/><path d="M22 2L15 22L11 13L2 9L22 2Z"/>'
}

const iconSvg = icons[props.icon] || ''

const handleClick = (e) => {
    if (props.stop) e.stopPropagation()
    emit('click')
}
</script>

<style scoped>
/* ---- 基础样式 ---- */
.action-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    border: none;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
    user-select: none;
    position: relative;
    z-index: 1;
}

/* ---- 尺寸变体 ---- */

/* normal — 大号按钮（用于卡片头部新建等场景） */
.action-btn--normal {
    padding: 8px 16px;
    font-size: 14px;
    border-radius: var(--radius-sm);
    gap: 6px;
}
.action-btn--normal .action-icon {
    width: 14px;
    height: 14px;
    transition: transform 0.15s ease;
}

/* small — 小号按钮（用于表格行内操作） */
.action-btn--small {
    padding: 4px 10px;
    font-size: 12px;
    border-radius: var(--radius-xs);
    gap: 4px;
    vertical-align: middle;
}
.action-btn--small .action-icon {
    width: 12px;
    height: 12px;
}

/* ================================================================
   颜色主题 — filled（实心）变体
   ================================================================ */

.action-btn--primary {
    background: var(--primary-color);
    color: #fff;
}
.action-btn--primary:hover {
    background: var(--primary-hover);
}
.action-btn--primary:active {
    background: var(--primary-active, #337ecc);
}
.action-btn--primary:disabled:hover {
    background: var(--primary-color);
}

.action-btn--danger {
    background: var(--danger-color);
    color: #fff;
}
.action-btn--danger:hover {
    background: var(--danger-hover);
}
.action-btn--danger:active {
    filter: brightness(0.95);
}
.action-btn--danger:disabled:hover {
    background: var(--danger-color);
}

.action-btn--info {
    background: var(--info-color, #909399);
    color: #fff;
}
.action-btn--info:hover {
    background: var(--info-hover, #a6a9ad);
}
.action-btn--info:active {
    filter: brightness(0.95);
}

.action-btn--success {
    background: var(--success-color, #67c23a);
    color: #fff;
}
.action-btn--success:hover {
    background: var(--success-hover, #85ce61);
}
.action-btn--success:active {
    filter: brightness(0.95);
}
.action-btn--success:disabled:hover {
    background: var(--success-color, #67c23a);
}

.action-btn--warning {
    background: var(--warning-color, #e6a23c);
    color: #fff;
}
.action-btn--warning:hover {
    background: var(--warning-hover, #ebb563);
}
.action-btn--warning:active {
    filter: brightness(0.95);
}
.action-btn--warning:disabled:hover {
    background: var(--warning-color, #e6a23c);
}

/* ================================================================
   颜色主题 — outline（描边）变体
   共性：边框 + 透明底色，文字颜色随 type 变化
   ================================================================ */

.action-btn--outline {
    border: 1px solid var(--border-color);
    background: var(--card-bg);
}

/* outline-neutral (ResetButton 风格：中性灰色文字) */
.action-btn--outline.action-btn--text {
    color: var(--text-primary);
}
.action-btn--outline.action-btn--text:hover {
    background: var(--bg-secondary, #f0f2f5);
    border-color: var(--border-dark, #d4d7de);
}
.action-btn--outline.action-btn--text:active {
    background: var(--bg-tertiary, #e5e7eb);
}
.action-btn--outline.action-btn--text:disabled:hover {
    background: var(--card-bg);
    border-color: var(--border-color);
}

/* outline-primary (ViewAllButton 风格：主色文字) */
.action-btn--outline.action-btn--primary {
    color: var(--primary-color);
}
.action-btn--outline.action-btn--primary:hover {
    background: var(--primary-bg, #ecf5ff);
    border-color: var(--primary-color-light-5, #c6e2ff);
}
.action-btn--outline.action-btn--primary:active {
    background: var(--bg-secondary);
}
.action-btn--outline.action-btn--primary:disabled:hover {
    background: var(--card-bg);
    border-color: var(--border-color);
}

/* outline-danger / info / success / warning 同理 */
.action-btn--outline.action-btn--danger { color: var(--danger-color); }
.action-btn--outline.action-btn--danger:hover {
    background: #fef0f0; border-color: var(--danger-color-light-5, #fbc4c4);
}
.action-btn--outline.action-btn--danger:disabled:hover {
    background: var(--card-bg); border-color: var(--border-color);
}

.action-btn--outline.action-btn--info { color: var(--info-color, #909399); }
.action-btn--outline.action-btn--info:hover {
    background: #f4f4f5; border-color: #c8c9cc;
}
.action-btn--outline.action-btn--info:disabled:hover {
    background: var(--card-bg); border-color: var(--border-color);
}

/* ---- 禁用态（所有变体通用） ---- */
.action-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* ---- hover 时图标旋转（如 + 号变成 × 感觉） ---- */
.action-btn--spin:hover .action-icon:not(.action-icon--after) {
    transform: rotate(90deg);
}

/* ---- 右侧图标特殊动效 (ViewAllButton 的箭头右移) ---- */
.action-btn--after .action-icon--after {
    transition: transform 0.15s ease;
}
.action-btn--after:hover .action-icon--after {
    transform: translateX(2px);
}
</style>
