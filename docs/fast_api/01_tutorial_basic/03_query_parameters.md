# FastAPI Query Parameters

## 概要
URL内でクエリパラメータ（`?`以降の`key=value`形式）を処理する方法について説明します。

## 基本的な使用方法

### 1. クエリパラメータの定義
```python
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
```
- URL例: `http://127.0.0.1:8000/items/?skip=0&limit=10`

### 2. パスパラメータとの組み合わせ
```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

## 型変換とバリデーション

### 1. 自動型変換
- クエリパラメータは自然に文字列だが、宣言された型に自動変換
- `int`, `bool`, `str`, その他の型をサポート
- 指定された型に対して入力値をバリデーション

### 2. ブール値の変換
```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
```
- `true`, `True`, `1`, `yes`, `on` → `True`に変換
- その他 → `False`に変換

## 必須・オプションパラメータ

### 1. 必須パラメータ
```python
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    # needy: 必須パラメータ（デフォルト値なし）
    item = {"item_id": item_id, "needy": needy}
    return item
```

### 2. オプションパラメータ
```python
@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item
```

### 3. 複雑な組み合わせ例
```python
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, 
    item_id: str, 
    q: str | None = None, 
    short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
```

## 主な特徴
- 自動型変換
- 組み込みバリデーション
- 型ヒント付きの明確な関数シグネチャ
- OpenAPI/Swaggerとのシームレスな統合
- デフォルト値とオプション値のサポート
- パスパラメータとの柔軟な組み合わせ

## URLの構造
- `http://127.0.0.1:8000/users/123/items/foo?q=bar&short=true`
- パスパラメータ: `user_id=123`, `item_id="foo"`
- クエリパラメータ: `q="bar"`, `short=True`

---
*出典: https://fastapi.tiangolo.com/tutorial/query-params/*