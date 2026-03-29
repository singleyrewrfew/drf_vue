<template>
    <div class="article-header">
        <h1 class="article-title">{{ article.title }}</h1>

        <div class="article-author">
            <el-avatar :size="40" :src="getAvatarUrl(article.author_avatar)">
                {{ article.author_name?.charAt(0) }}
            </el-avatar>
            <div class="author-info">
                <span class="author-name">{{ article.author_name || '匿名用户' }}</span>
                <span class="article-time">{{ formatRelativeTime(article.created_at) }}</span>
            </div>
        </div>
    </div>

    <div v-if="article.cover_image" class="article-cover">
        <img :src="getCoverUrl(article.cover_image)" alt="" loading="lazy"/>
    </div>
</template>

<script setup>
import { getCoverUrl, getAvatarUrl, formatRelativeTime } from '@/utils'

const props = defineProps({
    article: {
        type: Object,
        required: true
    }
})

console.log('ArticleHeader received article:', props.article)
</script>

<style scoped>
.article-header {
    padding: 16px;
    padding-bottom: 0;
}

.article-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.5;
    margin: 0 0 16px;
}

.article-author {
    display: flex;
    align-items: center;
    gap: 12px;
}

.author-info {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.author-name {
    font-size: 15px;
    font-weight: 500;
    color: var(--text-primary);
}

.article-time {
    font-size: 12px;
    color: var(--text-tertiary);
    margin-top: 2px;
}

.article-cover {
    margin: 16px;
    border-radius: var(--radius-md);
    overflow: hidden;
}

.article-cover img {
    width: 100%;
    display: block;
    aspect-ratio: 16/9;
    object-fit: cover;
}
</style>
