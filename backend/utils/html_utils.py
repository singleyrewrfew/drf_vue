"""
HTML 过滤工具

提供安全的 HTML 过滤功能，防止 XSS 攻击。
"""

import re
import bleach
import html

ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'b', 'i', 'u',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li',
    'blockquote', 'pre', 'code',
    'a', 'img',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'hr', 'span', 'div',
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'table': ['class'],
    'th': ['class', 'align'],
    'td': ['class', 'align'],
    'span': ['class'],
    'div': ['class'],
    'pre': ['class'],
    'code': ['class'],
}

ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']

DANGEROUS_TAGS = ['script', 'style', 'iframe', 'object', 'embed', 'form', 'input', 'button', 'meta', 'link', 'base', 'svg', 'math']


def _escape_code_blocks(content: str) -> str:
    """
    转义代码块中的 HTML 标签，使其显示为文本

    将 <pre><code>...</code></pre> 中的 HTML 标签转义为实体
    例如: <script> → &lt;script&gt;

    Args:
        content: HTML 内容

    Returns:
        处理后的内容
    """
    def escape_code_content(match):
        code_content = match.group(1)
        escaped = html.escape(code_content)
        return f'<pre><code>{escaped}</code></pre>'

    pattern = re.compile(
        r'<pre[^>]*><code[^>]*>(.*?)</code></pre>',
        re.IGNORECASE | re.DOTALL
    )
    return pattern.sub(escape_code_content, content)


def _remove_dangerous_tags_with_content(html_str: str) -> str:
    """
    移除危险标签及其内容

    Args:
        html_str: HTML 内容

    Returns:
        移除危险标签后的内容
    """
    for tag in DANGEROUS_TAGS:
        pattern = re.compile(
            rf'<{tag}[^>]*>.*?</{tag}>|<{tag}[^>]*/?>',
            re.IGNORECASE | re.DOTALL
        )
        html_str = pattern.sub('', html_str)
    return html_str


def sanitize_html(content: str, allow_html: bool = True) -> str:
    """
    过滤 HTML 内容，移除危险标签和属性

    Args:
        content: 需要过滤的内容
        allow_html: 是否允许 HTML 标签（默认允许安全标签）

    Returns:
        过滤后的安全内容
    """
    if not content:
        return content

    content = _remove_dangerous_tags_with_content(content)

    if not allow_html:
        return bleach.clean(content, tags=[], attributes={}, strip=True)

    return bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )


def sanitize_comment(content: str) -> str:
    """
    过滤评论内容，允许基本格式和代码块

    允许的标签:
    - 基本格式: p, br, strong, em, b, i, u
    - 链接: a (仅允许 href, title 属性)
    - 代码块: pre, code (代码块中的 HTML 会被转义显示)

    Args:
        content: 评论内容

    Returns:
        过滤后的安全内容
    """
    if not content:
        return content

    content = _escape_code_blocks(content)
    content = _remove_dangerous_tags_with_content(content)

    allowed_tags = ['p', 'br', 'strong', 'em', 'b', 'i', 'u', 'a', 'pre', 'code']
    allowed_attributes = {
        'a': ['href', 'title'],
        'pre': ['class'],
        'code': ['class'],
    }

    return bleach.clean(
        content,
        tags=allowed_tags,
        attributes=allowed_attributes,
        protocols=['http', 'https'],
        strip=True,
    )


def strip_all_html(content: str) -> str:
    """
    移除所有 HTML 标签，只保留纯文本

    Args:
        content: 需要处理的内容

    Returns:
        纯文本内容
    """
    if not content:
        return content

    return bleach.clean(content, tags=[], attributes={}, strip=True)
