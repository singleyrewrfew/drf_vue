"""
评论系统防刷机制测试

验证评论和点赞的频率限制功能，防止恶意刷评论和刷赞。

运行测试：
    pytest tests/test_comments/test_comment_rate_limit.py -v
"""
import pytest
from rest_framework.test import APIClient
from django.core.cache import cache
from apps.users.models import User
from apps.contents.models import Content
from apps.comments.models import Comment, CommentLike


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user1(db):
    """创建用户 1"""
    return User.objects.create_user(
        username='user1',
        email='user1@example.com',
        password='pass123'
    )


@pytest.fixture
def user2(db):
    """创建用户 2"""
    return User.objects.create_user(
        username='user2',
        email='user2@example.com',
        password='pass123'
    )


@pytest.fixture
def article1(db, user1):
    """创建文章 1"""
    return Content.objects.create(
        title='测试文章 1',
        slug='test-article-1',
        content='这是测试内容',
        author=user1,
        status='published'
    )


@pytest.fixture
def article2(db, user1):
    """创建文章 2"""
    return Content.objects.create(
        title='测试文章 2',
        slug='test-article-2',
        content='这是测试内容 2',
        author=user1,
        status='published'
    )


@pytest.fixture
def authenticated_client(api_client, user1):
    """认证的 API 客户端"""
    api_client.force_authenticate(user=user1)
    return api_client


@pytest.mark.unit
class TestCommentRateLimit:
    """评论频率限制测试"""
    
    def teardown_method(self, method):
        """清理缓存"""
        cache.clear()
    
    def test_normal_comment_allowed(self, authenticated_client, article1):
        """测试正常评论应该被允许"""
        data = {
            'content': '这是一条正常的评论',
            'article': str(article1.id)
        }
        
        response = authenticated_client.post('/api/comments/', data, format='json')
        assert response.status_code == 201
    
    def test_global_rate_limit_5_per_minute(self, authenticated_client, article1, article2):
        """测试全局频率限制：每分钟最多 10 条评论"""
        # 在两篇文章之间交替发送评论，避免触发文章级别限制
        articles = [article1, article2]
        
        for i in range(10):
            article = articles[i % 2]  # 交替使用两篇文章
            data = {
                'content': f'评论 {i+1}',
                'article': str(article.id)
            }
            response = authenticated_client.post('/api/comments/', data, format='json')
            assert response.status_code == 201, f'第 {i+1} 条评论应该成功'
        
        # 第 11 条应该被拒绝（达到全局限制）
        data = {
            'content': '第 11 条评论（应该被拒绝）',
            'article': str(article1.id)
        }
        response = authenticated_client.post('/api/comments/', data, format='json')
        assert response.status_code == 400, '第 11 条评论应该被拒绝'
        assert '评论过于频繁' in str(response.data), '错误消息应该说明频率限制'
    
    def test_article_rate_limit_3_per_minute(self, authenticated_client, article1):
        """测试文章级别频率限制：对同一篇文章每分钟最多 5 条"""
        # 发送 5 条正常评论
        for i in range(5):
            data = {
                'content': f'评论 {i+1}',
                'article': str(article1.id)
            }
            response = authenticated_client.post('/api/comments/', data, format='json')
            assert response.status_code == 201, f'第 {i+1} 条评论应该成功'
        
        # 第 6 条应该被拒绝
        data = {
            'content': '第 6 条评论（应该被拒绝）',
            'article': str(article1.id)
        }
        response = authenticated_client.post('/api/comments/', data, format='json')
        assert response.status_code == 400, '第 6 条评论应该被拒绝'
        assert '对该文章评论过于频繁' in str(response.data), '错误消息应该说明文章级别限制'
    
    def test_different_articles_have_separate_limits(self, authenticated_client, article1, article2):
        """测试不同文章的频率限制是独立的"""
        # 对文章 1 发送 5 条评论（达到文章级别限制）
        for i in range(5):
            data = {
                'content': f'文章 1 评论 {i+1}',
                'article': str(article1.id)
            }
            response = authenticated_client.post('/api/comments/', data, format='json')
            assert response.status_code == 201
        
        # 对文章 2 发送评论应该仍然允许（因为文章级别限制是独立的）
        data = {
            'content': '文章 2 评论 1',
            'article': str(article2.id)
        }
        response = authenticated_client.post('/api/comments/', data, format='json')
        assert response.status_code == 201, '对不同文章的评论应该被允许'
    
    def test_rate_limit_resets_after_timeout(self, authenticated_client, article1, article2):
        """测试频率限制在超时后重置"""
        # 发送 10 条评论达到限制（交替使用两篇文章）
        articles = [article1, article2]
        for i in range(10):
            article = articles[i % 2]
            data = {
                'content': f'评论 {i+1}',
                'article': str(article.id)
            }
            response = authenticated_client.post('/api/comments/', data, format='json')
            assert response.status_code == 201
        
        # 第 11 条应该被拒绝
        data = {
            'content': '第 11 条评论',
            'article': str(article1.id)
        }
        response = authenticated_client.post('/api/comments/', data, format='json')
        assert response.status_code == 400
        
        # 清除缓存模拟时间过期
        cache.clear()
        
        # 现在应该可以再次评论
        data = {
            'content': '新的评论（缓存已清除）',
            'article': str(article1.id)
        }
        response = authenticated_client.post('/api/comments/', data, format='json')
        assert response.status_code == 201, '缓存清除后应该可以再次评论'
    
    def test_different_users_have_separate_limits(self, api_client, user1, user2, article1, article2):
        """测试不同用户的频率限制是独立的"""
        # 用户 1 发送 10 条评论达到限制（交替使用两篇文章）
        api_client.force_authenticate(user=user1)
        articles = [article1, article2]
        for i in range(10):
            article = articles[i % 2]
            data = {
                'content': f'用户 1 评论 {i+1}',
                'article': str(article.id)
            }
            response = api_client.post('/api/comments/', data, format='json')
            assert response.status_code == 201
        
        # 用户 1 的第 11 条应该被拒绝
        data = {
            'content': '用户 1 第 11 条',
            'article': str(article1.id)
        }
        response = api_client.post('/api/comments/', data, format='json')
        assert response.status_code == 400
        
        # 用户 2 的评论应该仍然允许
        api_client.force_authenticate(user=user2)
        data = {
            'content': '用户 2 评论 1',
            'article': str(article1.id)
        }
        response = api_client.post('/api/comments/', data, format='json')
        assert response.status_code == 201, '不同用户的频率限制应该是独立的'


