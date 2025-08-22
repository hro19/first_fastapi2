from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base
from app.utils.datetime_utils import get_jst_now


class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    priority = Column(Integer, default=0)  # 0: Low, 1: Medium, 2: High
    
    # 日時フィールド（日本時間で保存）
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # 論理削除用フィールド
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}', completed={self.completed}, deleted_at={self.deleted_at})>"
    
    def soft_delete(self):
        """論理削除を実行"""
        self.deleted_at = get_jst_now()
    
    def restore(self):
        """論理削除を取り消し"""
        self.deleted_at = None
    
    @property
    def is_deleted(self):
        """論理削除されているかチェック"""
        return self.deleted_at is not None