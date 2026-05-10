import { marked } from 'marked'
import hljs from 'highlight.js'
import DOMPurify from 'dompurify'

let markedConfigured = false

function configureMarked() {
  if (markedConfigured) return
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
  markedConfigured = true
}

const ALLOWED_TAGS = [
  'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
  'p', 'br', 'hr',
  'ul', 'ol', 'li',
  'blockquote', 'pre', 'code', 'strong', 'em',
  'a', 'img',
  'table', 'thead', 'tbody', 'tr', 'th', 'td',
  'span', 'div',
  'button'
]

const ALLOWED_ATTR = [
  'href', 'src', 'alt', 'title', 'class', 'id', 'target', 'rel',
  'loading', 'data-clipboard-text'
]

export function generateHeadingId(text) {
  const baseId = text
    .toLowerCase()
    .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
    .replace(/^-+|-+$/g, '')

  return baseId || 'heading'
}

export function addHeadingIds(html) {
  const tempDiv = document.createElement('div')
  tempDiv.innerHTML = html

  const idCounters = {}
  const headingElements = tempDiv.querySelectorAll('h1, h2, h3, h4, h5, h6')

  headingElements.forEach(el => {
    const text = el.textContent.trim()
    const baseId = generateHeadingId(text)

    if (idCounters[baseId] === undefined) {
      idCounters[baseId] = 0
    } else {
      idCounters[baseId]++
    }

    const id = idCounters[baseId] === 0 ? baseId : `${baseId}-${idCounters[baseId]}`
    el.id = id
  })

  return tempDiv.innerHTML
}

function processExternalLinks(html) {
  const tempDiv = document.createElement('div')
  tempDiv.innerHTML = html

  const links = tempDiv.querySelectorAll('a[href]')
  links.forEach(link => {
    const href = link.getAttribute('href')
    if (href && (href.startsWith('http://') || href.startsWith('https://'))) {
      if (!link.hasAttribute('target')) {
        link.setAttribute('target', '_blank')
      }
      link.setAttribute('rel', 'noopener noreferrer')
    }
  })

  return tempDiv.innerHTML
}

function processImages(html) {
  const tempDiv = document.createElement('div')
  tempDiv.innerHTML = html

  const images = tempDiv.querySelectorAll('img')
  images.forEach(img => {
    if (!img.hasAttribute('loading')) {
      img.setAttribute('loading', 'lazy')
    }
  })

  return tempDiv.innerHTML
}

export function renderMarkdown(content) {
  if (!content) return ''

  configureMarked()

  let html = marked.parse(content)
  html = addHeadingIds(html)
  html = processExternalLinks(html)
  html = processImages(html)

  const safeHtml = DOMPurify.sanitize(html, {
    ALLOWED_TAGS,
    ALLOWED_ATTR
  })

  return safeHtml
}

const MARKDOWN_CLEANUP_RULES = [
  { pattern: /\*\*(.+?)\*\*/g, replacement: '$1' },
  { pattern: /\*(?=\S)(.+?)(?<=\S)\*/g, replacement: '$1' },
  { pattern: /__(.+?)__/g, replacement: '$1' },
  { pattern: /_(?=\S)(.+?)(?<=\S)_/g, replacement: '$1' },
  { pattern: /~~(.+?)~~/g, replacement: '$1' },
  { pattern: /==(.+?)==/g, replacement: '$1' },
  { pattern: /`(.+?)`/g, replacement: '$1' },
  { pattern: /\[(.+?)\]\(.+?\)/g, replacement: '$1' },
  { pattern: /!\[(.*?)\]\(.+?\)/g, replacement: '$1' },
  { pattern: /^\s*\[x\]\s+/gm, replacement: '' },
  { pattern: /^\s*\[\s]\s+/gm, replacement: '' },
  { pattern: /<[^>]+>/g, replacement: '' },
  { pattern: /&[a-zA-Z]+;/g, replacement: '' },
  { pattern: /\s{2,}/g, replacement: ' ' }
]

export function extractHeadings(content, maxLevel = 3) {
  if (!content) return []

  const result = []
  const idCounters = {}

  let processedContent = content
    .replace(/```[\s\S]*?```/g, '')
    .replace(/~~~[\s\S]*?~~~/g, '')

  const headingRegex = /^(#{1,6})\s+(.+?)\s*#*$/gm
  let match

  while ((match = headingRegex.exec(processedContent)) !== null) {
    const level = match[1].length

    if (level > maxLevel) continue

    let text = match[2].trim()

    for (const rule of MARKDOWN_CLEANUP_RULES) {
      text = text.replace(rule.pattern, rule.replacement)
    }

    text = text.trim()

    if (!text || text.length < 1 || text.length > 200) continue

    const baseId = generateHeadingId(text)

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

  return result
}

export default {
  renderMarkdown,
  extractHeadings,
  generateHeadingId,
  addHeadingIds
}
