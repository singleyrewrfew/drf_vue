<template>
  <div class="article-page">
    <div class="container">
      <el-row :gutter="24">
        <el-col :span="17">
          <div class="article-main" v-loading="loading">
            <article class="article">
              <header class="article-header">
                <div class="article-category" v-if="article.category_name">
                  <el-tag type="success" effect="plain" @click="$router.push(`/category/${article.category_slug || article.category_id}`)">{{ article.category_name }}</el-tag>
                </div>
                <h1>{{ article.title }}</h1>
                <div class="article-meta">
                  <div class="author-info">
                    <el-avatar :size="40" :src="getAvatarUrl(article.author_avatar)">{{ article.author_name?.charAt(0)?.toUpperCase() }}</el-avatar>
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
                    #{{ tag.name }}
                  </el-tag>
                </div>
              </header>

              <div v-if="article.cover_image" class="article-cover">
                <img :src="getCoverUrl(article.cover_image)" :alt="article.title" />
              </div>

              <div class="article-content markdown-body" v-html="renderedContent"></div>
              
              <div v-if="!fullContentLoaded && article.content_preview" class="full-content-loading">
                <el-skeleton :rows="10" animated />
              </div>
            </article>

            <div class="article-nav">
              <el-button v-if="prevArticle" text @click="$router.push(getArticleUrl(prevArticle))">
                <el-icon><ArrowLeft /></el-icon> 上一篇
              </el-button>
              <el-button v-if="nextArticle" text @click="$router.push(getArticleUrl(nextArticle))">
                下一篇 <el-icon><ArrowRight /></el-icon>
              </el-button>
            </div>

            <div class="comments-section">
              <div class="section-title">
                <el-icon><ChatDotRound /></el-icon>
                <span>评论 ({{ comments.length }})</span>
              </div>

              <div v-if="userStore.isLoggedIn" class="comment-form">
                <div class="comment-form-wrapper">
                  <el-avatar :size="36" :src="getAvatarUrl(userStore.user?.avatar)">{{ userStore.user?.username?.charAt(0).toUpperCase() }}</el-avatar>
                  <div class="comment-form-content">
                    <el-input
                      v-model="commentContent"
                      type="textarea"
                      :rows="3"
                      placeholder="理性发言，友善互动..."
                      :autosize="{ minRows: 3, maxRows: 8 }"
                      resize="none"
                      class="comment-textarea"
                    />
                    <div class="comment-form-footer">
                      <div class="comment-form-tools">
                        <el-popover placement="top-start" :width="300" trigger="click">
                          <template #reference>
                            <el-button link class="tool-btn">
                              <svg width="1.2em" height="1.2em" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M14.413 14.223a.785.785 0 0 1 1.45.601A4.174 4.174 0 0 1 12 17.4a4.19 4.19 0 0 1-2.957-1.221 4.174 4.174 0 0 1-.906-1.355.785.785 0 1 1 1.449-.601 2.604 2.604 0 0 0 1.413 1.41 2.621 2.621 0 0 0 2.849-.566c.242-.242.434-.529.565-.844ZM8.6 8.77a1.308 1.308 0 1 1 0 2.615 1.308 1.308 0 0 1 0-2.615ZM15.4 8.77a1.308 1.308 0 1 1 0 2.615 1.308 1.308 0 0 1 0-2.615Z"></path>
                                <path fill-rule="evenodd" d="M12 1.573c5.758 0 10.427 4.669 10.427 10.427S17.758 22.427 12 22.427 1.573 17.758 1.573 12 6.242 1.573 12 1.573Zm0 1.746a8.681 8.681 0 1 0 .001 17.362A8.681 8.681 0 0 0 12 3.32Z" clip-rule="evenodd"></path>
                              </svg>
                            </el-button>
                          </template>
                          <div class="emoji-picker">
                            <div class="emoji-list">
                              <span v-for="emoji in emojis" :key="emoji" class="emoji-item" @click="insertEmoji(emoji)">
                                {{ emoji }}
                              </span>
                            </div>
                          </div>
                        </el-popover>
                      </div>
                      <div class="comment-form-actions">
                        <span class="char-count">{{ commentContent.length }}/500</span>
                        <el-button type="primary" @click="submitComment" :loading="submitting" :disabled="!commentContent.trim()">
                          发布
                        </el-button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="login-tip">
                <p>登录后才能评论</p>
                <el-button type="primary" @click="$router.push('/login')">立即登录</el-button>
              </div>

              <div class="comment-list">
                <div v-for="comment in displayComments" :key="comment.id" class="comment-item">
                  <el-avatar :size="40" :src="getAvatarUrl(comment.user_avatar)">{{ comment.user_name?.charAt(0)?.toUpperCase() }}</el-avatar>
                  <div class="comment-body">
                    <div class="comment-main">
                      <div class="comment-header">
                        <span class="comment-author">{{ comment.user_name }}</span>
                        <span class="comment-time">{{ formatRelativeTime(comment.created_at) }}</span>
                      </div>
                      <p class="comment-text">{{ comment.content }}</p>
                      <div class="comment-actions">
                        <span 
                          class="action-btn" 
                          :class="{ liked: comment.is_liked }"
                          @click="handleLike(comment)"
                        >
                          <el-icon><Pointer /></el-icon>
                          <span>{{ comment.like_count || '' }}</span>
                        </span>
                        <span class="action-btn" @click="openReplyForm(comment.id, comment.user_name, comment.user)">
                          <el-icon><ChatDotRound /></el-icon>
                          <span>回复</span>
                        </span>
                      </div>
                    </div>
                    <div v-if="replyToParent === comment.id" class="reply-form">
                      <div class="reply-form-header">
                        <span>回复 <span class="reply-target">@{{ replyToName }}</span></span>
                        <el-button link size="small" @click="closeReplyForm">取消</el-button>
                      </div>
                      <el-input
                        v-model="replyContent"
                        type="textarea"
                        :rows="2"
                        placeholder="写下你的回复..."
                        :autosize="{ minRows: 2, maxRows: 6 }"
                        resize="none"
                        @keyup.ctrl.enter="submitReply(comment.id)"
                      />
                      <div class="reply-form-actions">
                        <span class="reply-tip">Ctrl + Enter 发送</span>
                        <el-button type="primary" size="small" @click="submitReply(comment.id)" :loading="submittingReply">
                          发送
                        </el-button>
                      </div>
                    </div>
                    <div v-if="comment.reply_count > 0" class="reply-section">
                      <div 
                        class="reply-toggle" 
                        @click="toggleReplies(comment.id)"
                      >
                        <span>{{ expandedReplies.includes(comment.id) ? '收起回复' : `${comment.reply_count} 条回复` }}</span>
                        <el-icon :class="{ rotated: expandedReplies.includes(comment.id) }"><ArrowRight /></el-icon>
                      </div>
                      <div v-if="expandedReplies.includes(comment.id) && comment.replies?.length" class="reply-list">
                        <div v-for="reply in comment.replies" :key="reply.id" class="reply-item">
                          <el-avatar :size="24" :src="getAvatarUrl(reply.user_avatar)">{{ reply.user_name?.charAt(0)?.toUpperCase() }}</el-avatar>
                          <div class="reply-body">
                            <div class="reply-header">
                              <span class="reply-author">{{ reply.user_name }}</span>
                              <template v-if="reply.reply_to_name">
                                <el-icon class="reply-arrow"><ArrowRight /></el-icon>
                                <span class="reply-to-user">{{ reply.reply_to_name }}</span>
                              </template>
                              <span class="reply-time">{{ formatRelativeTime(reply.created_at) }}</span>
                            </div>
                            <p class="reply-text">{{ reply.content }}</p>
                            <div class="reply-actions">
                              <span 
                                class="action-btn small" 
                                :class="{ liked: reply.is_liked }"
                                @click="handleLike(reply, comment.id)"
                              >
                                <el-icon><Pointer /></el-icon>
                                <span>{{ reply.like_count || '' }}</span>
                              </span>
                              <span class="action-btn small" @click="openReplyForm(comment.id, reply.user_name, reply.user_id)">
                                <el-icon><ChatDotRound /></el-icon>
                                <span>回复</span>
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-if="comments.length > 2" class="show-more-comments">
                  <el-button 
                    type="primary" 
                    plain 
                    @click="showCommentsDialog = true"
                  >
                    查看全部 {{ comments.length }} 条评论
                  </el-button>
                </div>
                <el-empty v-if="comments.length === 0" description="暂无评论，快来抢沙发吧~" />
              </div>
            </div>
          </div>

          <!-- 评论对话框 -->
          <el-dialog
            v-model="showCommentsDialog"
            title="全部评论"
            width="800px"
            destroy-on-close
          >
            <div class="dialog-comment-list">
              <div v-for="comment in comments" :key="comment.id" class="dialog-comment-item">
                <el-avatar :size="40" :src="getAvatarUrl(comment.user_avatar)">{{ comment.user_name?.charAt(0)?.toUpperCase() }}</el-avatar>
                <div class="dialog-comment-body">
                  <div class="dialog-comment-main">
                    <div class="dialog-comment-header">
                      <span class="dialog-comment-author">{{ comment.user_name }}</span>
                      <span class="dialog-comment-time">{{ formatRelativeTime(comment.created_at) }}</span>
                    </div>
                    <p class="dialog-comment-text">{{ comment.content }}</p>
                    <div class="dialog-comment-actions">
                      <span 
                        class="dialog-action-btn" 
                        :class="{ liked: comment.is_liked }"
                        @click="handleLike(comment)"
                      >
                        <el-icon><Pointer /></el-icon>
                        <span>{{ comment.like_count || '' }}</span>
                      </span>
                      <span class="dialog-action-btn" @click="openReplyForm(comment.id, comment.user_name, comment.user)">
                        <el-icon><ChatDotRound /></el-icon>
                        <span>回复</span>
                      </span>
                    </div>
                  </div>
                  <div v-if="replyToParent === comment.id" class="dialog-reply-form">
                      <div class="dialog-reply-form-header">
                        <span>回复 <span class="dialog-reply-target">@{{ replyToName }}</span></span>
                        <el-button link size="small" @click="closeReplyForm">取消</el-button>
                      </div>
                      <el-input
                        v-model="replyContent"
                        type="textarea"
                        :rows="2"
                        placeholder="写下你的回复..."
                        :autosize="{ minRows: 2, maxRows: 6 }"
                        resize="none"
                        @keyup.ctrl.enter="submitReply(comment.id)"
                      />
                      <div class="dialog-reply-form-actions">
                        <span class="dialog-reply-tip">Ctrl + Enter 发送</span>
                        <el-button type="primary" size="small" @click="submitReply(comment.id)" :loading="submittingReply">
                          发送
                        </el-button>
                      </div>
                    </div>
                  <div v-if="comment.reply_count > 0" class="dialog-reply-section">
                    <div 
                      class="dialog-reply-toggle" 
                      @click="toggleReplies(comment.id)"
                    >
                      <span>{{ expandedReplies.includes(comment.id) ? '收起回复' : `${comment.reply_count} 条回复` }}</span>
                      <el-icon :class="{ rotated: expandedReplies.includes(comment.id) }"><ArrowRight /></el-icon>
                    </div>
                    <div v-if="expandedReplies.includes(comment.id) && comment.replies?.length" class="dialog-reply-list">
                      <div v-for="reply in comment.replies" :key="reply.id" class="dialog-reply-item">
                        <el-avatar :size="24" :src="getAvatarUrl(reply.user_avatar)">{{ reply.user_name?.charAt(0)?.toUpperCase() }}</el-avatar>
                        <div class="dialog-reply-body">
                          <div class="dialog-reply-header">
                            <span class="dialog-reply-author">{{ reply.user_name }}</span>
                            <template v-if="reply.reply_to_name">
                              <el-icon class="dialog-reply-arrow"><ArrowRight /></el-icon>
                              <span class="dialog-reply-to-user">{{ reply.reply_to_name }}</span>
                            </template>
                            <span class="dialog-reply-time">{{ formatRelativeTime(reply.created_at) }}</span>
                          </div>
                          <p class="dialog-reply-text">{{ reply.content }}</p>
                          <div class="dialog-reply-actions">
                            <span 
                              class="dialog-action-btn small" 
                              :class="{ liked: reply.is_liked }"
                              @click="handleLike(reply, comment.id)"
                            >
                              <el-icon><Pointer /></el-icon>
                              <span>{{ reply.like_count || '' }}</span>
                            </span>
                            <span class="dialog-action-btn small" @click="openReplyForm(comment.id, reply.user_name, reply.user_id)">
                              <el-icon><ChatDotRound /></el-icon>
                              <span>回复</span>
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <el-empty v-if="comments.length === 0" description="暂无评论" />
            </div>
          </el-dialog>
        </el-col>

        <el-col :span="7">
          <div class="sidebar">
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
                  @click="$router.push(getArticleUrl(item))"
                >
                  <div class="related-cover" v-if="item.cover_image">
                    <img :src="getCoverUrl(item.cover_image)" />
                  </div>
                  <div class="related-info">
                    <span class="related-title">{{ item.title }}</span>
                    <span class="related-views">{{ item.view_count }} 阅读</span>
                  </div>
                </div>
                <el-empty v-if="relatedArticles.length === 0" description="暂无相关文章" :image-size="60" />
              </div>
            </div>

            <div class="sidebar-card toc-card">
              <div class="sidebar-title">
                <el-icon><List /></el-icon>
                <span>目录</span>
              </div>
              <div class="toc-list" v-if="headings.length">
                <div
                  v-for="(heading, index) in headings"
                  :key="index"
                  v-show="heading.level <= 3"
                  :class="['toc-item', 'toc-' + heading.level]"
                  @click="scrollToHeading(heading.id)"
                >
                  {{ heading.text }}
                </div>
              </div>
              <el-empty v-else description="暂无目录" :image-size="60" />
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { View, ArrowLeft, ArrowRight, ChatDotRound, Document, List, Pointer, Picture, VideoCamera, Link } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'
import { useUserStore } from '@/stores/user'
import { getContent, getContents, getComments, createComment, likeComment } from '@/api/content'

