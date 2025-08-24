# FastAPI 完全機能リファレンス

FastAPIの全機能を体系的にまとめた包括的なドキュメントです。

## 📚 ドキュメント構成

### 🏁 [01_tutorial_basic](./01_tutorial_basic/) - 基本チュートリアル
段階的にFastAPIの基本機能を学習できる構成です。

1. **[First Steps](./01_tutorial_basic/01_first_steps.md)** - 最初のAPI作成、自動ドキュメント生成
2. **[Path Parameters](./01_tutorial_basic/02_path_parameters.md)** - URLパラメータ、型変換、Enum使用
3. **[Query Parameters](./01_tutorial_basic/03_query_parameters.md)** - クエリパラメータ、デフォルト値、型変換
4. **[Request Body](./01_tutorial_basic/04_request_body.md)** - Pydanticモデル、JSON処理
5. **[Query Parameters Validation](./01_tutorial_basic/05_query_params_validation.md)** - 文字列バリデーション、メタデータ
6. **[Path Parameters Numeric Validation](./01_tutorial_basic/06_path_params_numeric_validation.md)** - 数値制約、バリデーション
7. **[Body Multiple Parameters](./01_tutorial_basic/07_body_multiple_parameters.md)** - 複数パラメータ、Body埋め込み
8. **[Body Fields](./01_tutorial_basic/08_body_fields.md)** - Fieldバリデーション、メタデータ
9. **[Body Nested Models](./01_tutorial_basic/09_body_nested_models.md)** - ネストしたモデル、リスト、セット
10. **[Schema Extra Example](./01_tutorial_basic/10_schema_extra_example.md)** - サンプルデータ、OpenAPIエクササンプル
11. **[Extra Data Types](./01_tutorial_basic/11_extra_data_types.md)** - UUID、datetime、Decimal、bytes
12. **[Response Model](./01_tutorial_basic/12_response_model.md)** - レスポンス制御、データフィルタリング
13. **[Cookie Parameters](./01_tutorial_basic/13_cookie_parameters.md)** - クッキー処理、セキュリティ
14. **[Header Parameters](./01_tutorial_basic/14_header_parameters.md)** - HTTPヘッダー、認証、メタデータ

### 🚀 [03_advanced_guide](./03_advanced_guide/) - 高度な機能

1. **[Advanced Dependencies](./03_advanced_guide/01_advanced_dependencies.md)** - 依存性注入、呼び出し可能クラス

*注: Advanced Guideの他のセクションは継続調査中*

## 🔍 機能別索引

### 🔐 認証・セキュリティ
- [Cookie Parameters](./01_tutorial_basic/13_cookie_parameters.md) - セッション管理、セキュリティトークン
- [Header Parameters](./01_tutorial_basic/14_header_parameters.md) - 認証ヘッダー、APIキー
- [Advanced Dependencies](./03_advanced_guide/01_advanced_dependencies.md) - セキュリティ依存性、権限管理

### 📊 データ処理
- [Request Body](./01_tutorial_basic/04_request_body.md) - JSON、Pydanticモデル
- [Body Nested Models](./01_tutorial_basic/09_body_nested_models.md) - 複雑なデータ構造
- [Extra Data Types](./01_tutorial_basic/11_extra_data_types.md) - UUID、日時、Decimal
- [Response Model](./01_tutorial_basic/12_response_model.md) - レスポンス制御

### 🛡️ バリデーション
- [Query Parameters Validation](./01_tutorial_basic/05_query_params_validation.md) - 文字列制約
- [Path Parameters Numeric Validation](./01_tutorial_basic/06_path_params_numeric_validation.md) - 数値制約
- [Body Fields](./01_tutorial_basic/08_body_fields.md) - フィールドレベルバリデーション

### 📝 ドキュメント生成
- [First Steps](./01_tutorial_basic/01_first_steps.md) - Swagger UI、ReDoc
- [Schema Extra Example](./01_tutorial_basic/10_schema_extra_example.md) - APIサンプル、OpenAPIカスタマイズ

### ⚙️ システム統合
- [Advanced Dependencies](./03_advanced_guide/01_advanced_dependencies.md) - 複雑な依存関係、データベース接続

## 🎯 FastAPIの主要特徴

### 🔥 コア機能
- **高性能**: 現代的で高速なWebフレームワーク
- **型ヒント**: Python型システムを活用した開発支援
- **自動ドキュメント**: Swagger UI/ReDocによる対話型ドキュメント
- **非同期サポート**: asyncプログラミング対応

### 💡 開発者体験
- **エディターサポート**: 自動補完、型チェック、リファクタリング支援
- **最小限のコード**: ボイラープレートコードの削減
- **直感的API**: Pythonの標準的な型システムを活用
- **段階的学習**: 基本から高度な機能への自然な進行

### 🔧 プロダクション対応
- **バリデーション**: 包括的な入力検証
- **セキュリティ**: 認証・認可の統合サポート
- **エラーハンドリング**: 明確なエラーメッセージ
- **テスト対応**: テスト容易性とモック支援

## 📈 学習パス推奨順序

### 🌱 初心者
1. [First Steps](./01_tutorial_basic/01_first_steps.md) - 基本的なAPI作成
2. [Path Parameters](./01_tutorial_basic/02_path_parameters.md) - URLパラメータの処理
3. [Query Parameters](./01_tutorial_basic/03_query_parameters.md) - クエリパラメータの処理
4. [Request Body](./01_tutorial_basic/04_request_body.md) - JSONデータの処理

### 🌿 中級者
5. [Query Parameters Validation](./01_tutorial_basic/05_query_params_validation.md) - バリデーション基礎
6. [Body Fields](./01_tutorial_basic/08_body_fields.md) - 詳細なバリデーション
7. [Response Model](./01_tutorial_basic/12_response_model.md) - レスポンス制御
8. [Cookie Parameters](./01_tutorial_basic/13_cookie_parameters.md) - クッキー処理

### 🌲 上級者
9. [Body Nested Models](./01_tutorial_basic/09_body_nested_models.md) - 複雑なデータ構造
10. [Extra Data Types](./01_tutorial_basic/11_extra_data_types.md) - 特殊データ型
11. [Advanced Dependencies](./03_advanced_guide/01_advanced_dependencies.md) - 高度な依存性注入
12. Header Parameters - HTTPヘッダー処理

## 🔗 関連リソース

### 📖 公式リソース
- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [FastAPI GitHub](https://github.com/tiangolo/fastapi)

### 🛠️ 開発ツール
- [Pydantic](https://pydantic-docs.helpmanual.io/) - データバリデーション
- [Starlette](https://www.starlette.io/) - 基盤フレームワーク
- [Uvicorn](https://www.uvicorn.org/) - ASGIサーバー

## 📊 調査状況

### ✅ 完了済み
- **基本チュートリアル**: 14セクション (主要機能を網羅)
- **Advanced Guide**: 1セクション (依存性注入)

### 🔄 調査継続中
- Advanced User Guide の残りのセクション
- API Reference
- デプロイメント機能
- セキュリティ機能詳細
- データベース統合
- テスト機能
- WebSockets
- Middleware

---

*このドキュメントは[FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)に基づいて作成されています。*
*最終更新: 2024年8月*