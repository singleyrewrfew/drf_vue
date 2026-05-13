<template>
    <div class="skeleton" :class="[`skeleton--${variant}`, { 'skeleton--animated': animated }]">
        <!-- 表格骨架屏 -->
        <template v-if="variant === 'table'">
            <div class="skeleton-table">
                <div class="skeleton-header">
                    <div v-for="n in columns" :key="`h-${n}`"
                         class="skeleton-cell skeleton-header-cell"
                         :style="{ width: getHeaderWidth(n) }"/>
                </div>
                <div class="skeleton-rows">
                    <div v-for="row in rows" :key="row" class="skeleton-row">
                        <div v-for="col in columns" :key="`${row}-${col}`"
                             class="skeleton-cell skeleton-row-cell"
                             :style="{ width: getCellWidth(col) }"/>
                    </div>
                </div>
            </div>
        </template>

        <!-- 卡片骨架屏（Dashboard 统计卡） -->
        <template v-else-if="variant === 'card'">
            <div class="skeleton-card">
                <div class="skeleton-icon"></div>
                <div class="skeleton-card-content">
                    <div class="skeleton-value"></div>
                    <div class="skeleton-label"></div>
                </div>
            </div>
        </template>

        <!-- 文章/内容骨架屏 -->
        <template v-else-if="variant === 'article'">
            <div class="skeleton-article">
                <div class="skeleton-title"></div>
                <div class="skeleton-meta">
                    <div class="skeleton-meta-item" style="width: 100px;"></div>
                    <div class="skeleton-meta-item" style="width: 80px;"></div>
                    <div class="skeleton-meta-item" style="width: 120px;"></div>
                </div>
                <div class="skeleton-lines">
                    <div v-for="n in 5" :key="n" class="skeleton-line" :class="{ 'skeleton-line--short': n === 3 }"></div>
                </div>
            </div>
        </template>

        <!-- 列表骨架屏 -->
        <template v-else-if="variant === 'list'">
            <div class="skeleton-list">
                <div v-for="item in items" :key="item" class="skeleton-list-item">
                    <div class="skeleton-avatar"></div>
                    <div class="skeleton-list-content">
                        <div class="skeleton-list-title"></div>
                        <div class="skeleton-list-desc"></div>
                    </div>
                </div>
            </div>
        </template>

        <!-- 默认通用骨架屏 -->
        <template v-else>
            <div class="skeleton-generic">
                <div class="skeleton-line" style="width: 60%; margin-bottom: 12px;"></div>
                <div class="skeleton-line" style="width: 80%; margin-bottom: 12px;"></div>
                <div class="skeleton-line" style="width: 45%;"></div>
            </div>
        </template>
    </div>
</template>

<script setup>
const props = defineProps({
    /** 骨架屏变体 */
    variant: {
        type: String,
        default: 'generic',
        validator: (v) => ['table', 'card', 'article', 'list', 'generic'].includes(v)
    },
    /** 是否启用动画 */
    animated: {
        type: Boolean,
        default: true
    },
    /** 表格列数（仅 table 变体） */
    columns: {
        type: Number,
        default: 4
    },
    /** 表格行数（仅 table 变体） */
    rows: {
        type: Number,
        default: 5
    },
    /** 列表项数（仅 list 变体） */
    items: {
        type: Number,
        default: 3
    }
})

/** 动态生成表头宽度 */
const getHeaderWidth = (index) => {
    const widths = ['30%', '20%', '15%', '20%', '15%']
    return widths[index - 1] || '20%'
}

/** 动态生成单元格宽度 */
const getCellWidth = (index) => {
    const widths = ['40%', '20%', '15%', '25%']
    return widths[index - 1] || '25%'
}
</script>

<style scoped>
/* ================================================================
   Skeleton Loading — 专业骨架屏组件
   设计标准：Shimmer 效果 + 物理光影模拟
   ================================================================ */