const route = useRoute()
const userStore = useUserStore()

const loading = ref(false)
const article = ref({})
const fullContentLoaded = ref(false)
const comments = ref([])
const commentContent = ref('')
const submitting = ref(false)
const replyToParent = ref(null)
const replyToName = ref('')
const replyToUserId = ref(null)
const replyContent = ref('')
const submittingReply = ref(false)
const expandedReplies = ref([])
const prevArticle = ref(null)
const nextArticle = ref(null)
const relatedArticles = ref([])
const showAllComments = ref(false)
const imageInput = ref(null)

const emojis = ['😀', '😂', '😍', '🥰', '😎', '🤔', '👍', '👎', '❤️', '💔', '🎉', '🔥', '✨', '🌟', '⭐', '💯', '💪', '🙏', '😭', '😱', '🤣', '😊', '🥺', '👏', '🙄', '😴', '😋', '😜', '🤪', '😇']

const displayComments = computed(() => {
  if (showAllComments.value) {
    return comments.value
  }
  return comments.value.slice(0, 2)
})

const showCommentsDialog = ref(false)

const getCoverUrl = (coverImage) => {
  if (!coverImage) return ''
  if (coverImage.startsWith('http')) return coverImage
  return `http://localhost:8001${coverImage}`
}

const getAvatarUrl = (avatar) => {
  if (!avatar) return ''
  if (avatar.startsWith('http')) return avatar
  return `http://localhost:8001${avatar}`
}

