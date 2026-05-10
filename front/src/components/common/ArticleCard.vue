<template>
  <div
    :class="['article-card', `article-card--${mode}`]"
    :style="{ animationDelay: animationDelay }"
    @click="handleClick"
  >
    <div v-if="showImage && article.cover_image" class="article-cover">
      <img
        :src="getCoverUrl(article.cover_image)"
        :alt="article.title"
        loading="lazy"
        decoding="async"
      />
      <div class="cover-overlay"></div>
      <div v-if="showTopTag && article.is_top" class="article-badges">
        <span class="top-tag">
          置顶
        </span>
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
          <span><el-icon><Calendar /></el-icon> {{ formatDate(article.created_at) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { Calendar, View } from '@element-plus/icons-vue'
import { getCoverUrl, getAvatarUrl, getArticleUrl, formatDate } from '@/utils'

const props = defineProps({
  article: {
    type: Object,
    required: true
  },
  mode: {
    type: String,
    default: 'grid',
    validator: v => ['grid', 'horizontal', 'list'].includes(v)
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

const animationDelay = computed(() => `${props.index * 0.12}s`)

const highlightText = text => {
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
/* ====== 卡片容器 (宣纸书卷风格) ====== */
.article-card {
  background: var(--paper-cream, #ede8dc);
  border-radius: var(--radius-sm);
  overflow: hidden;
  cursor: pointer;
  transition: all var(--transition-normal);
  border: 1px solid var(--paper-aged, #ddd6c8);
  position: relative;
  box-shadow:
    0 2px 4px rgba(26, 26, 26, 0.04),
    0 4px 8px rgba(26, 26, 26, 0.02);
}

.article-card:hover {
  border-color: var(--ink-medium, #595959);
  box-shadow:
    0 4px 8px rgba(26, 26, 26, 0.08),
    0 8px 16px rgba(26, 26, 26, 0.04);
}

/* ====== 布局模式 ====== */
.article-card--grid {
  display: block;
}

.article-card--horizontal {
  display: flex;
  gap: 20px;
  padding: 20px;
}

.article-card--list {
  display: flex;
  flex-direction: column;
}

/* ====== 封面图区域 (水墨边框) ====== */
.article-cover {
  position: relative;
  overflow: hidden;
  border-bottom: 1px solid var(--paper-aged, #ddd6c8);
}

.article-card--grid .article-cover {
  height: 200px;
}

.article-card--horizontal .article-cover {
  width: 220px;
  height: 140px;
  flex-shrink: 0;
  border-radius: var(--radius-xs);
  border: 1px solid var(--paper-aged, #ddd6c8);
  border-bottom: none;
}

.article-card--list .article-cover {
  height: 180px;
}

.article-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
  filter: sepia(0.05) contrast(1.05);
}

.article-card:hover .article-cover img {
  transform: scale(1.03);
  filter: sepia(0.08) contrast(1.08);
}

.cover-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(
    transparent,
    rgba(45, 90, 74, 0.15)
  );
  opacity: 0;
  transition: opacity var(--transition-normal);
}

.article-card:hover .cover-overlay {
  opacity: 1;
}

/* ====== 徽章/标签 (印章风格) ====== */
.article-badges {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 1;
}

.top-tag {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  background: var(--vermilion-color, #c53d43);
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  font-family: 'SimSun', serif;
  letter-spacing: 0.05em;
  border-radius: var(--radius-xs);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.2),
    1px 1px 4px rgba(197, 61, 67, 0.25);
}

.article-category {
  position: absolute;
  bottom: 10px;
  left: 10px;
  padding: 3px 10px;
  background: var(--vermilion-color, #c53d43);
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  font-family: 'SimSun', serif;
  letter-spacing: 0.03em;
  border-radius: var(--radius-xs);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.2),
    1px 1px 4px rgba(197, 61, 67, 0.25);
}

.article-card--horizontal .article-category {
  position: static;
  margin-top: 8px;
  display: inline-block;
}

/* ====== 信息区域 ====== */
.article-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.article-card--grid .article-info {
  padding: 18px;
}

.article-card--horizontal .article-info {
  padding: 0;
}

.article-card--list .article-info {
  padding: 14px;
}

/* ====== 标题 (楷体墨黑) ====== */
.article-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--ink-black, #1a1a1a);
  margin-bottom: 10px;
  line-height: 1.7;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color var(--transition-fast);
  font-family: "KaiTi", "STKaiti", "楷体", "Noto Serif SC", serif;
  letter-spacing: 0.03em;
}

.article-card--horizontal .article-title {
  font-size: 18px;
  margin-bottom: 8px;
}

.article-card:hover .article-title {
  color: var(--primary-color, #2d5a4a);
}

.article-title :deep(mark) {
  background: var(--vermilion-light, #fce4e4);
  color: var(--vermilion-color, #c53d43);
  padding: 0 2px;
  border-radius: 1px;
}

/* ====== 摘要 (楷体中墨) ====== */
.article-summary {
  font-size: 14px;
  color: var(--ink-medium, #595959);
  line-height: 1.9;
  height: 52px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  margin-bottom: 14px;
  font-family: "KaiTi", "STKaiti", "楷体", "Noto Serif SC", serif;
  letter-spacing: 0.02em;
}

.article-card--horizontal .article-summary {
  height: auto;
  -webkit-line-clamp: 2;
  margin-bottom: 12px;
  flex: 1;
}

.article-summary :deep(mark) {
  background: var(--vermilion-light, #fce4e4);
  color: var(--vermilion-color, #c53d43);
  padding: 0 2px;
  border-radius: 1px;
}

/* ====== 底部信息栏 (淡墨风格) ====== */
.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--paper-aged, #ddd6c8);
  margin-top: auto;
}

.article-card--horizontal .article-footer {
  border-top: none;
  padding-top: 0;
}

.article-author {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--ink-medium, #595959);
  font-family: "KaiTi", "STKaiti", "楷体", serif;
}

.article-author .el-avatar {
  border-radius: var(--radius-xs) !important;
  border: 1px solid var(--paper-aged, #ddd6c8) !important;
  font-family: 'SimSun', serif;
  background: var(--bg-secondary, #ede8dc) !important;
  color: var(--text-primary) !important;
}

.article-stats {
  display: flex;
  gap: 12px;
  font-size: 11px;
  color: var(--ink-light, #8c8c8c);
  font-family: "KaiTi", "STKaiti", "楷体", serif;
}

.article-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.article-stats .el-icon {
  font-size: 14px;
  opacity: 0.7;
}

.article-card--horizontal .article-stats span {
  padding: 3px 8px;
  background: var(--bg-primary, #f5f2eb);
  border-radius: var(--radius-xs);
  border: 1px solid var(--paper-aged, #ddd6c8);
  transition: all var(--transition-fast);
}

.article-card--horizontal .article-stats span:hover {
  background: var(--primary-light, #e8f0ec);
  color: var(--primary-color, #2d5a4a);
  border-color: var(--primary-color, #2d5a4a);
}

[data-theme='dark'] .article-card {
  background: var(--card-bg, #1a1814);
  border-color: var(--border-color, #3d3830);
}

[data-theme='dark'] .article-card:hover {
  border-color: #5c5649;
}

[data-theme='dark'] .article-cover {
  border-bottom-color: var(--border-color, #3d3830);
}

[data-theme='dark'] .article-title {
  color: var(--text-primary, #e8e4d9);
}

[data-theme='dark'] .article-summary {
  color: var(--text-secondary, #c4beb0);
}

[data-theme='dark'] .article-author {
  color: var(--text-secondary, #c4beb0);
}

[data-theme='dark'] .article-stats {
  color: var(--text-tertiary, #8c8578);
}

[data-theme='dark'] .article-footer {
  border-top-color: var(--border-color, #3d3830);
}

[data-theme='dark'] .article-card--horizontal .article-stats span {
  background: var(--bg-tertiary, #252219);
  border-color: var(--border-color, #3d3830);
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
    font-size: 10px;
    padding: 2px 8px;
  }

  .article-category {
    font-size: 10px;
    padding: 2px 8px;
  }
}
</style>
