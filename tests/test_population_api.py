#!/usr/bin/env python3
"""Population API endpoint tests focusing on 1990 census data."""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure the application package is importable when running tests directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app


client = TestClient(app)


@pytest.mark.fast
def test_population_over_four_million_1990():
    response = client.get("/api/v1/population/1990/over4million")

    assert response.status_code == 200

    payload = response.json()

    assert payload["year"] == 1990
    assert payload["threshold"] == 4_000_000
    assert payload["unit"] == "people"
    assert payload["count"] == 8

    prefectures = payload["prefectures"]
    names_jp = [entry["prefecture_jp"] for entry in prefectures]

    # Ensure the list is sorted by population in descending order
    assert names_jp == ["東京", "大阪", "神奈川", "愛知", "埼玉", "千葉", "兵庫", "福岡"]

    assert payload["prefecture_names_jp"] == names_jp
    assert payload["prefecture_names_en"] == [
        "Tokyo",
        "Osaka",
        "Kanagawa",
        "Aichi",
        "Saitama",
        "Chiba",
        "Hyogo",
        "Fukuoka",
    ]

    tokyo = prefectures[0]
    assert tokyo["prefecture_en"] == "Tokyo"
    assert tokyo["population_1990"] == 11_856_000
