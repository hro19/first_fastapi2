import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
from datetime import datetime
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """シンプルなメール送信サービス"""
    
    def __init__(self):
        self.smtp_host = settings.EMAIL_SMTP_HOST
        self.smtp_port = settings.EMAIL_SMTP_PORT
        self.username = settings.EMAIL_USERNAME
        self.password = settings.EMAIL_PASSWORD
        self.from_email = settings.EMAIL_FROM
        self.to_email = settings.EMAIL_TO
    
    async def send_first_email(self) -> Dict[str, Any]:
        """
        /api/v1/basic/email/first エンドポイント用のメール送信
        固定の送信者・受信者でシンプルなメールを送信
        """
        try:
            # メールの内容を作成
            subject = "FastAPI メール送信テスト - 初回メール"
            body = f"""
お疲れさまです。

FastAPI からの自動送信メールです。
/api/v1/email/first エンドポイントが正常に呼び出されました。

【送信情報】
送信時刻: {datetime.now().strftime('%Y年%m月%d日 %H時%M分%S秒')}
送信者: {self.from_email}
受信者: {self.to_email}
システム: FastAPI Email Service

このメールは API エンドポイントのテスト用として送信されています。
メール送信機能が正常に動作していることを確認できました。

何かご質問がございましたら、開発チームまでお知らせください。

FastAPI 自動メール送信システム
            """
            
            # メールメッセージを作成
            message = MIMEMultipart()
            message["From"] = self.from_email
            message["To"] = self.to_email
            message["Subject"] = subject
            
            # メール本文を添付
            message.attach(MIMEText(body, "plain", "utf-8"))
            
            # SMTP接続してメール送信
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.username, self.password)
                server.sendmail(self.from_email, self.to_email, message.as_string())
            
            logger.info(f"Email sent successfully from {self.from_email} to {self.to_email}")
            
            return {
                "status": "success",
                "message": "メールが正常に送信されました",
                "details": "自動メール送信が完了しました。受信者のメールボックスをご確認ください。",
                "from": self.from_email,
                "to": self.to_email,
                "subject": subject,
                "timestamp": datetime.now().isoformat(),
                "smtp_config": {
                    "host": self.smtp_host,
                    "port": self.smtp_port
                }
            }
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP Authentication Error: {str(e)}")
            return {
                "status": "error",
                "message": "メール認証に失敗しました。メールアカウントの設定を確認してください。",
                "details": "Gmail の場合、アプリパスワードの設定が必要です。2段階認証を有効にしてアプリパスワードを生成してください。",
                "error_type": "authentication_error",
                "timestamp": datetime.now().isoformat()
            }
            
        except smtplib.SMTPException as e:
            logger.error(f"SMTP Error: {str(e)}")
            return {
                "status": "error", 
                "message": f"SMTP サーバーエラーが発生しました: {str(e)}",
                "details": "メールサーバーとの通信中にエラーが発生しました。しばらく時間をおいて再試行してください。",
                "error_type": "smtp_error",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Unexpected error sending email: {str(e)}")
            return {
                "status": "error",
                "message": f"メール送信中に予期しないエラーが発生しました: {str(e)}",
                "details": "システムエラーが発生しました。開発チームにお問い合わせください。",
                "error_type": "general_error", 
                "timestamp": datetime.now().isoformat()
            }


# シングルトンインスタンス
email_service = EmailService()