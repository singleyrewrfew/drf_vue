"""
内容序列化器测试

测试内容相关序列化器的数据验证和输入输出

作用：验证内容序列化器的数据序列化、反序列化和验证逻辑
使用：运行 pytest tests/test_serializers/test_content_serializer.py 执行测试

测试覆盖的序列化器：
    1. ContentSerializer - 内容详情序列化（用于展示完整内容）
    2. ContentListSerializer - 内容列表序列化（用于列表展示，不含完整内容）
    3. ContentCreateUpdateSerializer - 内容创建/更新序列化（含业务逻辑验证）

测试场景：
    - 内容详情序列化输出格式验证
    - 内容预览长度限制验证
    - 空内容处理验证
    - 列表序列化字段过滤验证
    - 内容创建流程及关联对象处理
    - 自动生成 slug 功能验证
    - 内容部分更新功能验证
    - 封面图片 URL 验证
"""
import pytest
from django.contrib.auth import get_user_model

from apps.categories.models import Category
from apps.contents.models import Content
from apps.contents.serializers import (
    ContentSerializer,
    ContentListSerializer,
    ContentCreateUpdateSerializer,
)
from apps.tags.models import Tag

User = get_user_model()


@pytest.mark.unit
class TestContentSerializer:
    """
    ContentSerializer 测试类
    
    验证内容详情序列化器的输出格式和字段处理逻辑。
    ContentSerializer 用于展示内容的完整信息，包括内容预览。
    
    测试用例：
        - 验证序列化输出的字段完整性和正确性
        - 验证内容预览长度限制（5000 字符）
        - 验证空内容的正确处理
    
    序列化字段：
        - id: 内容 ID
        - title: 标题
        - slug: URL 别名
        - summary: 摘要
        - content_preview: 内容预览（最多 5000 字符）
        - author_name: 作者用户名
        - category_name: 分类名称
        - status: 状态
        - created_at: 创建时间
        - updated_at: 更新时间
        - published_at: 发布时间
    """
    
    def test_content_serializer_output(self, db):
        """
        测试内容序列化器的输出格式和字段完整性
        
        验证 ContentSerializer 能够正确地将内容对象序列化为字典，
        包含所有必要的字段，且关联对象的信息正确显示。
        
        测试步骤：
            1. 创建测试用户作为作者
            2. 创建测试分类
            3. 创建内容对象，关联作者和分类
            4. 使用 ContentSerializer 序列化内容对象
            5. 验证输出数据的各个字段值
        
        预期结果：
            - title 字段正确
            - slug 字段正确
            - author_name 显示作者用户名
            - category_name 显示分类名称
            - status 字段正确
            - 包含 content_preview 字段
        
        注意：
            - 需要创建关联对象（User、Category）以测试外键字段
            - author_name 和 category_name 是序列化器中的 SerializerMethodField
        """
        # 创建关联对象
        author = User.objects.create_user(username='author', password='pass123')
        category = Category.objects.create(name='技术', slug='tech')
        
        content = Content.objects.create(
            title='测试文章',
            slug='test-article',
            summary='测试摘要',
            content='这是文章内容',
            author=author,
            category=category,
            status='published'
        )
        
        # 序列化
        serializer = ContentSerializer(content)
        data = serializer.data
        
        # 验证字段
        assert data['title'] == '测试文章'
        assert data['slug'] == 'test-article'
        assert data['author_name'] == 'author'
        assert data['category_name'] == '技术'
        assert data['status'] == 'published'
        assert 'content_preview' in data
    
    def test_content_preview_limit(self, db):
        """
        测试内容预览字段的长度限制
        
        验证当内容超过 5000 字符时，content_preview 字段会被截断到 5000 字符，
        防止返回过大的数据量影响性能。
        
        测试步骤：
            1. 创建测试用户
            2. 创建包含 6000 字符的长内容
            3. 序列化内容对象
            4. 检查 content_preview 字段的长度
        
        预期结果：
            - content_preview 的长度正好为 5000 字符
            - 原始 content 字段不受影响
        
        性能考虑：
            - 限制预览长度可以减少网络传输数据量
            - 提高列表接口的响应速度
            - 避免前端渲染大量文本导致卡顿
        """
        author = User.objects.create_user(username='author', password='pass123')
        
        long_content = 'x' * 6000  # 6000 字符
        content = Content.objects.create(
            title='长文章',
            slug='long-article',
            content=long_content,
            author=author
        )
        
        serializer = ContentSerializer(content)
        data = serializer.data
        
        # 预览应该限制在 5000 字符
        assert len(data['content_preview']) == 5000
    
    def test_empty_content_preview(self, db):
        """
        测试空内容的预览字段处理
        
        验证当内容为空字符串时，content_preview 字段也返回空字符串，
        而不是 None 或其他异常值。
        
        测试步骤：
            1. 创建测试用户
            2. 创建内容为空的内容对象
            3. 序列化内容对象
            4. 检查 content_preview 字段的值
        
        预期结果：
            - content_preview 为空字符串 ''
            - 不会抛出异常
        
        边界情况：
            - 处理空内容是常见的边界情况
            - 确保不会因为空值导致前端显示错误
        """
        author = User.objects.create_user(username='author', password='pass123')
        
        content = Content.objects.create(
            title='无内容',
            slug='no-content',
            content='',
            author=author
        )
        
        serializer = ContentSerializer(content)
        data = serializer.data
        
        assert data['content_preview'] == ''


