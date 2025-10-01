"""
Population data API endpoints
"""
from fastapi import APIRouter, HTTPException
import pandas as pd
import os
from typing import List, Dict, Any

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
                
                # Skip if prefecture name or population is NaN
                if pd.notna(prefecture_raw) and pd.notna(population_1990):
                    # Clean prefecture name (remove number prefix)
                    prefecture = str(prefecture_raw).strip()
                    if prefecture.startswith(('01　', '02　', '03　', '04　', '05　', '06　', '07　', '08　', '09　')):
                        prefecture = prefecture[3:]  # Remove "XX　" prefix
                    elif prefecture.startswith(('10　', '11　', '12　', '13　', '14　', '15　', '16　', '17　', '18　', '19　')):
                        prefecture = prefecture[3:]  # Remove "XX　" prefix
                    elif prefecture.startswith(('20　', '21　', '22　', '23　', '24　', '25　', '26　', '27　', '28　', '29　')):
                        prefecture = prefecture[3:]  # Remove "XX　" prefix
                    elif prefecture.startswith(('30　', '31　', '32　', '33　', '34　', '35　', '36　', '37　', '38　', '39　')):
                        prefecture = prefecture[3:]  # Remove "XX　" prefix
                    elif prefecture.startswith(('40　', '41　', '42　', '43　', '44　', '45　', '46　', '47　')):
                        prefecture = prefecture[3:]  # Remove "XX　" prefix
                    
                    # Convert population (in thousands) to actual population
                    population = int(float(population_1990) * 1000)
                    
                    population_data.append({
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