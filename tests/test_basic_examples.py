#!/usr/bin/env python3
"""
pytestで実行できるシンプルなテスト例
DBアクセスなしのテストで、pytestの動作を確認
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# テスト用のシンプルなアプリ
test_app = FastAPI()

@test_app.get("/")
def read_root():
    return {"message": "Hello pytest"}

@test_app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}

@test_app.post("/items")
def create_item(item: dict):
    return {"status": "created", "item": item}

# TestClientを作成
client = TestClient(test_app)

# =====================================
# pytestで自動実行されるテスト関数
# =====================================

def test_read_root():
    """ルートエンドポイントのテスト"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello pytest"}

def test_read_item():
    """アイテム取得のテスト"""
    response = client.get("/items/42")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["item_id"] == 42
    assert json_data["name"] == "Item 42"

def test_create_item():
    """アイテム作成のテスト"""
    test_data = {"name": "Test Item", "price": 100}
    response = client.post("/items", json=test_data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "created"
    assert json_data["item"] == test_data

def test_invalid_item_id():
    """無効なアイテムIDのテスト"""
    response = client.get("/items/invalid")
    assert response.status_code == 422  # Validation error

# =====================================
# パラメータ化テスト（pytest固有機能）
# =====================================

@pytest.mark.parametrize("item_id,expected_name", [
    (1, "Item 1"),
    (100, "Item 100"),
    (999, "Item 999"),
])
def test_multiple_items(item_id, expected_name):
    """複数のアイテムIDをテスト（パラメータ化）"""
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == expected_name

# =====================================
# テストのグループ化（マーカー）
# =====================================

@pytest.mark.fast
def test_fast_operation():
    """高速テスト（マーカー付き）"""
    response = client.get("/")
    assert response.status_code == 200

@pytest.mark.slow
def test_slow_operation():
    """低速テスト（マーカー付き）"""
    # 実際には時間のかかる処理をシミュレート
    import time
    time.sleep(0.1)
    response = client.get("/")
    assert response.status_code == 200

# =====================================
# フィクスチャの使用例
# =====================================

@pytest.fixture
def sample_data():
    """テストデータを提供するフィクスチャ"""
    return {
        "name": "Fixture Item",
        "price": 200,
        "quantity": 5
    }

def test_with_fixture_data(sample_data):
    """フィクスチャを使ったテスト"""
    response = client.post("/items", json=sample_data)
    assert response.status_code == 200
    result = response.json()
    assert result["item"]["name"] == "Fixture Item"
    assert result["item"]["price"] == 200

# =====================================
# スキップとXFAIL
# =====================================

@pytest.mark.skip(reason="まだ実装されていない機能")
def test_unimplemented_feature():
    """スキップされるテスト"""
    assert False  # これは実行されない

@pytest.mark.xfail(reason="既知のバグ")
def test_known_bug():
    """失敗が予想されるテスト"""
    # バグがあると仮定
    assert 1 == 2  # 失敗するが、xfailなのでテスト全体は成功扱い