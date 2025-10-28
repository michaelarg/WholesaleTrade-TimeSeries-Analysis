from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- PROJECT CONFIGURATION: USE ABSOLUTE PATHS ---
# Ensures the script works regardless of where it’s run from
PROJECT_ROOT = Path(__file__).parent.parent

# Define key directories
RAW_DATA_PATH = PROJECT_ROOT / 'data' / 'raw'
PROCESSED_DATA_PATH = PROJECT_ROOT / 'data' / 'processed'
CHARTS_PATH = PROJECT_ROOT / 'charts'

# --- Input Files ---
SALES_FILE = RAW_DATA_PATH / "Sales_Adjusted.csv"
INVENTORIES_FILE = RAW_DATA_PATH / "Inventories_Adjusted.csv"

# --- Output File ---
MERGED_OUTPUT_FILE = PROCESSED_DATA_PATH / 'merged_wts_data_nominal.csv'


def load_and_clean_data(file_path: Path, column_name: str) -> pd.DataFrame:
    """
    Loads raw U.S. Census Bureau CSV files, cleans the header,
    and extracts the total series for NAICS 42 (Total Merchant Wholesalers).
    """
    try:
        df = pd.read_csv(file_path, header=16)
    except FileNotFoundError:
        print(f"❌ Error: File not found at {file_path}")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        print(f"❌ Error: File at {file_path} is empty or invalid.")
        return pd.DataFrame()

    # Rename first three columns to standard names
    df = df.rename(columns={
        'Month': 'Month',
        'Year': 'Year',
        '42': column_name
    })

    # Keep only necessary columns
    df_clean = df[['Month', 'Year', column_name]].copy()

    # Remove footnotes (like 'p', 'r') from Month and clean whitespace
    df_clean['Month'] = (
        df_clean['Month']
        .astype(str)
        .str.replace(r'[^\w\s]', '', regex=True)
        .str.replace(r'\s+', ' ', regex=True)
        .str.strip()
    )

    # Fix Year column: remove decimals and ensure it's an integer string
    df_clean['Year'] = df_clean['Year'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

    # Create date string and convert to datetime
    df_clean['Date_Str'] = df_clean['Month'] + ' ' + df_clean['Year']
    df_clean['Date'] = pd.to_datetime(df_clean['Date_Str'], format='%B %Y', errors='coerce')
    df_clean.dropna(subset=['Date'], inplace=True)

    # Convert to numeric, remove commas in values
    df_clean[column_name] = pd.to_numeric(
        df_clean[column_name].astype(str).str.replace(',', ''), errors='coerce'
    )
    df_clean.dropna(subset=[column_name], inplace=True)

    # Keep only Date and the main column
    df_clean = df_clean[['Date', column_name]].sort_values('Date').reset_index(drop=True)

    print(f"✅ Loaded {len(df_clean)} rows from {file_path.name}")
    return df_clean




# --- 2. MAIN EXECUTION AND PROCESSING LOGIC ---
def run_data_processing() -> pd.DataFrame | None:
    """
    Loads both datasets, merges them by Date,
    computes key metrics, and saves processed output.
    """

    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    os.makedirs(CHARTS_PATH, exist_ok=True)

    print("--- Starting Data Processing and Metric Calculation ---")

    sales_df = load_and_clean_data(SALES_FILE, 'Sales_Total_Nominal')
    inventories_df = load_and_clean_data(INVENTORIES_FILE, 'Inventories_Total_Nominal')

    if sales_df.empty:
        print("⚠️ Sales DataFrame is empty — check Sales_Adjusted.csv header or structure.")
    if inventories_df.empty:
        print("⚠️ Inventories DataFrame is empty — check Inventories_Adjusted.csv header or structure.")

    if sales_df.empty or inventories_df.empty:
        print("❌ Analysis failed: One or both DataFrames are empty. Aborting.")
        return None

    # Merge both DataFrames by Date
    merged_df = pd.merge(sales_df, inventories_df, on='Date', how='inner')

    # --- Key Metric Calculations ---
    merged_df['Inventories_to_Sales_Ratio_Nominal'] = (
        merged_df['Inventories_Total_Nominal'] / merged_df['Sales_Total_Nominal']
    )

    merged_df['Sales_YoY_Growth'] = merged_df['Sales_Total_Nominal'].pct_change(periods=12) * 100

    merged_df.to_csv(MERGED_OUTPUT_FILE, index=False)
    print(f"✅ Success: Processed data saved to {MERGED_OUTPUT_FILE}")

    return merged_df


# --- 3. CHART GENERATION (VERIFICATION) ---
def generate_charts(df: pd.DataFrame):
    """Generates 4 verification charts using Matplotlib."""

    print("📈 Generating verification charts...")

    # 1. Nominal Sales Trend
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Sales_Total_Nominal'], color='#1f77b4', label='Total Sales')
    plt.title('Nominal Sales Trend of U.S. Merchant Wholesalers (Seasonally Adjusted)', fontsize=16)
    plt.ylabel('Sales (Millions of Dollars)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.savefig(CHARTS_PATH / '1_nominal_sales_trend.png')
    plt.close()

    # 2. Inventory-to-Sales Ratio Trend
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Inventories_to_Sales_Ratio_Nominal'], color='#d62728', label='I/S Ratio')
    avg_ratio = df['Inventories_to_Sales_Ratio_Nominal'].mean()
    plt.axhline(avg_ratio, color='gray', linestyle='--', label=f'Average ({avg_ratio:.2f})')
    plt.title('Inventory-to-Sales Ratio Trend (Key Health Metric)', fontsize=16)
    plt.ylabel('Ratio (Inventories / Sales)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(CHARTS_PATH / '2_nominal_is_ratio_trend.png')
    plt.close()

    # 3. YoY Sales Growth
    plt.figure(figsize=(12, 6))
    growth_df = df.dropna(subset=['Sales_YoY_Growth'])
    plt.plot(growth_df['Date'], growth_df['Sales_YoY_Growth'], color='#2ca02c', label='YoY Sales Growth')
    plt.axhline(0, color='red', linestyle='-', linewidth=1)
    plt.title('Year-over-Year Sales Growth (Recession Indicator)', fontsize=16)
    plt.ylabel('Growth (%)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(CHARTS_PATH / '3_yoy_sales_growth.png')
    plt.close()

    # 4. Sales vs. Inventories
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Sales_Total_Nominal'], color='#1f77b4', label='Sales')
    plt.plot(df['Date'], df['Inventories_Total_Nominal'], color='#ff7f0e', label='Inventories')
    plt.title('Sales vs. Inventories (Comparative Levels)', fontsize=16)
    plt.ylabel('Millions of Dollars')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(CHARTS_PATH / '4_sales_vs_inventories_levels.png')
    plt.close()

    print("✅ Charts successfully saved to charts/ directory.")


# --- 4. SCRIPT ENTRY POINT ---
if __name__ == "__main__":
    final_data_df = run_data_processing()
    if final_data_df is not None and not final_data_df.empty:
        generate_charts(final_data_df)
        print("\n--- Project Execution Complete ---")
        print("Next Step: Load 'data/processed/merged_wts_data_nominal.csv' into Tableau.")
