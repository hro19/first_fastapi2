# FastAPI Header Parameters

## 概要
`Header`クラスを使用してHTTPヘッダーをパラメータとして処理する方法について説明します。

## 基本的な使用方法

### 1. Headerクラスのインポート
```python
from typing import Annotated
from fastapi import FastAPI, Header

app = FastAPI()
```

### 2. 基本的なヘッダーパラメータ
```python
@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
```

### 3. 複数ヘッダーの処理
```python
@app.get("/info/")
async def read_info(
    user_agent: Annotated[str | None, Header()] = None,
    accept_language: Annotated[str | None, Header()] = None,
    x_token: Annotated[str | None, Header()] = None
):
    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language,
        "X-Token": x_token
    }
```

## アンダースコア・ハイフン変換

### 1. 自動変換機能
```python
@app.get("/items/")
async def read_items(
    # accept_encoding → Accept-Encoding に自動変換
    accept_encoding: Annotated[str | None, Header()] = None,
    # content_type → Content-Type に自動変換
    content_type: Annotated[str | None, Header()] = None
):
    return {
        "Accept-Encoding": accept_encoding,
        "Content-Type": content_type
    }
```

### 2. 変換の無効化
```python
@app.get("/items/")
async def read_items(
    # アンダースコア変換を無効化
    x_custom_header: Annotated[
        str | None, 
        Header(convert_underscores=False)
    ] = None
):
    return {"x_custom_header": x_custom_header}
```

## 重複ヘッダーの処理

### 1. リスト型での受信
```python
@app.get("/items/")
async def read_items(
    # 複数のX-Tokenヘッダーをリストとして受信
    x_token: Annotated[list[str] | None, Header()] = None
):
    return {"X-Token values": x_token}
```

### 2. リクエスト例
```http
GET /items/
X-Token: foo
X-Token: bar
```
```json
{
    "X-Token values": ["foo", "bar"]
}
```

## 実用的な使用例

### 1. 認証ヘッダーの処理
```python
@app.get("/protected/")
async def protected_resource(
    authorization: Annotated[str | None, Header()] = None,
    x_api_key: Annotated[str | None, Header()] = None
):
    if not authorization and not x_api_key:
        raise HTTPException(status_code=401, detail="Authorization required")
    
    # 認証ロジック
    user = authenticate(authorization or x_api_key)
    return {"user": user, "data": "protected data"}
```

### 2. コンテントネゴシエーション
```python
@app.get("/data/")
async def get_data(
    accept: Annotated[str, Header()] = "application/json",
    accept_language: Annotated[str | None, Header()] = None,
    accept_encoding: Annotated[str | None, Header()] = None
):
    # コンテントタイプに基づいたレスポンス制御
    if "xml" in accept:
        return Response(content="<data>XML content</data>", media_type="application/xml")
    
    data = get_localized_data(accept_language or "en")
    return data
```

### 3. カスタムヘッダーでのメタデータ
```python
@app.post("/items/")
async def create_item(
    item: Item,
    x_request_id: Annotated[str | None, Header()] = None,
    x_client_version: Annotated[str | None, Header()] = None,
    x_forwarded_for: Annotated[str | None, Header()] = None
):
    # ログ記録
    logger.info(f"Request {x_request_id} from client {x_client_version}")
    
    result = create_item_service(item)
    
    return {
        "item": result,
        "request_id": x_request_id,
        "client_info": {
            "version": x_client_version,
            "forwarded_for": x_forwarded_for
        }
    }
```

## バリデーションとメタデータ

### 1. ヘッダー値のバリデーション
```python
@app.get("/api/")
async def api_endpoint(
    x_api_key: Annotated[
        str,
        Header(
            title="API Key",
            description="API access key",
            min_length=32,
            max_length=32,
            pattern=r'^[a-f0-9]{32}$'
        )
    ]
):
    return {"api_key_valid": True}
```

### 2. 条件付きヘッダー
```python
@app.get("/webhook/")
async def webhook_endpoint(
    x_github_event: Annotated[str | None, Header()] = None,
    x_hub_signature: Annotated[str | None, Header()] = None,
    content_type: Annotated[str, Header()] = "application/json"
):
    if x_github_event:
        return handle_github_webhook(x_github_event, x_hub_signature)
    
    return {"message": "Standard endpoint"}
```

## Python バージョン別対応

### 1. Python 3.10+（推奨）
```python
@app.get("/items/")
async def read_items(
    user_agent: Annotated[str | None, Header()] = None
):
    return {"User-Agent": user_agent}
```

### 2. Python 3.8+
```python
from typing import Union

@app.get("/items/")
async def read_items(
    user_agent: Annotated[Union[str, None], Header()] = None
):
    return {"User-Agent": user_agent}
```

### 3. Annotated無し（非推奨）
```python
@app.get("/items/")
async def read_items(user_agent: str | None = Header(None)):
    return {"User-Agent": user_agent}
```

## セキュリティ考慮事項

### 1. 機密ヘッダーの処理
```python
@app.get("/sensitive/")
async def sensitive_endpoint(
    authorization: Annotated[str, Header()],
    x_csrf_token: Annotated[str | None, Header()] = None
):
    # ヘッダーのサニタイゼーション
    if not is_valid_token_format(authorization):
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    return {"access": "granted"}
```

### 2. ヘッダーインジェクション防止
```python
import re

@app.get("/redirect/")
async def redirect_endpoint(
    x_forwarded_host: Annotated[str | None, Header()] = None
):
    if x_forwarded_host:
        # 不正なホスト名を除外
        if not re.match(r'^[a-zA-Z0-9.-]+$', x_forwarded_host):
            raise HTTPException(status_code=400, detail="Invalid host format")
    
    return {"forwarded_host": x_forwarded_host}
```

## エラーハンドリング

### 1. 必須ヘッダーの検証
```python
from fastapi import HTTPException

@app.get("/api/v1/")
async def api_v1(
    x_api_version: Annotated[str, Header()]
):
    if x_api_version != "1.0":
        raise HTTPException(
            status_code=400, 
            detail="Unsupported API version"
        )
    
    return {"version": x_api_version}
```

## 大文字・小文字の扱い

### 1. HTTPヘッダーの大文字・小文字非依存
```python
# これらはすべて同じヘッダーとして処理される
# Content-Type
# content-type
# CONTENT-TYPE
@app.get("/items/")
async def read_items(
    content_type: Annotated[str | None, Header()] = None
):
    return {"Content-Type": content_type}
```

## 主な特徴
- クエリ、パス、クッキーパラメータと同様の宣言方法
- 自動的なアンダースコア→ハイフン変換
- HTTPヘッダーの大文字・小文字非依存
- 重複ヘッダーの配列処理
- バリデーションとメタデータのサポート

## 主な利点
- 明示的なヘッダーパラメータ処理
- 自動バリデーション
- 型安全性
- OpenAPIドキュメント生成
- エディターサポート
- セキュリティ強化

## 使用シナリオ
- API認証・認可
- コンテントネゴシエーション
- リクエストメタデータの追跡
- セキュリティトークン管理
- プロキシ・ロードバランサー情報
- カスタムアプリケーションメタデータ

---
*出典: https://fastapi.tiangolo.com/tutorial/header-params/*