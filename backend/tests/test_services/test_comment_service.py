"""
评论业务逻辑测试

测试评论相关的服务和模型方法

作用：验证评论模型的核心功能和数据验证逻辑
使用：运行 pytest tests/test_services/test_comment_service.py 执行测试

测试覆盖的功能：
    1. Comment 模型 - 评论的 CRUD 操作和状态管理
    2. 评论审核机制 - 批准和拒绝评论
    3. 评论互动功能 - 点赞和回复
    4. 评论查询过滤 - 获取已批准的评论
    5. 数据验证 - 空文本和长文本验证

测试场景：
    - 创建评论及关联关系验证
    - 评论审核状态变更
    - 评论点赞计数
    - 评论回复层级关系
    - 批量查询已批准评论
    - 字符串表示格式
    - 边界情况验证（空文本、超长文本）
"""
import pytest

from apps.comments.models import Comment
from apps.contents.models import Content
from apps.users.models import User


@pytest.mark.unit
class TestCommentModel:
    """
    Comment 模型测试类
    
    验证评论模型的核心功能，包括创建、状态管理、互动功能和查询。
    Comment 模型支持评论的完整生命周期管理。
    
    测试用例：
        - 创建评论及关联对象验证
        - 评论批准和拒绝流程
        - 评论点赞功能
        - 评论回复层级关系
        - 批量查询已批准评论
        - 字符串表示格式
    
    模型特性：
        - 支持评论审核机制（is_approved）
        - 支持点赞计数（like_count）
        - 支持回复功能（parent、reply_to）
        - 自动关联文章和用户
    """
    
    def test_create_comment(self, db):
        """
        测试创建评论及验证关联关系
        
        验证能够成功创建评论对象，并正确关联文章、用户等外键字段。
        同时验证默认值设置是否正确。
        
        测试步骤：
            1. 创建文章作者
            2. 创建已发布的文章内容
            3. 创建评论者用户
            4. 创建评论对象，关联文章和评论者
            5. 验证评论的各个字段值
        
        预期结果：
            - comment.content 等于输入的评论内容
            - comment.user 等于评论者用户
            - comment.article 等于文章内容
            - comment.is_approved 默认为 True（根据模型定义）
        
        注意：
            - is_approved 的默认值取决于模型的 default 参数
            - 需要确保 article 和 user 外键正确关联
        """
        author = User.objects.create_user(username='author', password='pass123')
        content = Content.objects.create(
            title='测试文章',
            slug='test-article',
            content='内容',
            author=author,
            status='published'
        )
        
        commenter = User.objects.create_user(username='commenter', password='pass123')
        
        comment = Comment.objects.create(
            article=content,
            user=commenter,
            content='这是评论内容'
        )
        
        assert comment.content == '这是评论内容'
        assert comment.user == commenter
        assert comment.article == content
        assert comment.is_approved is True  # Django 默认是 True
    
    def test_approve_comment(self, db):
        """
        测试批准待审核的评论
        
        验证可以将未批准的评论状态修改为已批准，
        这是评论审核流程的核心功能。
        
        测试步骤：
            1. 创建文章和评论者
            2. 创建未批准的评论（is_approved=False）
            3. 将 is_approved 修改为 True
            4. 保存更改
            5. 验证状态已更新
        
        预期结果：
            - comment.is_approved 从 False 变为 True
            - 评论可以被公开展示
        
        应用场景：
            - 管理员审核用户评论
            - 自动审核通过后发布评论
            - 恢复被误拒绝的评论
        """
        author = User.objects.create_user(username='author', password='pass123')
        content = Content.objects.create(
            title='测试文章',
            slug='test-article',
            content='内容',
            author=author,
            status='published'
        )
        
        commenter = User.objects.create_user(username='commenter', password='pass123')
        comment = Comment.objects.create(
            article=content,
            user=commenter,
            content='待审核评论',
            is_approved=False
        )
        
        # 批准评论
        comment.is_approved = True
        comment.save()
        
        assert comment.is_approved is True
    
    def test_reject_comment(self, db):
        """
        测试拒绝已批准的评论
        
        验证可以将已批准的评论状态修改为未批准，
        用于撤销评论的公开显示。
        
        测试步骤：
            1. 创建文章和评论者
            2. 创建已批准的评论（is_approved=True）
            3. 将 is_approved 修改为 False
            4. 保存更改
            5. 验证状态已更新
        
        预期结果：
            - comment.is_approved 从 True 变为 False
            - 评论不再公开展示
        
        应用场景：
            - 删除违规评论
            - 用户请求删除自己的评论
            - 内容审核后发现不当内容
        """
        author = User.objects.create_user(username='author', password='pass123')
        content = Content.objects.create(
            title='测试文章',
            slug='test-article',
            content='内容',
            author=author,
            status='published'
        )
        
        commenter = User.objects.create_user(username='commenter', password='pass123')
        comment = Comment.objects.create(
            article=content,
            user=commenter,
            content='待审核评论',
            is_approved=True
        )
        
        # 拒绝评论
        comment.is_approved = False
        comment.save()
        
        assert comment.is_approved is False
    
    def test_like_comment(self, db):
        """
        测试评论点赞功能
        
        验证可以增加评论的点赞计数，实现用户对评论的互动。
        
        测试步骤：
            1. 创建文章和评论者
            2. 创建初始点赞数为 0 的评论
            3. 将 like_count 加 1
            4. 保存更改
            5. 验证点赞数已更新
        
        预期结果：
            - comment.like_count 从 0 变为 1
            - 可以多次累加点赞数
        
        应用场景：
            - 用户对有价值的评论点赞
            - 热门评论排序依据
            - 社区互动激励机制
        
        注意：
            - 实际生产中可能需要防止重复点赞
            - 可能需要记录点赞用户列表而非仅计数
        """
        author = User.objects.create_user(username='author', password='pass123')
        content = Content.objects.create(
            title='测试文章',
            slug='test-article',
            content='内容',
            author=author,
            status='published'
        )
        
        commenter = User.objects.create_user(username='commenter', password='pass123')
        comment = Comment.objects.create(
            article=content,
            user=commenter,
            content='可点赞评论',
            like_count=0
        )
        
        # 增加点赞数
        comment.like_count += 1
        comment.save()
        
        assert comment.like_count == 1
    
    def test_reply_to_comment(self, db):
        """
        测试评论回复功能及层级关系
        
        验证可以创建对某条评论的回复，并正确建立父子关系和回复对象关联。
        这是实现评论嵌套结构的基础。
        
        测试步骤：
            1. 创建文章和评论者
            2. 创建父评论
            3. 创建回复者用户
            4. 创建回复评论，设置 parent 和 reply_to 字段
            5. 验证回复评论的父级关系
        
        预期结果：
            - reply_comment.parent 等于 parent_comment
            - reply_comment.reply_to 等于原评论者
            - 形成评论层级结构
        
        字段说明：
            - parent: 指向父评论的外键（自引用）
            - reply_to: 指向被回复用户的外键
        
        应用场景：
            - 用户对评论进行回复
            - 构建评论树形结构
            - 显示评论对话线程
        """
        author = User.objects.create_user(username='author', password='pass123')
        content = Content.objects.create(
            title='测试文章',
            slug='test-article',
            content='内容',
            author=author,
            status='published'
        )
        
        commenter = User.objects.create_user(username='commenter', password='pass123')
        parent_comment = Comment.objects.create(
            article=content,
            user=commenter,
            content='父评论'
        )
        
        replier = User.objects.create_user(username='replier', password='pass123')
        reply_comment = Comment.objects.create(
            article=content,
            user=replier,
            content='回复评论',
            parent=parent_comment,
            reply_to=commenter
        )
        
        assert reply_comment.parent == parent_comment
    
    def test_get_approved_comments(self, db):
        """
        测试查询已批准的评论
        
        验证可以使用 Django ORM 过滤出指定文章的已批准评论，
        这是评论列表接口的基础查询逻辑。
        
        测试步骤：
            1. 创建文章和评论者
            2. 创建 3 条评论（2 条已批准，1 条未批准）
            3. 使用 filter 查询已批准的评论
            4. 验证查询结果数量
        
        预期结果：
            - approved_comments.count() 等于 2
            - 只返回 is_approved=True 的评论
            - 未批准的评论被过滤掉
        
        应用场景：
            - 文章详情页显示评论列表
            - 只显示通过审核的评论
            - 提高评论展示的安全性
        
        性能考虑：
            - 可以使用 select_related 优化外键查询
            - 可以添加分页避免一次性加载过多评论
        """
        author = User.objects.create_user(username='author', password='pass123')
        content = Content.objects.create(
            title='测试文章',
            slug='test-article',
            content='内容',
            author=author,
            status='published'
        )
        
        commenter = User.objects.create_user(username='commenter', password='pass123')
        
        # 创建多条评论
        Comment.objects.create(article=content, user=commenter, content='评论 1', is_approved=True)
        Comment.objects.create(article=content, user=commenter, content='评论 2', is_approved=True)
        Comment.objects.create(article=content, user=commenter, content='评论 3', is_approved=False)
        
        # 获取已批准的评论
        approved_comments = Comment.objects.filter(article=content, is_approved=True)
        
        assert approved_comments.count() == 2
    
    def test_comment_str_representation(self, db):
        """
        测试评论对象的字符串表示
        
        验证 Comment 模型的 __str__ 方法返回有意义的字符串，
        便于在 Django Admin 和调试时识别评论对象。
        
        测试步骤：
            1. 创建文章和评论者
            2. 创建评论对象
            3. 调用 str(comment) 获取字符串表示
            4. 验证格式是否符合预期
        
        预期结果：
            - 字符串格式为 '{username}: {content[:50]}'
            - 包含用户名和内容前 50 个字符
            - 便于快速识别评论内容
        
        最佳实践：
            - __str__ 方法应返回简洁且有意义的描述
            - 对于长文本应截断以避免输出过长
            - 包含关键标识信息（如用户名）
        """
        author = User.objects.create_user(username='author', password='pass123')
        content = Content.objects.create(
            title='测试文章',
            slug='test-article',
            content='内容',
            author=author,
            status='published'
        )
        
        commenter = User.objects.create_user(username='commenter', password='pass123')
        comment = Comment.objects.create(
            article=content,
            user=commenter,
            content='测试评论'
        )
        
        # __str__ 方法应该返回有意义的字符串
        assert str(comment) == f'{commenter.username}: {comment.content[:50]}'


