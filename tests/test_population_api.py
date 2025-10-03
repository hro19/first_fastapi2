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
    assert payload["count"] == 9

    prefectures = payload["prefectures"]
    names_jp = [entry["prefecture_jp"] for entry in prefectures]

    # Ensure the list is sorted by population in descending order
    assert names_jp == [
        "東京",
        "大阪",
        "神奈川",
        "愛知",
        "埼玉",
        "北海道",
        "千葉",
        "兵庫",
        "福岡",
    ]

    assert payload["prefecture_names_jp"] == names_jp
    assert payload["prefecture_names_en"] == [
        "Tokyo",
        "Osaka",
        "Kanagawa",
        "Aichi",
        "Saitama",
        "Hokkaido",
        "Chiba",
        "Hyogo",
        "Fukuoka",
    ]

    tokyo = prefectures[0]
    assert tokyo["prefecture_en"] == "Tokyo"
    assert tokyo["population_1990"] == 11_856_000


@pytest.mark.fast
def test_population_over_two_million_by_year():
    response = client.get("/api/v1/population/1980_2000/over2million")

    assert response.status_code == 200

    payload = response.json()

    assert payload["threshold"] == 2_000_000
    assert payload["unit"] == "people"
    assert payload["data_source"] == "Japanese Census 1980-2000"

    years = {entry["year"]: entry for entry in payload["years"]}

    assert set(years.keys()) == {1980, 1985, 1990, 1995, 2000}

    prefectures_1980 = years[1980]["prefecture_names_jp"]
    assert prefectures_1980 == [
        "東京",
        "大阪",
        "神奈川",
        "愛知",
        "北海道",
        "埼玉",
        "兵庫",
        "千葉",
        "福岡",
        "静岡",
        "広島",
        "茨城",
        "京都",
        "新潟",
        "長野",
        "宮城",
        "福島",
    ]

    prefectures_2000_en = years[2000]["prefecture_names_en"]
    assert prefectures_2000_en == [
        "Tokyo",
        "Osaka",
        "Kanagawa",
        "Aichi",
        "Saitama",
        "Chiba",
        "Hokkaido",
        "Hyogo",
        "Fukuoka",
        "Shizuoka",
        "Ibaraki",
        "Hiroshima",
        "Kyoto",
        "Niigata",
        "Miyagi",
        "Nagano",
        "Fukushima",
        "Gifu",
        "Gumma",
        "Tochigi",
    ]

    names_jp_by_year = payload["prefecture_names_jp_by_year"]
    assert names_jp_by_year["1980"] == prefectures_1980

    names_en_by_year = payload["prefecture_names_en_by_year"]
    assert names_en_by_year["2000"] == prefectures_2000_en
