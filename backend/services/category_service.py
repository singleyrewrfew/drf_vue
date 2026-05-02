from django.db.models import Count, Prefetch, Q

from apps.categories.models import Category
from services.base import ModelService


class CategoryService(ModelService):
    """
    分类业务逻辑服务层
    
    封装所有与分类相关的业务逻辑
    """
    model_class = Category

    @classmethod
    def get_root_categories(cls):
        """
        获取根分类列表
        
        Returns:
            QuerySet: 根分类查询集
        """
        return Category.objects.filter(parent__isnull=True)

    @classmethod
    def get_categories_with_content_count(cls):
        """
        获取分类列表（包含已发布内容数量）
        
        Returns:
            QuerySet: 带内容计数的分类查询集
        """
        return Category.objects.select_related('parent').annotate(
            content_count=Count('contents', filter=Q(contents__status='published'))
        )

    @classmethod
    def get_category_with_children(cls, category_id):
        """
        获取分类及其子分类
        
        Args:
            category_id: 分类 ID
            
        Returns:
            Category: 包含预加载子分类的分类对象
        """
        children_qs = Category.objects.annotate(
            content_count=Count('contents', filter=Q(contents__status='published'))
        )
        
        return Category.objects.prefetch_related(
            Prefetch('children', queryset=children_qs, to_attr='prefetched_children')
        ).annotate(
            content_count=Count('contents', filter=Q(contents__status='published'))
        ).get(id=category_id)

    @classmethod
    def get_category_tree(cls):
        """
        获取分类树结构
        
        Returns:
            list: 分类树列表
        """
        root_categories = cls.get_root_categories()
        
        def build_tree(category):
            return {
                'id': str(category.id),
                'name': category.name,
                'slug': category.slug,
                'full_name': category.full_name,
                'content_count': getattr(category, 'content_count', 0),
                'children': [build_tree(child) for child in category.children.all()]
            }
        
        return [build_tree(cat) for cat in root_categories]

    @classmethod
    def create_category(cls, name, parent=None, description='', sort_order=0):
        """
        创建分类
        
        Args:
            name: 分类名称
            parent: 父分类（可选）
            description: 描述
            sort_order: 排序
            
        Returns:
            Category: 创建的分类对象
        """
        return Category.objects.create(
            name=name,
            parent=parent,
            description=description,
            sort_order=sort_order
        )

    @classmethod
    def can_user_modify(cls, user):
        """
        检查用户是否可以修改分类
        
        Args:
            user: 用户对象
            
        Returns:
            bool: 是否可以修改
        """
        return user.is_admin or user.is_superuser or (user.role and user.role.code == 'editor')
