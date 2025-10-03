"""
Population data API endpoints
"""
from fastapi import APIRouter, HTTPException
import pandas as pd
import os
from typing import List, Dict, Any, Optional, Tuple

router = APIRouter()


def load_population_data():
    """Load and parse the population Excel file"""
    try:
        # Get the absolute path to the data file
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        file_path = os.path.join(current_dir, "data", "populatin.xlsx")
        
        # Load the Excel file without headers
        df = pd.read_excel(file_path, header=None)
        
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading population data: {str(e)}")


def parse_prefecture_cell(value: Any) -> Tuple[Optional[str], Optional[str]]:
    """Extract the prefecture code and Japanese name from the raw cell value."""
    if pd.isna(value):
        return None, None

    text = str(value).strip()
    if not text:
        return None, None

    delimiter = "\u3000"  # full-width space used in the spreadsheet
    if delimiter in text:
        code, name = text.split(delimiter, 1)
        return code.strip() or None, name.strip()

    return None, text


TARGET_PREFECTURES_JP = ["東京", "千葉", "神奈川"]
YEAR_COLUMN_INDEX = {
    1980: 15,
    1985: 16,
    1990: 17,
    1995: 18,
    2000: 19,
}

FOUR_MILLION_THRESHOLD = 4_000_000
TWO_MILLION_THRESHOLD = 2_000_000
DATA_SOURCE_1990 = "Japanese Census 1990"
DATA_SOURCE_1980_2000 = "Japanese Census 1980-2000"


def extract_population_records(
    df: pd.DataFrame,
    *,
    year: int,
    start_row: int = 16,
    end_row: int = 64,
) -> List[Dict[str, Any]]:
    """Return structured population records for a given census year."""
    column_index = YEAR_COLUMN_INDEX.get(year)
    if column_index is None:
        raise HTTPException(status_code=400, detail=f"Unsupported year requested: {year}")

    records: List[Dict[str, Any]] = []

    for row_index in range(start_row, end_row):
        if row_index >= len(df):
            break

        row = df.iloc[row_index]
        prefecture_raw = row.iloc[0]
        code, prefecture_jp = parse_prefecture_cell(prefecture_raw)

        if not prefecture_jp or column_index >= len(row):
            continue

        population_cell = row.iloc[column_index]
        if pd.isna(population_cell):
            continue

        population = int(float(population_cell) * 1000)
        prefecture_en = None

        if len(row) > 1 and pd.notna(row.iloc[1]):
            prefecture_en = str(row.iloc[1]).strip()

        label = prefecture_en or prefecture_jp

        records.append(
            {
                "prefecture_code": code,
                "prefecture_jp": prefecture_jp,
                "prefecture_en": prefecture_en,
                "population": population,
                "label": label,
            }
        )

    return records

@router.get("/1990", response_model=List[Dict[str, Any]])
async def get_1990_population():
    """
    Get 1990 population data for all prefectures in Japan
    
    Returns:
        List of dictionaries containing prefecture names and population data
    """
    df = load_population_data()

    try:
        records = extract_population_records(df, year=1990)

        population_data = [
            {
                "prefecture_code": record["prefecture_code"],
                "prefecture": record["prefecture_jp"],
                "population_1990": record["population"],
                "population_unit": "people",
                "data_source": DATA_SOURCE_1990,
            }
            for record in records
        ]

        if not population_data:
            raise HTTPException(status_code=404, detail="No population data found for 1990")
            
        return population_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing population data: {str(e)}")


