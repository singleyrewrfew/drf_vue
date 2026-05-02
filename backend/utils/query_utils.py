"""
查询工具函数

提供常用的数据库查询辅助功能。
"""

import uuid


def get_object_by_slug_or_id(model, value):
    """
    通过 slug 或 UUID/ID 查找对象

    查找顺序：slug → UUID → ID

    Args:
        model: Django 模型类
        value: 查找值（slug 字符串或 UUID/ID）

    Returns:
        模型实例或 None
    """
    if not value:
        return None

    obj = model.objects.filter(slug=value).first()
    if obj:
        return obj

    try:
        uuid.UUID(str(value))
        return model.objects.filter(id=value).first()
    except (ValueError, AttributeError):
        return None
