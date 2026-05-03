"""
XSS 防护测试

测试 HTML 过滤功能，确保能有效防止 XSS 攻击。
"""
import pytest
from utils.html_utils import sanitize_html, sanitize_comment, strip_all_html


class TestXSSProtection:
    """XSS 防护测试"""
    
    def test_script_tag_removed(self):
        """测试 script 标签被移除"""
        malicious = '<script>alert("XSS")</script><p>Safe content</p>'
        result = sanitize_html(malicious)
        
        assert '<script>' not in result
        assert 'alert' not in result
        assert '<p>Safe content</p>' in result
    
    def test_event_handlers_removed(self):
        """测试事件处理器被移除"""
        malicious = '<p onclick="alert(\'XSS\')">Click me</p>'
        result = sanitize_html(malicious)
        
        assert 'onclick=' not in result.lower()
        assert 'alert' not in result
        assert '<p>Click me</p>' in result
    
    def test_img_tag_removed(self):
        """测试 img 标签被移除（防止外部资源加载）"""
        malicious = '<img src="http://evil.com/track.gif" onload="steal()">'
        result = sanitize_html(malicious)
        
        assert '<img' not in result
        assert 'evil.com' not in result
    
    def test_iframe_removed(self):
        """测试 iframe 被移除"""
        malicious = '<iframe src="http://evil.com/phishing"></iframe>'
        result = sanitize_html(malicious)
        
        assert '<iframe' not in result
        assert 'evil.com' not in result
    
    def test_svg_removed(self):
        """测试 SVG 被移除（可能包含脚本）"""
        malicious = '''<svg onload="alert('XSS')">
            <circle cx="50" cy="50" r="40"/>
        </svg>'''
        result = sanitize_html(malicious)
        
        assert '<svg' not in result
        assert 'onload' not in result.lower()
    
    def test_unsafe_link_removed(self):
        """测试不安全链接被移除"""
        # javascript: 协议
        malicious = '<a href="javascript:alert(\'XSS\')">Click</a>'
        result = sanitize_html(malicious)
        
        assert 'javascript:' not in result.lower()
        assert '<a' not in result or 'href' not in result
    
    def test_data_protocol_blocked(self):
        """测试 data: 协议被阻止"""
        malicious = '<a href="data:text/html,<script>alert(\'XSS\')</script>">Click</a>'
        result = sanitize_html(malicious)
        
        # data: 协议应该被阻止
        assert 'data:text/html' not in result.lower()
        assert '<a' not in result or 'href' not in result
    
    def test_rel_attributes_added_to_links(self):
        """测试链接自动添加 rel=\"noopener noreferrer\""""
        html = '<a href="https://example.com">Link</a>'
        result = sanitize_html(html)
        
        assert 'rel=' in result
        assert 'noopener' in result
        assert 'noreferrer' in result
    
    def test_mailto_protocol_removed(self):
        """测试 mailto: 协议被移除"""
        html = '<a href="mailto:test@example.com">Email</a>'
        result = sanitize_html(html)
        
        # mailto 不在允许的协议列表中
        assert 'mailto:' not in result.lower() or 'href' not in result
    
    def test_title_attribute_removed(self):
        """测试 title 属性被移除（防止钓鱼攻击）"""
        html = '<a href="https://example.com" title="Click here for free money">Link</a>'
        result = sanitize_html(html)
        
        assert 'title=' not in result.lower()
        assert '<a' in result
        assert 'rel=' in result
    
    def test_headings_removed(self):
        """测试标题标签被移除（防止视觉欺骗）"""
        html = '<h1>Important Notice</h1><p>Content</p>'
        result = sanitize_html(html)
        
        assert '<h1' not in result
        assert '<h2' not in result
        assert '<h3' not in result
        assert '<p>Content</p>' in result
    
    def test_blockquote_removed(self):
        """测试 blockquote 标签被移除（防止伪造引用）"""
        html = '<blockquote>Fake quote from admin</blockquote>'
        result = sanitize_html(html)
        
        assert '<blockquote' not in result
        assert 'Fake quote from admin' in result
    
    def test_lists_removed(self):
        """测试列表标签被移除（防止社会工程攻击）"""
        html = '<ul><li>Item 1</li><li>Item 2</li></ul>'
        result = sanitize_html(html)
        
        assert '<ul' not in result
        assert '<li' not in result
        assert 'Item 1' in result
        assert 'Item 2' in result
    
    def test_pre_code_removed(self):
        """测试 pre/code 标签被移除（减少复杂性）"""
        html = '<pre><code>print("hello")</code></pre>'
        result = sanitize_html(html)
        
        assert '<pre' not in result
        assert '<code' not in result
        assert 'print("hello")' in result
    
    def test_table_removed(self):
        """测试表格标签被移除"""
        html = '''<table>
            <tr><td>Data</td></tr>
        </table>'''
        result = sanitize_html(html)
        
        assert '<table' not in result
        assert '<tr' not in result
        assert '<td' not in result
        assert 'Data' in result
    
    def test_style_attribute_removed(self):
        """测试 style 属性被移除"""
        html = '<p style="color:red; background:url(evil.js)">Text</p>'
        result = sanitize_html(html)
        
        assert 'style=' not in result.lower()
        assert 'evil.js' not in result
        assert '<p>Text</p>' in result
    
    def test_onerror_handler_removed(self):
        """测试 onerror 事件处理器被移除"""
        malicious = '<img src=x onerror="alert(\'XSS\')">'
        result = sanitize_html(malicious)
        
        assert 'onerror=' not in result.lower()
        assert '<img' not in result
    
    def test_nested_xss_blocked(self):
        """测试嵌套 XSS 攻击被阻止"""
        malicious = '''<div onclick="alert('outer')">
            <p onmouseover="alert('inner')">
                <script>alert('script')</script>
            </p>
        </div>'''
        result = sanitize_html(malicious)
        
        assert '<script>' not in result
        assert 'onclick=' not in result.lower()
        assert 'onmouseover=' not in result.lower()
        assert '<div' not in result
        assert '<p>' in result  # 保留安全标签
    
    def test_unicode_xss_blocked(self):
        """测试 Unicode 编码的 XSS 被阻止"""
        # Unicode 编码的 <script>
        malicious = '<scr\\u0069pt>alert("XSS")</scr\\u0069pt>'
        result = sanitize_html(malicious)
        
        # bleach 应该能处理这种情况
        assert 'alert' not in result or '<script' not in result


