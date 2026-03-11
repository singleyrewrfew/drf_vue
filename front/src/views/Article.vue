<template>
  <div class="article-page">
    <div class="container">
      <el-row :gutter="24">
        <el-col :span="17">
          <div class="article-main" v-loading="loading">
            <article class="article">
              <header class="article-header">
                <div class="article-category" v-if="article.category_name">
                  <el-tag type="primary" effect="plain">{{ article.category_name }}</el-tag>
                </div>
                <h1>{{ article.title }}</h1>
                <div class="article-meta">
                  <div class="author-info">
                    <el-avatar :size="40">{{ article.author_name?.charAt(0) }}</el-avatar>
                    <div class="author-detail">
                      <span class="author-name">{{ article.author_name }}</span>
                      <span class="publish-time">{{ formatDate(article.created_at) }}</span>
                    </div>
                  </div>
                  <div class="article-stats">
                    <span><el-icon><View /></el-icon> {{ article.view_count }} 阅读</span>
                  </div>
                </div>
                <div v-if="article.tags?.length" class="article-tags">
                  <el-tag 
                    v-for="tag in article.tags" 
                    :key="tag.id" 
                    size="small" 
                    effect="plain"
                    @click="$router.push(`/tag/${tag.id}`)"
                  >
                    {{ tag.name }}
                  </el-tag>
                </div>
              </header>

              <div v-if="article.cover_image" class="article-cover">
                <img :src="getCoverUrl(article.cover_image)" :alt="article.title" />
              </div>

              <div class="article-content" v-html="article.content"></div>
            </article>

            <div class="article-nav">
              <el-button v-if="prevArticle" text @click="$router.push(`/article/${prevArticle.id}`)">
                <el-icon><ArrowLeft /></el-icon> 上一篇
              </el-button>
              <el-button v-if="nextArticle" text @click="$router.push(`/article/${nextArticle.id}`)">
                下一篇 <el-icon><ArrowRight /></el-icon>
              </el-button>
            </div>

            <div class="comments-section">
              <div class="section-title">
                <el-icon><ChatDotRound /></el-icon>
                <span>评论 ({{ comments.length }})</span>
              </div>

              <div v-if="userStore.isLoggedIn" class="comment-form">
                <el-input
                  v-model="commentContent"
                  type="textarea"
                  :rows="3"
                  placeholder="写下你的评论..."
                />
                <el-button type="primary" @click="submitComment" :loading="submitting">发表评论</el-button>
              </div>
              <div v-else class="login-tip">
                <p>登录后才能评论</p>
                <el-button type="primary" @click="$router.push('/login')">立即登录</el-button>
              </div>

              <div class="comment-list">
                <div v-for="comment in comments" :key="comment.id" class="comment-item">
                  <el-avatar :size="40">{{ comment.user_name?.charAt(0) }}</el-avatar>
                  <div class="comment-content">
                    <div class="comment-header">
                      <span class="comment-author">{{ comment.user_name }}</span>
                      <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
                    </div>
                    <p class="comment-text">{{ comment.content }}</p>
                  </div>
                </div>
                <el-empty v-if="comments.length === 0" description="暂无评论，快来抢沙发吧~" />
              </div>
            </div>
          </div>
        </el-col>

        <el-col :span="7">
          <div class="sidebar">
            <div class="sidebar-card author-card">
              <div class="author-profile">
                <el-avatar :size="56">{{ article.author_name?.charAt(0) }}</el-avatar>
                <div class="author-info">
                  <span class="author-name">{{ article.author_name }}</span>
                  <span class="author-title">内容创作者</span>
                </div>
              </div>
            </div>

            <div class="sidebar-card">
              <div class="sidebar-title">
                <el-icon><Document /></el-icon>
                <span>相关文章</span>
              </div>
              <div class="related-list">
                <div
                  v-for="item in relatedArticles"
                  :key="item.id"
                  class="related-item"
                  @click="$router.push(`/article/${item.id}`)"
                >
                  <div class="related-cover" v-if="item.cover_image">
                    <img :src="getCoverUrl(item.cover_image)" />
                  </div>
                  <div class="related-info">
                    <span class="related-title">{{ item.title }}</span>
                    <span class="related-views">{{ item.view_count }} 阅读</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { View, ArrowLeft, ArrowRight, ChatDotRound, Document } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { getContent, getContents, getComments, createComment } from '@/api/content'

const route = useRoute()
const userStore = useUserStore()

const loading = ref(false)
const article = ref({})
const comments = ref([])
const commentContent = ref('')
const submitting = ref(false)
const prevArticle = ref(null)
const nextArticle = ref(null)
const relatedArticles = ref([])

