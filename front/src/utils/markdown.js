/**
 * Markdown 渲染工具函数
 * 统一封装 marked + DOMPurify 配置，避免重复代码
 */

import { marked } from 'marked'
import hljs from 'highlight.js'
import DOMPurify from 'dompurify'

// DOMPurify 允许的 HTML 标签白名单
const ALLOWED_TAGS = [
  'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
  'p', 'br', 'hr',
  'ul', 'ol', 'li',
  'blockquote', 'pre', 'code', 'strong', 'em',
  'a', 'img',
  'table', 'thead', 'tbody', 'tr', 'th', 'td',
  'span', 'div'
]

// DOMPurify 允许的 HTML 属性白名单
const ALLOWED_ATTR = [
  'href', 'src', 'alt', 'title', 'class', 'id', 'target', 'rel'
]

/**
 * 配置 marked 选项
 */
function configureMarked() {
  marked.setOptions({
    highlight(code, lang) {
      if (lang && hljs.getLanguage(lang)) {
        try {
          return hljs.highlight(code, { language: lang }).value
        } catch (e) {
          console.error('Highlight error:', e)
        }
      }
      return hljs.highlightAuto(code).value
    },
    breaks: true,
    gfm: true
  })
}

/**
 * 渲染 Markdown 内容为安全的 HTML
 * @param {string} content - Markdown 格式的文本内容
 * @returns {string} - 经过消毒的安全 HTML 字符串
 */
export function renderMarkdown(content) {
  if (!content) return ''

  configureMarked()

  const rawHtml = marked.parse(content)
  const safeHtml = DOMPurify.sanitize(rawHtml, {
    ALLOWED_TAGS,
    ALLOWED_ATTR
  })

  return safeHtml
}

/**
 * 从 Markdown 内容中提取标题列表（用于生成目录）
 * @param {string} content - Markdown 格式的文本内容
 * @param {number} maxLevel - 最大标题级别（默认为 3）
 * @returns {Array<{id: string, level: number, text: string}>}
 */
export function extractHeadings(content, maxLevel = 3) {
  if (!content) return []

  const result = []
  const idCounters = {}

  // 移除代码块，避免误匹配
  const contentWithoutCodeBlocks = content
    .replace(/```[\s\S]*?```/g, '')
    .replace(/~~~[\s\S]*?~~~/g, '')

  // 匹配 Markdown 标题
  const headingRegex = /^(#{1,6})\s+(.+)$/gm
  let match

  while ((match = headingRegex.exec(contentWithoutCodeBlocks)) !== null) {
    const level = match[1].length

    // 只提取指定级别以内的标题
    if (level > maxLevel) continue

    let text = match[2].trim()

    // 清理 Markdown 格式符号
    text = text
      .replace(/\*\*(.+?)\*\*/g, '$1')
      .replace(/\*(.+?)\*/g, '$1')
      .replace(/__(.+?)__/g, '$1')
      .replace(/_(.+?)_/g, '$1')
      .replace(/`(.+?)`/g, '$1')
      .replace(/\[(.+?)\]\(.+?\)/g, '$1')
      .replace(/!\[(.+?)\]\(.+?\)/g, '$1')
      .trim()

    // 过滤空标题和过长标题
    if (text && text.length < 200) {
      const baseId = text
        .toLowerCase()
        .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
        .replace(/^-+|-+$/g, '')

      if (idCounters[baseId] === undefined) {
        idCounters[baseId] = 0
      } else {
        idCounters[baseId]++
      }

      const id = idCounters[baseId] === 0 ? baseId : `${baseId}-${idCounters[baseId]}`

      result.push({
        id,
        level,
        text
      })
    }
  }

  return result
}

export default {
  renderMarkdown,
  extractHeadings
}
