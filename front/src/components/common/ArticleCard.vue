<template>
  <div
    :class="['article-card', `article-card--${mode}`]"
    :style="{ animationDelay: animationDelay }"
    @click="handleClick"
  >
    <div v-if="showImage && article.cover_image" class="article-cover">
      <img :src="getCoverUrl(article.cover_image)" :alt="article.title" />
      <div class="cover-overlay"></div>
      <div v-if="showTopTag && article.is_top" class="article-badges">
        <el-tag type="danger" size="small" effect="dark" class="top-tag">
          <el-icon><Top /></el-icon>
          置顶
        </el-tag>
      </div>
      <div v-if="showCategory && article.category_name" class="article-category">
        {{ article.category_name }}
      </div>
    </div>

    <div class="article-info">
      <h3 v-if="highlightKeyword" class="article-title" v-html="highlightText(article.title)"></h3>
      <h3 v-else class="article-title">{{ article.title }}</h3>

      <p v-if="showExcerpt" class="article-summary">
        <template v-if="highlightKeyword">
          <span v-html="highlightText(article.summary || '暂无摘要')"></span>
        </template>
        <template v-else>
          {{ article.summary || '暂无摘要' }}
        </template>
      </p>

      <div class="article-footer">
        <div v-if="showAuthor" class="article-author">
          <el-avatar :size="28" :src="getAvatarUrl(article.author_avatar)">
            {{ article.author_name?.charAt(0)?.toUpperCase() }}
          </el-avatar>
          <span>{{ article.author_name }}</span>
        </div>
        <div v-if="showStats" class="article-stats">
          <span><el-icon><View /></el-icon> {{ article.view_count }}</span>
          <span><el-icon><Clock /></el-icon> {{ formatDate(article.created_at) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { View, Clock, Top } from '@element-plus/icons-vue'
import { getCoverUrl, getAvatarUrl, getArticleUrl, formatDate } from '@/utils'

const props = defineProps({
  article: {
    type: Object,
    required: true
  },
  mode: {
    type: String,
    default: 'grid',
    validator: (v) => ['grid', 'horizontal', 'list'].includes(v)
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
  highlightKeyword: {
    type: String,
    default: ''
  },
  index: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['click'])

const router = useRouter()

const animationDelay = computed(() => `${props.index * 0.1}s`)

const highlightText = (text) => {
  if (!text || !props.highlightKeyword) return text
  const regex = new RegExp(`(${props.highlightKeyword})`, 'gi')
  return text.replace(regex, '<mark>$1</mark>')
}

const handleClick = () => {
  const url = getArticleUrl(props.article)
  emit('click', props.article)
  router.push(url)
}
</script>

<style scoped>
.article-card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: all var(--transition-fast);
  border: 1px solid var(--border-light);
  position: relative;
  animation: fadeInUp 0.15s ease-out backwards;
}

.article-card:hover {
  border-color: var(--primary-color);
  box-shadow: var(--shadow-md);
}

.article-card--grid {
  display: block;
}

.article-card--horizontal {
  display: flex;
  gap: 24px;
  padding: 24px;
}

.article-card--list {
  display: flex;
  flex-direction: column;
}

.article-cover {
  position: relative;
  overflow: hidden;
}

.article-card--grid .article-cover {
  height: 200px;
}

.article-card--horizontal .article-cover {
  width: 220px;
  height: 140px;
  flex-shrink: 0;
  border-radius: var(--radius-md);
}

.article-card--list .article-cover {
  height: 180px;
}

.article-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
}

.article-card:hover .article-cover img {
  transform: scale(1.08);
}

.cover-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.3));
  opacity: 0;
  transition: opacity var(--transition-normal);
}

.article-card:hover .cover-overlay {
  opacity: 1;
}

.article-badges {
  position: absolute;
  top: 12px;
  left: 12px;
  z-index: 1;
}

.top-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-weight: 500;
}

.top-tag :deep(.el-tag__content) {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.article-category {
  position: absolute;
  bottom: 12px;
  left: 12px;
  padding: 4px 12px;
  background: var(--primary-color);
  color: #fff;
  font-size: 12px;
  border-radius: var(--radius-sm);
  font-weight: 500;
}

.article-card--horizontal .article-category {
  position: static;
  margin-top: 8px;
}

.article-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.article-card--grid .article-info {
  padding: 20px;
}

.article-card--horizontal .article-info {
  padding: 0;
}

.article-card--list .article-info {
  padding: 16px;
}

.article-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 10px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color var(--transition-fast);
}

.article-card--horizontal .article-title {
  font-size: 18px;
  margin-bottom: 8px;
}

.article-card:hover .article-title {
  color: var(--primary-color);
}

.article-title :deep(mark) {
  background: var(--danger-bg);
  color: var(--danger-color);
  padding: 0 2px;
}

.article-summary {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
  height: 48px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  margin-bottom: 16px;
}

.article-card--horizontal .article-summary {
  height: auto;
  -webkit-line-clamp: 2;
  margin-bottom: 12px;
  flex: 1;
}

.article-summary :deep(mark) {
  background: var(--danger-bg);
  color: var(--danger-color);
  padding: 0 2px;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--border-light);
}

.article-card--horizontal .article-footer {
  border-top: none;
  padding-top: 0;
}

.article-author {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: var(--text-secondary);
}

.article-author .el-avatar {
  border-radius: var(--radius-sm) !important;
  border: 2px solid var(--border-light);
}

.article-stats {
  display: flex;
  gap: 14px;
  font-size: 12px;
  color: var(--text-tertiary);
}

.article-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.article-card--horizontal .article-stats span {
  padding: 4px 10px;
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
}

.article-card--horizontal .article-stats span:hover {
  background: var(--primary-bg);
  color: var(--primary-color);
}

[data-theme="dark"] .article-card--horizontal .article-stats span {
  background: var(--bg-tertiary);
}

@media (max-width: 768px) {
  .article-card--horizontal {
    flex-direction: column;
    padding: 16px;
    gap: 16px;
  }

  .article-card--horizontal .article-cover {
    width: 100%;
    height: 180px;
  }

  .article-title {
    font-size: 15px;
  }

  .article-card--horizontal .article-title {
    font-size: 16px;
  }

  .article-summary {
    font-size: 13px;
    height: auto;
  }

  .article-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .article-author {
    font-size: 12px;
  }

  .article-stats {
    width: 100%;
    justify-content: flex-start;
  }
}

@media (max-width: 576px) {
  .article-card--grid .article-cover {
    height: 140px;
  }

  .article-card--horizontal .article-cover {
    height: 160px;
  }

  .article-info {
    padding: 12px;
  }

  .article-title {
    font-size: 14px;
  }

  .article-badges {
    top: 8px;
    left: 8px;
  }

  .top-tag {
    font-size: 11px;
    padding: 2px 6px !important;
  }

  .article-category {
    font-size: 11px;
    padding: 2px 8px;
  }
}
</style>
