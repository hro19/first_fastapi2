# FastAPI Body - Fields

## 概要
Pydantic `Field`を使用してモデル属性にバリデーションとメタデータを追加する方法について説明します。

## 基本的な使用方法

### 1. Fieldのインポート
```python
from pydantic import BaseModel, Field
```
**重要**: `Field`は`pydantic`からインポート（`fastapi`からではない）

### 2. 基本的なField使用例
```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None
```

## フィールドバリデーション

### 1. 数値制約
```python
class Item(BaseModel):
    name: str
    price: float = Field(gt=0, description="The price must be greater than zero")
    discount: float = Field(ge=0, le=100, description="Discount percentage (0-100)")
    quantity: int = Field(gt=0, le=1000, description="Item quantity")
```

### 2. 文字列制約
```python
class User(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: str = Field(pattern=r'^[^@]+@[^@]+\.[^@]+$')
    bio: str | None = Field(default=None, max_length=500)
```

### 3. リスト制約
```python
class Item(BaseModel):
    name: str
    tags: list[str] = Field(default=[], max_items=10, min_items=0)
    categories: set[str] = Field(default_factory=set, max_items=5)
```

## メタデータオプション

### 1. 利用可能なメタデータ
```python
class Item(BaseModel):
    name: str = Field(
        title="Item Name",
        description="The name of the item",
        example="Laptop",
        max_length=100
    )
    price: float = Field(
        title="Price",
        description="The price in USD",
        example=999.99,
        gt=0
    )
```

### 2. エイリアス
```python
class Item(BaseModel):
    name: str = Field(alias="itemName")
    item_price: float = Field(alias="price", gt=0)
```

## デフォルト値とオプションフィールド

### 1. デフォルト値の設定
```python
class Item(BaseModel):
    name: str
    description: str = Field(default="No description provided")
    price: float = Field(gt=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
```

### 2. Factory関数の使用
```python
from datetime import datetime
from uuid import uuid4

class Item(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    created_at: datetime = Field(default_factory=datetime.now)
    tags: list[str] = Field(default_factory=list)
```

## バリデーション制約一覧

### 1. 数値制約
- `gt`: より大きい（Greater Than）
- `ge`: 以上（Greater than or Equal）
- `lt`: より小さい（Less Than）
- `le`: 以下（Less than or Equal）
- `multiple_of`: 倍数

### 2. 文字列制約
- `min_length`: 最小文字数
- `max_length`: 最大文字数
- `pattern`: 正規表現パターン

### 3. コレクション制約
- `min_items`: 最小要素数
- `max_items`: 最大要素数
- `unique_items`: 重複排除（セット型で自動適用）

## OpenAPI Schema統合

### 1. スキーマ生成
```python
class Item(BaseModel):
    name: str = Field(
        title="Product Name",
        description="The name of the product for sale",
        example="Gaming Laptop"
    )
    price: float = Field(
        title="Price (USD)",
        description="Price in US dollars",
        example=1299.99,
        gt=0
    )
```
- フィールド情報がJSON Schemaに含まれる
- APIドキュメンテーションが強化される

### 2. 注意事項
- 一部の追加キーは全てのOpenAPIツールと互換性がない可能性
- 標準的な制約とメタデータの使用を推奨

## 高度な使用例

### 1. 条件付きフィールド
```python
class Product(BaseModel):
    name: str
    type: str = Field(pattern=r'^(physical|digital)$')
    weight: float | None = Field(
        default=None,
        gt=0,
        description="Weight in kg (required for physical products)"
    )
    file_size: int | None = Field(
        default=None,
        gt=0,
        description="File size in bytes (for digital products)"
    )
```

## 推奨プラクティス
- 可能な場合は`Annotated`型ヒントを使用
- `Field`で包括的なモデル属性定義を提供
- 意味のある説明と制約を含める
- 適切なデフォルト値を設定

## 主な利点
- モデル定義内での豊富な型安全バリデーション
- 自動ドキュメント生成の強化
- 明確なエラーメッセージ
- エディターサポートの改善
- JSON Schemaの詳細化

---
*出典: https://fastapi.tiangolo.com/tutorial/body-fields/*