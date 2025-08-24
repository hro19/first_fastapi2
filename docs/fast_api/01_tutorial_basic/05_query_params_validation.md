# FastAPI Query Parameters and String Validations

## 概要
`Query`クラスと`Annotated`を使用して、クエリパラメータに詳細なバリデーションとメタデータを追加する方法について説明します。

## 基本的な文字列バリデーション

### 1. 基本的な使用方法
```python
from typing import Annotated
from fastapi import FastAPI, Query

@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

### 2. 複数の文字列バリデーション
```python
@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None, 
        Query(
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            alias="item-query",
        )
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

## バリデーションオプション

### 1. 文字列長の制約
- `min_length`: 最小文字数
- `max_length`: 最大文字数

### 2. 正規表現パターン
- `pattern`: 正規表現による形式チェック
- 例: `pattern="^fixedquery$"`（完全一致）

### 3. メタデータオプション
- `title`: パラメータのタイトル
- `description`: 詳細な説明
- `alias`: URLで使用する別名（ケバブケースなど）
- `deprecated`: 非推奨パラメータのマーク

## 必須パラメータの設定

### 1. デフォルト値なしで必須化
```python
@app.get("/items/")
async def read_items(q: Annotated[str, Query(min_length=3)]):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

### 2. `...`（Ellipsis）を使用した必須パラメータ
```python
@app.get("/items/")
async def read_items(q: Annotated[str, Query(min_length=3)] = ...):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    results.update({"q": q})
    return results
```

### 3. `Required`を使用した明示的な必須指定
```python
from pydantic import Required

@app.get("/items/")
async def read_items(q: Annotated[str, Query(min_length=3)] = Required):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    results.update({"q": q})
    return results
```

## 複数値パラメータ

### 1. リスト型クエリパラメータ
```python
@app.get("/items/")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items
```
- URL例: `http://localhost:8000/items/?q=foo&q=bar`
- 結果: `{"q": ["foo", "bar"]}`

### 2. デフォルト値付きリスト
```python
@app.get("/items/")
async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items
```

## 非推奨パラメータ

```python
@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

## OpenAPIスキーマからの除外

```python
@app.get("/items/")
async def read_items(
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}
```

## 主な利点
- 自動入力検証
- 明確なエラーメッセージ
- 強化されたAPIドキュメンテーション
- 柔軟なパラメータ設定
- 型安全性の向上
- エディタサポートの充実

## 推奨事項
- 現代的なFastAPIアプリケーションでは`Annotated`の使用を推奨
- パラメータバリデーションの際は`Query`を活用
- `alias`を使用してAPIのユーザビリティを向上

---
*出典: https://fastapi.tiangolo.com/tutorial/query-params-str-validations/*