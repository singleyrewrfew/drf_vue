/**
 * 全局消息常量
 * 统一管理所有用户提示信息，便于国际化和管理
 */

export const MESSAGES = {
  // 成功消息
  SUCCESS: {
    COMMENT_SUBMITTED: '评论成功',
    REPLY_SUBMITTED: '回复成功',
    COMMENT_LIKED: '点赞成功',
    ARTICLE_LOADED: '文章加载成功'
  },

  // 错误消息
  ERROR: {
    COMMENT_FAILED: '评论失败',
    REPLY_FAILED: '回复失败',
    ARTICLE_NOT_FOUND: '文章不存在',
    NETWORK_ERROR: '网络连接失败，请检查网络设置',
    TIMEOUT: '请求超时，请稍后重试',
    UNAUTHORIZED: '登录已过期，请重新登录',
    FORBIDDEN: '没有权限访问',
    SERVER_ERROR: '服务器错误，请稍后重试',
    VALIDATION_ERROR: '提交的数据有误，请检查后重试',
    UNKNOWN: '发生未知错误，请稍后重试',
    LOAD_COMMENTS_FAILED: '加载评论失败',
    LOAD_ARTICLE_FAILED: '加载文章失败'
  },

  // 提示消息
  INFO: {
    LOGIN_REQUIRED: '请先登录后再进行操作',
    CONTENT_LOADING: '内容加载中...',
    NO_DATA: '暂无数据',
    NO_COMMENTS: '暂无评论',
    NO_RELATED_ARTICLES: '暂无相关文章'
  }
}

export default MESSAGES