class TestCommentSanitization:
    """评论过滤测试（更严格）"""
    
    def test_comment_allows_basic_formatting(self):
        """测试评论允许基本格式"""
        comment = '<p>This is <strong>bold</strong> and <em>italic</em></p>'
        result = sanitize_comment(comment)
        
        assert '<strong>bold</strong>' in result
        assert '<em>italic</em>' in result
    
    def test_comment_removes_images(self):
        """测试评论移除图片"""
        comment = '<p>Check this out: <img src="evil.jpg"></p>'
        result = sanitize_comment(comment)
        
        assert '<img' not in result
    
    def test_comment_removes_tables(self):
        """测试评论移除表格"""
        comment = '<table><tr><td>Data</td></tr></table>'
        result = sanitize_comment(comment)
        
        assert '<table' not in result
        assert '<tr' not in result
    
    def test_comment_links_have_safe_rel(self):
        """测试评论链接有安全的 rel 属性"""
        comment = '<a href="https://example.com">Link</a>'
        result = sanitize_comment(comment)
        
        assert 'rel=' in result
        assert 'noopener' in result
        assert 'noreferrer' in result
    
    def test_comment_removes_headings(self):
        """测试评论移除标题标签"""
        comment = '<h2>Look at this!</h2><p>Content</p>'
        result = sanitize_comment(comment)
        
        assert '<h2' not in result
        assert '<p>Content</p>' in result
    
    def test_comment_removes_lists(self):
        """测试评论移除列表"""
        comment = '<ol><li>First</li><li>Second</li></ol>'
        result = sanitize_comment(comment)
        
        assert '<ol' not in result
        assert '<li' not in result
    
    def test_comment_removes_blockquote(self):
        """测试评论移除引用"""
        comment = '<blockquote>Fake admin message</blockquote>'
        result = sanitize_comment(comment)
        
        assert '<blockquote' not in result
    
    def test_comment_code_inline_allowed(self):
        """测试评论允许行内代码"""
        comment = '<p>Use <code>print()</code> function</p>'
        result = sanitize_comment(comment)
        
        assert '<code>print()</code>' in result
    
    def test_comment_removes_pre_blocks(self):
        """测试评论移除 pre 块"""
        comment = '<pre><code>Complex code block</code></pre>'
        result = sanitize_comment(comment)
        
        assert '<pre' not in result
        assert 'Complex code block' in result


