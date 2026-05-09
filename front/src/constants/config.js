/**
 * 全局配置常量
 * 统一管理所有硬编码的配置值
 */

export const CONFIG = {
  // API 相关配置
  API: {
    DEFAULT_PAGE_SIZE: 10,
    RELATED_ARTICLES_COUNT: 5,
    INITIAL_COMMENTS_COUNT: 2,
    CONTENT_PREVIEW_LENGTH: 5000
  },

  // 时间相关配置（毫秒）
  TIMING: {
    PROFILE_CHECK_INTERVAL: 300000, // 5分钟用户资料检查间隔
    DEBOUNCE_DELAY: 300,           // 防抖延迟
    THROTTLE_DELAY: 100,           // 节流延迟
    ANIMATION_DURATION: 250,       // 动画持续时间
    TOAST_DISPLAY_TIME: 3000       // 提示显示时间
  },

  // UI 配置
  UI: {
    SIDEBAR_WIDTH: '280px',
    MAX_SIDEBAR_WIDTH: '80vw',
    HEADER_HEIGHT: 72,
    SCROLL_OFFSET: 88,             // 滚动偏移量（header高度 + padding）
    MOBILE_BREAKPOINT: 768,        // 移动端断点
    TABLET_BREAKPOINT: 992,         // 平板断点
    SMALL_MOBILE_BREAKPOINT: 576   // 小屏手机断点
  },

  // 内容渲染配置
  RENDERING: {
    MAX_HEADING_LEVEL: 3,          // 目录最大标题级别
    MAX_TITLE_LENGTH: 200,          // 标题最大长度
    MARKDOWN_IMAGE_MAX_WIDTH: '100%'
  }
}

export default CONFIG
