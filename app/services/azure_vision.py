from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from typing import Dict, Any, Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class AzureVisionService:
    def __init__(self):
        if not settings.AZURE_VISION_KEY or not settings.AZURE_VISION_ENDPOINT:
            raise ValueError("Azure Vision API key and endpoint must be configured")
        
        self.client = ComputerVisionClient(
            settings.AZURE_VISION_ENDPOINT,
            CognitiveServicesCredentials(settings.AZURE_VISION_KEY)
        )
    
    async def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze an image using Azure Computer Vision API
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            with open(image_path, "rb") as image_data:
                # Define what visual features we want to analyze
                visual_features = [
                    VisualFeatureTypes.tags,
                    VisualFeatureTypes.description,
                    VisualFeatureTypes.categories,
                    VisualFeatureTypes.color,
                    VisualFeatureTypes.image_type,
                    VisualFeatureTypes.objects,
                    VisualFeatureTypes.brands,
                    VisualFeatureTypes.adult
                ]
                
                # Call the API
                analysis = self.client.analyze_image_in_stream(
                    image_data,
                    visual_features=visual_features
                )
                
                # Convert to dictionary
                result = self._format_analysis_result(analysis)
                
                logger.info(f"Successfully analyzed image: {image_path}")
                return result
                
        except Exception as e:
            logger.error(f"Error analyzing image {image_path}: {str(e)}")
            raise
    
    def _format_analysis_result(self, analysis) -> Dict[str, Any]:
        """
        Format the Azure API response into a structured dictionary
        """
        result = {}
        
        # Tags
        if hasattr(analysis, 'tags') and analysis.tags:
            result['tags'] = [
                {
                    'name': tag.name,
                    'confidence': tag.confidence
                }
                for tag in analysis.tags
            ]
        
        # Description
        if hasattr(analysis, 'description') and analysis.description:
            result['description'] = {
                'captions': [
                    {
                        'text': caption.text,
                        'confidence': caption.confidence
                    }
                    for caption in analysis.description.captions
                ] if analysis.description.captions else [],
                'tags': analysis.description.tags if analysis.description.tags else []
            }
        
        # Categories
        if hasattr(analysis, 'categories') and analysis.categories:
            result['categories'] = [
                {
                    'name': category.name,
                    'score': category.score
                }
                for category in analysis.categories
            ]
        
        # Color analysis
        if hasattr(analysis, 'color') and analysis.color:
            result['color'] = {
                'dominant_color_foreground': analysis.color.dominant_color_foreground,
                'dominant_color_background': analysis.color.dominant_color_background,
                'dominant_colors': analysis.color.dominant_colors,
                'accent_color': analysis.color.accent_color,
                'is_bw_img': analysis.color.is_bw_img
            }
        
        # Objects
        if hasattr(analysis, 'objects') and analysis.objects:
            result['objects'] = [
                {
                    'object_property': obj.object_property,
                    'confidence': obj.confidence,
                    'rectangle': {
                        'x': obj.rectangle.x,
                        'y': obj.rectangle.y,
                        'w': obj.rectangle.w,
                        'h': obj.rectangle.h
                    }
                }
                for obj in analysis.objects
            ]
        
        # Brands
        if hasattr(analysis, 'brands') and analysis.brands:
            result['brands'] = [
                {
                    'name': brand.name,
                    'confidence': brand.confidence,
                    'rectangle': {
                        'x': brand.rectangle.x,
                        'y': brand.rectangle.y,
                        'w': brand.rectangle.w,
                        'h': brand.rectangle.h
                    }
                }
                for brand in analysis.brands
            ]
        
        # Image type
        if hasattr(analysis, 'image_type') and analysis.image_type:
            result['image_type'] = {
                'clip_art_type': analysis.image_type.clip_art_type,
                'line_drawing_type': analysis.image_type.line_drawing_type
            }
        
        # Adult content
        if hasattr(analysis, 'adult') and analysis.adult:
            result['adult'] = {
                'is_adult_content': analysis.adult.is_adult_content,
                'adult_score': analysis.adult.adult_score,
                'is_racy_content': analysis.adult.is_racy_content,
                'racy_score': analysis.adult.racy_score,
                'is_gory_content': analysis.adult.is_gory_content,
                'gore_score': analysis.adult.gore_score
            }
        
        return result
    
    async def analyze_image_with_text(self, image_path: str) -> Optional[Dict[str, Any]]:
        """
        Extract text from an image using OCR
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing OCR results
        """
        try:
            with open(image_path, "rb") as image_data:
                # Use the read API for OCR
                read_response = self.client.read_in_stream(image_data, raw=True)
                
                # Get the operation location (URL with an ID at the end) from the response
                read_operation_location = read_response.headers["Operation-Location"]
                operation_id = read_operation_location.split("/")[-1]
                
                # Wait for the read operation to complete
                import time
                while True:
                    read_result = self.client.get_read_result(operation_id)
                    if read_result.status not in ['notStarted', 'running']:
                        break
                    time.sleep(1)
                
                # Process the OCR results
                if read_result.status == 'succeeded':
                    text_results = []
                    if read_result.analyze_result.read_results:
                        for text_result in read_result.analyze_result.read_results:
                            for line in text_result.lines:
                                text_results.append({
                                    'text': line.text,
                                    'bounding_box': line.bounding_box
                                })
                    
                    return {
                        'status': 'succeeded',
                        'text_results': text_results
                    }
                else:
                    return {
                        'status': 'failed',
                        'text_results': []
                    }
                    
        except Exception as e:
            logger.error(f"Error extracting text from image {image_path}: {str(e)}")
            return None


# Global instance
azure_vision_service = AzureVisionService() if settings.AZURE_VISION_KEY and settings.AZURE_VISION_ENDPOINT else None