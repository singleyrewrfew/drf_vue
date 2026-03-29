<template>
    <div class="page">
        <PageHeader :title="category?.name || '分类'" />

        <div class="page-content">
            <div v-if="loading" class="feed-list">
                <Skeleton v-for="i in 5" :key="i" type="card-image" />
            </div>

            <template v-else-if="articles.length">
                <div class="feed-list">
                    <ArticleCard v-for="article in articles" :key="article.id" :article="article" />
                </div>
            </template>

            <EmptyState v-else />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getCategory, getContents } from '@/api/content'
import Skeleton from '@/components/Skeleton.vue'
import ArticleCard from '@/components/ArticleCard.vue'
import EmptyState from '@/components/EmptyState.vue'
import PageHeader from '@/components/PageHeader.vue'

const route = useRoute()
const loading = ref(true)
const category = ref(null)
const articles = ref([])

const fetchData = async () => {
    loading.value = true
    try {
        const id = route.params.id_or_slug
        const [categoryRes, articlesRes] = await Promise.all([
            getCategory(id),
            getContents({ category: id, page_size: 20 }),
        ])
        category.value = categoryRes.data
        articles.value = articlesRes.data.results || articlesRes.data
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
}

watch(() => route.params.id_or_slug, fetchData)
onMounted(fetchData)
</script>

<style scoped>
.feed-list {
    background: var(--bg-color);
}
</style>
