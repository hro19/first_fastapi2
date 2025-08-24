# FastAPI Schema Extra - Example

## 概要
Pydanticモデル、フィールド、リクエストボディでサンプルデータを宣言し、APIドキュメンテーションを強化する方法について説明します。

## Pydanticモデル設定によるExample

### 1. model_configを使用したExample
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }
```

### 2. 関数による動的Example設定
```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    @staticmethod
    def json_schema_extra(schema, model_type):
        schema['examples'] = [
            {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        ]
```

## Field レベルでのExample

### 1. 個別フィールドでのExample指定
```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])
```

### 2. 複数のExample値
```python
class Item(BaseModel):
    name: str = Field(examples=["Laptop", "Phone", "Tablet"])
    price: float = Field(examples=[999.99, 699.99, 299.99])
    category: str = Field(examples=["electronics", "books", "clothing"])
```

## Body パラメータでのExample

### 1. Bodyクラスでの単一Example
```python
from typing import Annotated
from fastapi import Body

@app.put("/items/{item_id}")
async def update_item(
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "The description of the item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ],
        ),
    ],
):
    results = {"item": item}
    return results
```

### 2. 複数のExample
```python
@app.put("/items/{item_id}")
async def update_item(
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "The description of the item",
                    "price": 35.4,
                    "tax": 3.2,
                },
                {
                    "name": "Bar",
                    "description": "The bartenders",
                    "price": 62,
                    "tax": 20.2,
                },
                {
                    "name": "Baz",
                    "description": "There goes my baz",
                    "price": 50.2,
                    "tax": 10.5,
                },
            ],
        ),
    ],
):
    results = {"item": item}
    return results
```

## OpenAPI固有のExample

### 1. openapi_examples の使用
```python
@app.put("/items/{item_id}")
async def update_item(
    item: Annotated[
        Item,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
    results = {"item": item}
    return results
```

### 2. openapi_examples の構造
```python
{
    "example_name": {
        "summary": "短い要約",
        "description": "詳細な説明（Markdown対応）",
        "value": {
            # 実際のサンプルデータ
        }
    }
}
```

## 複数パラメータでのExample

### 1. 各パラメータごとのExample
```python
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "The description of the item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ],
        ),
    ],
    user: Annotated[
        User,
        Body(
            examples=[
                {
                    "username": "johndoe",
                    "email": "john@example.com",
                }
            ],
        ),
    ],
):
    results = {"item_id": item_id, "item": item, "user": user}
    return results
```

## Exampleの優先順位

### 1. 階層構造
1. **openapi_examples** （最優先）
2. **examples**
3. **Field レベルのexamples**
4. **model_config の examples**

### 2. 実際の優先適用例
```python
class Item(BaseModel):
    name: str = Field(examples=["Field Example"])  # 優先度: 低
    price: float
    
    model_config = {
        "json_schema_extra": {
            "examples": [{"name": "Model Example", "price": 100}]  # 優先度: 中
        }
    }

@app.post("/items/")
async def create_item(
    item: Annotated[
        Item,
        Body(
            examples=[{"name": "Body Example", "price": 200}],  # 優先度: 高
            openapi_examples={
                "main": {
                    "value": {"name": "OpenAPI Example", "price": 300}  # 優先度: 最高
                }
            }
        )
    ]
):
    return item
```

## Technical Note

### 1. OpenAPI 3.1.0 対応
- `examples` はJSON Schemaで標準化
- FastAPI は OpenAPI 3.1.0 をサポート
- Swagger UI 5.0 以降で完全サポート

### 2. 下位互換性
```python
# OpenAPI 3.0.x 互換
"example": {
    "name": "Foo",
    "price": 35.4
}

# OpenAPI 3.1.0 推奨
"examples": [
    {
        "name": "Foo", 
        "price": 35.4
    }
]
```

## 使用シナリオ

### 1. API ドキュメンテーション強化
- Swagger UI でのサンプル表示
- 開発者向けの明確な例示
- テストケースの提供

### 2. 開発・テスト支援
- 有効なリクエスト形式の例示
- 無効なデータでのエラー例
- エッジケースの説明

## 主な利点
- 強化されたAPIドキュメンテーション
- 開発者体験の向上
- 明確なAPI使用例
- テストケース提供
- エラーケースの説明
- 自動生成されるSDK品質の向上

---
*出典: https://fastapi.tiangolo.com/tutorial/schema-extra-example/*