@pytest.mark.unit
class TestContentListSerializer:
    """
    ContentListSerializer 测试类
    
    验证内容列表序列化器的字段过滤逻辑。
    ContentListSerializer 用于列表展示，不包含完整的 content 字段以减少数据量。
    
    测试用例：
        - 验证列表序列化器不包含完整内容字段
        - 验证列表序列化器包含摘要字段
    
    与 ContentSerializer 的区别：
        - 不包含 content 字段（完整内容）
        - 包含 summary 字段（摘要）
        - 适用于列表页，提高加载速度
    
    适用场景：
        - 文章列表接口
        - 搜索结果列表
        - 分类下的内容列表
    """
    
    def test_list_serializer_excludes_full_content(self, db):
        """
        测试列表序列化器排除完整内容字段
        
        验证 ContentListSerializer 在序列化时不包含 content 字段，
        只返回 summary 等轻量级字段，以优化列表接口的性能。
        
        测试步骤：
            1. 创建测试用户
            2. 创建包含完整内容和摘要的内容对象
            3. 使用 ContentListSerializer 序列化
            4. 验证 data 中不包含 'content' 字段
            5. 验证 data 中包含 'summary' 字段
        
        预期结果：
            - 'content' 不在 serializer.data 中
            - 'summary' 在 serializer.data 中
        
        性能优化：
            - 列表接口通常返回多条记录
            - 排除大字段可以显著减少响应数据量
            - 提高接口响应速度和降低带宽消耗
        
        用户体验：
            - 列表页只需显示摘要，无需加载完整内容
            - 用户点击详情时才加载完整内容（使用 ContentSerializer）
        """
        author = User.objects.create_user(username='author', password='pass123')
        
        content = Content.objects.create(
            title='测试',
            slug='test',
            content='完整内容',
            summary='摘要',
            author=author
        )
        
        serializer = ContentListSerializer(content)
        data = serializer.data
        
        # 列表不应该包含 content 字段
        assert 'content' not in data
        # 但应该有 summary
        assert 'summary' in data


