export const CONTENT_STATUS = {
  DRAFT: 'draft',
  PUBLISHED: 'published',
  ARCHIVED: 'archived'
}

export const ORDERING_OPTIONS = {
  CREATED_AT_DESC: '-created_at',
  CREATED_AT_ASC: 'created_at',
  VIEW_COUNT_DESC: '-view_count',
  LIKE_COUNT_DESC: '-like_count',
  COMMENT_COUNT_DESC: '-comment_count',
  UPDATED_AT_DESC: '-updated_at',
  UPDATED_AT_ASC: 'updated_at'
}

export const PAGINATION_DEFAULTS = {
  PAGE: 1,
  PAGE_SIZE: 10,
  PAGE_SIZES: [10, 20, 50, 100]
}

export const STORAGE_KEYS = {
  TOKEN: 'front_token',
  REFRESH_TOKEN: 'front_refresh',
  USER: 'front_user',
  THEME: 'theme'
}

export const API_CONTENT_TYPES = {
  ARTICLE: 'contents.Content',
  COMMENT: 'comments.Comment'
}
