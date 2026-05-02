from rest_framework import serializers

from utils.html_utils import sanitize_comment
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.ImageField(source='user.avatar', read_only=True)
    user_id = serializers.CharField(source='user.id', read_only=True)
    reply_to_name = serializers.CharField(source='reply_to.username', read_only=True)
    replies = serializers.SerializerMethodField()
    is_reply = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'article', 'user', 'user_id', 'user_name', 'user_avatar', 'parent', 'reply_to', 'reply_to_name', 'is_reply', 'is_approved', 'like_count', 'is_liked', 'reply_count', 'replies', 'created_at']
        read_only_fields = ['id', 'user', 'is_approved', 'like_count', 'created_at']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            liked_comment_ids = getattr(self.context.get('view'), '_liked_comment_ids', set())
            return obj.id in liked_comment_ids
        return False

    def get_reply_count(self, obj):
        return getattr(obj, 'reply_count', 0) or obj.replies.filter(is_approved=True).count()

    def get_replies(self, obj):
        replies = getattr(obj, 'prefetched_replies', None)
        if replies is None:
            replies = obj.replies.filter(is_approved=True)
        return CommentReplySerializer(replies, many=True, context=self.context).data


class CommentReplySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.ImageField(source='user.avatar', read_only=True)
    user_id = serializers.CharField(source='user.id', read_only=True)
    reply_to_name = serializers.CharField(source='reply_to.username', read_only=True)
    is_reply = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user_id', 'user_name', 'user_avatar', 'reply_to', 'reply_to_name', 'is_reply', 'is_approved', 'like_count', 'is_liked', 'created_at']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            liked_comment_ids = getattr(self.context.get('view'), '_liked_comment_ids', set())
            return obj.id in liked_comment_ids
        return False


class CommentCreateSerializer(serializers.ModelSerializer):
    reply_to_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    article = serializers.CharField(write_only=True)

    class Meta:
        model = Comment
        fields = ['content', 'article', 'parent', 'reply_to_id']

    def validate_article(self, value):
        from apps.contents.models import Content
        import uuid

        try:
            uuid.UUID(value)
            try:
                return Content.objects.get(id=value)
            except Content.DoesNotExist:
                raise serializers.ValidationError('文章不存在')
        except (ValueError, AttributeError):
            try:
                return Content.objects.get(slug=value)
            except Content.DoesNotExist:
                raise serializers.ValidationError('文章不存在')

    def validate_content(self, value):
        return sanitize_comment(value)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        reply_to_id = validated_data.pop('reply_to_id', None)
        if reply_to_id:
            from apps.core.models import User
            try:
                validated_data['reply_to'] = User.objects.get(id=reply_to_id)
            except User.DoesNotExist:
                pass
        return super().create(validated_data)


class CommentListSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.id', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.ImageField(source='user.avatar', read_only=True)
    reply_to_name = serializers.CharField(source='reply_to.username', read_only=True)
    article_title = serializers.CharField(source='article.title', read_only=True)
    is_reply = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'article', 'article_title', 'user_id', 'user_name', 'user_avatar', 'parent', 'reply_to', 'reply_to_name', 'is_reply', 'is_approved', 'like_count', 'is_liked', 'reply_count', 'replies', 'created_at']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            liked_comment_ids = getattr(self.context.get('view'), '_liked_comment_ids', set())
            return obj.id in liked_comment_ids
        return False

    def get_reply_count(self, obj):
        return getattr(obj, 'reply_count', 0) or obj.replies.filter(is_approved=True).count()

    def get_replies(self, obj):
        replies = getattr(obj, 'prefetched_replies', None)
        if replies is None:
            replies = obj.replies.filter(is_approved=True)
        return CommentReplySerializer(replies, many=True, context=self.context).data
