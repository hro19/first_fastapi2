from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.playing_with_neon import PlayingWithNeon
from app.schemas.playing_with_neon import PlayingWithNeonResponse, PlayingWithNeonCreate

router = APIRouter()


@router.get("/", response_model=List[PlayingWithNeonResponse])
async def get_playing_with_neon(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """Get all playing_with_neon records"""
    result = await db.execute(
        select(PlayingWithNeon).offset(skip).limit(limit)
    )
    return result.scalars().all()


@router.get("/{item_id}", response_model=PlayingWithNeonResponse)
async def get_playing_with_neon_by_id(
    item_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """Get a specific playing_with_neon record by ID"""
    result = await db.execute(
        select(PlayingWithNeon).where(PlayingWithNeon.id == item_id)
    )
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item


@router.post("/", response_model=PlayingWithNeonResponse)
async def create_playing_with_neon(
    item: PlayingWithNeonCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new playing_with_neon record"""
    db_item = PlayingWithNeon(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item