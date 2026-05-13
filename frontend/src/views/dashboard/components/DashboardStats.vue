<template>
    <div class="dashboard-stats">
        <!-- 管理员视图：均衡式 Bento Grid -->
        <template v-if="isAdmin">
            <div class="stats-grid admin-grid">
                <!-- 主指标卡片 -->
                <div class="stat-item stat-item--contents stagger-reveal--slide delay-0">
                    <StatCard :value="stats.contents" label="内容总数" type="primary" icon="Document" clickable size="large" :animated="true">
                        <template #footer>
                            <div class="footer-stats">
                                <span>已发布 <strong>{{ stats.published }}</strong></span>
                                <span>草稿 <strong>{{ stats.drafts }}</strong></span>
                            </div>
                        </template>
                    </StatCard>
                </div>

                <!-- 评论数 -->
                <div class="stat-item stat-item--comments stagger-reveal--slide delay-1">
                    <StatCard :value="stats.comments" label="评论数" type="success" icon="ChatDotRound" size="normal" :animated="true">
                        <template #footer>互动数据</template>
                    </StatCard>
                </div>

                <!-- 用户数 -->
                <div class="stat-item stat-item--users stagger-reveal--slide delay-2">
                    <StatCard :value="stats.users" label="用户数" type="warning" icon="User" size="normal" :animated="true">
                        <template #footer>注册用户</template>
                    </StatCard>
                </div>

                <!-- 全宽数据流：总浏览量 -->
                <div class="stat-item stat-item--views stagger-reveal--scale delay-3">
                    <StatCard :value="formatNumber(stats.views)" label="总浏览量" type="danger" icon="View" size="wide" :animated="true">
                        <template #footer>累计访问量</template>
                    </StatCard>
                </div>
            </div>
        </template>

        <!-- 普通用户视图：简化版 -->
        <template v-else>
            <div class="stats-grid user-grid">
                <div class="stat-item stat-item--my-contents stagger-reveal--slide delay-0">
                    <StatCard :value="stats.my_contents || 0" label="我的内容" type="primary" icon="Document" clickable size="large" :animated="true">
                        <template #footer>
                            <div class="footer-stats">
                                <span>已发布 <strong>{{ stats.my_published || 0 }}</strong></span>
                                <span>草稿 <strong>{{ stats.my_drafts || 0 }}</strong></span>
                            </div>
                        </template>
                    </StatCard>
                </div>

                <div class="stat-item stat-item--my-views stagger-reveal--slide delay-1">
                    <StatCard :value="formatNumber(stats.my_views || 0)" label="浏览量" type="success" icon="View" size="normal" :animated="true">
                        <template #footer>累计访问</template>
                    </StatCard>
                </div>

                <div class="stat-item stat-item--my-comments stagger-reveal--slide delay-2">
                    <StatCard :value="stats.my_comments || 0" label="评论" type="warning" icon="ChatDotRound" size="normal" :animated="true">
                        <template #footer>互动数据</template>
                    </StatCard>
                </div>
            </div>
        </template>
    </div>
</template>

<script setup>
import {computed} from 'vue'
import {useUserStore} from '@/stores/user'
import StatCard from '@/components/StatCard.vue'

const props = defineProps({
    stats: {
        type: Object,
        required: true
    }
})

const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin())

const formatNumber = (num) => {
    if (num >= 10000) return (num / 10000).toFixed(1) + 'w'
    if (num >= 1000) return (num / 1000).toFixed(1) + 'k'
    return num
}
</script>

<style scoped>
/* ================================================================
   Dashboard Stats — 均衡式网格布局（语义化类名版）
   设计理念：视觉节奏 + 黄金比例 + 层次分明
   ================================================================ */

.dashboard-stats {
    margin-bottom: 24px;
}

.stats-grid {
    display: grid;
    gap: 20px;
    align-items: stretch;
}

