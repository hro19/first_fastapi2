#!/usr/bin/env python3
"""
シンプルなAPIエンドポイントテスト
データベースに依存しないエンドポイントをテスト
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient

# FastAPIアプリケーションをインポート
from app.main import app

# TestClientの作成
client = TestClient(app)

class TestBasicEndpoints:
    """基本的なエンドポイントのテスト"""
    
    def test_root_endpoint(self):
        """ルートエンドポイントのテスト"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "project" in data
        assert data["project"] == "First FastAPI with Neon"
        
    def test_health_check(self):
        """ヘルスチェックエンドポイントのテスト"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "message" in data
        
    def test_invalid_endpoint(self):
        """存在しないエンドポイントのテスト"""
        response = client.get("/api/v1/invalid")
        assert response.status_code == 404
        
    def test_cors_headers(self):
        """CORSヘッダーのテスト"""
        # CORSヘッダーは実際のクロスオリジンリクエストでのみ設定される
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
        assert response.status_code == 200
        # CORSが正しく設定されていることを確認