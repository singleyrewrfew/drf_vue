<template>
    <div class="quick-action-card" :class="[type]" @click="$emit('click')">
        <div class="action-icon">
            <el-icon :size="20">
                <slot></slot>
            </el-icon>
        </div>
        <span class="action-title">{{ title }}</span>
    </div>
</template>

<script setup>
defineEmits(['click'])
defineProps({
    title: {
        type: String,
        required: true
    },
    description: {
        type: String,
        default: ''
    },
    type: {
        type: String,
        default: 'primary',
        validator: (v) => ['primary', 'success', 'warning', 'danger', 'info'].includes(v)
    }
})
</script>

<style scoped>
.quick-action-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 20px 12px;
    background: var(--card-bg);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition:
        transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1),
        box-shadow 0.3s ease,
        border-color 0.25s ease;
    border: 1px solid var(--border-color);
    min-height: 88px;
    position: relative;
}

/* ---- 底部光晕装饰线（hover 时亮起） ---- */
.quick-action-card::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 15%;
    right: 15%;
    height: 2px;
    border-radius: 2px;
    opacity: 0;
    transform: scaleX(0.5);
    transition: all 0.3s ease;
}

/* ---- 统一 hover 效果 ---- */
.quick-action-card:hover {
    transform: translateY(-4px);
    box-shadow:
        0 8px 24px -6px rgba(0, 0, 0, 0.12),
        0 4px 8px -4px rgba(0, 0, 0, 0.06);
    border-color: transparent;
}

.quick-action-card:hover::after {
    opacity: 1;
    transform: scaleX(1);
}

/* 各主题光晕颜色 + 图标背景加深 */
.quick-action-card.primary:hover { --icon-hover-bg: var(--primary-color-light-7); }
.quick-action-card.primary:hover::after { background: var(--primary-color); box-shadow: 0 0 12px var(--primary-color); }

.quick-action-card.success:hover { --icon-hover-bg: var(--success-color-light-7); }
.quick-action-card.success:hover::after { background: var(--success-color); box-shadow: 0 0 12px var(--success-color); }

.quick-action-card.warning:hover { --icon-hover-bg: var(--warning-color-light-7); }
.quick-action-card.warning:hover::after { background: var(--warning-color); box-shadow: 0 0 12px var(--warning-color); }

.quick-action-card.danger:hover { --icon-hover-bg: var(--danger-color-light-7); }
.quick-action-card.danger:hover::after { background: var(--danger-color); box-shadow: 0 0 12px var(--danger-color); }

.quick-action-card.info:hover { --icon-hover-bg: var(--info-color-light-7); }
.quick-action-card.info:hover::after { background: var(--info-color); box-shadow: 0 0 12px var(--info-color); }

/* 点击按下时：覆盖 hover 的 translateY(-4px)，优先级高于单 :hover */
.quick-action-card:hover:active {
    transform: translateY(-2px);
}

.action-icon {
    width: 40px;
    height: 40px;
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--icon-bg);
    color: var(--icon-color);
    transition:
        transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1),
        background 0.3s ease;
}

/* hover 图标弹跳 + 背景加深 */
.quick-action-card:hover .action-icon {
    transform: rotate(-8deg) scale(1.15);
    background: var(--icon-hover-bg, var(--icon-bg));
}

.action-title {
    font-size: 13px;
    font-weight: 500;
    color: var(--text-primary);
    text-align: center;
    transition: color 0.3s ease;
}

.quick-action-card:hover .action-title {
    opacity: 0.85;
}

/* ---- 各主题图标色 ---- */
.quick-action-card.primary {
    --icon-bg: var(--primary-bg);
    --icon-color: var(--primary-color);
}
.quick-action-card.success {
    --icon-bg: var(--success-bg);
    --icon-color: var(--success-color);
}
.quick-action-card.warning {
    --icon-bg: var(--warning-bg, #fdf6ec);
    --icon-color: var(--warning-color);
}
.quick-action-card.danger {
    --icon-bg: var(--danger-bg, #fef0f0);
    --icon-color: var(--danger-color);
}
.quick-action-card.info {
    --icon-bg: var(--info-bg, #f4f4f5);
    --icon-color: var(--info-color, #909399);
}
</style>
