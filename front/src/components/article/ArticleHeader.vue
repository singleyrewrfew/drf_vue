<template>
    <header class="article-header">
        <div class="article-category" v-if="article.category_name">
            <el-tag 
                type="success" 
                effect="plain" 
                @click="handleCategoryClick"
                class="category-tag"
            >
                {{ article.category_name }}
            </el-tag>
        </div>
        
        <h1 class="article-title">{{ article.title }}</h1>
        
        <div class="article-meta">
            <div class="author-info">
                <el-avatar 
                    :size="40" 
                    :src="avatarUrl"
                    class="author-avatar"
                >
                    {{ authorInitial }}
                </el-avatar>
                <div class="author-detail">
                    <span class="author-name">{{ article.author_name }}</span>
                    <span class="publish-time">{{ formattedDate }}</span>
                </div>
            </div>
            
            <div class="article-stats">
                <span class="stat-item">
                    <el-icon><View/></el-icon>
                    {{ article.view_count }} 阅读
                </span>
            </div>
        </div>
        
        <div v-if="hasTags" class="article-tags">
            <el-tag
                v-for="tag in article.tags"
                :key="tag.id"
                size="small"
                effect="plain"
                @click="handleTagClick(tag)"
                class="tag-item"
            >
                #{{ tag.name }}
            </el-tag>
        </div>
    </header>
</template>

<script setup>
import { computed } from 'vue'
import { View } from '@element-plus/icons-vue'
import { getAvatarUrl, formatDate } from '@/utils'

const props = defineProps({
    article: {
        type: Object,
        required: true,
        default: () => ({})
    }
})

const emit = defineEmits(['category-click', 'tag-click'])

const avatarUrl = computed(() => getAvatarUrl(props.article.author_avatar))

const authorInitial = computed(() => {
    return props.article.author_name?.charAt(0)?.toUpperCase() || ''
})

const formattedDate = computed(() => formatDate(props.article.created_at))

const hasTags = computed(() => {
    return props.article.tags && props.article.tags.length > 0
})

const handleCategoryClick = () => {
    emit('category-click')
}

const handleTagClick = (tag) => {
    emit('tag-click', tag)
}
</script>

<style scoped>
.article-header {
    margin-bottom: 32px;
}

.article-category {
    margin-bottom: 16px;
}

.category-tag {
    cursor: pointer;
    transition: all var(--transition-fast);
}

.category-tag:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
}

.article-title {
    font-size: 32px;
    font-weight: 700;
    line-height: 1.3;
    color: var(--text-primary);
    margin-bottom: 24px;
    letter-spacing: -0.5px;
}

@media (max-width: 768px) {
    .article-title {
        font-size: 24px;
    }
}

.article-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 0;
    border-top: 1px solid var(--border-light);
    border-bottom: 1px solid var(--border-light);
    margin-bottom: 24px;
}

.author-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.author-avatar {
    border-radius: var(--radius-sm) !important;
    border: 2px solid var(--border-light);
    transition: all var(--transition-fast);
}

.author-avatar:hover {
    box-shadow: 0 0 0 3px var(--primary-bg);
}

.author-detail {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.author-name {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
}

.publish-time {
    font-size: 13px;
    color: var(--text-tertiary);
}

.article-stats {
    display: flex;
    gap: 16px;
}

.stat-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    color: var(--text-secondary);
}

.article-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.tag-item {
    cursor: pointer;
    transition: all var(--transition-fast);
}

.tag-item:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
}

@media (max-width: 576px) {
    .article-meta {
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
    }
    
    .article-stats {
        width: 100%;
    }
}
</style>
