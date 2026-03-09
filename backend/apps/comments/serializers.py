from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.ImageField(source='user.avatar', read_only=True)
    replies = serializers.SerializerMethodField()
    is_reply = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'article', 'user', 'user_name', 'user_avatar', 'parent', 'is_reply', 'is_approved', 'replies', 'created_at']
        read_only_fields = ['id', 'user', 'is_approved', 'created_at']

    def get_replies(self, obj):
        replies = obj.replies.filter(is_approved=True)
        return CommentSerializer(replies, many=True).data


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'article', 'parent']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CommentListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.ImageField(source='user.avatar', read_only=True)
    article_title = serializers.CharField(source='article.title', read_only=True)
    is_reply = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'article', 'article_title', 'user_name', 'user_avatar', 'parent', 'is_reply', 'is_approved', 'created_at']
