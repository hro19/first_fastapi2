# FastAPI Path Parameters and Numeric Validations

## 概要
`Path`クラスと`Annotated`を使用して、パスパラメータに数値バリデーションとメタデータを追加する方法について説明します。

## 基本的な使用方法

### 1. Pathクラスのインポート
```python
from typing import Annotated
from fastapi import FastAPI, Path

app = FastAPI()
```

### 2. 基本的なパスパラメータバリデーション
```python
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")]
):
    return {"item_id": item_id}
```

## 数値バリデーション

### 1. 数値範囲の制約
```python
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)]
):
    return {"item_id": item_id}
```

### 2. 完全な数値制約例
```python
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1, le=1000)]
):
    return {"item_id": item_id}
```

## バリデーションオプション

### 1. 数値比較演算子
- `ge`: Greater than or Equal（以上）
- `gt`: Greater Than（より大きい）
- `le`: Less than or Equal（以下）
- `lt`: Less Than（より小さい）

### 2. 浮動小数点数での使用
```python
@app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str,
    size: Annotated[float, Query(gt=0, lt=10.5)]
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

## パラメータ順序の管理

### 1. アスタリスク（*）を使った順序制御
```python
@app.get("/items/{item_id}")
async def read_items(
    *, item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)], q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```
- `*` を使用してデフォルト値なしのパラメータ順序を制御

### 2. Annotatedによる簡潔な記述
```python
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)],
    q: Annotated[str, Query()]
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

## 複合バリデーション例

### 1. 複数制約の組み合わせ
```python
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: Annotated[int, Path(title="The ID of the user", ge=1)],
    item_id: Annotated[int, Path(title="The ID of the item", ge=1, le=1000)],
    q: Annotated[str | None, Query(alias="item-query")] = None,
    short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item"})
    return item
```

## メタデータオプション

### 1. 利用可能なメタデータ
- `title`: パラメータのタイトル
- `description`: 詳細な説明（Pathでは通常省略）
- `gt`, `ge`, `lt`, `le`: 数値制約
- `example`: サンプル値

### 2. 完全なメタデータ例
```python
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[
        int,
        Path(
            title="Item ID",
            description="The ID of the item to retrieve",
            ge=1,
            le=1000,
            example=123
        )
    ]
):
    return {"item_id": item_id}
```

## 主な利点
- 自動入力検証
- 数値範囲の強制
- 明確なエラーメッセージ
- 強化されたAPIドキュメンテーション
- 型安全性
- OpenAPIスキーマ生成

## ベストプラクティス
- `Annotated`の使用を推奨
- 特定の数値制約を設定
- パラメータに意味のあるメタデータを追加
- 整数と浮動小数点数の両方をサポート

---
*出典: https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/*