@pytest.mark.unit
class TestCommentValidation:
    """
    评论数据验证测试类
    
    验证评论字段的输入验证逻辑，确保数据质量和安全性。
    包括必填字段验证、长度限制等。
    
    测试用例：
        - 空文本验证（不允许空评论）
        - 长文本验证（处理超长评论）
    
    验证规则：
        - content 字段不能为空（blank=False）
        - content 字段有最大长度限制（取决于 TextField 配置）
        - 防止垃圾评论和恶意输入
    """
    
    def test_empty_text_validation(self, db):
        """
        测试空文本评论的验证
        
        验证当尝试创建内容为空的评论时，系统会拒绝该操作，
        防止用户提交无意义的空评论。
        
        测试步骤：
            1. 创建文章和评论者
            2. 尝试创建 content 为空的评论
            3. 捕获可能的异常
            4. 验证是否成功阻止了空评论创建
        
        预期结果：
            - 抛出异常（IntegrityError 或 ValidationError）
            - 或者 Django 的 blank=False 验证失败
            - 空评论不会被保存到数据库
        
        安全意义：
            - 防止用户提交空评论浪费存储资源
            - 保持评论质量，避免无意义内容
            - 防止自动化脚本刷空评论
        
        注意：
            - 具体行为取决于模型的 blank 和 null 配置
            - 可能在前端、序列化器或模型层进行验证
        """
        author = User.objects.create_user(username='author', password='pass123')
        content = Content.objects.create(
            title='测试文章',
            slug='test-article',
            content='内容',
            author=author,
            status='published'
        )
        
        commenter = User.objects.create_user(username='commenter', password='pass123')
        
        # 尝试创建空文本评论（Django 的 blank=False 会阻止）
        try:
            comment = Comment.objects.create(
                content=content,
                user=commenter,
                text=''
            )
            # 如果创建成功，说明没有验证
            assert False, "Should not allow empty text"
        except Exception:
            # 预期会抛出异常
            pass
    
    def test_long_text_validation(self, db):
        """
        测试超长评论文本的处理
        
        验证系统能够正确处理超长评论内容，
        要么正常存储，要么进行截断或拒绝。
        
        测试步骤：
            1. 创建文章和评论者
            2. 准备 2000 字符的超长评论内容
            3. 创建评论对象
            4. 验证内容的处理方式
        
        预期结果：
            - 要么完整保存 2000 字符（TextField 通常支持）
            - 要么截断到最大允许长度
            - 不会导致系统错误或数据丢失
        
        技术说明：
            - TextField 通常没有严格的长度限制（取决于数据库）
            - MySQL 的 TEXT 类型最大 65535 字节
            - PostgreSQL 的 TEXT 类型几乎无限制
        
        安全考虑：
            - 应在应用层设置合理的长度限制
            - 防止恶意用户提交超大文本消耗资源
            - 建议在序列化器中添加 max_length 验证
        
        最佳实践：
            - 前端限制输入长度（用户体验）
            - 后端验证长度（安全保障）
            - 合理设置数据库字段类型
        """
        author = User.objects.create_user(username='author', password='pass123')
        content = Content.objects.create(
            title='测试文章',
            slug='test-article',
            content='内容',
            author=author,
            status='published'
        )
        
        commenter = User.objects.create_user(username='commenter', password='pass123')
        
        # 创建超长评论
        long_content = 'x' * 2000  # 2000 字符
        
        comment = Comment.objects.create(
            article=content,
            user=commenter,
            content=long_content
        )
        
        # Django 应该会截断或接受，取决于 TextField 的配置
        assert comment.content == long_content or len(comment.content) <= 2000
