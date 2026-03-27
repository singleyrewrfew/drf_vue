<template>
    <router-link
        :to="`/article/${article.slug || article.id}`"
        class="feed-card"
    >
        <div class="feed-header">
            <span class="feed-author-name">{{ article.author_name || '匿名用户' }}</span>
            <span class="feed-dot">·</span>
            <span class="feed-time">{{ formatRelativeTime(article.created_at) }}</span>
            <span v-if="article.category_name" class="feed-category">{{ article.category_name }}</span>
        </div>

        <div class="feed-body">
            <div class="feed-content">
                <h3 class="feed-title">{{ article.title }}</h3>
                <p v-if="showExcerpt && (article.summary || article.content)" class="feed-excerpt">
                    {{ truncateText(article.summary || article.content, excerptLength) }}
                </p>
            </div>
            <img
                v-if="showImage && article.cover_image"
                :src="getCoverUrl(article.cover_image)"
                class="feed-image"
                loading="lazy"
            />
        </div>

        <div v-if="showStats" class="feed-footer">
      <span v-if="article.views_count" class="feed-stat">
        <el-icon><View/></el-icon>
        {{ article.views_count }}
      </span>
            <span v-if="article.comments_count" class="feed-stat">
        <el-icon><ChatDotRound/></el-icon>
        {{ article.comments_count }}
      </span>
            <span v-if="article.likes_count" class="feed-stat">
        <el-icon><Star/></el-icon>
        {{ article.likes_count }}
      </span>
        </div>
    </router-link>
</template>

<script setup>
import {View, ChatDotRound, Star} from '@element-plus/icons-vue'
import {getCoverUrl, truncateText, formatRelativeTime} from '@/utils'

defineProps({
    article: {type: Object, required: true},
    showExcerpt: {type: Boolean, default: true},
    showImage: {type: Boolean, default: true},
    showStats: {type: Boolean, default: true},
    excerptLength: {type: Number, default: 100}
})
</script>

<style scoped>
.feed-card {
    display: block;
    text-decoration: none;
    background: var(--card-bg);
    margin-bottom: 10px;
    border-radius: var(--radius-md);
    overflow: hidden;
}

.feed-header {
    display: flex;
    align-items: center;
    padding: 12px 16px 8px;
    font-size: 12px;
    color: var(--text-tertiary);
}

.feed-author-name {
    color: var(--text-secondary);
    font-weight: 500;
}

.feed-dot {
    margin: 0 4px;
}

.feed-category {
    margin-left: auto;
    color: var(--primary-color);
    background: var(--primary-bg);
    padding: 2px 8px;
    border-radius: var(--radius-full);
    font-size: 11px;
}

.feed-body {
    display: flex;
    padding: 0 16px 12px;
    gap: 12px;
}

.feed-content {
    flex: 1;
    min-width: 0;
}

.feed-title {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.5;
    margin-bottom: 8px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.feed-excerpt {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.6;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    margin: 0;
}

.feed-image {
    width: 100px;
    height: 75px;
    object-fit: cover;
    border-radius: var(--radius-sm);
    flex-shrink: 0;
}

.feed-footer {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 0 16px 12px;
    font-size: 12px;
    color: var(--text-tertiary);
}

.feed-stat {
    display: flex;
    align-items: center;
    gap: 4px;
}

.feed-stat .el-icon {
    font-size: 14px;
}
</style>
