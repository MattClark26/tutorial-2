"""Panel 4: The Irish Lens"""
from pathlib import Path
from pyjstat import pyjstat
import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CSO_DATASET_URL = (
    "https://ws.cso.ie/public/api.restful/"
    "PxStat.Data.Cube_API.ReadDataset/{table_code}/JSON-stat/2.0/en"
)
def fetch_cso_table(
    table_code: str,
    cache_filename: str,
    data_dir: Path | str = DATA_DIR,
    ) -> pd.DataFrame:
    """Fetch a CSO table and fall back to its local CSV cache."""
    cache_path = Path(data_dir) / cache_filename
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    url = CSO_DATASET_URL.format(table_code=table_code)

    try:
        dataset = pyjstat.Dataset.read(url)
        frame = dataset.write("dataframe")
        frame.to_csv(cache_path, index=False)
        return frame
    except Exception as error:
        if cache_path.exists():
            st.warning(
                f"CSO table {table_code} could not be refreshed. "
                f"Using cached data from {cache_path.name}. Details: {error}"
            )
            return pd.read_csv(cache_path)
        raise RuntimeError(
            f"CSO table {table_code} is unavailable and has no local cache."
        ) from error
      
def render_panel(selected_date: pd.Timestamp) -> dict:
  """Render the Irish Lens panel and return Thermometer metrics."""
  st.subheader("Panel 4 - The Irish Lens")
  st.caption(f"Selected date: {selected_date:%Y-%m-%d}")
  st.info("Irish Lens data analysis will be added later")
  return { 
        "score": 0.0,
        "status": "green",
        "verdict": "Irish Lens analysis is not available yet.",
        "track_record": {
            "caught": 0,
            "false_alarms": 0,
            "avg_lead_months": 0,
        },
  }
  
   