@router.get("/1990/over4million", response_model=Dict[str, Any])
async def get_1990_population_over_four_million() -> Dict[str, Any]:
    """Return prefectures where the 1990 population exceeded four million people."""
    df = load_population_data()

    try:
        records = extract_population_records(df, year=1990)

        filtered = [
            {
                "prefecture_code": record["prefecture_code"],
                "prefecture_jp": record["prefecture_jp"],
                "prefecture_en": record["prefecture_en"],
                "population_1990": record["population"],
                "population_unit": "people",
            }
            for record in records
            if record["population"] > FOUR_MILLION_THRESHOLD
        ]

        filtered.sort(key=lambda entry: entry["population_1990"], reverse=True)

        if not filtered:
            raise HTTPException(
                status_code=404,
                detail="No prefectures exceeded four million residents in 1990",
            )

        prefecture_names_jp = [entry["prefecture_jp"] for entry in filtered]
        prefecture_names_en = [
            entry["prefecture_en"]
            for entry in filtered
            if entry["prefecture_en"] is not None
        ]

        return {
            "year": 1990,
            "threshold": FOUR_MILLION_THRESHOLD,
            "unit": "people",
            "data_source": DATA_SOURCE_1990,
            "count": len(filtered),
            "prefectures": filtered,
            "prefecture_names_jp": prefecture_names_jp,
            "prefecture_names_en": prefecture_names_en,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error filtering population data: {str(e)}")


@router.get("/1990_series")
async def get_1990_population_series() -> Dict[str, Any]:
    """Return 1990 population data summarized via a pandas Series."""
    df = load_population_data()

    try:
        records = extract_population_records(df, year=1990)

        if not records:
            raise HTTPException(status_code=404, detail="No population data found for 1990")

        series = pd.Series(
            {record["label"]: record["population"] for record in records},
            name="population_1990",
            dtype="int64",
        )

        sorted_series = series.sort_values(ascending=False)
        top5 = sorted_series.head(5)

        summary = {
            "count": int(series.count()),
            "total_population": int(series.sum()),
            "average_population": int(series.mean()),
            "max_population": {
                "label": sorted_series.index[0],
                "population": int(sorted_series.iloc[0]),
            },
        }

        return {
            "series_name": series.name,
            "unit": "people",
            "summary": summary,
            "top5": {label: int(value) for label, value in top5.items()},
            "data": [
                {
                    "prefecture_code": record["prefecture_code"],
                    "prefecture_jp": record["prefecture_jp"],
                    "prefecture_en": record["prefecture_en"],
                    "population": record["population"],
                }
                for record in records
            ],
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating 1990 population series: {str(e)}")


@router.get("/1980_2000")
async def get_population_1980_2000() -> Dict[str, Any]:
    """Return population table data for Tokyo, Chiba, and Kanagawa from 1980 to 2000."""
    df = load_population_data()

    try:
        prefecture_order = {name: index for index, name in enumerate(TARGET_PREFECTURES_JP)}
        prefecture_rows = []

        for i in range(len(df)):
            row = df.iloc[i]
            prefecture_raw = row.iloc[0]
            code, prefecture_jp = parse_prefecture_cell(prefecture_raw)

            if prefecture_jp not in prefecture_order:
                continue

            prefecture_en = None
            if len(row) > 1 and pd.notna(row.iloc[1]):
                prefecture_en = str(row.iloc[1]).strip()

            year_populations: Dict[str, Optional[int]] = {}
            for year, column_index in YEAR_COLUMN_INDEX.items():
                population_value = None
                if column_index < len(row):
                    cell_value = row.iloc[column_index]
                    if pd.notna(cell_value):
                        population_value = int(float(cell_value) * 1000)
                year_populations[str(year)] = population_value

            prefecture_rows.append(
                {
                    "prefecture_code": code,
                    "prefecture_jp": prefecture_jp,
                    "prefecture_en": prefecture_en,
                    "populations": year_populations,
                    "population_unit": "people",
                }
            )

        if not prefecture_rows:
            raise HTTPException(status_code=404, detail="No population data found for requested prefectures")

        prefecture_rows.sort(key=lambda entry: prefecture_order[entry["prefecture_jp"]])

        return {
            "years": list(YEAR_COLUMN_INDEX.keys()),
            "unit": "people",
            "data_source": DATA_SOURCE_1980_2000,
            "prefectures": prefecture_rows,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing population data: {str(e)}")


@router.get("/1980_2000/over2million", response_model=Dict[str, Any])
async def get_population_1980_2000_over_two_million() -> Dict[str, Any]:
    """Return prefectures exceeding two million residents for each census year between 1980 and 2000."""
    df = load_population_data()

    try:
        yearly_results: List[Dict[str, Any]] = []

        for year in sorted(YEAR_COLUMN_INDEX.keys()):
            records = extract_population_records(df, year=year)

            filtered = [
                {
                    "prefecture_code": record["prefecture_code"],
                    "prefecture_jp": record["prefecture_jp"],
                    "prefecture_en": record["prefecture_en"],
                    "population": record["population"],
                    "population_unit": "people",
                }
                for record in records
                if record["population"] > TWO_MILLION_THRESHOLD
            ]

            filtered.sort(key=lambda entry: entry["population"], reverse=True)

            prefecture_names_jp = [entry["prefecture_jp"] for entry in filtered]
            prefecture_names_en = [
                entry["prefecture_en"]
                for entry in filtered
                if entry["prefecture_en"] is not None
            ]

            yearly_results.append(
                {
                    "year": year,
                    "count": len(filtered),
                    "prefectures": filtered,
                    "prefecture_names_jp": prefecture_names_jp,
                    "prefecture_names_en": prefecture_names_en,
                }
            )

        if not yearly_results:
            raise HTTPException(status_code=404, detail="No population data found for requested years")

        prefecture_names_jp_by_year = {
            result["year"]: result["prefecture_names_jp"] for result in yearly_results
        }
        prefecture_names_en_by_year = {
            result["year"]: result["prefecture_names_en"] for result in yearly_results
        }

        return {
            "years": yearly_results,
            "threshold": TWO_MILLION_THRESHOLD,
            "unit": "people",
            "data_source": DATA_SOURCE_1980_2000,
            "prefecture_names_jp_by_year": prefecture_names_jp_by_year,
            "prefecture_names_en_by_year": prefecture_names_en_by_year,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error filtering population data: {str(e)}")