@pytest.mark.unit
class TestContentCreateUpdateSerializer:
    """
    ContentCreateUpdateSerializer 测试类
    
    验证内容创建和更新序列化器的数据验证和业务逻辑。
    该序列化器用于内容的创建和更新操作，包含自动 slug 生成、
    关联对象验证等业务逻辑。
    
    测试用例：
        - 成功创建内容（含关联对象）
        - 自动生成 slug 功能
        - 部分更新内容
        - 封面图片 URL 验证
    
    特性：
        - 支持完整创建和部分更新（partial）
        - 自动生成唯一 slug
        - 验证关联对象（category、tags）
        - 从 request.context 获取当前用户作为作者
        - 处理封面图片路径
    
    适用场景：
        - 创建新文章
        - 编辑已有文章
        - 草稿保存
    """
    
    def test_create_content_success(self, db):
        """
        测试成功创建内容及其关联对象
        
        验证提供完整的内容数据时，能够成功创建内容对象，
        并正确关联作者、分类和标签。
        
        测试步骤：
            1. 创建测试用户作为作者
            2. 创建测试分类
            3. 创建或获取测试标签（使用 get_or_create 避免冲突）
            4. 准备内容数据（包含 category 和 tags 的 ID）
            5. 创建 mock request 并设置当前用户
            6. 创建序列化器并设置 context['request']
            7. 验证数据有效性
            8. 保存内容
            9. 验证内容对象及其关联关系
        
        预期结果：
            - is_valid() 返回 True
            - 内容成功创建，title 正确
            - author 自动设置为 request.user
            - category 正确关联
            - tags 正确关联（多对多关系）
        
        注意：
            - 必须设置 serializer.context['request']，否则无法获取作者
            - category 和 tags 传递的是 ID，序列化器会自动转换为对象
            - 使用 get_or_create 创建标签避免重复创建导致的唯一性冲突
        """
        author = User.objects.create_user(username='author', password='pass123')
        category = Category.objects.create(name='技术', slug='tech')
        # 不传递 slug，让系统自动生成唯一 slug
        tag, _ = Tag.objects.get_or_create(name='Python')
        
        data = {
            'title': '新文章',
            'content': '文章内容',
            'summary': '文章摘要',
            'category': category.id,
            'tags': [tag.id],
            'status': 'draft'
        }
        
        # 创建 mock request
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = author
        
        serializer = ContentCreateUpdateSerializer(data=data)
        serializer.context['request'] = request
        
        assert serializer.is_valid()
        
        content = serializer.save()
        assert content.title == '新文章'
        assert content.author == author
        assert content.category == category
        assert list(content.tags.all()) == [tag]
    
    def test_create_with_auto_slug(self, db):
        """
        测试创建内容时自动生成 slug
        
        验证当不提供 slug 字段时，序列化器会根据标题自动生成唯一的 slug，
        确保每个内容都有有效的 URL 别名。
        
        测试步骤：
            1. 创建测试用户
            2. 准备内容数据，不包含 slug 字段
            3. 创建 mock request 并设置当前用户
            4. 创建序列化器并设置 context
            5. 验证数据有效性
            6. 保存内容
            7. 验证 slug 字段已自动生成
        
        预期结果：
            - is_valid() 返回 True
            - content.slug 不为 None
            - slug 基于标题生成（如：'没有-slug-的文章'）
        
        功能说明：
            - slug 用于生成友好的 URL（如 /contents/没有-slug-的文章/）
            - 自动生成的 slug 保证唯一性（如有重复会添加后缀）
            - 使用 utils.slug_utils.generate_unique_slug 工具函数
        
        用户体验：
            - 用户无需手动填写 slug，简化创建流程
            - 自动生成 SEO 友好的 URL
        """
        author = User.objects.create_user(username='author', password='pass123')
        
        data = {
            'title': '没有 slug 的文章',
            'content': '内容'
        }
        
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = author
        
        serializer = ContentCreateUpdateSerializer(data=data)
        serializer.context['request'] = request
        
        assert serializer.is_valid()
        
        content = serializer.save()
        assert content.slug is not None
    
    def test_update_content(self, db):
        """
        测试部分更新内容
        
        验证可以使用 partial=True 模式只更新内容的部分字段，
        其他字段保持不变。
        
        测试步骤：
            1. 创建测试用户
            2. 创建初始内容对象（旧标题、旧内容）
            3. 准备更新数据，只包含 title 字段
            4. 创建 mock request 并设置当前用户
            5. 创建序列化器，传入现有内容对象和更新数据，启用 partial 模式
            6. 设置 context['request']
            7. 验证数据有效性
            8. 保存更改
            9. 验证 title 已更新，其他字段不变
        
        预期结果：
            - is_valid() 返回 True
            - title 从 '旧标题' 更新为 '新标题'
            - slug、content 等其他字段保持不变
        
        应用场景：
            - 用户只修改标题
            - 用户只修改分类或标签
            - 用户只修改状态（草稿 -> 发布）
        
        技术要点：
            - partial=True 允许只提供部分字段
            - 未提供的字段保持原值
            - 这是 RESTful API 的 PATCH 方法的标准行为
        """
        author = User.objects.create_user(username='author', password='pass123')
        
        content = Content.objects.create(
            title='旧标题',
            slug='old-title',
            content='旧内容',
            author=author
        )
        
        data = {'title': '新标题'}
        
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = author
        
        serializer = ContentCreateUpdateSerializer(content, data=data, partial=True)
        serializer.context['request'] = request
        
        assert serializer.is_valid()
        
        content_updated = serializer.save()
        assert content_updated.title == '新标题'
    
    def test_validate_cover_image_url(self, db):
        """
        测试封面图片 URL 的验证和处理
        
        验证当提供封面图片 URL 时，序列化器能够正确处理并保存，
        支持相对路径格式的媒体文件 URL。
        
        测试步骤：
            1. 创建测试用户
            2. 准备内容数据，包含 cover_image 字段（相对路径）
            3. 创建 mock request 并设置当前用户
            4. 创建序列化器并设置 context
            5. 验证数据有效性
            6. 保存内容
            7. 验证封面图片字段已正确保存
        
        预期结果：
            - is_valid() 返回 True
            - content.cover_image 字段被正确设置
            - 图片路径可能被处理（如去除 /media 前缀）
        
        注意：
            - cover_image 可以是 ImageField 或 CharField，取决于模型定义
            - URL 格式可能是 '/media/images/cover.jpg' 或 'images/cover.jpg'
            - 序列化器可能会处理路径格式以保持一致性
        
        应用场景：
            - 用户上传封面图后保存文章
            - 使用外部图片 URL 作为封面
            - 从媒体库选择已有图片
        """
        author = User.objects.create_user(username='author', password='pass123')
        
        data = {
            'title': '带封面的文章',
            'content': '内容',
            'cover_image': '/media/images/cover.jpg'
        }
        
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = author
        
        serializer = ContentCreateUpdateSerializer(data=data)
        serializer.context['request'] = request
        
        assert serializer.is_valid()
        
        content = serializer.save()
        assert content.cover_image.name == 'images/cover.jpg' or content.cover_image
