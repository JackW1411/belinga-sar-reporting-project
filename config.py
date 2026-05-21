# config.py
# Central config for Belinga SAR change detection pipeline

# --- Project ---
GEE_PROJECT = 'belinga-sar'

# --- AOI ---
# Belinga, Gabon -- [west, south, east, north] WGS84
# Source: UTM Zone 33N corners converted to WGS84
AOI_COORDS = [13.0925, 0.9359, 13.2558, 1.1967]

# --- Sentinel-1 collection ---
S1_COLLECTION = 'COPERNICUS/S1_GRD'
POLARISATIONS = ['VV', 'VH']
INSTRUMENT_MODE = 'IW'
ORBIT_PASS = 'DESCENDING'  # change to 'ASCENDING' or remove filter if scene count is low

# --- Temporal ---
BASELINE_START = '2021-01-01'
BASELINE_END   = '2023-06-30'
MONITOR_START  = '2024-01-01'
MONITOR_END    = '2024-12-31'

# --- Change detection ---
CHANGE_THRESHOLD_DB = 0.64   # Carstairs et al. 2022
MIN_SCENES_BASELINE = 40
MIN_SCENES_MONITOR  = 5

# --- Export ---
EXPORT_FOLDER = 'belinga_sar_exports'
EXPORT_SCALE  = 10           # metres
EXPORT_CRS    = 'EPSG:32633' # UTM Zone 33N