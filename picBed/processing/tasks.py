from celery import shared_task
from PIL import Image as PILImage
from io import BytesIO
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger('picBed')


@shared_task(bind=True)
def process_image_task(self, image_id, operations):
    from images.models import Image
    
    try:
        image_obj = Image.objects.get(id=image_id)
        logger.info(f'Starting image processing task for image {image_id}')
        
        from .processor import ImageProcessor
        processor = ImageProcessor(image_file=image_obj.file)
        
        result_file = None
        
        for operation in operations:
            op_type = operation.get('type')
            params = operation.get('params', {})
            
            if op_type == 'compress':
                result_file = processor.compress(**params)
            elif op_type == 'convert':
                result_file = processor.convert_format(**params)
            elif op_type == 'resize':
                result_file = processor.resize(**params)
            elif op_type == 'watermark':
                result_file = processor.add_watermark(**params)
            elif op_type == 'crop':
                result_file = processor.crop(**params)
            elif op_type == 'rotate':
                result_file = processor.rotate(**params)
            elif op_type == 'flip':
                result_file = processor.flip(**params)
            else:
                logger.warning(f'Unknown operation type: {op_type}')
                continue
            
            if result_file:
                processor = ImageProcessor(image_file=result_file)
        
        if result_file:
            new_filename = f'processed_{image_obj.filename}'
            image_obj.file.save(new_filename, ContentFile(result_file.read()), save=True)
            
            img = PILImage.open(image_obj.file)
            image_obj.width = img.width
            image_obj.height = img.height
            image_obj.format = img.format
            image_obj.file_size = image_obj.file.size
            image_obj.save()
            
            logger.info(f'Image processing task completed for image {image_id}')
            return {'status': 'success', 'image_id': image_id}
        else:
            logger.warning(f'No processing performed for image {image_id}')
            return {'status': 'no_change', 'image_id': image_id}
            
    except Image.DoesNotExist:
        logger.error(f'Image {image_id} not found')
        return {'status': 'error', 'message': 'Image not found'}
    except Exception as e:
        logger.error(f'Image processing task failed: {str(e)}', exc_info=True)
        return {'status': 'error', 'message': str(e)}


@shared_task
def batch_process_images(image_ids, operations):
    results = []
    for image_id in image_ids:
        result = process_image_task.delay(image_id, operations)
        results.append({'image_id': image_id, 'task_id': result.id})
    
    logger.info(f'Batch processing initiated for {len(image_ids)} images')
    return results
