import os
from io import BytesIO
from PIL import Image as PILImage, ImageDraw, ImageFont
from django.conf import settings
import logging

logger = logging.getLogger('picBed')


class ImageProcessor:
    def __init__(self, image_path=None, image_file=None):
        if image_path:
            self.image = PILImage.open(image_path)
        elif image_file:
            self.image = PILImage.open(image_file)
        else:
            raise ValueError('Either image_path or image_file must be provided')
        
        self.original_format = self.image.format
        self.original_mode = self.image.mode
    
    def compress(self, quality=85, format=None):
        if format is None:
            format = self.original_format or 'JPEG'
        
        output = BytesIO()
        
        if format.upper() == 'JPEG':
            if self.image.mode in ('RGBA', 'P'):
                self.image = self.image.convert('RGB')
            self.image.save(output, format=format, quality=quality, optimize=True)
        elif format.upper() == 'PNG':
            self.image.save(output, format=format, optimize=True)
        elif format.upper() == 'WEBP':
            self.image.save(output, format=format, quality=quality)
        else:
            self.image.save(output, format=format)
        
        output.seek(0)
        logger.info(f'Image compressed: quality={quality}, format={format}')
        return output
    
    def convert_format(self, target_format):
        target_format = target_format.upper()
        
        if target_format not in ['JPEG', 'PNG', 'GIF', 'WEBP', 'BMP']:
            raise ValueError(f'Unsupported format: {target_format}')
        
        output = BytesIO()
        
        if target_format == 'JPEG':
            if self.image.mode in ('RGBA', 'P'):
                self.image = self.image.convert('RGB')
        
        self.image.save(output, format=target_format)
        output.seek(0)
        
        logger.info(f'Image format converted: {self.original_format} -> {target_format}')
        return output
    
    def resize(self, width=None, height=None, maintain_aspect=True):
        original_width, original_height = self.image.size
        
        if width is None and height is None:
            raise ValueError('At least one of width or height must be provided')
        
        if maintain_aspect:
            if width is None:
                ratio = height / original_height
                width = int(original_width * ratio)
            elif height is None:
                ratio = width / original_width
                height = int(original_height * ratio)
        else:
            if width is None:
                width = original_width
            if height is None:
                height = original_height
        
        resized_image = self.image.resize((width, height), PILImage.LANCZOS)
        
        output = BytesIO()
        resized_image.save(output, format=self.original_format or 'JPEG')
        output.seek(0)
        
        logger.info(f'Image resized: {original_width}x{original_height} -> {width}x{height}')
        return output
    
    def add_watermark(self, watermark_text=None, watermark_image=None, position='bottom-right', opacity=128):
        if watermark_text and watermark_image:
            raise ValueError('Only one of watermark_text or watermark_image can be provided')
        
        if watermark_text:
            watermarked = self._add_text_watermark(watermark_text, position, opacity)
        elif watermark_image:
            watermarked = self._add_image_watermark(watermark_image, position, opacity)
        else:
            raise ValueError('Either watermark_text or watermark_image must be provided')
        
        output = BytesIO()
        watermarked.save(output, format=self.original_format or 'JPEG')
        output.seek(0)
        
        logger.info(f'Watermark added: position={position}')
        return output
    
    def _add_text_watermark(self, text, position, opacity):
        img = self.image.copy()
        
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        txt_img = PILImage.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()
        
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x, y = self._calculate_position(position, img.size, (text_width, text_height))
        
        draw.text((x, y), text, fill=(255, 255, 255, opacity), font=font)
        
        watermarked = PILImage.alpha_composite(img, txt_img)
        
        if self.original_mode != 'RGBA':
            watermarked = watermarked.convert(self.original_mode)
        
        return watermarked
    
    def _add_image_watermark(self, watermark_path, position, opacity):
        img = self.image.copy()
        
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        watermark = PILImage.open(watermark_path)
        
        if watermark.mode != 'RGBA':
            watermark = watermark.convert('RGBA')
        
        watermark = watermark.resize(
            (img.width // 4, img.height // 4),
            PILImage.LANCZOS
        )
        
        x, y = self._calculate_position(position, img.size, watermark.size)
        
        watermark_with_opacity = PILImage.new('RGBA', watermark.size, (0, 0, 0, 0))
        for i in range(watermark.width):
            for j in range(watermark.height):
                r, g, b, a = watermark.getpixel((i, j))
                watermark_with_opacity.putpixel((i, j), (r, g, b, int(a * opacity / 255)))
        
        img.paste(watermark_with_opacity, (x, y), watermark_with_opacity)
        
        if self.original_mode != 'RGBA':
            img = img.convert(self.original_mode)
        
        return img
    
    def _calculate_position(self, position, img_size, watermark_size):
        img_width, img_height = img_size
        wm_width, wm_height = watermark_size
        padding = 20
        
        positions = {
            'top-left': (padding, padding),
            'top-center': ((img_width - wm_width) // 2, padding),
            'top-right': (img_width - wm_width - padding, padding),
            'center-left': (padding, (img_height - wm_height) // 2),
            'center': ((img_width - wm_width) // 2, (img_height - wm_height) // 2),
            'center-right': (img_width - wm_width - padding, (img_height - wm_height) // 2),
            'bottom-left': (padding, img_height - wm_height - padding),
            'bottom-center': ((img_width - wm_width) // 2, img_height - wm_height - padding),
            'bottom-right': (img_width - wm_width - padding, img_height - wm_height - padding),
        }
        
        return positions.get(position, positions['bottom-right'])
    
    def crop(self, left, top, right, bottom):
        cropped = self.image.crop((left, top, right, bottom))
        
        output = BytesIO()
        cropped.save(output, format=self.original_format or 'JPEG')
        output.seek(0)
        
        logger.info(f'Image cropped: ({left}, {top}, {right}, {bottom})')
        return output
    
    def rotate(self, angle):
        rotated = self.image.rotate(angle, expand=True)
        
        output = BytesIO()
        rotated.save(output, format=self.original_format or 'JPEG')
        output.seek(0)
        
        logger.info(f'Image rotated: {angle} degrees')
        return output
    
    def flip(self, direction='horizontal'):
        if direction == 'horizontal':
            flipped = self.image.transpose(PILImage.FLIP_LEFT_RIGHT)
        elif direction == 'vertical':
            flipped = self.image.transpose(PILImage.FLIP_TOP_BOTTOM)
        else:
            raise ValueError('Direction must be "horizontal" or "vertical"')
        
        output = BytesIO()
        flipped.save(output, format=self.original_format or 'JPEG')
        output.seek(0)
        
        logger.info(f'Image flipped: {direction}')
        return output
