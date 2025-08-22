from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from typing import List, Optional
import uuid
import logging
from datetime import datetime

from app.core.database import get_db
from app.models.image_analysis import ImageAnalysis
from app.schemas.image_analysis import (
    AnalysisResponse, 
    AnalysisHistoryResponse, 
    AnalysisStats
)
from app.services.azure_vision import azure_vision_service
from app.services.image_processing import image_processing_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_image(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload and analyze an image using Azure AI Vision
    
    Args:
        file: The image file to analyze
        db: Database session
        
    Returns:
        Analysis results with Azure AI Vision data
    """
    if not azure_vision_service:
        raise HTTPException(
            status_code=503,
            detail="Azure AI Vision service is not configured. Please set AZURE_VISION_KEY and AZURE_VISION_ENDPOINT."
        )
    
    try:
        # Validate and save the uploaded file
        file_info = await image_processing_service.validate_and_save_image(file)
        
        # Perform Azure AI Vision analysis
        azure_analysis = await azure_vision_service.analyze_image(file_info['file_path'])
        
        # Also get OCR results if available
        ocr_results = await azure_vision_service.analyze_image_with_text(file_info['file_path'])
        if ocr_results:
            azure_analysis['ocr'] = ocr_results
        
        # Save analysis results to database
        db_analysis = ImageAnalysis(
            filename=file_info['filename'],
            file_path=file_info['file_path'],
            file_size=file_info['file_size'],
            content_type=file_info['content_type'],
            azure_analysis=azure_analysis
        )
        
        db.add(db_analysis)
        await db.commit()
        await db.refresh(db_analysis)
        
        logger.info(f"Successfully analyzed image: {file_info['filename']} (ID: {db_analysis.id})")
        
        return db_analysis
        
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors, etc.)
        raise
    except Exception as e:
        logger.error(f"Error analyzing image {file.filename}: {str(e)}")
        
        # Clean up the saved file if something went wrong
        if 'file_info' in locals():
            await image_processing_service.delete_image_file(file_info['file_path'])
        
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing image: {str(e)}"
        )


@router.get("/history", response_model=List[AnalysisHistoryResponse])
async def get_analysis_history(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    content_type: Optional[str] = Query(None, description="Filter by content type"),
    search: Optional[str] = Query(None, description="Search in filename"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get analysis history with optional filtering
    
    Args:
        skip: Number of records to skip
        limit: Number of records to return
        content_type: Filter by content type
        search: Search in filename
        db: Database session
        
    Returns:
        List of analysis records
    """
    query = select(ImageAnalysis).order_by(desc(ImageAnalysis.created_at))
    
    # Apply filters
    if content_type:
        query = query.where(ImageAnalysis.content_type == content_type)
    if search:
        query = query.where(ImageAnalysis.filename.ilike(f"%{search}%"))
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    analyses = result.scalars().all()
    
    # Transform to history response format
    history_responses = []
    for analysis in analyses:
        # Calculate summary statistics from azure_analysis
        tags_count = None
        has_text = None
        
        if analysis.azure_analysis:
            if 'tags' in analysis.azure_analysis:
                tags_count = len(analysis.azure_analysis['tags'])
            if 'ocr' in analysis.azure_analysis:
                has_text = len(analysis.azure_analysis['ocr'].get('text_results', [])) > 0
        
        history_response = AnalysisHistoryResponse(
            id=analysis.id,
            filename=analysis.filename,
            file_size=analysis.file_size,
            content_type=analysis.content_type,
            created_at=analysis.created_at,
            tags_count=tags_count,
            has_text=has_text
        )
        history_responses.append(history_response)
    
    return history_responses


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis_by_id(
    analysis_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific analysis by ID
    
    Args:
        analysis_id: UUID of the analysis record
        db: Database session
        
    Returns:
        Full analysis details
    """
    result = await db.execute(
        select(ImageAnalysis).where(ImageAnalysis.id == analysis_id)
    )
    analysis = result.scalar_one_or_none()
    
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return analysis


@router.delete("/{analysis_id}")
async def delete_analysis(
    analysis_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete an analysis record and associated file
    
    Args:
        analysis_id: UUID of the analysis record
        db: Database session
        
    Returns:
        Success message
    """
    result = await db.execute(
        select(ImageAnalysis).where(ImageAnalysis.id == analysis_id)
    )
    analysis = result.scalar_one_or_none()
    
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # Delete the image file
    file_deleted = await image_processing_service.delete_image_file(analysis.file_path)
    if not file_deleted:
        logger.warning(f"Could not delete file: {analysis.file_path}")
    
    # Delete the database record
    await db.delete(analysis)
    await db.commit()
    
    logger.info(f"Deleted analysis: {analysis_id}")
    
    return {
        "message": "Analysis deleted successfully",
        "analysis_id": str(analysis_id),
        "file_deleted": file_deleted
    }


@router.get("/stats/summary", response_model=AnalysisStats)
async def get_analysis_stats(
    db: AsyncSession = Depends(get_db)
):
    """
    Get summary statistics for all analyses
    
    Args:
        db: Database session
        
    Returns:
        Analysis statistics
    """
    # Total analyses count
    total_count_result = await db.execute(
        select(func.count(ImageAnalysis.id))
    )
    total_analyses = total_count_result.scalar()
    
    # Total file size
    total_size_result = await db.execute(
        select(func.sum(ImageAnalysis.file_size))
    )
    total_file_size = total_size_result.scalar() or 0
    
    # Get all analyses for tag analysis
    all_analyses_result = await db.execute(
        select(ImageAnalysis.azure_analysis, ImageAnalysis.created_at)
    )
    all_analyses = all_analyses_result.all()
    
    # Calculate most common tags
    tag_counts = {}
    for analysis_data, created_at in all_analyses:
        if analysis_data and 'tags' in analysis_data:
            for tag in analysis_data['tags']:
                tag_name = tag.get('name', '').lower()
                if tag_name:
                    tag_counts[tag_name] = tag_counts.get(tag_name, 0) + 1
    
    # Get top 10 most common tags
    most_common_tags = [
        {"tag": tag, "count": count}
        for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    ]
    
    # Analysis by month (last 12 months)
    from collections import defaultdict
    monthly_counts = defaultdict(int)
    
    for analysis_data, created_at in all_analyses:
        if created_at:
            month_key = created_at.strftime("%Y-%m")
            monthly_counts[month_key] += 1
    
    analysis_by_month = [
        {"month": month, "count": count}
        for month, count in sorted(monthly_counts.items())
    ]
    
    return AnalysisStats(
        total_analyses=total_analyses,
        total_file_size=total_file_size,
        most_common_tags=most_common_tags,
        analysis_by_month=analysis_by_month
    )