const getCoverUrl = (coverImage) => {
  if (!coverImage) return ''
  if (coverImage.startsWith('http')) return coverImage
  return `http://localhost:8001${coverImage}`
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

const fetchArticle = async () => {
  loading.value = true
  try {
    const { data } = await getContent(route.params.id)
    article.value = data
    fetchComments()
    fetchRelatedArticles()
  } catch (e) {
    ElMessage.error('文章不存在')
  } finally {
    loading.value = false
  }
}

const fetchComments = async () => {
  try {
    const { data } = await getComments({ article: route.params.id })
    comments.value = data.results || data
  } catch (e) {
    console.error(e)
  }
}

const fetchRelatedArticles = async () => {
  try {
    const params = { status: 'published', page_size: 5 }
    if (article.value.category) {
      params.category = article.value.category
    }
    const { data } = await getContents(params)
    const results = data.results || data
    relatedArticles.value = results.filter(item => item.id !== article.value.id).slice(0, 5)
  } catch (e) {
    console.error(e)
  }
}

const submitComment = async () => {
  if (!commentContent.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }
  submitting.value = true
  try {
    await createComment({
      article: route.params.id,
      content: commentContent.value,
    })
    ElMessage.success('评论成功，等待审核')
    commentContent.value = ''
  } catch (e) {
    ElMessage.error('评论失败')
  } finally {
    submitting.value = false
  }
}

watch(() => route.params.id, () => {
  if (route.params.id) {
    fetchArticle()
  }
}, { immediate: true })
</script>

<style scoped>
.article-page {
  padding: 24px 0;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
}

.article-main {
  background: #fff;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.article-header {
  margin-bottom: 28px;
}

.article-category {
  margin-bottom: 16px;
}

.article-header h1 {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  line-height: 1.4;
  margin-bottom: 20px;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-detail {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-weight: 500;
  color: #303133;
  font-size: 15px;
}

.publish-time {
  font-size: 13px;
  color: #909399;
}

.article-stats {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: #909399;
}

.article-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.article-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.article-tags .el-tag {
  cursor: pointer;
}

.article-cover {
  margin-bottom: 28px;
  border-radius: 8px;
  overflow: hidden;
}

.article-cover img {
  width: 100%;
  height: auto;
}

.article-content {
  font-size: 16px;
  line-height: 1.8;
  color: #303133;
}

.article-content :deep(p) {
  margin-bottom: 20px;
}

.article-content :deep(h2) {
  font-size: 22px;
  margin: 28px 0 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #ebeef5;
}

.article-content :deep(h3) {
  font-size: 18px;
  margin: 24px 0 12px;
}

.article-content :deep(img) {
  max-width: 100%;
  border-radius: 8px;
  margin: 16px 0;
}

.article-content :deep(pre) {
  background: #f5f7fa;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
}

.article-content :deep(blockquote) {
  border-left: 4px solid #409eff;
  padding-left: 16px;
  margin: 16px 0;
  color: #606266;
}

.article-nav {
  display: flex;
  justify-content: space-between;
  margin-top: 40px;
  padding-top: 24px;
  border-top: 1px solid #ebeef5;
}

.comments-section {
  margin-top: 40px;
  padding-top: 32px;
  border-top: 1px solid #ebeef5;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 24px;
}

.section-title .el-icon {
  color: #409eff;
}

.comment-form {
  margin-bottom: 28px;
}

.comment-form .el-textarea {
  margin-bottom: 12px;
}

.login-tip {
  text-align: center;
  padding: 32px;
  background: #f5f7fa;
  border-radius: 12px;
  margin-bottom: 28px;
}

.login-tip p {
  color: #909399;
  margin-bottom: 12px;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-item {
  display: flex;
  gap: 12px;
}

.comment-content {
  flex: 1;
  background: #f5f7fa;
  padding: 16px;
  border-radius: 8px;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: 500;
  color: #303133;
}

.comment-time {
  font-size: 12px;
  color: #909399;
}

.comment-text {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #ebeef5;
}

.sidebar-title .el-icon {
  color: #409eff;
}

.author-card {
  padding: 24px;
}

.author-profile {
  display: flex;
  align-items: center;
  gap: 16px;
}

.author-profile .author-info {
  display: flex;
  flex-direction: column;
}

.author-profile .author-name {
  font-size: 16px;
  font-weight: 600;
}

.author-profile .author-title {
  font-size: 13px;
  color: #909399;
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.related-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.related-item:hover {
  background: #f5f7fa;
}

.related-cover {
  width: 80px;
  height: 60px;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
}

.related-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.related-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
}

.related-title {
  font-size: 14px;
  color: #303133;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 4px;
}

.related-views {
  font-size: 12px;
  color: #909399;
}
</style>
