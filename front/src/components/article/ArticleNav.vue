<template>
    <nav v-if="hasNav" class="article-nav">
        <router-link 
            v-if="prevArticle" 
            :to="getArticleUrl(prevArticle)"
            class="nav-item prev"
        >
            <div class="nav-content">
                <span class="nav-label">
                    <el-icon><ArrowLeft/></el-icon>
                    上一篇
                </span>
                <h4 class="nav-title">{{ prevArticle.title }}</h4>
            </div>
        </router-link>
        
        <router-link 
            v-if="nextArticle" 
            :to="getArticleUrl(nextArticle)"
            class="nav-item next"
        >
            <div class="nav-content">
                <span class="nav-label">
                    下一篇
                    <el-icon><ArrowRight/></el-icon>
                </span>
                <h4 class="nav-title">{{ nextArticle.title }}</h4>
            </div>
        </router-link>
    </nav>
</template>

<script setup>
import { computed } from 'vue'
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import { getArticleUrl } from '@/utils'

const props = defineProps({
    prevArticle: {
        type: Object,
        default: null
    },
    nextArticle: {
        type: Object,
        default: null
    }
})

const hasNav = computed(() => {
    return props.prevArticle || props.nextArticle
})
</script>

<style scoped>
.article-nav {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin: 48px 0;
    padding: 24px 0;
    border-top: 1px solid var(--border-light);
}

.nav-item {
    display: block;
    padding: 20px;
    background: var(--card-bg);
    border-radius: var(--radius-lg);
    border: 1px solid var(--border-light);
    transition: all var(--transition-fast);
    text-decoration: none;
}

.nav-item:hover {
    border-color: rgba(0, 120, 212, 0.3);
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}

.nav-content {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.nav-label {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: var(--text-tertiary);
    font-weight: 500;
}

.nav-label .el-icon {
    font-size: 14px;
}

.nav-item.prev .nav-label {
    justify-content: flex-start;
}

.nav-item.next .nav-label {
    justify-content: flex-end;
}

.nav-title {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.4;
    margin: 0;
    transition: color var(--transition-fast);
    
    /* 限制显示两行 */
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.nav-item:hover .nav-title {
    color: var(--primary-color);
}

@media (max-width: 768px) {
    .article-nav {
        grid-template-columns: 1fr;
        margin: 32px 0;
        padding: 16px 0;
    }
    
    .nav-item {
        padding: 16px;
    }
}
</style>
