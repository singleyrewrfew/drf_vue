"""
文件验证工具

提供基于文件内容的真实 MIME 类型验证，防止 MIME 类型伪造攻击。
"""
import logging
import magic
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


def validate_file_mime_type(file, allowed_types):
    """
    验证文件的真实 MIME 类型（基于文件内容而非扩展名或 Content-Type）
    
    使用 libmagic 库读取文件魔数（magic bytes）来确定真实类型，
    防止攻击者通过修改文件扩展名或 Content-Type 头部来上传恶意文件。
    
    Args:
        file: Django UploadedFile 对象
        allowed_types: 允许的 MIME 类型列表，如 ['image/jpeg', 'image/png']
    
    Returns:
        str: 检测到的真实 MIME 类型
    
    Raises:
        ValidationError: 如果文件类型不在允许列表中
    
    Example:
        >>> validate_file_mime_type(uploaded_file, ['image/jpeg', 'image/png'])
        'image/jpeg'
    """
    if not file:
        raise ValidationError('文件不能为空')
    
    try:
        # 读取文件前 2048 字节用于检测（足够识别大多数文件格式）
        file_header = file.read(2048)
        file.seek(0)  # 重置文件指针，确保后续操作正常
        
        if not file_header:
            raise ValidationError('文件内容为空')
        
        # 使用 libmagic 检测真实 MIME 类型
        detected_mime = magic.from_buffer(file_header, mime=True)
        
        logger.info(f"Detected MIME type: {detected_mime} (declared: {file.content_type})")
        
        # 检查是否在白名单中
        if detected_mime not in allowed_types:
            logger.warning(
                f"File type mismatch: declared={file.content_type}, "
                f"detected={detected_mime}, allowed={allowed_types}"
            )
            raise ValidationError(
                f'不支持的文件类型: {detected_mime}。'
                f'请上传以下类型的文件: {", ".join(allowed_types)}'
            )
        
        # 额外检查：如果声明的类型与检测的类型不一致，记录警告
        if file.content_type and detected_mime != file.content_type:
            logger.warning(
                f"MIME type mismatch detected! "
                f"Declared: {file.content_type}, Actual: {detected_mime}. "
                f"This could be a security risk."
            )
        
        return detected_mime
    
    except ValidationError:
        # 重新抛出验证错误
        raise
    except Exception as e:
        logger.error(f"Failed to validate file MIME type: {type(e).__name__}: {e}", exc_info=True)
        raise ValidationError(f'文件验证失败: {str(e)}')


def validate_image_file(file):
    """
    验证图片文件
    
    Args:
        file: Django UploadedFile 对象
    
    Returns:
        str: 检测到的 MIME 类型
    
    Raises:
        ValidationError: 如果不是有效的图片文件
    """
    from django.conf import settings
    
    allowed_types = getattr(settings, 'ALLOWED_IMAGE_TYPES', [
        'image/jpeg', 'image/png', 'image/gif', 'image/webp'
    ])
    
    return validate_file_mime_type(file, allowed_types)


def validate_video_file(file):
    """
    验证视频文件
    
    Args:
        file: Django UploadedFile 对象
    
    Returns:
        str: 检测到的 MIME 类型
    
    Raises:
        ValidationError: 如果不是有效的视频文件
    """
    from django.conf import settings
    
    allowed_types = getattr(settings, 'ALLOWED_VIDEO_TYPES', [
        'video/mp4', 'video/webm', 'video/ogg'
    ])
    
    return validate_file_mime_type(file, allowed_types)


def validate_document_file(file):
    """
    验证文档文件
    
    Args:
        file: Django UploadedFile 对象
    
    Returns:
        str: 检测到的 MIME 类型
    
    Raises:
        ValidationError: 如果不是有效的文档文件
    """
    from django.conf import settings
    
    allowed_types = getattr(settings, 'ALLOWED_DOCUMENT_TYPES', [
        'application/pdf', 'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ])
    
    return validate_file_mime_type(file, allowed_types)


def sanitize_svg(svg_content):
    """
    清洗 SVG 文件内容，移除潜在的 XSS 攻击向量
    
    SVG 文件可能包含 JavaScript，需要特别处理。
    
    Args:
        svg_content: SVG 文件内容字符串
    
    Returns:
        str: 清洗后的 SVG 内容
    
    Raises:
        ValidationError: 如果 SVG 包含危险内容
    """
    import re
    from utils.html_utils import _remove_dangerous_tags_with_content
    
    # 移除 script 标签及其内容
    svg_content = re.sub(
        r'<script[^>]*>.*?</script>',
        '',
        svg_content,
        flags=re.IGNORECASE | re.DOTALL
    )
    
    # 移除事件处理器属性 (onclick, onerror, onload 等)
    svg_content = re.sub(
        r'\s+on\w+\s*=\s*(["\']).*?\1',
        '',
        svg_content,
        flags=re.IGNORECASE
    )
    
    # 移除 javascript: 协议
    svg_content = re.sub(
        r'javascript\s*:',
        '',
        svg_content,
        flags=re.IGNORECASE
    )
    
    # 移除 data: 协议（可能包含嵌入式脚本）
    svg_content = re.sub(
        r'data\s*:[^"\'>\s]+',
        '',
        svg_content,
        flags=re.IGNORECASE
    )
    
    return svg_content
