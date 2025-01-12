# CLI module initialization
from .ocr import OCR
from .image_processing import ImageProcessor
from .vision_module import Vision  # Add this line

__all__ = ['OCR', 'ImageProcessor', 'Vision']