"""
HTML 过滤工具

提供安全的 HTML 过滤功能，防止 XSS 攻击。
"""

import re
import bleach
import html
from bleach.linkifier import Linker

# 严格限制的允许标签列表（最小化原则）
# 仅保留最基本的文本格式化标签
ALLOWED_TAGS = [
    'p', 'br', 
    'strong', 'em', 'b', 'i', 'u',  # 基本文本格式
    'a',  # 链接（会强制添加 rel="noopener noreferrer"）
    # 注意：移除了以下标签以减少攻击面：
    # - h1-h6: 可能被用于视觉欺骗/钓鱼
    # - blockquote: 可能被滥用来伪造引用
    # - pre/code: 虽然有转义，但减少不必要的复杂性
    # - ul/ol/li: 列表可能被用于社会工程攻击
    # - img/div/span/table: 高风险标签
]

# 评论场景允许的标签（更严格）
COMMENT_ALLOWED_TAGS = [
    'p', 'br',
    'strong', 'em', 'b', 'i', 'u',
    'a',  # 链接
    'code',  # 行内代码（不包含 pre，避免复杂嵌套）
]

# 严格限制的允许属性（最小化原则）
ALLOWED_ATTRIBUTES = {
    'a': ['href'],  # 只允许 href，移除 title（可能被用于钓鱼）
}

# 评论场景的允许属性
COMMENT_ALLOWED_ATTRIBUTES = {
    'a': ['href'],  # 评论中链接也只允许 href
}

# 严格的协议白名单（仅允许 http/https，禁止所有其他协议）
ALLOWED_PROTOCOLS = ['http', 'https']

# 可选的域名白名单（如果启用，只允许这些域名的链接）
# 设置为 None 或空列表表示不限制域名
# ALLOWED_DOMAINS = ['example.com', 'yourdomain.com']
ALLOWED_DOMAINS = []  # 默认不限制，但可以通过配置启用

# 危险标签列表（用于预清理）
DANGEROUS_TAGS = [
    'script', 'style', 'iframe', 'object', 'embed', 'form', 
    'input', 'button', 'meta', 'link', 'base', 'svg', 'math',
    'video', 'audio', 'source', 'track',  # 媒体标签
    'applet', 'canvas', 'dialog',  # 其他潜在危险标签
]


def _is_safe_url(url: str) -> bool:
    """
    验证 URL 是否安全
    
    Args:
        url: 需要验证的 URL
    
    Returns:
        bool: URL 是否安全
    """
    if not url:
        return False
    
    # 检查是否是相对路径（以 / 开头但不以 // 开头）
    if url.startswith('/') and not url.startswith('//'):
        return True
    
    # 解析 URL
    from urllib.parse import urlparse
    try:
        parsed = urlparse(url)
        
        # 必须有有效的 scheme 和 netloc
        if parsed.scheme not in ['http', 'https']:
            return False
        
        if not parsed.netloc:
            return False
        
        # 如果配置了域名白名单，进行检查
        if ALLOWED_DOMAINS:
            domain = parsed.netloc.lower()
            # 移除端口号
            if ':' in domain:
                domain = domain.split(':')[0]
            
            # 检查是否在白名单中（支持子域名匹配）
            is_allowed = any(
                domain == allowed_domain or domain.endswith('.' + allowed_domain)
                for allowed_domain in ALLOWED_DOMAINS
            )
            if not is_allowed:
                return False
        
        return True
    except Exception:
        return False


def _add_safe_rel_attributes(attrs, new=False):
    """
    为所有外链自动添加安全的 rel 属性
    
    防止 tabnabbing 攻击和反向 tabnabbing。
    
    Args:
        attrs: 属性字典
        new: 是否是新创建的链接
    
    Returns:
        更新后的属性字典，如果不安全则返回 None
    """
    # 验证 URL 安全性
    href = attrs.get('href', '')
    if href and not _is_safe_url(href):
        return None  # 不安全的 URL，移除该链接
    
    # 强制添加 noopener 和 noreferrer
    attrs['rel'] = 'noopener noreferrer'
    
    return attrs


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


