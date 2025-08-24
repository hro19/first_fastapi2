# FastAPI Cookie Parameters

## 概要
`Cookie`クラスを使用してHTTPクッキーをパラメータとして処理する方法について説明します。

## 基本的な使用方法

### 1. Cookieクラスのインポート
```python
from typing import Annotated
from fastapi import Cookie, FastAPI

app = FastAPI()
```

### 2. 基本的なクッキーパラメータ
```python
@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}
```

### 3. 必須クッキーパラメータ
```python
@app.get("/user-profile/")
async def read_user_profile(session_id: Annotated[str, Cookie()]):
    return {"session_id": session_id}
```

## 複数のクッキーパラメータ

### 1. 複数クッキーの同時処理
```python
@app.get("/analytics/")
async def read_analytics(
    user_id: Annotated[str | None, Cookie()] = None,
    session_id: Annotated[str | None, Cookie()] = None,
    tracking_id: Annotated[str | None, Cookie()] = None
):
    return {
        "user_id": user_id,
        "session_id": session_id, 
        "tracking_id": tracking_id
    }
```

### 2. 他のパラメータとの組み合わせ
```python
from fastapi import Path, Query

@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path()],
    q: Annotated[str | None, Query()] = None,
    ads_id: Annotated[str | None, Cookie()] = None,
    user_agent: Annotated[str | None, Cookie(alias="User-Agent")] = None
):
    return {
        "item_id": item_id,
        "q": q,
        "ads_id": ads_id,
        "user_agent": user_agent
    }
```

## バリデーションとメタデータ

### 1. クッキー値のバリデーション
```python
@app.get("/secure/")
async def read_secure_data(
    auth_token: Annotated[
        str, 
        Cookie(
            title="Authentication Token",
            description="JWT token for user authentication",
            min_length=10,
            max_length=500
        )
    ]
):
    return {"token_length": len(auth_token)}
```

### 2. パターンマッチング
```python
@app.get("/api-access/")
async def api_access(
    api_key: Annotated[
        str, 
        Cookie(
            pattern=r'^[A-Za-z0-9]{32}$',
            description="32-character alphanumeric API key"
        )
    ]
):
    return {"api_key": api_key}
```

## Python バージョン別対応

### 1. Python 3.10+（推奨）
```python
@app.get("/items/")
async def read_items(
    ads_id: Annotated[str | None, Cookie()] = None
):
    return {"ads_id": ads_id}
```

### 2. Python 3.8+
```python
from typing import Union

@app.get("/items/")
async def read_items(
    ads_id: Annotated[Union[str, None], Cookie()] = None
):
    return {"ads_id": ads_id}
```

### 3. Annotated無し（非推奨）
```python
@app.get("/items/")
async def read_items(ads_id: str | None = Cookie(None)):
    return {"ads_id": ads_id}
```

## 実用的な使用例

### 1. ユーザーセッション管理
```python
@app.get("/dashboard/")
async def dashboard(
    session_token: Annotated[str | None, Cookie()] = None,
    csrf_token: Annotated[str | None, Cookie()] = None
):
    if not session_token:
        return {"error": "Not authenticated"}
    
    # セッション検証ロジック
    user = validate_session(session_token)
    
    return {
        "user": user,
        "csrf_token": csrf_token,
        "dashboard_data": get_user_dashboard(user)
    }
```

### 2. 多言語対応
```python
@app.get("/content/")
async def get_content(
    language: Annotated[str, Cookie(alias="lang")] = "en",
    timezone: Annotated[str | None, Cookie()] = None
):
    content = get_localized_content(language)
    
    if timezone:
        content = adjust_for_timezone(content, timezone)
    
    return {"content": content, "language": language}
```

### 3. A/Bテスト
```python
@app.get("/feature/")
async def get_feature(
    experiment_id: Annotated[str | None, Cookie(alias="exp-id")] = None,
    variant: Annotated[str | None, Cookie()] = None
):
    if experiment_id and variant:
        feature_config = get_experiment_config(experiment_id, variant)
    else:
        feature_config = get_default_config()
    
    return {"config": feature_config}
```

## セキュリティ考慮事項

### 1. 機密クッキーの処理
```python
@app.get("/admin/")
async def admin_panel(
    admin_token: Annotated[
        str | None, 
        Cookie(
            description="Admin authentication token",
            # Cookie自体にはsecure属性は設定できないが、
            # レスポンスでSet-Cookieヘッダーを使用
        )
    ] = None
):
    if not admin_token or not verify_admin_token(admin_token):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return {"admin_data": get_admin_data()}
```

### 2. クッキー値のサニタイゼーション
```python
import re

@app.get("/search/")
async def search(
    search_history: Annotated[str | None, Cookie()] = None
):
    if search_history:
        # XSS攻撃を防ぐためサニタイズ
        clean_history = re.sub(r'[<>"\']', '', search_history)
        return {"history": clean_history.split(",")}
    
    return {"history": []}
```

## エラーハンドリング

### 1. クッキー検証エラー
```python
from fastapi import HTTPException

@app.get("/protected/")
async def protected_resource(
    auth_cookie: Annotated[
        str,
        Cookie(min_length=10, pattern=r'^[A-Za-z0-9]+$')
    ]
):
    try:
        user = authenticate_user(auth_cookie)
        return {"user": user}
    except AuthenticationError:
        raise HTTPException(
            status_code=401, 
            detail="Invalid authentication cookie"
        )
```

## Cookie設定（レスポンス側）

### 1. レスポンスでクッキーを設定
```python
from fastapi import Response

@app.post("/login/")
async def login(credentials: UserCredentials, response: Response):
    user = authenticate(credentials)
    
    if user:
        # セッションクッキーを設定
        response.set_cookie(
            key="session_token",
            value=create_session_token(user),
            httponly=True,
            secure=True,
            samesite="strict"
        )
        return {"status": "logged_in"}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")
```

## 重要なポイント

### 1. Cookie() の明示的使用
```python
# ❌ 間違い - クエリパラメータとして解釈される
async def read_items(ads_id: str | None = None):
    pass

# ✅ 正しい - クッキーパラメータとして処理
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    pass
```

### 2. 継承関係
- `Cookie` は `Path` や `Query` の姉妹クラス
- 共通の `Param` クラスから継承
- 同様のバリデーションとメタデータ機能を提供

## 主な利点
- 明示的なクッキーパラメータ宣言
- 自動バリデーション
- 型安全性
- OpenAPI ドキュメント生成
- エディターサポート
- セキュリティ強化

## 使用シナリオ
- ユーザー認証・セッション管理
- パーソナライゼーション
- A/Bテスト・実験
- 分析・トラッキング
- 言語・地域設定
- セキュリティトークン管理

---
*出典: https://fastapi.tiangolo.com/tutorial/cookie-params/*