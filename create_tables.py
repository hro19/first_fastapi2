#!/usr/bin/env python3
"""
データベーステーブル作成スクリプト
SQLAlchemyモデルからデータベーステーブルを作成します。
"""

import asyncio
import sys
from app.core.database import engine, Base
from app.models.todo import Todo
from app.models.profiles import Profile  
from app.models.product_result import ProductResult
from app.models.products import Product
from app.models.image_analysis import ImageAnalysis


async def create_tables():
    """データベーステーブルを作成"""
    print("🗃️  データベーステーブルを作成中...")
    
    try:
        # すべてのテーブルを作成
        async with engine.begin() as conn:
            print("🛠️  SQLAlchemy メタデータからテーブルを作成中...")
            
            # メタデータから全テーブルを作成
            await conn.run_sync(Base.metadata.create_all)
            
            print("✅ テーブル作成完了！")
            
            # 作成されたテーブル一覧を確認
            print("📋 作成されたテーブル:")
            for table_name, table in Base.metadata.tables.items():
                print(f"   ✓ {table_name}")
                # カラム情報も表示
                for column in table.columns:
                    nullable = "NULL" if column.nullable else "NOT NULL"
                    print(f"      - {column.name}: {column.type} ({nullable})")
            
        return True
        
    except Exception as e:
        print(f"❌ テーブル作成エラー: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 データベーステーブル作成ツール")
    print("=" * 60)
    
    success = asyncio.run(create_tables())
    
    if success:
        print("\n🎉 すべてのテーブルが正常に作成されました！")
        print("💡 Todo APIのテストを実行できます:")
        print("   uv run python test_todo_api.py")
        sys.exit(0)
    else:
        print("\n💥 テーブル作成に失敗しました。")
        print("🔧 データベース接続設定を確認してください。")
        sys.exit(1)
