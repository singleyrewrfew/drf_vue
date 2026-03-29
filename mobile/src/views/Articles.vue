<template>
    <div class="page">
        <PageHeader title="发现">
            <template #right>
                <button class="btn-icon" @click="$router.push('/search')">
                    <el-icon>
                        <Search />
                    </el-icon>
                </button>
            </template>
        </PageHeader>

        <div class="page-content">
            <div v-if="loading && !articles.length" class="feed-list">
                <Skeleton v-for="i in 5" :key="i" type="card-image" />
            </div>

            <template v-else-if="articles.length">
                <div class="feed-list">
                    <ArticleCard v-for="article in articles" :key="article.id" :article="article" />
                </div>

                <div v-if="hasMore" class="loading-more">
                    <template v-if="loadingMore">
                        <el-icon class="loading-icon">
                            <Loading />
                        </el-icon>
                        <span>加载中...</span>
                    </template>
                    <button v-else class="btn btn-secondary btn-block" @click="loadMore">
                        加载更多
                    </button>
                </div>
            </template>

            <EmptyState v-else />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, Loading } from '@element-plus/icons-vue'
import { getContents } from '@/api/content'
import Skeleton from '@/components/Skeleton.vue'
import ArticleCard from '@/components/ArticleCard.vue'
import EmptyState from '@/components/EmptyState.vue'
import PageHeader from '@/components/PageHeader.vue'

const loading = ref(true)
const loadingMore = ref(false)
const articles = ref([])
const page = ref(1)
const hasMore = ref(true)

const fetchArticles = async (isLoadMore = false) => {
    if (isLoadMore) loadingMore.value = true
    else loading.value = true

    try {
        const { data } = await getContents({ page: page.value, page_size: 10 })
        const results = data.results || data
        articles.value = isLoadMore ? [...articles.value, ...results] : results
        hasMore.value = data.next || results.length >= 10
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
        loadingMore.value = false
    }
}

const loadMore = () => {
    page.value++
    fetchArticles(true)
}

onMounted(() => fetchArticles())
</script>

<style scoped>
.feed-list {
    background: var(--bg-color);
}

.loading-more {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    color: var(--text-tertiary);
    font-size: 13px;
}

.loading-icon {
    animation: spin 1s linear infinite;
    margin-right: 8px;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}
</style>
