from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="First FastAPI App", version="0.1.0")


class HealthResponse(BaseModel):
    status: str
    message: str


@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        message="Application is running successfully"
    )


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "query": q}


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False


@app.post("/items/")
async def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price, "is_offer": item.is_offer}