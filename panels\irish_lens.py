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

def _read_cached_frame(filename: str) -> pd.DataFrame:
    """Read one cached CSO table, or return an empty frame if absent."""
    cache_path = DATA_DIR / filename
    if not cache_path.exists():
        return pd.DataFrame()
    return pd.read_csv(cache_path)

def _find_column(
    columns: pd.Index,
    candidates: tuple[str, ...],
) -> str | None:
    """Find a column without depending on CSO's exact capitalization."""
    columns_by_lowercase = {str(column).lower(): str(column) for column in columns}
    for candidate in candidates:
        if candidate.lower() in columns_by_lowercase:
            return columns_by_lowercase[candidate.lower()]
    return None


def _to_time_series(frame: pd.DataFrame) -> pd.Series:
    """Convert a cached CSO frame into a sorted dated numeric series."""
    if frame.empty:
        return pd.Series(dtype="float64")

    time_column = _find_column(
        frame.columns,
        ("time", "date", "period", "quarter", "month"),
    )
    value_column = _find_column(
        frame.columns,
        ("value", "obs_value", "obs value"),
    )
    if time_column is None or value_column is None:
        raise ValueError(
            "Cached CSO data must contain a time column and a value column. "
            f"Found columns: {list(frame.columns)}."
        )
        raw_dates = frame[time_column].astype(str)
    dates = pd.Series(pd.NaT, index=frame.index, dtype="datetime64[ns]")
    regular_mask = ~raw_dates.str.match(r"^\d{4}\s*Q[1-4]$")
    dates.loc[regular_mask] = pd.to_datetime(
        raw_dates.loc[regular_mask],
        errors="coerce",
    ).to_numpy()
    quarter_mask = dates.isna() & raw_dates.str.match(r"^\d{4}\s*Q[1-4]$")
    if quarter_mask.any():
        quarters = raw_dates.loc[quarter_mask].str.replace(" ", "", regex=False)
        dates.loc[quarter_mask] = pd.Series(
            pd.PeriodIndex(quarters, freq="Q")
            .to_timestamp(how="end")
            .normalize(),
            index=quarters.index,
        )

    values = pd.to_numeric(frame[value_column], errors="coerce")
    series = pd.Series(values.to_numpy(), index=dates, name=value_column)
    series = series[~series.index.isna()].dropna().sort_index()
    return series[~series.index.duplicated(keep="last")]
      
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
  
   
