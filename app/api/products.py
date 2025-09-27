from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.core.database import get_db
from app.models.products import Product
from app.schemas.products import (
    ProductResponse,
    ProductCreate,
    ProductUpdate,
    ProductGroup,
)

router = APIRouter()


@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0, 
    limit: int = 100,
    profile_id: Optional[str] = Query(None, description="Filter by profile ID"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    search: Optional[str] = Query(None, description="Search in product name"),
    db: AsyncSession = Depends(get_db)
):
    """Get all products with optional filtering"""
    query = select(Product).options(selectinload(Product.profile))
    
    # Apply filters
    if profile_id:
        query = query.where(Product.profile_id == profile_id)
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)
    if search:
        query = query.where(Product.name.ilike(f"%{search}%"))
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/cat/{category}", response_model=List[ProductResponse])
async def get_products_by_category(
    category: str,
    db: AsyncSession = Depends(get_db)
):
    """Get all products matching a category"""
    query = select(Product).where(Product.category == category)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/groupby", response_model=List[ProductGroup])
async def get_products_grouped_by_category(
    db: AsyncSession = Depends(get_db)
):
    """Get products grouped by category"""
    result = await db.execute(select(Product))
    products = result.scalars().all()

    grouped = {}
    for product in products:
        category = product.category or "未分類"
        grouped.setdefault(category, []).append(product)

    response: List[ProductGroup] = []
    for category, items in grouped.items():
        prices = [item.price for item in items if item.price is not None]
        total_price = float(sum(prices)) if prices else 0.0
        avg_price = round(total_price / len(prices), 2) if prices else 0.0

        response.append(
            ProductGroup(
                category=category,
                length=len(items),
                total_price=total_price,
                avg_price=avg_price,
                products=items,
            )
        )

    return response


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_by_id(
    product_id: str, 
    db: AsyncSession = Depends(get_db)
):
    """Get a specific product by ID"""
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.profile))
        .where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product


@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new product"""
    # Verify profile exists if profile_id is provided
    if product.profile_id:
        result = await db.execute(
            select(Product).where(Product.profile_id == product.profile_id).limit(1)
        )
        if not result.scalar_one_or_none():
            # Check if profile exists
            from app.models.profiles import Profile
            profile_result = await db.execute(
                select(Profile).where(Profile.id == product.profile_id)
            )
            if not profile_result.scalar_one_or_none():
                raise HTTPException(status_code=404, detail="Profile not found")
    
    # For this example, we'll generate a simple ID (in real app, use the same function as DB)
    import secrets
    import string
    product_id = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(9))
    
    db_product = Product(id=product_id, **product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing product"""
    result = await db.execute(select(Product).where(Product.id == product_id))
    db_product = result.scalar_one_or_none()

    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product.model_dump(exclude_unset=True)

    if "profile_id" in update_data and update_data["profile_id"]:
        from app.models.profiles import Profile

        profile_result = await db.execute(
            select(Profile).where(Profile.id == update_data["profile_id"])
        )
        if profile_result.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail="Profile not found")

    for key, value in update_data.items():
        setattr(db_product, key, value)

    await db.commit()
    await db.refresh(db_product)
    return db_product
