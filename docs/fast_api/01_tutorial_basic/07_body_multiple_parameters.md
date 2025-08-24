# FastAPI Body - Multiple Parameters

## 概要
複数のリクエストボディパラメータを組み合わせ、パス・クエリ・ボディパラメータを統合的に処理する方法について説明します。

## 基本的な複数パラメータ

### 1. 複数のPydanticモデル
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results
```

### 2. リクエストボディ例
```json
{
  "item": {
    "name": "Foo",
    "description": "A very nice Item",
    "price": 35.4,
    "tax": 3.2
  },
  "user": {
    "username": "dave",
    "full_name": "Dave Grohl"
  }
}
```

## パス・クエリ・ボディの混合

### 1. 全パラメータタイプの組み合わせ
```python
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body()],
    q: str | None = None
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results
```

### 2. 対応するリクエストボディ
```json
{
  "item": {
    "name": "Foo",
    "description": "The description of the item",
    "price": 35.4,
    "tax": 3.2
  },
  "user": {
    "username": "dave",
    "full_name": "Dave Grohl"
  },
  "importance": 5
}
```

## 単一値ボディパラメータ

### 1. Bodyクラスの明示的使用
```python
from fastapi import Body

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],
    q: str | None = None
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results
```

### 2. 数値バリデーション付きボディ
```python
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    timestamp: Annotated[datetime, Body()],
    priority: Annotated[int, Body(gt=0, le=5)]
):
    results = {
        "item_id": item_id,
        "item": item,
        "timestamp": timestamp,
        "priority": priority
    }
    return results
```

## 埋め込み（Embed）オプション

### 1. 単一パラメータの埋め込み
```python
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results
```

### 2. 埋め込み時のリクエストボディ
```json
{
  "item": {
    "name": "Foo",
    "description": "The description of the item",
    "price": 35.4,
    "tax": 3.2
  }
}
```

### 3. 埋め込みなしの場合（通常）
```json
{
  "name": "Foo",
  "description": "The description of the item",
  "price": 35.4,
  "tax": 3.2
}
```

## 複雑な組み合わせ例

### 1. フル機能の組み合わせ
```python
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: Annotated[int, Path(title="The ID of the item", ge=0, le=1000)],
    q: Annotated[str | None, Query()] = None,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0, le=5)],
    notes: Annotated[str, Body(max_length=300)]
):
    results = {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance,
        "notes": notes
    }
    if q:
        results.update({"q": q})
    return results
```

### 2. 対応するリクエストボディ
```json
{
  "item": {
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 1200.50,
    "tax": 120.05
  },
  "user": {
    "username": "johndoe",
    "full_name": "John Doe"
  },
  "importance": 4,
  "notes": "Urgent order for corporate client"
}
```

## パラメータの分類

### 1. パスパラメータ
- URL内で `{parameter}` として定義
- 必須パラメータ

### 2. クエリパラメータ
- パス操作関数でPydanticモデルでない単一型
- オプションまたは必須

### 3. リクエストボディ
- Pydanticモデルとして宣言
- `Body()` で明示的に宣言された単一値

## 主な利点
- 柔軟なパラメータ組み合わせ
- 自動型変換とバリデーション
- 包括的なドキュメント生成
- 明確な分離されたデータ構造
- リクエスト構造の一貫性

## 使用シナリオ
- 複雑なAPIエンドポイント
- 複数エンティティの操作
- メタデータと主要データの分離
- バリデーション規則の細分化

---
*出典: https://fastapi.tiangolo.com/tutorial/body-multiple-params/*