@pytest.mark.unit
class TestLikeRateLimit:
    """点赞频率限制测试"""
    
    def teardown_method(self, method):
        """清理缓存"""
        cache.clear()
    
    def test_normal_like_allowed(self, authenticated_client, article1, user2):
        """测试正常点赞应该被允许"""
        comment = Comment.objects.create(
            user=user2,
            article=article1,
            content='测试评论',
            is_approved=True
        )
        
        response = authenticated_client.post(f'/api/comments/{comment.id}/like/')
        assert response.status_code == 200
    
    def test_like_rate_limit_20_per_minute(self, authenticated_client, article1, user2):
        """测试点赞频率限制：每分钟最多 20 次"""
        # 创建 20 个评论用于点赞
        comments = []
        for i in range(20):
            comment = Comment.objects.create(
                user=user2,
                article=article1,
                content=f'测试评论 {i+1}',
                is_approved=True
            )
            comments.append(comment)
        
        # 点赞前 20 次应该成功
        for i, comment in enumerate(comments):
            response = authenticated_client.post(f'/api/comments/{comment.id}/like/')
            assert response.status_code == 200, f'第 {i+1} 次点赞应该成功'
        
        # 第 21 次应该被拒绝
        extra_comment = Comment.objects.create(
            user=user2,
            article=article1,
            content='额外评论',
            is_approved=True
        )
        response = authenticated_client.post(f'/api/comments/{extra_comment.id}/like/')
        assert response.status_code == 400, '第 21 次点赞应该被拒绝'
        assert '点赞操作过于频繁' in str(response.data), '错误消息应该说明频率限制'
    
    def test_like_and_unlike_count_towards_limit(self, authenticated_client, article1, user2):
        """测试点赞和取消点赞都计入频率限制"""
        comment = Comment.objects.create(
            user=user2,
            article=article1,
            content='测试评论',
            is_approved=True
        )
        
        # 点赞（第 1 次）
        response = authenticated_client.post(f'/api/comments/{comment.id}/like/')
        assert response.status_code == 200
        
        # 取消点赞（第 2 次）
        response = authenticated_client.post(f'/api/comments/{comment.id}/like/')
        assert response.status_code == 200
        
        # 再点赞（第 3 次）
        response = authenticated_client.post(f'/api/comments/{comment.id}/like/')
        assert response.status_code == 200
        
        # 每次操作都计入频率限制
    
    def test_like_rate_limit_resets_after_timeout(self, authenticated_client, article1, user2):
        """测试点赞频率限制在超时后重置"""
        comment = Comment.objects.create(
            user=user2,
            article=article1,
            content='测试评论',
            is_approved=True
        )
        
        # 快速点赞 20 次达到限制
        for i in range(20):
            temp_comment = Comment.objects.create(
                user=user2,
                article=article1,
                content=f'临时评论 {i}',
                is_approved=True
            )
            response = authenticated_client.post(f'/api/comments/{temp_comment.id}/like/')
            if response.status_code == 400:
                break  # 达到限制
        
        # 清除缓存模拟时间过期
        cache.clear()
        
        # 现在应该可以再次点赞
        response = authenticated_client.post(f'/api/comments/{comment.id}/like/')
        assert response.status_code == 200, '缓存清除后应该可以再次点赞'


