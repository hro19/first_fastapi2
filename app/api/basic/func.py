from fastapi import APIRouter
from typing import Dict, Any
from datetime import datetime
from zoneinfo import ZoneInfo

router = APIRouter()

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

# TODO(human) - Add a function that processes a list of numbers
@router.post("/process-numbers")
async def process_numbers(numbers: list[int]) -> Dict[str, Any]:
    # TODO(human): Implement number processing logic
    # Consider calculating: sum, average, min, max, count
    # Return a comprehensive analysis of the input numbers
    pass