.skeleton {
    --skeleton-bg: var(--bg-secondary, #f5f5f5);
    --skeleton-shine: rgba(255, 255, 255, 0.4);
    --radius-sm: 4px;
    --radius-md: 6px;
    --radius-lg: 8px;
}

/* ---- Shimmer 动画（物理光影效果） ---- */
.skeleton--animated .skeleton-cell,
.skeleton--animated .skeleton-icon,
.skeleton--animated .skeleton-value,
.skeleton--animated .skeleton-label,
.skeleton--animated .skeleton-avatar,
.skeleton--animated .skeleton-title,
.skeleton--animated .skeleton-meta-item,
.skeleton--animated .skeleton-line,
.skeleton--animated .skeleton-list-title,
.skeleton--animated .skeleton-list-desc {
    background: linear-gradient(
        90deg,
        var(--skeleton-bg) 0%,
        #e8e8e8 50%,
        var(--skeleton-bg) 100%
    );
    background-size: 200% 100%;
    animation: shimmer 1.5s ease-in-out infinite;
}

@keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

/* 暗色模式适配 */
[data-theme="dark"] .skeleton {
    --skeleton-bg: #2d2d2d;
    --skeleton-shine: rgba(255, 255, 255, 0.05);
}

[data-theme="dark"] .skeleton--animated .skeleton-cell,
[data-theme="dark"] .skeleton--animated .skeleton-icon,
[data-theme="dark"] .skeleton--animated .skeleton-value,
[data-theme="dark"] .skeleton--animated .skeleton-label,
[data-theme="dark"] .skeleton--animated .skeleton-avatar,
[data-theme="dark"] .skeleton--animated .skeleton-title,
[data-theme="dark"] .skeleton--animated .skeleton-meta-item,
[data-theme="dark"] .skeleton--animated .skeleton-line,
[data-theme="dark"] .skeleton--animated .skeleton-list-title,
[data-theme="dark"] .skeleton--animated .skeleton-list-desc {
    background: linear-gradient(
        90deg,
        var(--skeleton-bg) 0%,
        #383838 50%,
        var(--skeleton-bg) 100%
    );
    background-size: 200% 100%;
}

/* ================================================================
   表格骨架屏
   ================================================================ */

.skeleton-table {
    width: 100%;
}

.skeleton-header {
    display: flex;
    gap: 12px;
    padding: 12px 16px;
    border-bottom: 1px solid var(--border-light);
    margin-bottom: 8px;
}

.skeleton-header-cell {
    height: 14px;
    border-radius: var(--radius-sm);
}

.skeleton-rows {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 0 16px 16px;
}

.skeleton-row {
    display: flex;
    gap: 12px;
    align-items: center;
    padding: 16px 0;
    border-bottom: 1px solid var(--border-light);
}

.skeleton-row:last-child {
    border-bottom: none;
}

.skeleton-row-cell {
    height: 14px;
    border-radius: var(--radius-sm);
}

/* ================================================================
   卡片骨架屏（Dashboard 统计卡）
   ================================================================ */

.skeleton-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px;
    border-radius: var(--radius-md);
    background: var(--card-bg);
    border: 1px solid var(--border-color);
}

.skeleton-icon {
    width: 48px;
    height: 48px;
    border-radius: var(--radius-sm);
    flex-shrink: 0;
}

.skeleton-card-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.skeleton-value {
    height: 32px;
    width: 40%;
    border-radius: var(--radius-sm);
}

.skeleton-label {
    height: 13px;
    width: 35%;
    border-radius: var(--radius-sm);
}

/* ================================================================
   文章/内容骨架屏
   ================================================================ */

.skeleton-article {
    padding: 24px;
}

.skeleton-title {
    height: 28px;
    width: 55%;
    border-radius: var(--radius-md);
    margin-bottom: 16px;
}

.skeleton-meta {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
}

.skeleton-meta-item {
    height: 12px;
    border-radius: var(--radius-sm);
}

.skeleton-lines {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.skeleton-line {
    height: 14px;
    border-radius: var(--radius-sm);
}

.skeleton-line--short {
    width: 65% !important;
}

/* ================================================================
   列表骨架屏
   ================================================================ */

.skeleton-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.skeleton-list-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border-radius: var(--radius-md);
    background: var(--card-bg);
    border: 1px solid var(--border-color);
}

.skeleton-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    flex-shrink: 0;
}

.skeleton-list-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.skeleton-list-title {
    height: 15px;
    width: 45%;
    border-radius: var(--radius-sm);
}

.skeleton-list-desc {
    height: 12px;
    width: 70%;
    border-radius: var(--radius-sm);
}

/* ================================================================
   通用骨架屏（默认）
   ================================================================ */

.skeleton-generic {
    padding: 16px;
}
</style>
