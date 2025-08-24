# FastAPI Response Model

## 概要
`response_model`パラメータを使用して、レスポンスデータの検証、フィルタリング、ドキュメンテーション生成を行う方法について説明します。

## 基本的な使用方法

### 1. response_modelの基本
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
```

### 2. 入力データと異なるレスポンスモデル
```python
class UserIn(BaseModel):
    username: str
    password: str
    email: str
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: str
    full_name: str | None = None

@app.post("/users/", response_model=UserOut)
async def create_user(user: UserIn):
    return user  # パスワードは自動的に除外される
```

## 機密データの除外

### 1. パスワードなど機密データの安全な処理
```python
class UserIn(BaseModel):
    username: str
    password: str
    email: str
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: str
    full_name: str | None = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: str
    full_name: str | None = None

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db

@app.post("/users/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved  # hashed_passwordは除外される
```

## レスポンスフィルタリング

### 1. response_model_exclude_unset
```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []

@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return {
        "name": "Laptop",
        "price": 999.99
        # description, tax, tagsは除外される（デフォルト値）
    }
```

### 2. response_model_include
```python
@app.get("/items/{item_id}", response_model=Item, response_model_include={"name", "price"})
async def read_item(item_id: str):
    return {
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 999.99,
        "tax": 99.99,
        "tags": ["electronics"]
    }
    # nameとpriceのみが返される
```

### 3. response_model_exclude
```python
@app.get("/items/{item_id}", response_model=Item, response_model_exclude={"tax"})
async def read_item(item_id: str):
    return {
        "name": "Laptop",
        "description": "Gaming laptop", 
        "price": 999.99,
        "tax": 99.99,  # 除外される
        "tags": ["electronics"]
    }
```

## モデル継承とDRY原則

### 1. 基底モデルの活用
```python
class UserBase(BaseModel):
    username: str
    email: str
    full_name: str | None = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass  # パスワードを含まない

class UserInDB(UserBase):
    hashed_password: str

@app.post("/users/", response_model=UserOut)
async def create_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    return user_in_db
```

## 複合レスポンスモデル

### 1. Union型の使用
```python
from typing import Union

class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type: str = "car"

class PlaneItem(BaseItem):
    type: str = "plane"
    size: int

@app.get("/items/{item_id}", response_model=Union[CarItem, PlaneItem])
async def read_item(item_id: str):
    if item_id == "car":
        return {"description": "Car description"}
    return {"description": "Plane description", "size": 5}
```

### 2. リスト型のレスポンス
```python
@app.get("/items/", response_model=list[Item])
async def read_items():
    return [
        {"name": "Item 1", "price": 100.0},
        {"name": "Item 2", "price": 200.0},
    ]
```

## 任意の辞書レスポンス

### 1. 辞書型レスポンス
```python
from typing import Any

@app.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}

@app.get("/items/{item_id}", response_model=dict[str, Any])
async def read_item(item_id: str):
    return {
        "item_id": item_id,
        "name": "Laptop",
        "price": 999.99,
        "metadata": {"category": "electronics", "in_stock": True}
    }
```

## レスポンスモデルの無効化

### 1. response_model=None
```python
@app.get("/items/{item_id}", response_model=None)
async def read_item(item_id: str):
    # 任意の形式で返却可能（バリデーション無し）
    return {"anything": "you want"}
```

## 高度な使用例

### 1. 動的フィールドフィルタリング
```python
@app.get("/items/{item_id}")
async def read_item(
    item_id: str, 
    include_sensitive: bool = False
):
    item_data = {
        "name": "Laptop",
        "price": 999.99,
        "internal_code": "INTERNAL_123",  # 機密情報
        "supplier": "SecretSupplier"       # 機密情報
    }
    
    if not include_sensitive:
        # 機密情報を動的に除外
        return {k: v for k, v in item_data.items() 
                if k not in ["internal_code", "supplier"]}
    
    return item_data
```

### 2. 条件付きレスポンスモデル
```python
def get_response_model(user_role: str):
    if user_role == "admin":
        return ItemWithInternalInfo
    return Item

@app.get("/items/{item_id}")
async def read_item(
    item_id: str,
    current_user_role: str = "user"
):
    model = get_response_model(current_user_role)
    # 動的にレスポンスモデルを適用
    pass
```

## 主な利点

### 1. セキュリティ
- 機密データの自動除外
- 意図しない情報漏洩の防止
- フィールドレベルの制御

### 2. ドキュメンテーション
- OpenAPI スキーマの自動生成
- 明確なAPIインターフェース定義
- クライアントコード生成の支援

### 3. 開発効率
- データ変換の自動化
- バリデーションの統一
- 型安全性の保証

## 使用シナリオ
- ユーザー管理システム（パスワード除外）
- 管理者・一般ユーザーでの情報制限
- API バージョニング
- データフィルタリング
- レスポンス最適化

---
*出典: https://fastapi.tiangolo.com/tutorial/response-model/*