const getArticleUrl = (article) => {
  return `/article/${article.slug || article.id}`
}

const scrollToHeading = (id) => {
  const element = document.getElementById(id)
  if (element) {
    const headerHeight = 72
    const elementPosition = element.getBoundingClientRect().top + window.pageYOffset
    window.scrollTo({
      top: elementPosition - headerHeight - 16,
      behavior: 'smooth'
    })
  }
}

const formatRelativeTime = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  
  if (seconds < 60) return '刚刚'
  if (minutes < 60) return `${minutes} 分钟前`
  if (hours < 24) return `${hours} 小时前`
  if (days < 7) return `${days} 天前`
  if (days < 30) return `${Math.floor(days / 7)} 周前`
  if (days < 365) return `${Math.floor(days / 30)} 个月前`
  return `${Math.floor(days / 365)} 年前`
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

const headings = ref([])

const extractHeadings = (html) => {
  const tempDiv = document.createElement('div')
  tempDiv.innerHTML = html
  const headingElements = tempDiv.querySelectorAll('h1, h2, h3, h4, h5, h6')
  const result = []
  headingElements.forEach((el, index) => {
    const id = `heading-${index}`
    el.id = id
    result.push({
      id,
      level: parseInt(el.tagName.charAt(1)),
      text: el.textContent,
    })
  })
  return { html: tempDiv.innerHTML, headings: result }
}

