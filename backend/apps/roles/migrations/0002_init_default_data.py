from django.db import migrations


def create_default_roles_and_permissions(apps, schema_editor):
    Permission = apps.get_model('roles', 'Permission')
    Role = apps.get_model('roles', 'Role')

    permissions_data = [
        {'code': 'user_view', 'name': '查看用户', 'description': '查看用户列表和详情'},
        {'code': 'user_create', 'name': '创建用户', 'description': '创建新用户'},
        {'code': 'user_update', 'name': '编辑用户', 'description': '编辑用户信息'},
        {'code': 'user_delete', 'name': '删除用户', 'description': '删除用户'},
        {'code': 'content_view', 'name': '查看内容', 'description': '查看内容列表和详情'},
        {'code': 'content_create', 'name': '创建内容', 'description': '创建新内容'},
        {'code': 'content_update', 'name': '编辑内容', 'description': '编辑内容'},
        {'code': 'content_delete', 'name': '删除内容', 'description': '删除内容'},
        {'code': 'content_publish', 'name': '发布内容', 'description': '发布和归档内容'},
        {'code': 'category_view', 'name': '查看分类', 'description': '查看分类列表和详情'},
        {'code': 'category_manage', 'name': '管理分类', 'description': '创建、编辑、删除分类'},
        {'code': 'tag_view', 'name': '查看标签', 'description': '查看标签列表和详情'},
        {'code': 'tag_manage', 'name': '管理标签', 'description': '创建、编辑、删除标签'},
        {'code': 'media_view', 'name': '查看媒体', 'description': '查看媒体文件列表'},
        {'code': 'media_upload', 'name': '上传媒体', 'description': '上传媒体文件'},
        {'code': 'media_delete', 'name': '删除媒体', 'description': '删除媒体文件'},
        {'code': 'comment_view', 'name': '查看评论', 'description': '查看评论列表'},
        {'code': 'comment_manage', 'name': '管理评论', 'description': '审核和删除评论'},
        {'code': 'role_view', 'name': '查看角色', 'description': '查看角色和权限'},
        {'code': 'role_manage', 'name': '管理角色', 'description': '管理角色和分配权限'},
    ]

    permissions = {}
    for perm_data in permissions_data:
        perm, _ = Permission.objects.get_or_create(
            code=perm_data['code'],
            defaults=perm_data
        )
        permissions[perm_data['code']] = perm

    roles_data = [
        {
            'name': '管理员',
            'code': 'admin',
            'description': '系统管理员，拥有所有权限',
            'is_system': True,
            'permission_codes': list(permissions.keys())
        },
        {
            'name': '编辑',
            'code': 'editor',
            'description': '内容编辑，可以管理内容和媒体',
            'is_system': True,
            'permission_codes': [
                'content_view', 'content_create', 'content_update', 'content_delete', 'content_publish',
                'category_view', 'category_manage',
                'tag_view', 'tag_manage',
                'media_view', 'media_upload', 'media_delete',
                'comment_view', 'comment_manage',
            ]
        },
        {
            'name': '普通用户',
            'code': 'user',
            'description': '普通用户，只能查看和评论',
            'is_system': True,
            'permission_codes': [
                'content_view',
                'category_view',
                'tag_view',
                'media_view',
                'comment_view',
            ]
        },
    ]

    for role_data in roles_data:
        permission_codes = role_data.pop('permission_codes')
        role, _ = Role.objects.get_or_create(
            code=role_data['code'],
            defaults=role_data
        )
        for code in permission_codes:
            role.permissions.add(permissions[code])


class Migration(migrations.Migration):
    dependencies = [
        ('roles', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_roles_and_permissions),
    ]
