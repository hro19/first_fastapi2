# FastAPI Request Body

## 概要
クライアントからAPIに送信されるリクエストボディをPydanticモデルで処理する方法について説明します。

## 基本的な実装

### 1. Pydanticモデルの定義
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
```

### 2. リクエストボディを受け取るエンドポイント
```python
@app.post("/items/")
async def create_item(item: Item):
    return item
```

### 3. リクエストボディの使用例
```python
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
```

## パラメータの組み合わせ

### 1. パス、クエリ、ボディパラメータの併用
```python
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
```

## 主な機能

### 1. 自動JSON解析
- JSONリクエストボディを自動的にPythonオブジェクトに変換
- 手動でJSONパースする必要がない

### 2. 型バリデーション
- Pydanticモデルによる強力なバリデーション
- 型の不一致時に明確なエラーメッセージ
- ネストしたデータ構造もサポート

### 3. エディターサポート
- 型ヒントによる自動補完
- IDEでの型チェック
- リファクタリング支援

### 4. 自動ドキュメント生成
- OpenAPI/Swaggerで自動ドキュメンテーション
- JSON Schemaの自動生成
- 対話型API explorer

## リクエスト例
```json
{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 1200.50,
    "tax": 120.05
}
```

## レスポンス例
```json
{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 1200.50,
    "tax": 120.05,
    "price_with_tax": 1320.55
}
```

## 高度な機能

### 1. オプショナルフィールド
- `| None = None` による省略可能フィールド
- デフォルト値の設定

### 2. ネストしたモデル
```python
class Image(BaseModel):
    url: str
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
    images: list[Image] | None = None
```

### 3. カスタムバリデーション
- Pydanticのバリデーター機能
- 複雑なビジネスロジックの実装

## 主な利点
- 強い型付け
- ランタイム型チェック
- セルフドキュメンテーションコード
- 自動APIドキュメント
- 簡素化されたデータ処理
- 明確なエラーメッセージ

---
*出典: https://fastapi.tiangolo.com/tutorial/body/*