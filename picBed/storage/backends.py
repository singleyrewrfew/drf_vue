import os
import logging
from abc import ABC, abstractmethod
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import File

logger = logging.getLogger('picBed')


class StorageBackend(ABC):
    @abstractmethod
    def save(self, name, content):
        pass
    
    @abstractmethod
    def delete(self, name):
        pass
    
    @abstractmethod
    def exists(self, name):
        pass
    
    @abstractmethod
    def url(self, name):
        pass
    
    @abstractmethod
    def size(self, name):
        pass


class LocalStorageBackend(StorageBackend):
    def __init__(self):
        self.storage = default_storage
    
    def save(self, name, content):
        try:
            saved_path = self.storage.save(name, content)
            logger.info(f'File saved locally: {saved_path}')
            return saved_path
        except Exception as e:
            logger.error(f'Failed to save file locally: {str(e)}')
            raise
    
    def delete(self, name):
        try:
            self.storage.delete(name)
            logger.info(f'File deleted from local storage: {name}')
        except Exception as e:
            logger.error(f'Failed to delete file from local storage: {str(e)}')
            raise
    
    def exists(self, name):
        return self.storage.exists(name)
    
    def url(self, name):
        return self.storage.url(name)
    
    def size(self, name):
        return self.storage.size(name)


class S3StorageBackend(StorageBackend):
    def __init__(self):
        import boto3
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    
    def save(self, name, content):
        try:
            self.s3_client.upload_fileobj(
                content,
                self.bucket_name,
                name,
                ExtraArgs={
                    'ContentType': content.content_type if hasattr(content, 'content_type') else 'application/octet-stream'
                }
            )
            url = f'https://{self.bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{name}'
            logger.info(f'File saved to S3: {name}')
            return url
        except Exception as e:
            logger.error(f'Failed to save file to S3: {str(e)}')
            raise
    
    def delete(self, name):
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=name)
            logger.info(f'File deleted from S3: {name}')
        except Exception as e:
            logger.error(f'Failed to delete file from S3: {str(e)}')
            raise
    
    def exists(self, name):
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=name)
            return True
        except:
            return False
    
    def url(self, name):
        return f'https://{self.bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{name}'
    
    def size(self, name):
        try:
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=name)
            return response['ContentLength']
        except:
            return 0


class OSSStorageBackend(StorageBackend):
    def __init__(self):
        import oss2
        auth = oss2.Auth(
            settings.ALIYUN_ACCESS_KEY_ID,
            settings.ALIYUN_ACCESS_KEY_SECRET
        )
        self.bucket = oss2.Bucket(
            auth,
            settings.ALIYUN_OSS_ENDPOINT,
            settings.ALIYUN_OSS_BUCKET_NAME
        )
    
    def save(self, name, content):
        try:
            content.seek(0)
            self.bucket.put_object(name, content.read())
            url = f'https://{settings.ALIYUN_OSS_BUCKET_NAME}.{settings.ALIYUN_OSS_ENDPOINT}/{name}'
            logger.info(f'File saved to OSS: {name}')
            return url
        except Exception as e:
            logger.error(f'Failed to save file to OSS: {str(e)}')
            raise
    
    def delete(self, name):
        try:
            self.bucket.delete_object(name)
            logger.info(f'File deleted from OSS: {name}')
        except Exception as e:
            logger.error(f'Failed to delete file from OSS: {str(e)}')
            raise
    
    def exists(self, name):
        return self.bucket.object_exists(name)
    
    def url(self, name):
        return f'https://{settings.ALIYUN_OSS_BUCKET_NAME}.{settings.ALIYUN_OSS_ENDPOINT}/{name}'
    
    def size(self, name):
        try:
            info = self.bucket.get_object_meta(name)
            return info.content_length
        except:
            return 0


class StorageManager:
    _backends = {
        'local': LocalStorageBackend,
        's3': S3StorageBackend,
        'oss': OSSStorageBackend,
    }
    
    _instances = {}
    
    @classmethod
    def get_backend(cls, backend_name=None):
        if backend_name is None:
            backend_name = settings.STORAGE_BACKEND
        
        if backend_name not in cls._instances:
            backend_class = cls._backends.get(backend_name)
            if backend_class is None:
                raise ValueError(f'Unsupported storage backend: {backend_name}')
            cls._instances[backend_name] = backend_class()
        
        return cls._instances[backend_name]
    
    @classmethod
    def save(cls, name, content, backend_name=None):
        backend = cls.get_backend(backend_name)
        return backend.save(name, content)
    
    @classmethod
    def delete(cls, name, backend_name=None):
        backend = cls.get_backend(backend_name)
        return backend.delete(name)
    
    @classmethod
    def exists(cls, name, backend_name=None):
        backend = cls.get_backend(backend_name)
        return backend.exists(name)
    
    @classmethod
    def url(cls, name, backend_name=None):
        backend = cls.get_backend(backend_name)
        return backend.url(name)
    
    @classmethod
    def size(cls, name, backend_name=None):
        backend = cls.get_backend(backend_name)
        return backend.size(name)
