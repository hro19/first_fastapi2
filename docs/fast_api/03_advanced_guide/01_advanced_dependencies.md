# FastAPI Advanced Dependencies

## 概要
パラメータ化可能な依存関数を作成し、複雑な依存性注入パターンを実装する高度な手法について説明します。

## 呼び出し可能クラス（Callable Classes）

### 1. 基本的なパラメータ化依存性
```python
class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False

# インスタンス化して特定のパラメータを設定
checker = FixedContentQueryChecker("bar")

@app.get("/query-checker/")
async def read_query_check(fixed_content_included: bool = Depends(checker)):
    return {"fixed_content_in_query": fixed_content_included}
```

### 2. 設定可能なセキュリティ依存性
```python
class TokenAuthChecker:
    def __init__(self, allowed_roles: list[str], require_admin: bool = False):
        self.allowed_roles = allowed_roles
        self.require_admin = require_admin

    def __call__(self, token: str = Depends(oauth2_scheme)):
        payload = decode_token(token)
        user_role = payload.get("role")
        
        if self.require_admin and user_role != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")
        
        if user_role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        return payload

# 異なる権限レベルの依存性を作成
admin_only = TokenAuthChecker(["admin"], require_admin=True)
moderator_or_admin = TokenAuthChecker(["moderator", "admin"])
any_authenticated = TokenAuthChecker(["user", "moderator", "admin"])

@app.get("/admin/users/")
async def admin_users(user: dict = Depends(admin_only)):
    return get_all_users()

@app.get("/moderate/posts/")
async def moderate_posts(user: dict = Depends(moderator_or_admin)):
    return get_posts_for_moderation()
```

## データベース接続管理

### 1. 設定可能なデータベース依存性
```python
class DatabaseManager:
    def __init__(self, database_url: str, pool_size: int = 5):
        self.database_url = database_url
        self.pool_size = pool_size
        self._engine = None

    def __call__(self):
        if not self._engine:
            self._engine = create_engine(
                self.database_url,
                poolclass=StaticPool,
                pool_size=self.pool_size
            )
        return self._engine

# 異なる環境用のDB管理者を作成
prod_db = DatabaseManager(
    database_url="postgresql://user:password@prod-server/db",
    pool_size=10
)
test_db = DatabaseManager(
    database_url="sqlite:///test.db",
    pool_size=1
)

@app.get("/users/")
async def get_users(db = Depends(prod_db if ENVIRONMENT == "production" else test_db)):
    return query_users(db)
```

## キャッシュ依存性

### 1. 設定可能キャッシュシステム
```python
from functools import lru_cache
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self, ttl_seconds: int = 300, max_size: int = 128):
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self._cache = {}

    def __call__(self, key: str):
        now = datetime.now()
        
        if key in self._cache:
            value, timestamp = self._cache[key]
            if now - timestamp < timedelta(seconds=self.ttl_seconds):
                return value
            else:
                del self._cache[key]
        
        return None

    def set(self, key: str, value):
        if len(self._cache) >= self.max_size:
            # 最古のエントリを削除
            oldest_key = min(self._cache.keys(), 
                           key=lambda k: self._cache[k][1])
            del self._cache[oldest_key]
        
        self._cache[key] = (value, datetime.now())

# 異なるTTL設定でキャッシュ管理者を作成
short_cache = CacheManager(ttl_seconds=60, max_size=50)
long_cache = CacheManager(ttl_seconds=3600, max_size=200)

@app.get("/fast-data/")
async def get_fast_data(cache_value = Depends(short_cache)):
    if cache_value is not None:
        return cache_value
    
    # データを取得してキャッシュ
    data = fetch_expensive_data()
    short_cache.set("fast-data", data)
    return data
```

## バリデーション依存性

