from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import IntEnum


class Priority(IntEnum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Todoのタイトル")
    description: Optional[str] = Field(None, description="Todoの詳細説明")
    priority: Priority = Field(Priority.LOW, description="優先度 (0: Low, 1: Medium, 2: High)")


class TodoCreate(TodoBase):
    """Todo作成用スキーマ"""
    pass


class TodoUpdate(BaseModel):
    """Todo更新用スキーマ（部分更新対応）"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[Priority] = None


class TodoResponse(TodoBase):
    """Todoレスポンス用スキーマ"""
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    # 日本時間でフォーマットされた文字列
    created_at_jst: Optional[str] = None
    updated_at_jst: Optional[str] = None
    completed_at_jst: Optional[str] = None
    deleted_at_jst: Optional[str] = None
    
    class Config:
        from_attributes = True
        use_enum_values = True


class TodoListResponse(BaseModel):
    """Todo一覧レスポンス用スキーマ"""
    total: int
    items: list[TodoResponse]
    
    class Config:
        from_attributes = True