const renderedContent = computed(() => {
  if (!article.value.content) return ''
  
  marked.setOptions({
    highlight: function(code, lang) {
      if (lang && hljs.getLanguage(lang)) {
        try {
          return hljs.highlight(code, { language: lang }).value
        } catch (e) {
          console.error(e)
        }
      }
      return hljs.highlightAuto(code).value
    },
    breaks: true,
    gfm: true,
  })
  
  let html = marked.parse(article.value.content)
  const result = extractHeadings(html)
  headings.value = result.headings
  return result.html
})

const initArticleContent = () => {
  if (!article.value.content) return
  
  marked.setOptions({
    highlight: function(code, lang) {
      if (lang && hljs.getLanguage(lang)) {
        try {
          return hljs.highlight(code, { language: lang }).value
        } catch (e) {
          console.error(e)
        }
      }
      return hljs.highlightAuto(code).value
    },
    breaks: true,
    gfm: true,
  })
  
  let html = marked.parse(article.value.content)
  const result = extractHeadings(html)
  headings.value = result.headings
  
  // 文章渲染完成后，初始化图片懒加载
  nextTick(() => {
    initImageLazyLoad()
  })
  
  // 如果当前是预览内容且内容长度等于 5000，异步加载完整内容
  if (article.value.content === article.value.content_preview && 
      article.value.content.length === 5000 && 
      !fullContentLoaded.value) {
    loadFullContent()
  } else {
    // 否则标记为已加载完成
    fullContentLoaded.value = true
  }
}

