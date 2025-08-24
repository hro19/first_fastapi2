# FastAPI First Steps

## 概要
FastAPIを使った最初のAPIの作成方法とその特徴について説明します。

## 基本的なコード例

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

## セットアップ手順

### 1. FastAPIのインポートと初期化
- `FastAPI` クラスをインポート
- アプリケーションインスタンスを作成

### 2. パス操作の定義
- デコレータを使用してHTTPメソッドとパスを定義
- パス操作関数を作成
- JSON形式で結果を返却（通常は辞書型）

### 3. アプリケーションの実行
```bash
fastapi dev main.py
```
- 開発サーバーが `http://127.0.0.1:8000` で起動

## 自動機能

### 1. 対話型APIドキュメンテーション
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### 2. OpenAPIスキーマ
- `http://127.0.0.1:8000/openapi.json` で自動生成されたスキーマを確認可能

## サポート対象HTTPメソッド
- GET
- POST
- PUT
- DELETE
- OPTIONS
- HEAD
- PATCH
- TRACE

## 主な特徴
- 非同期（async）と同期（sync）関数の両方をサポート
- 自動JSON変換
- 型ヒントとバリデーション
- セルフドキュメンテーション機能
- 最小限のボイラープレートコード

---
*出典: https://fastapi.tiangolo.com/tutorial/first-steps/*