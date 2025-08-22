from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
from app.core.database import get_db
from app.models.profiles import Profile
from app.schemas.profiles import ProfileResponse

router = APIRouter()


@router.get("/", response_model=List[ProfileResponse])
async def get_profiles(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """Get all profiles with their products"""
    result = await db.execute(
        select(Profile)
        .options(selectinload(Profile.products))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@router.get("/{profile_id}", response_model=ProfileResponse)
async def get_profile_by_id(
    profile_id: str, 
    db: AsyncSession = Depends(get_db)
):
    """Get a specific profile by ID with their products"""
    result = await db.execute(
        select(Profile)
        .options(selectinload(Profile.products))
        .where(Profile.id == profile_id)
    )
    profile = result.scalar_one_or_none()
    
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile