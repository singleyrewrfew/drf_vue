import os
import hashlib
from PIL import Image as PILImage
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Image, Album, UploadChunk


class AlbumSerializer(serializers.ModelSerializer):
    image_count = serializers.ReadOnlyField()
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Album
        fields = [
            'id', 'name', 'description', 'cover', 'is_public',
            'image_count', 'user_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class ImageSerializer(serializers.ModelSerializer):
    url = serializers.ReadOnlyField()
    user_username = serializers.CharField(source='user.username', read_only=True)
    album_name = serializers.CharField(source='album.name', read_only=True)
    
    class Meta:
        model = Image
        fields = [
            'id', 'album', 'filename', 'file_size', 'file_hash',
            'width', 'height', 'format', 'title', 'description',
            'tags', 'is_public', 'access_count', 'storage_backend',
            'url', 'user_username', 'album_name', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'file_size', 'file_hash', 'width', 'height',
            'format', 'storage_backend', 'storage_path', 'access_count',
            'created_at', 'updated_at'
        ]


class ImageUploadSerializer(serializers.Serializer):
    file = serializers.ImageField()
    album = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(),
        required=False,
        allow_null=True
    )
    title = serializers.CharField(max_length=200, required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        allow_empty=True
    )
    is_public = serializers.BooleanField(default=False)
    
    def validate_file(self, value):
        if value.size > settings.MAX_FILE_SIZE:
            raise ValidationError(f'文件大小不能超过 {settings.MAX_FILE_SIZE / 1024 / 1024}MB')
        
        try:
            img = PILImage.open(value)
            img.verify()
            
            if img.format not in settings.ALLOWED_IMAGE_FORMATS:
                raise ValidationError(f'不支持的图片格式: {img.format}')
            
            value.image = img
            
        except Exception as e:
            raise ValidationError(f'无效的图片文件: {str(e)}')
        
        return value
    
    def validate_album(self, value):
        if value and value.user != self.context['request'].user:
            raise ValidationError('无权访问该相册')
        return value
    
    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        file = validated_data['file']
        
        file.seek(0)
        file_hash = hashlib.md5(file.read()).hexdigest()
        file.seek(0)
        
        if Image.objects.filter(file_hash=file_hash).exists():
            existing_image = Image.objects.get(file_hash=file_hash)
            return existing_image
        
        img = PILImage.open(file)
        file.seek(0)
        
        image = Image.objects.create(
            user=user,
            file=file,
            filename=file.name,
            file_size=file.size,
            file_hash=file_hash,
            width=img.width,
            height=img.height,
            format=img.format,
            album=validated_data.get('album'),
            title=validated_data.get('title', ''),
            description=validated_data.get('description', ''),
            tags=validated_data.get('tags', []),
            is_public=validated_data.get('is_public', False),
            storage_backend=settings.STORAGE_BACKEND,
            storage_path=''
        )
        
        user.storage_used += file.size
        user.save(update_fields=['storage_used'])
        
        return image


class ChunkUploadInitSerializer(serializers.Serializer):
    filename = serializers.CharField(max_length=255)
    file_size = serializers.IntegerField(min_value=1)
    file_hash = serializers.CharField(max_length=64)
    chunk_size = serializers.IntegerField(min_value=1, max_value=10485760)
    
    def validate_file_size(self, value):
        if value > settings.MAX_FILE_SIZE:
            raise ValidationError(f'文件大小不能超过 {settings.MAX_FILE_SIZE / 1024 / 1024}MB')
        return value


class ChunkUploadSerializer(serializers.Serializer):
    upload_id = serializers.CharField(max_length=64)
    chunk_number = serializers.IntegerField(min_value=1)
    chunk = serializers.FileField()
    
    def validate_chunk(self, value):
        max_chunk_size = 10485760
        if value.size > max_chunk_size:
            raise ValidationError(f'分块大小不能超过 {max_chunk_size / 1024 / 1024}MB')
        return value


class ChunkUploadCompleteSerializer(serializers.Serializer):
    upload_id = serializers.CharField(max_length=64)
    album = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(),
        required=False,
        allow_null=True
    )
    title = serializers.CharField(max_length=200, required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        allow_empty=True
    )
    is_public = serializers.BooleanField(default=False)
