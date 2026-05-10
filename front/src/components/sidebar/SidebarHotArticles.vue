<template>
  <SidebarContainer title="热门文章">
    <div class="hot-list">
      <div
        v-for="(article, index) in displayArticles"
        :key="article.id"
        class="hot-item"
        @click="handleClick(article)"
      >
        <div class="hot-info">
          <el-tooltip :content="article.title" placement="top" :show-after="300">
            <div class="scrolling-wrapper">
              <h4 class="scrolling-title">{{ article.title }}</h4>
              <h4 class="scrolling-title" aria-hidden="true">{{ article.title }}</h4>
            </div>
          </el-tooltip>
        </div>
      </div>
    </div>
  </SidebarContainer>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import SidebarContainer from './SidebarContainer.vue'
import { getArticleUrl } from '@/utils'

const props = defineProps({
  articles: {
    type: Array,
    default: () => []
  },
  maxItems: {
    type: Number,
    default: 8
  }
})

const router = useRouter()

const displayArticles = computed(() => {
  return props.articles.slice(0, props.maxItems)
})

const handleClick = article => {
  router.push(getArticleUrl(article))
}
</script>

<style scoped>
.hot-list {
  display: flex;
  flex-direction: column;
}

.hot-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 10px;
  border-bottom: 1px solid var(--paper-aged, #ddd6c8);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.hot-item:last-child {
  border-bottom: none;
}

.hot-item:hover {
  background: rgba(45, 90, 74, 0.06);
  color: var(--primary-color, #2d5a4a);
  border-radius: var(--radius-xs);
}

.hot-info {
  flex: 1;
  min-width: 0;
  overflow: hidden;
}

.scrolling-wrapper {
  display: flex;
  width: max-content;
  animation: scroll-left 15s linear infinite;
}

.scrolling-wrapper:hover {
  animation-play-state: paused;
}

.scrolling-title {
  font-size: 13px;
  color: var(--ink-medium, #595959);
  line-height: 1.6;
  margin: 0;
  white-space: nowrap;
  padding-right: 50px;
  transition: color var(--transition-fast);
  font-family: "KaiTi", "STKaiti", "楷体", "Noto Serif SC", serif;
  letter-spacing: var(--tracking-normal, 0.03em);
}

.hot-item:hover .scrolling-title {
  color: var(--primary-color, #2d5a4a);
}

@keyframes scroll-left {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}

[data-theme='dark'] .hot-item {
  border-bottom-color: var(--border-color, #3d3830);
}

[data-theme='dark'] .hot-item:hover {
  background: rgba(74, 157, 130, 0.08);
  color: var(--primary-color, #4a9d82);
}

[data-theme='dark'] .scrolling-title {
  color: var(--text-secondary, #c4beb0);
}
</style>