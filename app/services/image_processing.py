import os
import uuid
import aiofiles
from PIL import Image
from fastapi import HTTPException, UploadFile
from typing import Tuple, Dict, Any
import magic
import hashlib
from pathlib import Path
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class ImageProcessingService:
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.max_file_size = settings.MAX_FILE_SIZE
        self.allowed_types = settings.ALLOWED_IMAGE_TYPES
    
    async def validate_and_save_image(self, file: UploadFile) -> Dict[str, Any]:
        """
        Validate an uploaded image file and save it to disk
        
        Args:
            file: The uploaded file from FastAPI
            
        Returns:
            Dictionary containing file information
            
        Raises:
            HTTPException: If validation fails
        """
        # Validate file size
        if file.size and file.size > self.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size allowed: {self.max_file_size / (1024*1024):.1f}MB"
            )
        
        # Read file content
        content = await file.read()
        if len(content) > self.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size allowed: {self.max_file_size / (1024*1024):.1f}MB"
            )
        
        # Validate file type using python-magic
        file_type = magic.from_buffer(content, mime=True)
        if file_type not in self.allowed_types:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file type: {file_type}. Allowed types: {', '.join(self.allowed_types)}"
            )
        
        # Validate that it's actually an image using PIL
        try:
            image = Image.open(file.file)
            image.verify()  # Verify it's a valid image
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image file: {str(e)}"
            )
        
        # Reset file pointer after verification
        await file.seek(0)
        content = await file.read()
        
        # Generate unique filename
        file_extension = self._get_file_extension(file_type)
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Ensure upload directory exists
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Save file
        file_path = self.upload_dir / unique_filename
        try:
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(content)
        except Exception as e:
            logger.error(f"Error saving file {unique_filename}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error saving file")
        
        # Get image metadata
        image_info = await self._get_image_metadata(file_path)
        
        # Calculate file hash for deduplication
        file_hash = hashlib.md5(content).hexdigest()
        
        return {
            'filename': file.filename,
            'saved_filename': unique_filename,
            'file_path': str(file_path),
            'file_size': len(content),
            'content_type': file_type,
            'file_hash': file_hash,
            'image_info': image_info
        }
    
    def _get_file_extension(self, mime_type: str) -> str:
        """Get file extension from MIME type"""
        extensions = {
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'image/webp': '.webp'
        }
        return extensions.get(mime_type, '.jpg')
    
    async def _get_image_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from image file"""
        try:
            with Image.open(file_path) as img:
                metadata = {
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'mode': img.mode
                }
                
                # Extract EXIF data if available
                if hasattr(img, '_getexif') and img._getexif():
                    exif_data = img._getexif()
                    metadata['exif'] = {
                        k: v for k, v in exif_data.items() 
                        if isinstance(v, (str, int, float))
                    }
                
                return metadata
        except Exception as e:
            logger.warning(f"Could not extract metadata from {file_path}: {str(e)}")
            return {}
    
    async def delete_image_file(self, file_path: str) -> bool:
        """
        Delete an image file from disk
        
        Args:
            file_path: Path to the file to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            file_path_obj = Path(file_path)
            if file_path_obj.exists() and file_path_obj.parent == self.upload_dir:
                file_path_obj.unlink()
                logger.info(f"Deleted file: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {str(e)}")
            return False
    
    def get_file_size_formatted(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    async def validate_image_security(self, file_path: Path) -> bool:
        """
        Perform basic security validation on uploaded image
        
        Args:
            file_path: Path to the uploaded image
            
        Returns:
            True if image is safe, False otherwise
        """
        try:
            # Check file size again
            if file_path.stat().st_size > self.max_file_size:
                return False
            
            # Try to open and validate the image
            with Image.open(file_path) as img:
                # Check image dimensions (prevent extremely large images)
                if img.width > 10000 or img.height > 10000:
                    logger.warning(f"Image dimensions too large: {img.width}x{img.height}")
                    return False
                
                # Check for suspicious metadata
                if hasattr(img, '_getexif') and img._getexif():
                    exif_data = img._getexif()
                    # Look for suspicious EXIF data (this is a basic check)
                    if any(key in str(exif_data) for key in ['script', 'javascript', 'php']):
                        logger.warning("Suspicious EXIF data detected")
                        return False
            
            return True
        except Exception as e:
            logger.error(f"Security validation failed for {file_path}: {str(e)}")
            return False


# Global instance
image_processing_service = ImageProcessingService()