const loadFullContent = async () => {
  try {
    const { data } = await getContent(route.params.id)
    if (data.content && data.content !== article.value.content) {
      article.value.content = data.content
      fullContentLoaded.value = true
      
      // 重新渲染完整内容
      nextTick(() => {
        initArticleContent()
      })
    }
  } catch (e) {
    console.error('加载完整内容失败:', e)
  }
}

const fetchArticle = async () => {
  loading.value = true
  fullContentLoaded.value = false
  try {
    // 支持通过 slug 或 ID 获取文章
    const articleId = route.params.slug || route.params.id
    const { data } = await getContent(articleId)
    article.value = data
    
    // 如果有 preview 字段且内容超过 preview，先使用 preview
    if (data.content_preview && data.content.length > data.content_preview.length) {
      article.value.content = data.content_preview
    }
    
    // 文章加载成功后，初始化内容渲染
    initArticleContent()
    
    // 并行加载评论和相关文章（失败不影响文章显示）
    Promise.all([
      fetchComments(),
      fetchRelatedArticles(),
    ]).catch(e => {
      console.error('加载评论或相关文章失败:', e)
    })
  } catch (e) {
    console.error(e)
    ElMessage.error('文章不存在')
  } finally {
    loading.value = false
  }
}

const fetchComments = async () => {
  try {
    const articleId = route.params.slug || route.params.id
    const { data } = await getComments({ article: articleId })
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

const triggerImageUpload = () => {
  imageInput.value?.click()
}

const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  if (file.size > 5 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过 5MB')
    return
  }
  
  try {
    // 这里需要调用上传接口，暂时只显示图片
    const reader = new FileReader()
    reader.onload = (e) => {
      const imgMarkdown = `![图片](${e.target.result})`
      commentContent.value += imgMarkdown
    }
    reader.readAsDataURL(file)
  } catch (e) {
    ElMessage.error('图片上传失败')
  }
  
  // 清空 input，确保同一文件可以再次选择
  event.target.value = ''
}

const insertLink = () => {
  const url = prompt('请输入链接地址：')
  if (!url) return
  
  const text = prompt('请输入链接文本：', url)
  if (!text) return
  
  const linkMarkdown = `[${text}](${url})`
  commentContent.value += linkMarkdown
}

const showTooltip = (message) => {
  ElMessage.info(message)
}

const insertEmoji = (emoji) => {
  commentContent.value += emoji
}

// 图片懒加载
const imageObserver = ref(null)

const initImageLazyLoad = () => {
  if (!('IntersectionObserver' in window)) {
    // 不支持 IntersectionObserver 的浏览器直接加载所有图片
    return
  }
  
  // 创建 IntersectionObserver 实例
  imageObserver.value = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target
        const dataSrc = img.getAttribute('data-src')
        if (dataSrc) {
          img.src = dataSrc
          img.removeAttribute('data-src')
          img.classList.remove('lazy-loading')
          imageObserver.value.unobserve(img)
        }
      }
    })
  }, {
    rootMargin: '50px 0px', // 提前 50px 开始加载
    threshold: 0.01
  })
  
  // 查找文章内容中的所有图片
  const articleContent = document.querySelector('.article-content')
  if (articleContent) {
    const images = articleContent.querySelectorAll('img')
    images.forEach(img => {
      const src = img.getAttribute('src')
      if (src) {
        img.setAttribute('data-src', src)
        img.removeAttribute('src')
        img.classList.add('lazy-loading')
        imageObserver.value.observe(img)
      }
    })
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
    ElMessage.success('评论成功')
    commentContent.value = ''
    fetchComments()
  } catch (e) {
    ElMessage.error('评论失败')
  } finally {
    submitting.value = false
  }
}

const openReplyForm = (parentId, userName, userId) => {
  replyToParent.value = parentId
  replyToName.value = userName
  replyToUserId.value = userId
  replyContent.value = ''
}

const closeReplyForm = () => {
  replyToParent.value = null
  replyToName.value = ''
  replyToUserId.value = null
  replyContent.value = ''
}

const toggleReplies = (commentId) => {
  const index = expandedReplies.value.indexOf(commentId)
  if (index > -1) {
    expandedReplies.value.splice(index, 1)
  } else {
    expandedReplies.value.push(commentId)
  }
}

