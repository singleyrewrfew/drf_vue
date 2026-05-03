"""
Domain Events - 领域事件定义

提供统一的事件机制，解耦模块间依赖

使用场景:
- 内容发布后触发通知、缓存更新
- 评论审核后触发消息推送
- 媒体上传后触发处理任务
- 用户注册后触发欢迎邮件

优势:
1. 解耦: Service 不需要知道谁会响应事件
2. 扩展: 新功能只需添加监听器，无需修改 Service
3. 测试: 可以独立测试事件处理器
4. 异步: 可以配置为异步执行，提升性能
"""
from django.dispatch import Signal

# ==========================================
# Content Events (内容相关事件)
# ==========================================

content_published = Signal()
"""
内容发布事件

参数:
    content: Content 实例
    user: 操作用户
    published_at: 发布时间

监听示例:
    @receiver(content_published)
    def handle_content_published(sender, content, user, **kwargs):
        # 发送通知给关注者
        # 更新搜索引擎索引
        # 清除相关缓存
        pass
"""

content_archived = Signal()
"""
内容归档事件

参数:
    content: Content 实例
    user: 操作用户
"""

content_created = Signal()
"""
内容创建事件（草稿）

参数:
    content: Content 实例
    user: 作者
"""

content_updated = Signal()
"""
内容更新事件

参数:
    content: Content 实例
    user: 操作用户
    updated_fields: 更新的字段列表
"""

content_deleted = Signal()
"""
内容删除事件

参数:
    content_id: 内容ID
    user: 操作用户
"""


# ==========================================
# Comment Events (评论相关事件)
# ==========================================

comment_created = Signal()
"""
评论创建事件

参数:
    comment: Comment 实例
    user: 评论者
    article: 关联文章
"""

comment_approved = Signal()
"""
评论审核通过事件

参数:
    comment: Comment 实例
    approved_by: 审核人
"""

comment_rejected = Signal()
"""
评论审核拒绝事件

参数:
    comment: Comment 实例
    rejected_by: 拒绝人
    reason: 拒绝原因
"""

comment_liked = Signal()
"""
评论点赞事件

参数:
    comment: Comment 实例
    user: 点赞用户
"""


# ==========================================
# Media Events (媒体相关事件)
# ==========================================

media_uploaded = Signal()
"""
媒体上传完成事件

参数:
    media: Media 实例
    uploader: 上传者
"""

media_processed = Signal()
"""
媒体处理完成事件（视频转码、缩略图生成等）

参数:
    media: Media 实例
    processing_type: 处理类型 ('thumbnail', 'transcode', etc.)
    success: 是否成功
    error: 错误信息（如果失败）
"""

media_deleted = Signal()
"""
媒体删除事件

参数:
    media_id: 媒体ID
    uploader: 上传者
"""


# ==========================================
# User Events (用户相关事件)
# ==========================================

user_registered = Signal()
"""
用户注册事件

参数:
    user: User 实例
    registration_method: 注册方式 ('email', 'social', etc.)
"""

user_logged_in = Signal()
"""
用户登录事件

参数:
    user: User 实例
    login_method: 登录方式
    ip_address: IP地址
"""

user_profile_updated = Signal()
"""
用户资料更新事件

参数:
    user: User 实例
    updated_fields: 更新的字段列表
"""


# ==========================================
# Category & Tag Events (分类标签事件)
# ==========================================

category_created = Signal()
"""
分类创建事件

参数:
    category: Category 实例
    created_by: 创建人
"""

tag_created = Signal()
"""
标签创建事件

参数:
    tag: Tag 实例
    created_by: 创建人
"""