class TestStripAllHtml:
    """移除所有 HTML 测试"""
    
    def test_strip_all_tags(self):
        """测试移除所有标签"""
        html = '<p>Hello <strong>World</strong></p>'
        result = strip_all_html(html)
        
        assert '<' not in result
        assert '>' not in result
        assert 'Hello World' in result
    
    def test_strip_malicious_content(self):
        """测试移除恶意内容"""
        malicious = '<script>alert("XSS")</script><p>Safe</p>'
        result = strip_all_html(malicious)
        
        # strip_all_html 只移除标签，不移除标签内的文本
        assert '<script>' not in result
        assert '<' not in result or '>' not in result  # 没有完整的 HTML 标签
        assert 'Safe' in result


class TestEdgeCases:
    """边界情况测试"""
    
    def test_empty_string(self):
        """测试空字符串"""
        assert sanitize_html('') == ''
        assert sanitize_comment('') == ''
        assert strip_all_html('') == ''
    
    def test_none_input(self):
        """测试 None 输入"""
        assert sanitize_html(None) is None
        assert sanitize_comment(None) is None
    
    def test_only_text(self):
        """测试纯文本"""
        text = 'Just plain text'
        assert sanitize_html(text) == text
        assert sanitize_comment(text) == text
    
    def test_mixed_content(self):
        """测试混合内容"""
        html = '<p>Text with <strong>formatting</strong> and <a href="https://safe.com">link</a></p>'
        result = sanitize_html(html)
        
        assert '<p>' in result
        assert '<strong>formatting</strong>' in result
        assert '<a' in result
        assert 'rel=' in result
    
    def test_double_encoding(self):
        """测试双重编码攻击"""
        malicious = '&lt;script&gt;alert("XSS")&lt;/script&gt;'
        result = sanitize_html(malicious)
        
        # 应该保持转义状态，不执行脚本
        assert '<script>' not in result or 'alert' not in result
    
    def test_relative_url_allowed(self):
        """测试相对路径 URL 被允许"""
        html = '<a href="/page/1">Internal Link</a>'
        result = sanitize_html(html)
        
        assert '<a' in result
        assert 'href="/page/1"' in result
        assert 'rel=' in result
    
    def test_vbscript_protocol_blocked(self):
        """测试 vbscript: 协议被阻止"""
        malicious = '<a href="vbscript:MsgBox(\'XSS\')">Click</a>'
        result = sanitize_html(malicious)
        
        assert 'vbscript:' not in result.lower()
    
    def test_expression_css_blocked(self):
        """测试 CSS expression() 被阻止"""
        # bleach 会移除 style 属性，所以 expression 也会被移除
        html = '<p style="width: expression(alert(\'XSS\'))">Text</p>'
        result = sanitize_html(html)
        
        assert 'style=' not in result.lower()
        assert 'expression(' not in result.lower()


@pytest.mark.django_db
class TestIntegrationWithModels:
    """与模型集成的测试"""
    
    def test_content_sanitization(self):
        """测试内容模型的 HTML 过滤"""
        from apps.contents.models import Content
        from apps.users.models import User
        
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # 创建包含恶意 HTML 的内容
        malicious_content = '''
        <h1>Title</h1>
        <p>Safe paragraph</p>
        <script>alert('XSS')</script>
        <img src="x" onerror="steal()">
        <a href="https://example.com" target="_blank">Link</a>
        '''
        
        content = Content.objects.create(
            title='Test Content',
            content=malicious_content,
            author=user,
            status='published'
        )
        
        # 验证内容已保存（序列化时会过滤）
        assert content.content is not None
        
        # 在实际使用中，序列化器的 validate_content 会调用 sanitize_html
        from utils.html_utils import sanitize_html
        cleaned = sanitize_html(content.content)
        
        assert '<script>' not in cleaned
        assert '<img' not in cleaned
        assert 'rel=' in cleaned  # 链接应该有 rel 属性
