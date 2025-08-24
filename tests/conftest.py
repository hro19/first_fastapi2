import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
def mock_db_session():
    """モックのデータベースセッション"""
    session = AsyncMock(spec=AsyncSession)
    return session