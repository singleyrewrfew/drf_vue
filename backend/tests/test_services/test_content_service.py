"""
Test Content Service

内容服务单元测试
"""
import pytest
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied, ValidationError

from services.content_service import ContentService
from tests.utils import MockUser, MockContent


@pytest.mark.unit
class TestContentService:
    """内容服务测试类"""
    
    def test_publish_content_success(self):
        """测试成功发布内容"""
        content = MockContent(status='draft')
        user = MockUser(permissions=['content_publish'])
        
        result = ContentService.publish_content(content, user)
        
        assert result.status == 'published'
        assert result.published_at is not None
    
    def test_publish_content_without_permission(self):
        """测试无权限发布内容"""
        content = MockContent(status='draft')
        user = MockUser(permissions=[])
        
        with pytest.raises(PermissionDenied, match='无发布权限'):
            ContentService.publish_content(content, user)
    
    def test_publish_already_published_content(self):
        """测试发布已发布的内容"""
        content = MockContent(status='published')
        user = MockUser(permissions=['content_publish'])
        
        with pytest.raises(ValidationError, match='内容已发布'):
            ContentService.publish_content(content, user)
    
    def test_archive_content_success(self):
        """测试成功归档内容"""
        content = MockContent(status='published')
        user = MockUser(permissions=['content_archive'])
        
        result = ContentService.archive_content(content, user)
        
        assert result.status == 'archived'
    
    def test_archive_content_without_permission(self):
        """测试无权限归档内容"""
        content = MockContent(status='published')
        user = MockUser(permissions=[])
        
        with pytest.raises(PermissionDenied, match='无归档权限'):
            ContentService.archive_content(content, user)
    
    def test_increment_view_count(self):
        """测试增加浏览量"""
        content = MockContent(view_count=0)
        
        result = ContentService.increment_view_count(content)
        
        assert result.view_count == 1
    
    def test_can_user_edit_as_author(self):
        """测试作者可以编辑内容"""
        author = MockUser(id=1)
        content = MockContent(author=author)
        
        result = ContentService.can_user_edit(content, author)
        
        assert result is True
    
    def test_can_user_edit_as_admin(self):
        """测试管理员可以编辑内容"""
        author = MockUser(id=1)
        admin = MockUser(id=2, is_admin=True)
        content = MockContent(author=author)
        
        result = ContentService.can_user_edit(content, admin)
        
        assert result is True
    
    def test_can_user_edit_as_other_user(self):
        """测试其他用户不能编辑内容"""
        author = MockUser(id=1)
        other_user = MockUser(id=2)
        content = MockContent(author=author)
        
        result = ContentService.can_user_edit(content, other_user)
        
        assert result is False
    
    def test_can_user_delete_as_author(self):
        """测试作者可以删除内容"""
        author = MockUser(id=1)
        content = MockContent(author=author)
        
        result = ContentService.can_user_delete(content, author)
        
        assert result is True
    
    def test_can_user_delete_as_admin(self):
        """测试管理员可以删除内容"""
        author = MockUser(id=1)
        admin = MockUser(id=2, is_admin=True)
        content = MockContent(author=author)
        
        result = ContentService.can_user_delete(content, admin)
        
        assert result is True
    
    def test_can_user_delete_as_other_user(self):
        """测试其他用户不能删除内容"""
        author = MockUser(id=1)
        other_user = MockUser(id=2)
        content = MockContent(author=author)
        
        result = ContentService.can_user_delete(content, other_user)
        
        assert result is False


@pytest.mark.unit
class TestContentServiceQuery:
    """内容服务查询测试类"""
    
    def test_get_published_contents(self, db):
        """测试获取已发布内容列表"""
        from tests.utils import create_test_user, create_test_content
        
        author = create_test_user()
        create_test_content(author, status='published', title='Published 1')
        create_test_content(author, status='published', title='Published 2')
        create_test_content(author, status='draft', title='Draft')
        
        result = ContentService.get_published_contents()
        
        assert result.count() == 2
    
    def test_get_contents_by_author(self, db):
        """测试获取作者的内容列表"""
        from tests.utils import create_test_user, create_test_content
        
        author1 = create_test_user(username='author1')
        author2 = create_test_user(username='author2')
        
        create_test_content(author1, title='Content 1')
        create_test_content(author1, title='Content 2')
        create_test_content(author2, title='Content 3')
        
        result = ContentService.get_contents_by_author(author1)
        
        assert result.count() == 2
    
    def test_search_contents(self, db):
        """测试搜索内容"""
        from tests.utils import create_test_user, create_test_content
        
        author = create_test_user()
        create_test_content(author, title='Python Tutorial', status='published')
        create_test_content(author, title='Django Guide', status='published')
        create_test_content(author, title='JavaScript Course', status='published')
        
        result = ContentService.search_contents('Python')
        
        assert result.count() == 1
        assert result.first().title == 'Python Tutorial'
