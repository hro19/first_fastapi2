#!/usr/bin/env python3
"""
Todo API テストスクリプト
FastAPI Todo APIのCRUD操作をテストします。
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any


class TodoAPITester:
    """Todo API テストクラス"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8001"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1/todos"
        self.created_todo_id = None
        
    def print_test_result(self, test_name: str, success: bool, response: requests.Response, details: str = ""):
        """テスト結果を整形して出力"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"\n{status} {test_name}")
        print(f"   Status Code: {response.status_code}")
        
        try:
            response_data = response.json()
            print(f"   Response: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        except:
            print(f"   Response Text: {response.text}")
            
        if details:
            print(f"   Details: {details}")
        print("-" * 60)
    
    def test_health_check(self):
        """アプリケーションのヘルスチェック"""
        print("🔍 Testing: Application Health Check")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            success = response.status_code == 200
            self.print_test_result("Health Check", success, response)
            return success
        except Exception as e:
            print(f"❌ Health Check Failed: {e}")
            return False
    
    def test_create_todo(self):
        """Todo新規作成のテスト"""
        print("🔍 Testing: Todo Creation (POST)")
        
        # テストデータ
        test_todo = {
            "title": "Python HTTPテスト用Todo",
            "description": "requestsライブラリを使用してAPIをテストしています。日本語も含みます。",
            "priority": 2  # High priority
        }
        
        try:
            response = requests.post(
                self.api_url, 
                json=test_todo,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            success = response.status_code == 200
            
            if success:
                response_data = response.json()
                self.created_todo_id = response_data.get("id")
                details = f"Created Todo ID: {self.created_todo_id}"
                
                # レスポンスの必須フィールドをチェック
                required_fields = ["id", "title", "description", "completed", "priority", 
                                 "created_at", "created_at_jst"]
                missing_fields = [field for field in required_fields if field not in response_data]
                
                if missing_fields:
                    success = False
                    details += f" | Missing fields: {missing_fields}"
                else:
                    details += f" | Title: '{response_data['title']}' | Priority: {response_data['priority']}"
            else:
                details = "Todo creation failed"
                
            self.print_test_result("Todo Creation", success, response, details)
            return success
            
        except Exception as e:
            print(f"❌ Todo Creation Test Failed: {e}")
            return False
    
    def test_get_todo_by_id(self):
        """作成したTodoを個別取得するテスト"""
        if not self.created_todo_id:
            print("❌ Skipping Get Todo by ID: No todo created")
            return False
            
        print(f"🔍 Testing: Get Todo by ID ({self.created_todo_id})")
        
        try:
            response = requests.get(f"{self.api_url}/{self.created_todo_id}", timeout=5)
            success = response.status_code == 200
            
            if success:
                response_data = response.json()
                details = f"Retrieved Todo: {response_data.get('title', 'N/A')}"
                
                # 日本時間フォーマットのチェック
                if response_data.get("created_at_jst"):
                    details += f" | JST: {response_data['created_at_jst']}"
            else:
                details = "Todo retrieval failed"
                
            self.print_test_result("Get Todo by ID", success, response, details)
            return success
            
        except Exception as e:
            print(f"❌ Get Todo by ID Test Failed: {e}")
            return False
    
    def test_get_all_todos(self):
        """Todo一覧取得のテスト"""
        print("🔍 Testing: Get All Todos (GET)")
        
        try:
            response = requests.get(self.api_url, timeout=5)
            success = response.status_code == 200
            
            if success:
                response_data = response.json()
                total = response_data.get("total", 0)
                items = response_data.get("items", [])
                details = f"Total: {total} | Items returned: {len(items)}"
                
                # 日本時間フィールドの存在確認
                if items:
                    first_item = items[0]
                    if "created_at_jst" in first_item:
                        details += f" | JST format: {first_item['created_at_jst']}"
            else:
                details = "Todo list retrieval failed"
                
            self.print_test_result("Get All Todos", success, response, details)
            return success
            
        except Exception as e:
            print(f"❌ Get All Todos Test Failed: {e}")
            return False
    
    def test_update_todo(self):
        """Todo更新のテスト"""
        if not self.created_todo_id:
            print("❌ Skipping Update Todo: No todo created")
            return False
            
        print(f"🔍 Testing: Update Todo ({self.created_todo_id})")
        
        update_data = {
            "title": "更新されたTodoタイトル",
            "completed": True
        }
        
        try:
            response = requests.patch(
                f"{self.api_url}/{self.created_todo_id}",
                json=update_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            success = response.status_code == 200
            
            if success:
                response_data = response.json()
                details = f"Updated: completed={response_data.get('completed')}"
                if response_data.get("completed_at_jst"):
                    details += f" | Completed at: {response_data['completed_at_jst']}"
            else:
                details = "Todo update failed"
                
            self.print_test_result("Update Todo", success, response, details)
            return success
            
        except Exception as e:
            print(f"❌ Update Todo Test Failed: {e}")
            return False
    
    def run_all_tests(self):
        """全テストを実行"""
        print("=" * 80)
        print("🚀 Todo API テスト開始")
        print(f"📍 Base URL: {self.base_url}")
        print(f"⏰ Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Create Todo", self.test_create_todo),
            ("Get Todo by ID", self.test_get_todo_by_id),
            ("Get All Todos", self.test_get_all_todos),
            ("Update Todo", self.test_update_todo),
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            results[test_name] = test_func()
        
        # テスト結果サマリ
        print("\n" + "=" * 80)
        print("📊 テスト結果サマリ")
        print("=" * 80)
        
        passed = sum(results.values())
        total = len(results)
        
        for test_name, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {status} {test_name}")
        
        print(f"\n🎯 合計: {passed}/{total} テストが成功")
        print(f"📈 成功率: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 全てのテストが成功しました！")
        else:
            print("⚠️  一部のテストが失敗しました。")
        
        return passed == total


if __name__ == "__main__":
    # テスト実行
    tester = TodoAPITester()
    success = tester.run_all_tests()
    
    # 終了コード
    exit(0 if success else 1)