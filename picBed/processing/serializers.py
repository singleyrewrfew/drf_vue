from rest_framework import serializers


class ImageProcessSerializer(serializers.Serializer):
    operations = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False
    )
    
    def validate_operations(self, value):
        valid_operations = ['compress', 'convert', 'resize', 'watermark', 'crop', 'rotate', 'flip']
        
        for operation in value:
            if 'type' not in operation:
                raise serializers.ValidationError('Each operation must have a "type" field')
            
            if operation['type'] not in valid_operations:
                raise serializers.ValidationError(f'Invalid operation type: {operation["type"]}')
        
        return value


class CompressOperationSerializer(serializers.Serializer):
    quality = serializers.IntegerField(min_value=1, max_value=100, default=85)
    format = serializers.ChoiceField(
        choices=['JPEG', 'PNG', 'WEBP'],
        required=False
    )


class ConvertOperationSerializer(serializers.Serializer):
    target_format = serializers.ChoiceField(
        choices=['JPEG', 'PNG', 'GIF', 'WEBP', 'BMP']
    )


class ResizeOperationSerializer(serializers.Serializer):
    width = serializers.IntegerField(min_value=1, required=False)
    height = serializers.IntegerField(min_value=1, required=False)
    maintain_aspect = serializers.BooleanField(default=True)
    
    def validate(self, data):
        if 'width' not in data and 'height' not in data:
            raise serializers.ValidationError('At least one of width or height must be provided')
        return data


class WatermarkOperationSerializer(serializers.Serializer):
    watermark_text = serializers.CharField(max_length=200, required=False)
    watermark_image = serializers.ImageField(required=False)
    position = serializers.ChoiceField(
        choices=[
            'top-left', 'top-center', 'top-right',
            'center-left', 'center', 'center-right',
            'bottom-left', 'bottom-center', 'bottom-right'
        ],
        default='bottom-right'
    )
    opacity = serializers.IntegerField(min_value=0, max_value=255, default=128)
    
    def validate(self, data):
        if 'watermark_text' not in data and 'watermark_image' not in data:
            raise serializers.ValidationError('Either watermark_text or watermark_image must be provided')
        return data


class CropOperationSerializer(serializers.Serializer):
    left = serializers.IntegerField(min_value=0)
    top = serializers.IntegerField(min_value=0)
    right = serializers.IntegerField(min_value=1)
    bottom = serializers.IntegerField(min_value=1)
    
    def validate(self, data):
        if data['right'] <= data['left']:
            raise serializers.ValidationError('right must be greater than left')
        if data['bottom'] <= data['top']:
            raise serializers.ValidationError('bottom must be greater than top')
        return data


class RotateOperationSerializer(serializers.Serializer):
    angle = serializers.FloatField()


class FlipOperationSerializer(serializers.Serializer):
    direction = serializers.ChoiceField(choices=['horizontal', 'vertical'])
