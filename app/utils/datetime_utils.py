from datetime import datetime, timezone, timedelta
from typing import Optional

# 日本標準時（JST）の設定
JST = timezone(timedelta(hours=9))


def get_jst_now() -> datetime:
    """現在の日本時間を取得"""
    return datetime.now(JST)


def to_jst(dt: Optional[datetime]) -> Optional[datetime]:
    """datetimeを日本時間に変換"""
    if dt is None:
        return None
    
    # timezone-naiveな場合はUTCとして扱い、JSTに変換
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    return dt.astimezone(JST)


def format_jst(dt: Optional[datetime], format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[str]:
    """日本時間として整形した文字列を返す"""
    if dt is None:
        return None
    
    jst_dt = to_jst(dt)
    return jst_dt.strftime(format_str) if jst_dt else None


def parse_jst(date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """日本時間の文字列をdatetimeに変換"""
    dt = datetime.strptime(date_str, format_str)
    return dt.replace(tzinfo=JST)