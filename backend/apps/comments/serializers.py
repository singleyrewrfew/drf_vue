from rest_framework import serializers

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
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_reply_count(self, obj):
        return obj.replies.filter(is_approved=True).count()

    def get_replies(self, obj):
        replies = obj.replies.filter(is_approved=True)
        return CommentSerializer(replies, many=True).data


class CommentCreateSerializer(serializers.ModelSerializer):
    reply_to_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = ['content', 'article', 'parent', 'reply_to_id']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        reply_to_id = validated_data.pop('reply_to_id', None)
        if reply_to_id:
            from django.contrib.auth import get_user_model
            User = get_user_model()
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
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_reply_count(self, obj):
        return obj.replies.filter(is_approved=True).count()

    def get_replies(self, obj):
        replies = obj.replies.filter(is_approved=True)
        return CommentListSerializer(replies, many=True).data