### 1. 設定可能バリデーター
```python
class ParameterValidator:
    def __init__(self, min_length: int = 1, max_length: int = 100, 
                 allowed_chars: str = None, required_prefix: str = None):
        self.min_length = min_length
        self.max_length = max_length
        self.allowed_chars = allowed_chars
        self.required_prefix = required_prefix

    def __call__(self, value: str = Query(...)):
        if len(value) < self.min_length:
            raise HTTPException(
                status_code=400, 
                detail=f"Value too short, minimum {self.min_length} characters"
            )
        
        if len(value) > self.max_length:
            raise HTTPException(
                status_code=400,
                detail=f"Value too long, maximum {self.max_length} characters"
            )
        
        if self.required_prefix and not value.startswith(self.required_prefix):
            raise HTTPException(
                status_code=400,
                detail=f"Value must start with '{self.required_prefix}'"
            )
        
        if self.allowed_chars:
            if not all(c in self.allowed_chars for c in value):
                raise HTTPException(
                    status_code=400,
                    detail="Value contains invalid characters"
                )
        
        return value

# 異なるバリデーション規則
username_validator = ParameterValidator(
    min_length=3, 
    max_length=20, 
    allowed_chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
)

api_key_validator = ParameterValidator(
    min_length=32, 
    max_length=32, 
    required_prefix="ak_"
)

@app.get("/user/{username}")
async def get_user(username: str = Depends(username_validator)):
    return {"username": username}

@app.get("/api-resource/")
async def api_resource(api_key: str = Depends(api_key_validator)):
    return {"access": "granted"}
```

## レート制限依存性

### 1. 設定可能レート制限
```python
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, calls: int, period: int):
        self.calls = calls
        self.period = period
        self.call_times = defaultdict(list)

    def __call__(self, request: Request):
        client_ip = request.client.host
        now = time.time()
        
        # 古い記録をクリーンアップ
        self.call_times[client_ip] = [
            call_time for call_time in self.call_times[client_ip]
            if now - call_time < self.period
        ]
        
        # レート制限チェック
        if len(self.call_times[client_ip]) >= self.calls:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded: {self.calls} calls per {self.period} seconds"
            )
        
        # 現在の呼び出しを記録
        self.call_times[client_ip].append(now)
        return True

# 異なるレート制限設定
strict_rate_limit = RateLimiter(calls=10, period=60)  # 10 calls per minute
relaxed_rate_limit = RateLimiter(calls=100, period=60)  # 100 calls per minute

@app.get("/public-api/")
async def public_api(rate_check: bool = Depends(strict_rate_limit)):
    return {"data": "public data"}

@app.get("/premium-api/")
async def premium_api(rate_check: bool = Depends(relaxed_rate_limit)):
    return {"data": "premium data"}
```

## 複合依存性パターン

### 1. 依存性チェーン
```python
class AuthenticationChecker:
    def __init__(self, token_type: str = "Bearer"):
        self.token_type = token_type

    def __call__(self, authorization: str = Header(None)):
        if not authorization:
            raise HTTPException(status_code=401, detail="Authorization header required")
        
        if not authorization.startswith(f"{self.token_type} "):
            raise HTTPException(status_code=401, detail=f"Invalid token type, expected {self.token_type}")
        
        token = authorization[len(f"{self.token_type} "):]
        return decode_token(token)

class AuthorizationChecker:
    def __init__(self, required_permission: str):
        self.required_permission = required_permission

    def __call__(self, user_data: dict = Depends(AuthenticationChecker())):
        user_permissions = user_data.get("permissions", [])
        
        if self.required_permission not in user_permissions:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        return user_data

# 権限チェック依存性の作成
write_permission = AuthorizationChecker("write")
delete_permission = AuthorizationChecker("delete")

@app.post("/items/")
async def create_item(item: Item, user: dict = Depends(write_permission)):
    return create_item_service(item, user["user_id"])

@app.delete("/items/{item_id}")
async def delete_item(item_id: int, user: dict = Depends(delete_permission)):
    return delete_item_service(item_id, user["user_id"])
```

## テストでの依存性オーバーライド

### 1. テスト用依存性
```python
class MockDatabaseManager:
    def __init__(self, test_data: dict = None):
        self.test_data = test_data or {}

    def __call__(self):
        return self.test_data

# テスト時の依存性オーバーライド
def test_api():
    test_db = MockDatabaseManager({"users": [{"id": 1, "name": "test"}]})
    app.dependency_overrides[DatabaseManager] = test_db
    
    with TestClient(app) as client:
        response = client.get("/users/")
        assert response.status_code == 200
```

## 主な利点
- **再利用性**: 同じ依存性ロジックを異なるパラメータで使用
- **設定の柔軟性**: 環境やユースケースに応じた動的設定
- **テスト容易性**: モックやスタブでの簡単な置き換え
- **保守性**: 一箇所での依存性ロジック管理
- **スケーラビリティ**: 複雑な依存関係の体系的管理

## 使用シナリオ
- セキュリティシステム（認証・認可）
- データベース接続管理
- キャッシュシステム
- レート制限
- バリデーションシステム
- ログ記録・監査
- マルチテナント対応

---
*出典: https://fastapi.tiangolo.com/advanced/advanced-dependencies/*