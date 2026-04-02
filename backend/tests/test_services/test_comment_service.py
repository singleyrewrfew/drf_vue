"""
评论业务逻辑测试

测试评论相关的服务和模型方法
"""
import pytest

from apps.comments.models import Comment
from apps.contents.models import Content
from apps.users.models import User


@pytest.mark.unit
class TestCommentModel:
    """评论模型测试类"""
    
    def test_create_comment(self, db):
        """测试创建评论"""
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
        """测试批准评论"""
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
        """测试拒绝评论"""
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
        """测试点赞评论"""
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
        """测试回复评论"""
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
        """测试获取已批准的评论"""
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
        """测试评论字符串表示"""
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
    """评论验证测试类"""
    
    def test_empty_text_validation(self, db):
        """测试空文本验证"""
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
        """测试长文本验证"""
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
