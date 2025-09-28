from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

from app.services.email_service import email_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/first")
async def send_first_email() -> Dict[str, Any]:
    """
    固定のメールアドレス間でテストメールを送信するエンドポイント
    
    送信者: dropmoment19@gmail.com
    受信者: jatain19@gmail.com
    
    このエンドポイントを呼び出すと自動的にメールが送信されます。
    
    Returns:
        Dict[str, Any]: メール送信結果（成功・失敗の詳細情報）
        
    Examples:
        GET /api/v1/email/first
        
    Note:
        メール送信には環境変数の設定が必要です：
        - EMAIL_PASSWORD: アプリパスワード（Gmailの2段階認証が必要）
    """
    
    logger.info("メール送信リクエストを受信しました: /api/v1/email/first")
    
    try:
        # メール送信サービスを呼び出し
        result = await email_service.send_first_email()
        
        if result["status"] == "success":
            logger.info(f"メール送信成功: {result}")
            return result
        else:
            logger.error(f"メール送信失敗: {result}")
            # エラーレスポンスでもHTTP 200で返す（エラー詳細は結果に含まれる）
            return result
            
    except Exception as e:
        logger.error(f"メールエンドポイントで予期しないエラー: {str(e)}")
        return {
            "status": "error",
            "message": f"エンドポイントエラーが発生しました: {str(e)}",
            "details": "API エンドポイント内部でエラーが発生しました。",
            "error_type": "endpoint_error"
        }


@router.get("/status") 
async def get_email_status() -> Dict[str, Any]:
    """
    メール設定の状態確認エンドポイント
    
    Returns:
        Dict[str, Any]: メール設定の状態情報
    """
    
    from app.core.config import settings
    
    # パスワードは表示しない（セキュリティのため）
    password_configured = bool(settings.EMAIL_PASSWORD)
    
    return {
        "smtp_host": settings.EMAIL_SMTP_HOST,
        "smtp_port": settings.EMAIL_SMTP_PORT,
        "password_configured": password_configured,
        "from_email": settings.EMAIL_FROM,
        "to_email": settings.EMAIL_TO,
        "status": "configured" if (settings.EMAIL_FROM and password_configured) else "not_configured",
        "message": "メールサービスの準備が完了しています" if (settings.EMAIL_FROM and password_configured) else ".env ファイルに EMAIL_FROM と EMAIL_PASSWORD を設定してください",
        "note": "Gmail を使用する場合は、2段階認証を有効にしてアプリパスワードを生成する必要があります"
    }