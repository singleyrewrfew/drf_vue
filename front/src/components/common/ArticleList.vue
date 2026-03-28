<template>
  <div class="article-list">
    <template v-if="loading">
      <SkeletonCard
        v-for="i in pageSize"
        :key="'skeleton-' + i"
        :mode="mode"
        :show-excerpt="showExcerpt"
      />
    </template>
    <template v-else-if="articles.length > 0">
      <ArticleCard
        v-for="(article, index) in articles"
        :key="article.id"
        :article="article"
        :mode="mode"
        :index="index"
        :show-image="showImage"
        :show-excerpt="showExcerpt"
        :show-author="showAuthor"
        :show-stats="showStats"
        :show-category="showCategory"
        :show-top-tag="showTopTag"
        :highlight-keyword="highlightKeyword"
        @click="handleClick"
      />
    </template>
    <template v-else>
      <EmptyState :text="emptyText" :hint="emptyHint">
        <slot name="empty-action"></slot>
      </EmptyState>
    </template>
  </div>
</template>

<script setup>
import ArticleCard from './ArticleCard.vue'
import SkeletonCard from './SkeletonCard.vue'
import EmptyState from './EmptyState.vue'

const props = defineProps({
  articles: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  mode: {
    type: String,
    default: 'grid'
  },
  pageSize: {
    type: Number,
    default: 4
  },
  showImage: {
    type: Boolean,
    default: true
  },
  showExcerpt: {
    type: Boolean,
    default: true
  },
  showAuthor: {
    type: Boolean,
    default: true
  },
  showStats: {
    type: Boolean,
    default: true
  },
  showCategory: {
    type: Boolean,
    default: true
  },
  showTopTag: {
    type: Boolean,
    default: true
  },
  emptyText: {
    type: String,
    default: '暂无文章'
  },
  emptyHint: {
    type: String,
    default: ''
  },
  highlightKeyword: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['article-click'])

const handleClick = (article) => {
  emit('article-click', article)
}
</script>

<style scoped>
.article-list {
  display: grid;
  gap: 24px;
}

.article-list:has(.skeleton-card),
.article-list:has(.empty-state) {
  display: flex;
  flex-direction: column;
}

.article-list:has(.article-card--grid) {
  grid-template-columns: repeat(2, 1fr);
}

.article-list:has(.article-card--horizontal),
.article-list:has(.article-card--list) {
  display: flex;
  flex-direction: column;
}

@media (max-width: 1200px) {
  .article-list:has(.article-card--grid) {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .article-list {
    gap: 16px;
  }
}
</style>