def sanitize_html(content: str, allow_html: bool = True, strip_unsafe_links: bool = True) -> str:
    """
    过滤 HTML 内容，移除危险标签和属性
    
    安全特性：
    1. 移除所有危险标签（script, iframe, svg 等）
    2. 只允许基本文本格式标签（p, br, strong, em, b, i, u, a）
    3. 自动为链接添加 rel="noopener noreferrer"
    4. 仅允许 http/https 协议
    5. 移除所有事件处理器和危险属性
    6. 可选：验证链接域名白名单
    7. 移除 title 属性（防止钓鱼攻击）

    Args:
        content: 需要过滤的内容
        allow_html: 是否允许 HTML 标签（默认允许安全标签）
        strip_unsafe_links: 是否移除不安全的链接（默认True）

    Returns:
        过滤后的安全内容
    """
    if not content:
        return content

    # 第 1 步：预清理 - 移除危险标签及其内容
    content = _remove_dangerous_tags_with_content(content)

    if not allow_html:
        return bleach.clean(content, tags=[], attributes={}, strip=True)

    # 第 2 步：使用 bleach 进行严格过滤，使用回调验证链接
    cleaned = bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes={'a': ['href']} if strip_unsafe_links else ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )
    
    # 第 3 步：为所有链接添加安全的 rel 属性并验证 URL
    if '<a ' in cleaned.lower():
        def process_link(match):
            link_tag = match.group(0)
            
            # 提取 href
            href_match = re.search(r'href=["\']([^"\']*)["\']', link_tag, re.IGNORECASE)
            if href_match:
                href = href_match.group(1)
                # 验证 URL 安全性
                if strip_unsafe_links and not _is_safe_url(href):
                    # 不安全的链接，只保留文本内容
                    text_match = re.search(r'>([^<]*)<', link_tag)
                    return text_match.group(1) if text_match else ''
            
            # 安全的链接，添加 rel 属性
            if 'rel=' not in link_tag.lower():
                link_tag = link_tag.replace('<a ', '<a rel="noopener noreferrer" ', 1)
            else:
                # 确保 rel 包含必要值
                link_tag = re.sub(
                    r'rel=["\'][^"\']*["\']',
                    'rel="noopener noreferrer"',
                    link_tag,
                    flags=re.IGNORECASE
                )
            
            # 移除 title 属性（防止钓鱼）
            link_tag = re.sub(
                r'\s+title=["\'][^"\']*["\']',
                '',
                link_tag,
                flags=re.IGNORECASE
            )
            
            return link_tag
        
        cleaned = re.sub(r'<a\s[^>]*>.*?</a>', process_link, cleaned, flags=re.IGNORECASE | re.DOTALL)
    
    return cleaned


def sanitize_comment(content: str, strip_unsafe_links: bool = True) -> str:
    """
    过滤评论内容，允许基本格式和行内代码
    
    比 sanitize_html 更严格，适用于用户评论场景。

    允许的标签:
    - 基本格式: p, br, strong, em, b, i, u
    - 链接: a (自动添加 rel="noopener noreferrer"，可配置域名白名单)
    - 行内代码: code (不包含 pre，避免复杂嵌套)
    
    禁止的标签:
    - 所有媒体标签 (img, video, audio)
    - 所有布局标签 (div, span, table)
    - 所有脚本相关标签
    - 标题标签 (h1-h6，防止视觉欺骗)
    - 列表标签 (ul, ol, li，防止社会工程攻击)
    - 引用标签 (blockquote，防止伪造引用)

    Args:
        content: 评论内容
        strip_unsafe_links: 是否移除不安全的链接（默认True）

    Returns:
        过滤后的安全内容
    """
    if not content:
        return content
    
    # 预清理危险标签
    content = _remove_dangerous_tags_with_content(content)

    # 评论场景使用更严格的标签白名单
    allowed_attributes = COMMENT_ALLOWED_ATTRIBUTES

    # 严格过滤
    cleaned = bleach.clean(
        content,
        tags=COMMENT_ALLOWED_TAGS,
        attributes=allowed_attributes,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )
    
    # 为链接添加安全属性并验证 URL
    if '<a ' in cleaned.lower():
        def process_link(match):
            link_tag = match.group(0)
            full_match = match.group(0)
            
            # 提取 href
            href_match = re.search(r'href=["\']([^"\']*)["\']', link_tag, re.IGNORECASE)
            if href_match:
                href = href_match.group(1)
                # 验证 URL 安全性
                if strip_unsafe_links and not _is_safe_url(href):
                    # 不安全的链接，只保留文本内容
                    text_match = re.search(r'>([^<]*)<', full_match)
                    return text_match.group(1) if text_match else ''
            
            # 安全的链接，添加 rel 属性
            if 'rel=' not in link_tag.lower():
                link_tag = link_tag.replace('<a ', '<a rel="noopener noreferrer" ', 1)
            
            # 移除 title 属性
            link_tag = re.sub(
                r'\s+title=["\'][^"\']*["\']',
                '',
                link_tag,
                flags=re.IGNORECASE
            )
            
            return link_tag
        
        cleaned = re.sub(r'<a\s[^>]*>.*?</a>', process_link, cleaned, flags=re.IGNORECASE | re.DOTALL)
    
    return cleaned


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
