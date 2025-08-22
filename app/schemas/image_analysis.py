from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID


class AnalysisBase(BaseModel):
    filename: str
    file_path: str
    file_size: int
    content_type: str
    azure_analysis: Optional[Dict[str, Any]] = None


class AnalysisCreate(AnalysisBase):
    pass


class AnalysisResponse(AnalysisBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnalysisHistoryResponse(BaseModel):
    id: UUID
    filename: str
    file_size: int
    content_type: str
    created_at: datetime
    
    # Azure analysis summary for list view
    tags_count: Optional[int] = None
    has_text: Optional[bool] = None

    class Config:
        from_attributes = True


class AnalysisStats(BaseModel):
    total_analyses: int
    total_file_size: int
    most_common_tags: List[Dict[str, Any]]
    analysis_by_month: List[Dict[str, Any]]