/* ---- 管理员布局（3列 + 全宽底部） ---- */
.admin-grid {
    grid-template-columns: 5fr 3fr 3fr; /* 接近黄金分割比例 */
    grid-template-rows: auto auto;
}

/* 语义化类名定位 - 管理员视图 */
.admin-grid .stat-item--contents { grid-column: 1 / 2; grid-row: 1 / 2; }
.admin-grid .stat-item--comments { grid-column: 2 / 3; grid-row: 1 / 2; }
.admin-grid .stat-item--users { grid-column: 3 / 4; grid-row: 1 / 2; }
.admin-grid .stat-item--views { grid-column: 1 / -1; grid-row: 2 / 3; }

/* ---- 用户布局（简化版） ---- */
.user-grid {
    grid-template-columns: 5fr 3fr 3fr;
}

/* 语义化类名定位 - 用户视图 */
.user-grid .stat-item--my-contents { grid-column: 1 / 2; }
.user-grid .stat-item--my-views { grid-column: 2 / 3; }
.user-grid .stat-item--my-comments { grid-column: 3 / 4; }

/* ---- 底部统计数据样式 ---- */
.footer-stats {
    display: flex;
    gap: 16px;
    font-size: 12px;
    color: var(--text-secondary);
}

.footer-stats strong {
    color: var(--text-primary);
    font-weight: 600;
    margin-left: 4px;
}

/* ================================================================
   动画延迟工具类
   ================================================================ */

.delay-0 { --stagger-delay: 0ms; }
.delay-1 { --stagger-delay: 100ms; }
.delay-2 { --stagger-delay: 200ms; }
.delay-3 { --stagger-delay: 300ms; }
.delay-4 { --stagger-delay: 400ms; }
.delay-5 { --stagger-delay: 500ms; }

/* ================================================================
   响应式断点（渐进式降级）
   ================================================================ */

/* 大屏优化（≥1400px）*/
@media (min-width: 1400px) {
    .admin-grid {
        gap: 24px;
    }
}

/* 中等屏幕（平板/笔记本 1024-1399px）*/
@media (max-width: 1399px) and (min-width: 1024px) {
    .admin-grid,
    .user-grid {
        grid-template-columns: 1.5fr 1fr 1fr;
        gap: 16px;
    }
}

/* 小屏平板/大手机（768-1023px）*/
@media (max-width: 1023px) and (min-width: 769px) {
    .admin-grid,
    .user-grid {
        grid-template-columns: 1fr 1fr;
        grid-template-rows: auto auto auto auto;
        gap: 14px;
    }

    /* 管理员视图响应式 */
    .admin-grid .stat-item--contents { grid-column: 1 / -1; grid-row: 1 / 2; }
    .admin-grid .stat-item--comments { grid-column: 1 / 2; grid-row: 2 / 3; }
    .admin-grid .stat-item--users { grid-column: 2 / 3; grid-row: 2 / 3; }
    .admin-grid .stat-item--views { grid-column: 1 / -1; grid-row: 3 / 4; }

    /* 用户视图响应式 */
    .user-grid .stat-item--my-contents { grid-column: 1 / -1; }
    .user-grid .stat-item--my-views { grid-column: 1 / 2; }
    .user-grid .stat-item--my-comments { grid-column: 2 / 3; }
}

/* 手机竖屏（<768px）*/
@media (max-width: 768px) {
    .dashboard-stats {
        margin-bottom: 16px;
    }

    .admin-grid,
    .user-grid {
        grid-template-columns: 1fr;
        grid-template-rows: auto;
        gap: 12px;
    }

    .stat-item {
        grid-column: 1 !important;
        grid-row: auto !important;
        min-width: 0;
    }

    .footer-stats {
        flex-direction: column;
        gap: 4px;
        align-items: flex-start;
    }
}

/* 超小屏（<480px）*/
@media (max-width: 480px) {
    .admin-grid,
    .user-grid {
        gap: 10px;
    }
}
</style>
