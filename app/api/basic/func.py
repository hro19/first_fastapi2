from fastapi import APIRouter
from typing import Dict, Any, List
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field, field_validator

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
            "/status - Service status"
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