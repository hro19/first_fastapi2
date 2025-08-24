#!/usr/bin/env python3
"""
Todo CRUD 詳細テストスクリプト
SwaggerUI仕様に基づいて各CRUD操作を個別にテストします。
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List


class TodoCRUDTester:
    """Todo CRUD 詳細テスト専用クラス"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8001"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1/todos"
        self.created_todos = []  # テストで作成したTodoのIDリスト
        self.test_results = {}
        
    def print_section(self, title: str):
        """セクション区切りを表示"""
        print(f"\n{'='*80}")
        print(f"🔥 {title}")
        print('='*80)
        
    def print_test_result(self, test_name: str, success: bool, response: requests.Response, details: str = ""):
        """テスト結果を整形して出力"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"\n{status} {test_name}")
        print(f"   Status: {response.status_code}")
        
        # レスポンスの表示
        try:
            if response.text:
                response_data = response.json()
                if len(str(response_data)) > 500:  # 長い場合は要約
                    if isinstance(response_data, dict) and 'items' in response_data:
                        print(f"   Items: {len(response_data['items'])}")
                        if response_data['items']:
                            print(f"   Sample: {response_data['items'][0].get('title', 'N/A')}")
                    else:
                        print(f"   Response: {str(response_data)[:200]}...")
                else:
                    print(f"   Response: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        except Exception as e:
            print(f"   Response: {response.text}")
            
        if details:
            print(f"   Details: {details}")
        print("-" * 60)
        
        return success

    # =============================================
    # CREATE (作成) テスト
    # =============================================
    
    def test_create_basic(self):
        """基本的なTodo作成テスト"""
        self.print_section("CREATE 操作テスト")
        
        test_cases = [
            {
                "name": "基本Todo作成",
                "data": {
                    "title": "基本的なTodo",
                    "description": "シンプルな作成テスト",
                    "priority": 0  # Low
                }
            },
            {
                "name": "優先度HIGH Todo作成", 
                "data": {
                    "title": "重要なタスク",
                    "description": "優先度の高いタスクです",
                    "priority": 2  # High
                }
            },
            {
                "name": "日本語Todo作成",
                "data": {
                    "title": "日本語のタスク 🎌",
                    "description": "日本語の説明文です。絵文字も含まれています。",
                    "priority": 1  # Medium
                }
            },
            {
                "name": "最小限Todo作成",
                "data": {
                    "title": "最小限のタスク"
                    # descriptionとpriorityを省略
                }
            }
        ]
        
        results = []
        for case in test_cases:
            try:
                response = requests.post(
                    self.api_url,
                    json=case["data"],
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                success = response.status_code == 200
                if success:
                    todo_data = response.json()
                    self.created_todos.append(todo_data["id"])
                    details = f"Created ID: {todo_data['id']} | Title: '{todo_data['title']}'"
                else:
                    details = "作成に失敗"
                    
                results.append(self.print_test_result(
                    case["name"], success, response, details
                ))
                
            except Exception as e:
                print(f"❌ {case['name']} - Exception: {e}")
                results.append(False)
        
        return all(results)

    # =============================================
    # READ (読み取り) テスト 
    # =============================================
    
    def test_read_operations(self):
        """読み取り操作の詳細テスト"""
        self.print_section("READ 操作テスト")
        
        results = []
        
        # 1. 全件取得テスト
        try:
            response = requests.get(self.api_url, timeout=5)
            success = response.status_code == 200
            if success:
                data = response.json()
                details = f"Total: {data['total']} | Items: {len(data['items'])}"
            else:
                details = "取得失敗"
            results.append(self.print_test_result(
                "全Todo取得", success, response, details
            ))
        except Exception as e:
            print(f"❌ 全Todo取得 - Exception: {e}")
            results.append(False)
        
        # 2. 個別取得テスト（作成されたTodoがあれば）
        if self.created_todos:
            todo_id = self.created_todos[0]
            try:
                response = requests.get(f"{self.api_url}/{todo_id}", timeout=5)
                success = response.status_code == 200
                if success:
                    data = response.json()
                    details = f"ID: {data['id']} | Title: '{data['title']}'"
                else:
                    details = f"取得失敗 (ID: {todo_id})"
                results.append(self.print_test_result(
                    f"個別Todo取得 (ID: {todo_id})", success, response, details
                ))
            except Exception as e:
                print(f"❌ 個別Todo取得 - Exception: {e}")
                results.append(False)
        
        # 3. フィルタリング機能テスト
        filter_tests = [
            {"params": {"limit": 2}, "name": "件数制限 (limit=2)"},
            {"params": {"completed": False}, "name": "未完了フィルタ"},
            {"params": {"priority": 2}, "name": "高優先度フィルタ"},
            {"params": {"include_deleted": False}, "name": "削除済み除外"}
        ]
        
        for filter_test in filter_tests:
            try:
                response = requests.get(self.api_url, params=filter_test["params"], timeout=5)
                success = response.status_code == 200
                if success:
                    data = response.json()
                    details = f"Filtered Items: {len(data['items'])}"
                else:
                    details = "フィルタリング失敗"
                results.append(self.print_test_result(
                    filter_test["name"], success, response, details
                ))
            except Exception as e:
                print(f"❌ {filter_test['name']} - Exception: {e}")
                results.append(False)
        
        return all(results)

    # =============================================
    # UPDATE (更新) テスト
    # =============================================
    
    def test_update_operations(self):
        """更新操作の詳細テスト"""
        self.print_section("UPDATE 操作テスト")
        
        if not self.created_todos:
            print("❌ 更新テスト用のTodoが存在しません")
            return False
            
        results = []
        todo_id = self.created_todos[0]  # 最初のTodoを使用
        
        # 1. タイトル更新テスト
        try:
            update_data = {"title": "更新されたタイトル"}
            response = requests.patch(
                f"{self.api_url}/{todo_id}",
                json=update_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                details = f"New Title: '{data['title']}'"
            else:
                details = "タイトル更新失敗"
            results.append(self.print_test_result(
                "タイトル更新", success, response, details
            ))
        except Exception as e:
            print(f"❌ タイトル更新 - Exception: {e}")
            results.append(False)
        
        # 2. 複数フィールド更新テスト
        try:
            update_data = {
                "description": "更新された説明文",
                "priority": 1,  # Medium
                "completed": False
            }
            response = requests.patch(
                f"{self.api_url}/{todo_id}",
                json=update_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                details = f"Priority: {data['priority']} | Completed: {data['completed']}"
            else:
                details = "複数フィールド更新失敗"
            results.append(self.print_test_result(
                "複数フィールド更新", success, response, details
            ))
        except Exception as e:
            print(f"❌ 複数フィールド更新 - Exception: {e}")
            results.append(False)
        
        # 3. 完了フラグ更新（タイムスタンプ確認）
        try:
            update_data = {"completed": True}
            response = requests.patch(
                f"{self.api_url}/{todo_id}",
                json=update_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                completed_at = data.get('completed_at_jst')
                details = f"Completed: {data['completed']} | Completed at: {completed_at}"
            else:
                details = "完了フラグ更新失敗"
            results.append(self.print_test_result(
                "完了フラグ更新（タイムスタンプ付き）", success, response, details
            ))
        except Exception as e:
            print(f"❌ 完了フラグ更新 - Exception: {e}")
            results.append(False)
        
        return all(results)

    # =============================================
    # DELETE (削除) テスト
    # =============================================
    
    def test_delete_operations(self):
        """削除操作の詳細テスト（論理削除・物理削除）"""
        self.print_section("DELETE 操作テスト")
        
        if len(self.created_todos) < 2:
            print("❌ 削除テスト用のTodoが不足しています")
            return False
            
        results = []
        
        # 1. 論理削除テスト
        todo_id_soft = self.created_todos[1]  # 2番目のTodoを使用
        try:
            response = requests.delete(
                f"{self.api_url}/{todo_id_soft}",
                params={"permanent": False},  # 論理削除
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                deleted_at = data.get('deleted_at_jst')
                details = f"Soft deleted at: {deleted_at}"
            else:
                details = "論理削除失敗"
            results.append(self.print_test_result(
                f"論理削除 (ID: {todo_id_soft})", success, response, details
            ))
        except Exception as e:
            print(f"❌ 論理削除 - Exception: {e}")
            results.append(False)
        
        # 2. 論理削除されたTodoが通常の取得で見えないことを確認
        try:
            response = requests.get(f"{self.api_url}/{todo_id_soft}", timeout=5)
            success = response.status_code == 404  # 見えないはず
            details = "論理削除されたTodoは通常取得で見えない" if success else "論理削除が機能していない"
            results.append(self.print_test_result(
                "論理削除の確認（通常取得）", success, response, details
            ))
        except Exception as e:
            print(f"❌ 論理削除確認 - Exception: {e}")
            results.append(False)
        
        # 3. include_deletedで論理削除されたTodoを取得
        try:
            response = requests.get(
                f"{self.api_url}/{todo_id_soft}",
                params={"include_deleted": True},
                timeout=5
            )
            success = response.status_code == 200
            if success:
                data = response.json()
                details = f"Deleted Todo found: '{data['title']}'"
            else:
                details = "削除済みTodo取得失敗"
            results.append(self.print_test_result(
                "論理削除済みTodo取得", success, response, details
            ))
        except Exception as e:
            print(f"❌ 削除済みTodo取得 - Exception: {e}")
            results.append(False)
        
        return all(results)

    # =============================================
    # 特殊操作テスト
    # =============================================
    
    def test_special_operations(self):
        """復元・完了などの特殊操作テスト"""
        self.print_section("SPECIAL 操作テスト")
        
        results = []
        
        # 論理削除されたTodoがあることを前提
        if len(self.created_todos) < 2:
            print("❌ 特殊操作テスト用のTodoが不足")
            return False
            
        todo_id_deleted = self.created_todos[1]  # 論理削除したTodo
        
        # 1. 復元テスト
        try:
            response = requests.post(f"{self.api_url}/{todo_id_deleted}/restore", timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                deleted_at = data.get('deleted_at')
                details = f"Restored: deleted_at={deleted_at}"
            else:
                details = "復元失敗"
            results.append(self.print_test_result(
                f"Todo復元 (ID: {todo_id_deleted})", success, response, details
            ))
        except Exception as e:
            print(f"❌ Todo復元 - Exception: {e}")
            results.append(False)
        
        # 2. 完了操作テスト
        if self.created_todos:
            todo_id_complete = self.created_todos[0]
            try:
                response = requests.post(f"{self.api_url}/{todo_id_complete}/complete", timeout=10)
                success = response.status_code == 200
                if success:
                    data = response.json()
                    completed_at = data.get('completed_at_jst')
                    details = f"Completed: {data['completed']} | Time: {completed_at}"
                else:
                    details = "完了操作失敗"
                results.append(self.print_test_result(
                    f"Todo完了 (ID: {todo_id_complete})", success, response, details
                ))
            except Exception as e:
                print(f"❌ Todo完了 - Exception: {e}")
                results.append(False)
        
        return all(results)

    # =============================================
    # エラーケーステスト
    # =============================================
    
    def test_error_cases(self):
        """エラーケースのテスト"""
        self.print_section("ERROR CASES テスト")
        
        results = []
        
        # 1. 存在しないTodo取得
        try:
            response = requests.get(f"{self.api_url}/99999", timeout=5)
            success = response.status_code == 404
            details = "存在しないTodoで404エラー" if success else "エラーハンドリング不正"
            results.append(self.print_test_result(
                "存在しないTodo取得", success, response, details
            ))
        except Exception as e:
            print(f"❌ 存在しないTodo取得 - Exception: {e}")
            results.append(False)
        
        # 2. 無効なデータでTodo作成
        try:
            invalid_data = {"title": ""}  # 空のタイトル
            response = requests.post(
                self.api_url,
                json=invalid_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            success = response.status_code == 422  # Validation Error
            details = "無効データでValidation Error" if success else "バリデーション未実装"
            results.append(self.print_test_result(
                "無効データでTodo作成", success, response, details
            ))
        except Exception as e:
            print(f"❌ 無効データでTodo作成 - Exception: {e}")
            results.append(False)
        
        # 3. 無効な優先度
        try:
            invalid_data = {"title": "テスト", "priority": 5}  # 無効な優先度
            response = requests.post(
                self.api_url,
                json=invalid_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            success = response.status_code == 422  # Validation Error
            details = "無効優先度でValidation Error" if success else "優先度バリデーション未実装"
            results.append(self.print_test_result(
                "無効な優先度でTodo作成", success, response, details
            ))
        except Exception as e:
            print(f"❌ 無効優先度でTodo作成 - Exception: {e}")
            results.append(False)
        
        return all(results)

    # =============================================
    # メインテスト実行
    # =============================================
    
    def run_comprehensive_tests(self):
        """包括的なCRUDテストを実行"""
        print("🚀" * 30)
        print("🔥 Todo CRUD 包括テスト開始 🔥")
        print(f"📍 Base URL: {self.base_url}")
        print(f"⏰ Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🚀" * 30)
        
        # 各テストの実行
        test_functions = [
            ("CREATE Operations", self.test_create_basic),
            ("READ Operations", self.test_read_operations), 
            ("UPDATE Operations", self.test_update_operations),
            ("DELETE Operations", self.test_delete_operations),
            ("SPECIAL Operations", self.test_special_operations),
            ("ERROR Cases", self.test_error_cases)
        ]
        
        overall_results = {}
        
        for test_name, test_func in test_functions:
            print(f"\n🔥 Starting: {test_name}")
            try:
                result = test_func()
                overall_results[test_name] = result
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"\n{status} {test_name} Complete")
            except Exception as e:
                print(f"❌ {test_name} - Unexpected Error: {e}")
                overall_results[test_name] = False
                
            # 各テスト間で少し待機
            time.sleep(0.5)
        
        # 最終結果サマリ
        self.print_section("📊 最終テスト結果サマリ")
        
        passed = sum(overall_results.values())
        total = len(overall_results)
        
        for test_name, result in overall_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {status} {test_name}")
        
        print(f"\n🎯 総合結果: {passed}/{total} テストセット成功")
        print(f"📈 成功率: {(passed/total)*100:.1f}%")
        print(f"📝 作成されたTodo数: {len(self.created_todos)}")
        
        if passed == total:
            print("🎉 全てのCRUDテストが成功しました！")
            print("💪 Todo APIは完全に動作しています！")
        else:
            print("⚠️  一部のテストが失敗しました。")
            print("🔍 失敗したテストを確認してください。")
        
        return passed == total


if __name__ == "__main__":
    # 詳細CRUDテストを実行
    tester = TodoCRUDTester()
    success = tester.run_comprehensive_tests()
    
    # 終了コード
    exit(0 if success else 1)