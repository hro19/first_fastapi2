from fastapi import APIRouter
from typing import Dict, Any
import json
from datetime import datetime

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
            "/info - Service information",
            "/calculate/add/{a}/{b} - Add two numbers",
            "/status - Service status"
        ]
    }

@router.get("/calculate/add/{a}/{b}")
async def add_numbers(a: int, b: int) -> Dict[str, Any]:
    result = a + b
    return {
        "operation": "addition",
        "operands": [a, b],
        "result": result,
        "formula": f"{a} + {b} = {result}"
    }

@router.get("/calculate/multiply/{a}/{b}")
async def multiply_numbers(a: int, b: int) -> Dict[str, Any]:
    result = a * b
    return {
        "operation": "multiplication",
        "operands": [a, b],
        "result": result,
        "formula": f"{a} × {b} = {result}"
    }

@router.get("/status")
async def get_status() -> Dict[str, Any]:
    return {
        "service_name": "Basic Functions",
        "status": "running",
        "uptime": "active",
        "last_check": datetime.now().isoformat(),
        "health": "OK"
    }

# TODO(human) - Add a function that processes a list of numbers
@router.post("/process-numbers")
async def process_numbers(numbers: list[int]) -> Dict[str, Any]:
    # TODO(human): Implement number processing logic
    # Consider calculating: sum, average, min, max, count
    # Return a comprehensive analysis of the input numbers
    pass