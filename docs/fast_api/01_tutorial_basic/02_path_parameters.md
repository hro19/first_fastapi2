# FastAPI Path Parameters

## 概要
URLパス内で変数を定義し、関数の引数として利用する方法について説明します。

## 基本的な使用方法

### 1. パスパラメータの定義
```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

### 2. 型変換とバリデーション
- パスパラメータは宣言された型に自動変換される
- `int`, `str`, `float` など様々な型をサポート
- 型が合わない場合、明確なエラーメッセージが表示される

## 高度な機能

### 1. Enumによる事前定義値
```python
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}
```

### 2. パスを含むパラメータ
```python
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
```
- `:path` コンバーターを使用
- ファイルパスのような `/` を含む値を処理可能
- 例: `/files/home/johndoe/myfile.txt` → `file_path="home/johndoe/myfile.txt"`

## 重要な考慮点

### 1. パス操作の順序
```python
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```
- より具体的なパス（`/users/me`）を先に定義
- 順序が重要（上から下へ評価される）

### 2. パス操作の重複禁止
- 同一のパスとHTTPメソッドの組み合わせは再定義不可

## 主な利点
- 最小限のコードで堅牢なパラメータ処理
- 型安全性
- 自動ドキュメント生成
- 組み込みバリデーション
- Pydanticによる複雑な型バリデーション

## 自動ドキュメンテーション
- Swagger UIで対話型ドキュメント生成
- パラメータの型と制約を表示
- ReDoc代替ドキュメントも利用可能

---
*出典: https://fastapi.tiangolo.com/tutorial/path-params/*