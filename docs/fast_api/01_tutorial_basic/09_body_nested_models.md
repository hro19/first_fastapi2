# FastAPI Body - Nested Models

## 概要
Pydanticモデル内でのリスト、セット、ネストしたモデル、複雑なデータ構造の使用方法について説明します。

## リスト型フィールド

### 1. 基本的なリスト
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
```

### 2. Python バージョン別の記法
```python
# Python 3.9+
tags: list[str] = []

# Python 3.8以前
from typing import List
tags: List[str] = []
```

## セット型フィールド

### 1. 重複排除されたリスト
```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
```
- セット型は自動的に重複を排除
- JSON変換時はリストとして表現

## ネストしたモデル

### 1. サブモデルの定義
```python
from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None
```

### 2. リクエスト例
```json
{
    "name": "Laptop",
    "description": "Gaming laptop",
    "price": 1299.99,
    "tax": 130.0,
    "tags": ["electronics", "computers"],
    "image": {
        "url": "https://example.com/laptop.jpg",
        "name": "laptop-image"
    }
}
```

## 特別な型

### 1. HttpUrl型
```python
from pydantic import HttpUrl

class Image(BaseModel):
    url: HttpUrl  # URL形式を自動バリデーション
    name: str
```

### 2. その他の特別な型
```python
from datetime import datetime
from pydantic import BaseModel, EmailStr, validator

class User(BaseModel):
    username: str
    email: EmailStr  # メールアドレス形式をバリデーション
    signup_ts: datetime | None = None
    age: int | None = None
```

## リストとしてのネストしたモデル

### 1. モデルのリスト
```python
class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None
```

### 2. 複数画像のリクエスト例
```json
{
    "name": "Laptop",
    "description": "Gaming laptop",
    "price": 1299.99,
    "tax": 130.0,
    "tags": ["electronics", "computers"],
    "images": [
        {
            "url": "https://example.com/laptop-front.jpg",
            "name": "front-view"
        },
        {
            "url": "https://example.com/laptop-side.jpg",
            "name": "side-view"
        }
    ]
}
```

## 深いネスト構造

### 1. 複雑なネストモデル
```python
class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None

class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]
```

### 2. 任意の辞書型
```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
    metadata: dict[str, str] = {}
```

## 純粋なリスト

### 1. ルートレベルでのリスト
```python
@app.post("/items/")
async def create_items(items: list[Item]):
    return items
```

### 2. リクエスト例
```json
[
    {
        "name": "Laptop",
        "price": 1299.99
    },
    {
        "name": "Mouse",
        "price": 29.99
    }
]
```

## URLからのリクエスト本文

### 1. HTTPから直接リクエスト受信
```python
@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images
```

### 2. エディターサポート
- 自動補完が利用可能
- 型チェック
- エラーハイライト
- リファクタリング支援

## 複雑な例

### 1. 完全なネストしたアプリケーション
```python
from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field

class Image(BaseModel):
    url: HttpUrl
    name: str
    created_at: datetime = Field(default_factory=datetime.now)

class Tag(BaseModel):
    name: str
    color: str = "#000000"

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float = Field(gt=0)
    tax: float | None = Field(default=None, ge=0)
    tags: list[Tag] = []
    images: list[Image] = []
    metadata: dict[str, str | int | float] = {}

class Order(BaseModel):
    items: list[Item]
    customer_id: int
    order_date: datetime = Field(default_factory=datetime.now)
    notes: str | None = None
```

## 主な利点
- 自動データ変換
- 型バリデーション
- スキーマドキュメンテーション
- 優秀なエディターサポート
- 直感的なモデル定義
- 複雑なJSON構造のサポート

## 使用シナリオ
- 製品カタログ
- ユーザープロファイル
- 注文システム
- コンテンツ管理
- 設定データ
- API間のデータ交換

---
*出典: https://fastapi.tiangolo.com/tutorial/body-nested-models/*