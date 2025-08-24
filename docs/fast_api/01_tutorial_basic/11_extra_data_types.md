# FastAPI Extra Data Types

## 概要
FastAPIでサポートされている標準的なPython型以外の追加データ型について説明します。これらの型は自動変換、バリデーション、OpenAPIスキーマ生成が可能です。

## 主要なExtra Data Types

### 1. UUID
```python
from uuid import UUID

@app.get("/items/{item_id}")
async def read_item(item_id: UUID):
    return {"item_id": item_id}
```
- **用途**: データベースのユニークID
- **表現**: 文字列として送受信
- **バリデーション**: 有効なUUID形式のチェック
- **例**: `550e8400-e29b-41d4-a716-446655440000`

### 2. 日時関連型

#### datetime.datetime
```python
from datetime import datetime

@app.post("/items/")
async def create_item(
    item: Item,
    timestamp: datetime
):
    return {
        "item": item,
        "timestamp": timestamp,
        "formatted": timestamp.isoformat()
    }
```
- **形式**: ISO 8601（例: `2023-12-25T10:30:00`）
- **用途**: 完全なタイムスタンプ

#### datetime.date
```python
from datetime import date

@app.post("/events/")
async def create_event(
    name: str,
    event_date: date
):
    return {"name": name, "date": event_date}
```
- **形式**: `YYYY-MM-DD`（例: `2023-12-25`）
- **用途**: 日付のみ

#### datetime.time
```python
from datetime import time

@app.post("/schedule/")
async def set_schedule(
    activity: str,
    start_time: time
):
    return {"activity": activity, "time": start_time}
```
- **形式**: `HH:MM:SS`（例: `14:30:00`）
- **用途**: 時刻のみ

#### datetime.timedelta
```python
from datetime import timedelta

@app.post("/tasks/")
async def create_task(
    name: str,
    duration: timedelta
):
    return {
        "name": name,
        "duration_seconds": duration.total_seconds()
    }
```
- **用途**: 時間の差分・期間
- **表現**: 秒数として送受信

### 3. Decimal型
```python
from decimal import Decimal

class Product(BaseModel):
    name: str
    price: Decimal
    tax_rate: Decimal

@app.post("/products/")
async def create_product(product: Product):
    total = product.price * (1 + product.tax_rate)
    return {
        "product": product,
        "total_price": total
    }
```
- **用途**: 金融計算での精密な数値
- **利点**: 浮動小数点数の丸め誤差を回避

### 4. bytes型
```python
@app.post("/process-data/")
async def process_data(data: bytes):
    # バイナリデータの処理
    processed = data.upper()
    return {"length": len(data), "processed": processed}
```
- **用途**: バイナリデータ
- **エンコーディング**: Base64として送受信

### 5. frozenset型
```python
@app.post("/tags/")
async def process_tags(tags: frozenset[str]):
    return {
        "unique_tags": list(tags),
        "count": len(tags)
    }
```
- **特徴**: 不変のセット（重複排除）
- **JSON表現**: 配列として送受信

## 複合例

### 1. 複数のExtra Data Types使用
```python
from datetime import datetime, date, time, timedelta
from decimal import Decimal
from uuid import UUID

class Event(BaseModel):
    id: UUID
    name: str
    start_date: date
    start_time: time
    duration: timedelta
    price: Decimal
    created_at: datetime

@app.post("/events/")
async def create_event(event: Event):
    end_datetime = datetime.combine(event.start_date, event.start_time) + event.duration
    
    return {
        "event": event,
        "end_time": end_datetime,
        "price_formatted": f"${event.price:.2f}"
    }
```

### 2. リクエスト例
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Conference",
    "start_date": "2024-03-15",
    "start_time": "09:00:00",
    "duration": 28800,
    "price": "299.99",
    "created_at": "2024-01-15T10:30:00"
}
```

## データ変換の特徴

### 1. 自動変換
```python
@app.put("/items/{item_id}")
async def update_item(
    item_id: UUID,
    start_datetime: datetime,
    end_datetime: datetime,
    process_after: timedelta
):
    # 日時計算が自然に行える
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    
    return {
        "item_id": item_id,
        "process_start": start_process,
        "total_duration": duration.total_seconds()
    }
```

### 2. バリデーション
- **UUID**: 有効なUUID形式
- **datetime**: ISO 8601形式
- **Decimal**: 有効な数値形式
- **bytes**: 有効なBase64エンコード

### 3. JSON Schema生成
```python
# OpenAPIスキーマで適切な型情報を生成
{
    "item_id": {
        "type": "string",
        "format": "uuid"
    },
    "timestamp": {
        "type": "string",
        "format": "date-time"
    },
    "price": {
        "type": "number"
    }
}
```

## エラーハンドリング

### 1. 型変換エラー
```json
// 無効なUUID
{
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "value is not a valid uuid",
            "type": "type_error.uuid"
        }
    ]
}
```

### 2. 日時フォーマットエラー
```json
// 無効な日時形式
{
    "detail": [
        {
            "loc": ["body", "created_at"],
            "msg": "invalid datetime format",
            "type": "value_error.datetime"
        }
    ]
}
```

## 使用シナリオ

### 1. データベース統合
- UUID: プライマリキー
- datetime: タイムスタンプ
- Decimal: 金融データ

### 2. API間通信
- 型安全なデータ交換
- 自動シリアライゼーション
- スキーマ検証

### 3. ドメイン固有の処理
- 日時計算
- 金融計算
- バイナリデータ処理

## 主な利点
- 自動データ変換
- 型安全性の保証
- バリデーション機能
- OpenAPIスキーマ対応
- エディターサポート
- エラーメッセージの明確化

---
*出典: https://fastapi.tiangolo.com/tutorial/extra-data-types/*