const handleLike = async (comment, parentCommentId = null) => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  try {
    const { data } = await likeComment(comment.id)
    if (parentCommentId) {
      const parentComment = comments.value.find(c => c.id === parentCommentId)
      if (parentComment && parentComment.replies) {
        const replyIndex = parentComment.replies.findIndex(r => r.id === comment.id)
        if (replyIndex > -1) {
          parentComment.replies[replyIndex] = data
        }
      }
    } else {
      const commentIndex = comments.value.findIndex(c => c.id === comment.id)
      if (commentIndex > -1) {
        comments.value[commentIndex] = { ...comments.value[commentIndex], ...data }
      }
    }
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

const submitReply = async (parentId) => {
  if (!replyContent.value.trim()) {
    ElMessage.warning('请输入回复内容')
    return
  }
  submittingReply.value = true
  try {
    await createComment({
      article: route.params.id,
      content: replyContent.value,
      parent: parentId,
      reply_to_id: replyToUserId.value,
    })
    ElMessage.success('回复成功')
    closeReplyForm()
    fetchComments()
  } catch (e) {
    ElMessage.error('回复失败')
  } finally {
    submittingReply.value = false
  }
}

watch(() => route.params.id, () => {
  if (route.params.id) {
    fetchArticle()
  }
}, { immediate: true })

onUnmounted(() => {
  // 清理图片观察者
  if (imageObserver.value) {
    imageObserver.value.disconnect()
  }
})
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

.author-info .el-avatar {
  border-radius: 4px !important;
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

.comment-form-wrapper {
  display: flex;
  gap: 12px;
  background: #f7f8fa;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e8e8e8;
}

.comment-form-wrapper .el-avatar {
  border-radius: 4px !important;
}

.comment-form-content {
  flex: 1;
}

.comment-form-title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.comment-textarea .el-textarea__inner {
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  padding: 12px;
  font-size: 14px;
  line-height: 1.6;
}

.comment-form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
}

.comment-form-tools {
  display: flex;
  gap: 8px;
}

.tool-btn {
  padding: 4px 8px;
  color: #8590a6;
  font-size: 18px;
  transition: all 0.2s;
}

.tool-btn:hover {
  color: #409eff;
  background: #ecf5ff;
}

.comment-form-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.char-count {
  font-size: 12px;
  color: #8590a6;
}

.comment-form .el-button--primary {
  min-width: 80px;
  height: 32px;
  font-size: 14px;
}

.emoji-picker {
  max-height: 200px;
  overflow-y: auto;
}

.emoji-list {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 8px;
}

.emoji-item {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  font-size: 20px;
  cursor: pointer;
  border-radius: 4px;
  transition: background 0.2s;
}

.emoji-item:hover {
  background: #f0f2f5;
}

/* 图片懒加载样式 */
.article-content img {
  transition: opacity 0.3s;
}

.article-content img.lazy-loading {
  opacity: 0;
  background: #f0f2f5;
  min-height: 200px;
}

.article-content img[data-src] {
  opacity: 0;
}

/* 完整内容加载提示 */
.full-content-loading {
  margin-top: 20px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
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
  gap: 24px;
}

.comment-item {
  display: flex;
  gap: 12px;
  background: #f7f8fa;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
}

.comment-item .el-avatar {
  border-radius: 4px !important;
}

.comment-body {
  flex: 1;
}

.comment-main {
  background: transparent;
  padding: 0;
  border-radius: 0;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: 600;
  color: #303133;
  font-size: 15px;
}

.comment-time {
  font-size: 13px;
  color: #8590a6;
}

.comment-text {
  font-size: 15px;
  color: #1a1a1a;
  line-height: 1.7;
}

.comment-actions {
  margin-top: 12px;
  display: flex;
  gap: 20px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #8590a6;
  cursor: pointer;
  transition: color 0.2s;
}

.action-btn:hover {
  color: #409eff;
}

.action-btn.liked {
  color: #409eff;
}

.action-btn.small {
  font-size: 12px;
}

.reply-form {
  margin-top: 12px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  border: 1px solid #e8e8e8;
}

.reply-form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.reply-target {
  color: #409eff;
  font-weight: 500;
}

.reply-form .el-textarea {
  margin-bottom: 8px;
}

.reply-form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.reply-tip {
  font-size: 12px;
  color: #8590a6;
}

.reply-section {
  margin-top: 8px;
}

.reply-toggle {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: #f0f0f0;
  color: #666;
  font-size: 12px;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s;
  border: 1px solid #e0e0e0;
  font-weight: 500;
}

.reply-toggle:hover {
  background: #e0e0e0;
  border-color: #d0d0d0;
}

.reply-toggle .el-icon {
  font-size: 16px;
  color: #666;
  transition: transform 0.3s;
}

.reply-toggle .el-icon.rotated {
  transform: rotate(90deg);
}

.reply-list {
  margin-top: 12px;
  padding-left: 24px;
}

.reply-item {
  display: flex;
  gap: 10px;
  padding: 12px;
  margin-bottom: 8px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 6px;
  border: 1px solid #f0f2f5;
}

.reply-item .el-avatar {
  border-radius: 3px !important;
}

.reply-item:last-child {
  margin-bottom: 0;
}

.reply-body {
  flex: 1;
}

.reply-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.reply-arrow {
  color: #8590a6;
  font-size: 12px;
}

.reply-author {
  font-weight: 600;
  color: #303133;
  font-size: 14px;
}

.reply-time {
  font-size: 12px;
  color: #8590a6;
}

.reply-text {
  font-size: 14px;
  color: #1a1a1a;
  line-height: 1.6;
}

.reply-actions {
  margin-top: 8px;
  display: flex;
  gap: 16px;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-self: flex-start;
  position: sticky;
  top: 96px;
  max-height: calc(100vh - 116px);
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.sidebar::-webkit-scrollbar {
  display: none;
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

.toc-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-height: 400px;
  overflow-y: auto;
  padding-right: 8px;
}

.toc-list::-webkit-scrollbar {
  width: 6px;
}

.toc-list::-webkit-scrollbar-track {
  background: #f5f7fa;
  border-radius: 3px;
}

.toc-list::-webkit-scrollbar-thumb {
  background: #c0c4cc;
  border-radius: 3px;
  transition: background 0.3s;
}

.toc-list::-webkit-scrollbar-thumb:hover {
  background: #909399;
}

.toc-item {
  font-size: 13px;
  color: #606266;
  text-decoration: none;
  padding: 6px 0;
  display: block;
  transition: color 0.3s;
  cursor: pointer;
}

.toc-item:hover {
  color: #409eff;
}

.toc-2 {
  padding-left: 0;
}

.toc-3 {
  padding-left: 12px;
}

.toc-4 {
  padding-left: 24px;
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

.show-more-comments {
  margin-top: 20px;
  text-align: center;
}

/* 对话框评论样式 */
.dialog-comment-list {
  height: 100%;
  max-height: calc(80vh - 120px);
  overflow-y: auto;
  padding-right: 8px;
}

.dialog-comment-item {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  background: #f7f8fa;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
}

.dialog-comment-item .el-avatar {
  border-radius: 4px !important;
}

.dialog-comment-body {
  flex: 1;
}

.dialog-comment-main {
  background: transparent;
  padding: 0;
  border-radius: 0;
}

.dialog-comment-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.dialog-comment-author {
  font-weight: 600;
  color: #303133;
  font-size: 15px;
}

.dialog-comment-time {
  font-size: 13px;
  color: #8590a6;
}

.dialog-comment-text {
  font-size: 15px;
  color: #1a1a1a;
  line-height: 1.7;
}

.dialog-comment-actions {
  margin-top: 12px;
  display: flex;
  gap: 20px;
}

.dialog-action-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #8590a6;
  cursor: pointer;
  transition: color 0.2s;
}

.dialog-action-btn:hover {
  color: #409eff;
}

.dialog-action-btn.liked {
  color: #409eff;
}

.dialog-action-btn.small {
  font-size: 12px;
}

.dialog-reply-form {
  margin-top: 12px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  border: 1px solid #e8e8e8;
}

.dialog-reply-form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.dialog-reply-target {
  color: #409eff;
  font-weight: 500;
}

.dialog-reply-form .el-textarea {
  margin-bottom: 8px;
}

.dialog-reply-form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.dialog-reply-tip {
  font-size: 12px;
  color: #8590a6;
}

.dialog-reply-section {
  margin-top: 8px;
}

.dialog-reply-toggle {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: #f0f0f0;
  color: #666;
  font-size: 12px;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s;
  border: 1px solid #e0e0e0;
  font-weight: 500;
}

.dialog-reply-toggle:hover {
  background: #e0e0e0;
  border-color: #d0d0d0;
}

.dialog-reply-toggle .el-icon {
  font-size: 16px;
  color: #666;
  transition: transform 0.3s;
}

.dialog-reply-toggle .el-icon.rotated {
  transform: rotate(90deg);
}

.dialog-reply-list {
  margin-top: 12px;
  padding-left: 24px;
}

.dialog-reply-item {
  display: flex;
  gap: 10px;
  padding: 12px;
  margin-bottom: 8px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 6px;
  border: 1px solid #f0f2f5;
}

.dialog-reply-item .el-avatar {
  border-radius: 3px !important;
}

.dialog-reply-item:last-child {
  margin-bottom: 0;
}

.dialog-reply-body {
  flex: 1;
}

.dialog-reply-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.dialog-reply-author {
  font-weight: 600;
  color: #303133;
  font-size: 14px;
}

.dialog-reply-time {
  font-size: 12px;
  color: #8590a6;
}

.dialog-reply-text {
  font-size: 14px;
  color: #1a1a1a;
  line-height: 1.6;
}

.dialog-reply-actions {
  margin-top: 8px;
  display: flex;
  gap: 16px;
}

.dialog-reply-arrow {
  color: #8590a6;
  font-size: 12px;
}
</style>

<style>
.markdown-body {
  font-size: 16px;
  line-height: 1.8;
  color: #303133;
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4,
.markdown-body h5,
.markdown-body h6 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.4;
}

.markdown-body h1 {
  font-size: 28px;
  padding-bottom: 12px;
  border-bottom: 1px solid #ebeef5;
}

.markdown-body h2 {
  font-size: 24px;
  padding-bottom: 8px;
  border-bottom: 1px solid #ebeef5;
}

.markdown-body h3 {
  font-size: 20px;
}

.markdown-body h4 {
  font-size: 18px;
}

.markdown-body p {
  margin-bottom: 16px;
}

.markdown-body a {
  color: #409eff;
  text-decoration: none;
}

.markdown-body a:hover {
  text-decoration: underline;
}

.markdown-body img {
  max-width: 100%;
  border-radius: 8px;
  margin: 16px 0;
}

.markdown-body pre {
  background: #1e1e1e;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 16px 0;
}

.markdown-body code {
  font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
  font-size: 14px;
}

.markdown-body pre code {
  color: #d4d4d4;
}

.markdown-body p code {
  background: #f5f7fa;
  padding: 2px 6px;
  border-radius: 4px;
  color: #e96900;
  font-size: 14px;
}

.markdown-body blockquote {
  border-left: 4px solid #409eff;
  padding: 12px 16px;
  margin: 16px 0;
  background: #ecf5ff;
  color: #606266;
  border-radius: 0 8px 8px 0;
}

.markdown-body ul,
.markdown-body ol {
  padding-left: 24px;
  margin-bottom: 16px;
}

.markdown-body li {
  margin-bottom: 8px;
}

.markdown-body table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
}

.markdown-body th,
.markdown-body td {
  border: 1px solid #ebeef5;
  padding: 12px;
  text-align: left;
}

.markdown-body th {
  background: #f5f7fa;
  font-weight: 600;
}

.markdown-body tr:hover {
  background: #f5f7fa;
}

.markdown-body hr {
  border: none;
  border-top: 1px solid #ebeef5;
  margin: 24px 0;
}

.markdown-body .hljs {
  background: transparent;
}

/* 确保所有 textarea 不能调整大小 */
textarea {
  resize: none !important;
  scrollbar-width: none; /* Firefox */
}

textarea::-webkit-scrollbar {
  display: none; /* Chrome/Safari */
}

/* 确保 Element Plus 的 textarea 不能调整大小 */
.el-textarea__inner {
  resize: none !important;
  scrollbar-width: none; /* Firefox */
}

.el-textarea__inner::-webkit-scrollbar {
  display: none; /* Chrome/Safari */
}

/* 确保评论和回复的 textarea 不能调整大小 */
.comment-form .el-textarea__inner,
.reply-form .el-textarea__inner,
.dialog-reply-form .el-textarea__inner {
  resize: none !important;
  scrollbar-width: none; /* Firefox */
}

.comment-form .el-textarea__inner::-webkit-scrollbar,
.reply-form .el-textarea__inner::-webkit-scrollbar,
.dialog-reply-form .el-textarea__inner::-webkit-scrollbar {
  display: none; /* Chrome/Safari */
}

/* 评论对话框固定位置样式 */
.article-page .el-dialog {
  position: fixed !important;
  top: 50% !important;
  left: 50% !important;
  transform: translate(-50%, -50%) !important;
  margin: 0 !important;
  max-height: 80vh !important;
  display: flex !important;
  flex-direction: column !important;
}

.article-page .el-dialog .el-dialog__header {
  flex-shrink: 0;
}

.article-page .el-dialog .el-dialog__body {
  overflow: hidden !important;
  flex: 1;
  min-height: 0;
  padding: 10px 20px 20px !important;
}
</style>
