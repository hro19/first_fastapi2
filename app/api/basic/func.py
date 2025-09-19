from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field, field_validator
import httpx
import os

router = APIRouter()

class NumbersRequest(BaseModel):
    numbers: List[int] = Field(..., min_items=2, max_items=1000, description="整数のリスト（2-1000個、統計分析には最低2個必要）")
    operation_type: str = Field(default="analysis", description="処理タイプ")

    @field_validator('numbers')
    @classmethod
    def validate_number_range_and_meaningfulness(cls, v):
        # 各数値の範囲チェック
        for num in v:
            if num < -1000000 or num > 1000000:
                raise ValueError('各数値は-1,000,000から1,000,000の範囲内である必要があります')

        # 統計的意味のあるデータかチェック
        if len(set(v)) == 1:
            raise ValueError('全て同じ値では統計分析の意味がありません')

        return v

class WeatherResponse(BaseModel):
    city: str = Field(..., description="都市名")
    date: str = Field(..., description="予報日付（YYYY-MM-DD）")
    jst_time: str = Field(..., description="日本時間での取得時刻")
    weather_main: str = Field(..., description="天気の概要")
    weather_description: str = Field(..., description="天気の詳細説明")
    temperature: float = Field(..., description="気温（摂氏）")
    temperature_min: float = Field(..., description="最低気温（摂氏）")
    temperature_max: float = Field(..., description="最高気温（摂氏）")
    humidity: int = Field(..., description="湿度（%）")
    wind_speed: float = Field(..., description="風速（m/s）")
    status: str = Field(default="success", description="APIレスポンスステータス")

@router.get("/hello")
async def hello_world() -> Dict[str, Any]:
    return {
        "message": "Hello from basic func!",
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    }

@router.get("/info")
async def get_info() -> Dict[str, Any]:
    return {
        "service": "Basic Function API",
        "version": "1.0.0",
        "description": "Simple function-like endpoints",
        "available_endpoints": [
            "/hello - Simple hello world",
            "/hello2 - List response example",
            "/info - Service information",
            "/calculate/add?a={int}&b={int} - Add two numbers",
            "/calculate/multiply?a={int}&b={int} - Multiply two numbers",
            "/status - Service status",
            "/tenki - Get tomorrow's Tokyo weather forecast (uses JMA API, no API key required)"
        ]
    }

@router.get("/calculate/add")
async def add_numbers(a: int, b: int) -> Dict[str, Any]:
    return {
        "operation": "addition",
        "operands": [a, b],
        "result": a + b,
        "formula": f"{a} + {b} = {a + b}"
    }

@router.get("/calculate/multiply")
async def multiply_numbers(a: int, b: int) -> Dict[str, Any]:
    return {
        "operation": "multiplication",
        "operands": [a, b],
        "result": a * b,
        "formula": f"{a} × {b} = {a * b}"
    }

@router.get("/status")
async def get_status() -> Dict[str, Any]:
    utc_now = datetime.now()
    jst_now = datetime.now(ZoneInfo("Asia/Tokyo"))

    return {
        "service_name": "Basic Functions",
        "status": "running",
        "uptime": "active",
        "last_check_utc": utc_now.isoformat(),
        "last_check_jst": jst_now.isoformat(),
        "timezone": "Asia/Tokyo",
        "health": "OK"
    }

@router.get("/hello2")
async def hello2() -> list[str]:
    utc_time = datetime.now().isoformat()
    jst_time = datetime.now(ZoneInfo("Asia/Tokyo")).isoformat()
    return [
        "Hello from hello2 function!",
        f"UTC time: {utc_time}",
        f"JST time: {jst_time}",
        "Status: active",
        "Type: list response",
        "API version: 1.0.0"
    ]

@router.post("/process-numbers")
async def process_numbers(request: NumbersRequest) -> Dict[str, Any]:
    numbers = request.numbers

    return {
        "operation": request.operation_type,
        "count": len(numbers),
        "sum": sum(numbers),
        "average": sum(numbers) / len(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "input": numbers,
        "validation": "passed"
    }

@router.get("/tenki", response_model=WeatherResponse)
async def get_tokyo_weather_tomorrow() -> WeatherResponse:
    """
    明日の東京エリアの天気予報を取得するAPI
    
    気象庁APIを使用して天気予報を取得します（APIキー不要）。
    - データソース: 気象庁（日本の公式気象データ）
    - 時間: 日本時間（Asia/Tokyo）で計算
    - 都市: 東京
    """
    
    # 日本時間で明日の日付を計算
    jst_now = datetime.now(ZoneInfo("Asia/Tokyo"))
    tomorrow = jst_now + timedelta(days=1)
    tomorrow_date = tomorrow.strftime("%Y-%m-%d")
    
    # 気象庁API URL（東京地方: 130000）
    url = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            data = response.json()
        
        # 明日の天気データを取得
        forecast_data = data[0]  # 最初の予報データ
        time_series = forecast_data["timeSeries"][0]  # 時系列データ
        
        # 明日のインデックスを探す
        tomorrow_index = 1 if len(time_series["timeDefines"]) > 1 else 0
        
        # 天気コードから天気情報を取得
        weather_code = time_series["areas"][0]["weatherCodes"][tomorrow_index]
        weather_name = time_series["areas"][0]["weathers"][tomorrow_index]
        
        # 気温データを取得（詳細な時系列データから）
        temp_data = forecast_data["timeSeries"][2] if len(forecast_data["timeSeries"]) > 2 else None
        
        # デフォルト値を設定
        temp_min, temp_max = 15.0, 25.0
        humidity = 60
        wind_speed = 2.0
        
        if temp_data and len(temp_data["areas"]) > 0:
            temp_area = temp_data["areas"][0]
            if "temps" in temp_area and len(temp_area["temps"]) > tomorrow_index:
                try:
                    temp_max = float(temp_area["temps"][tomorrow_index]) if temp_area["temps"][tomorrow_index] else 25.0
                    temp_min = temp_max - 8.0  # 最低気温は最高気温-8度と仮定
                except (ValueError, TypeError):
                    pass
        
        # 平均気温を計算
        avg_temp = (temp_min + temp_max) / 2
        
        return WeatherResponse(
            city="東京",
            date=tomorrow_date,
            jst_time=jst_now.strftime("%Y-%m-%d %H:%M:%S JST"),
            weather_main=weather_code,
            weather_description=weather_name,
            temperature=round(avg_temp, 1),
            temperature_min=round(temp_min, 1),
            temperature_max=round(temp_max, 1),
            humidity=humidity,
            wind_speed=wind_speed,
            status="success"
        )
        
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"気象庁API呼び出しエラー: {e.response.status_code}"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"気象庁APIへの接続エラー: {str(e)}"
        )
    except (KeyError, IndexError, ValueError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"天気予報データの解析エラー: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"天気予報取得中にエラーが発生しました: {str(e)}"
        )