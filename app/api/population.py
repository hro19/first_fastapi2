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

@router.get("/1990", response_model=List[Dict[str, Any]])
async def get_1990_population():
    """
    Get 1990 population data for all prefectures in Japan
    
    Returns:
        List of dictionaries containing prefecture names and population data
    """
    df = load_population_data()
    
    try:
        # Extract 1990 population data
        # Data starts from row 17 (index 17) and goes to row 63 (index 63)
        # Column 0 has prefecture names, Column 17 has 1990 population
        population_data = []
        
        for i in range(17, 64):  # Row 17-63 (index 17-63)
            if i < len(df):
                row = df.iloc[i]
                prefecture_raw = row.iloc[0]
                population_1990 = row.iloc[17]

                code, prefecture = parse_prefecture_cell(prefecture_raw)

                # Skip if prefecture name or population is NaN
                if prefecture and pd.notna(population_1990):
                    population = int(float(population_1990) * 1000)

                    population_data.append({
                        "prefecture_code": code,
                        "prefecture": prefecture,
                        "population_1990": population,
                        "population_unit": "people",
                        "data_source": "Japanese Census 1990"
                    })
        
        if not population_data:
            raise HTTPException(status_code=404, detail="No population data found for 1990")
            
        return population_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing population data: {str(e)}")


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
            "data_source": "Japanese Census 1980-2000",
            "prefectures": prefecture_rows,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing population data: {str(e)}")