@pytest.mark.integration
class TestAntiSpamIntegration:
    """防刷机制集成测试"""
    
    def teardown_method(self, method):
        """清理缓存"""
        cache.clear()
    
    def test_combined_comment_and_like_limits(self, authenticated_client, article1, article2, user2):
        """测试评论和点赞的限制是独立的"""
        # 发送 10 条评论达到评论限制（交替使用两篇文章）
        articles = [article1, article2]
        for i in range(10):
            article = articles[i % 2]
            data = {
                'content': f'评论 {i+1}',
                'article': str(article.id)
            }
            response = authenticated_client.post('/api/comments/', data, format='json')
            assert response.status_code == 201
        
        # 评论达到限制
        data = {
            'content': '第 11 条评论',
            'article': str(article1.id)
        }
        response = authenticated_client.post('/api/comments/', data, format='json')
        assert response.status_code == 400
        
        # 但点赞仍然可以工作
        comment = Comment.objects.create(
            user=user2,
            article=article1,
            content='测试评论',
            is_approved=True
        )
        response = authenticated_client.post(f'/api/comments/{comment.id}/like/')
        assert response.status_code == 200, '评论受限不应影响点赞'
    
    def test_error_message_clarity(self, authenticated_client, article1, article2):
        """测试错误消息清晰易懂"""
        # 达到全局限制（交替使用两篇文章）
        articles = [article1, article2]
        for i in range(10):
            article = articles[i % 2]
            data = {
                'content': f'评论 {i+1}',
                'article': str(article.id)
            }
            authenticated_client.post('/api/comments/', data, format='json')
        
        # 检查错误消息
        data = {
            'content': '超限评论',
            'article': str(article1.id)
        }
        response = authenticated_client.post('/api/comments/', data, format='json')
        
        assert response.status_code == 400
        error_msg = str(response.data)
        
        # 错误消息应该包含有用的信息
        assert '评论' in error_msg or '频繁' in error_msg, '错误消息应该提到评论或频率'
        assert '稍后再试' in error_msg or '分钟' in error_msg, '错误消息应该提供解决建议'
