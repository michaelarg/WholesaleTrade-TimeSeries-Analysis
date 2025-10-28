📊 WholesaleTrade_TimeSeries_Analysis


🌟 Project Abstract
This repository contains an automated diagnostic analysis of the U.S. Wholesale Trade Sector (NAICS 42) health, translating raw U.S. Census Bureau time series data (1992–Present) into actionable economic signals. The project utilizes a reproducible Python script to clean and process data, calculate two crucial metrics—the Inventory-to-Sales (I/S) Ratio and Year-over-Year (YoY) Sales Growth—and outputs a final dataset for immediate visualization. The resulting Tableau dashboard provides clear, objective insights, allowing users to instantly assess inventory risk (by comparing the I/S Ratio to its historical average) and market momentum (by tracking YoY growth against the 0% contraction baseline).

1. ❓oblem Statement: Diagnostic Analysis of Wholesale Trade Health
   This analysis translates raw U.S. Census Bureau data into four easy-to-read charts to provide immediate clarity on the sector's health. The analysis is built to answer two practical questions using the available data (1992–Present):

A. Sales Momentum Assessment (YoY Growth)
Question: Is the wholesale market currently expanding or shrinking?

Metric: Year-over-Year (YoY) Sales Growth, using the 0% baseline as the signal for contraction.

B. Inventory Risk Assessment (I/S Ratio)
Question: Are wholesalers holding too much stock relative to sales (overstocked) or too little (understocked)?

Metric: Inventory-to-Sales (I/S) Ratio, comparing the current ratio against its historical average.

2. 🌟 Significance: Data Objectives and Utility
   This project's significance lies in its ability to generate immediate, objective insights by translating raw government data into actionable economic signals. The analysis is designed to accomplish the following utility goals:

Quantify Inventory Balance: Determine if the sector is currently overstocked or understocked by measuring the Inventory-to-Sales (I/S) Ratio against its historical average.

Identify Market Contraction: Identify periods of expansion and precisely locate drops below the 0% baseline using the Year-over-Year (YoY) Sales Growth.

Establish Data Context: Provide the long-term context (Nominal Sales Trend) and validate the key I/S Ratio by charting the underlying absolute dollar levels of Sales and Inventories.

3. 🔬 Configuration and Methodology
   This project utilizes monthly time series data for Total Merchant Wholesalers (NAICS 42), specifically the Seasonally Adjusted Nominal Estimates, accessed from the U.S. Census Bureau. The data is public and can be accessed from https://www.census.gov/wholesale/current/index.html.

Data Acquisition and Preparation
Original Data Format: The raw data was sourced as a single Excel file (.xlsx).

Conversion: The necessary sales and inventory sheets were extracted and saved into the required Comma Separated Value (.csv) format (Sales_Adjusted.csv and Inventories_Adjusted.csv).

Configuration: The script utilizes the pathlib module to define project directories (data/raw, data/processed, charts) using absolute paths.

Methodology
The analysis is executed using a structured Python script (analysis_script.py) designed for reliability and reproducibility.

3.1. Project Configuration and Path Management
Code Section: Imports and Root Definition

Python

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import os

# Ensures the script works regardless of where it’s run from

PROJECT_ROOT = Path(file).parent.parent
Code Section: Path Definitions

Python

# Define key directories

RAW_DATA_PATH = PROJECT_ROOT / 'data' / 'raw'
PROCESSED_DATA_PATH = PROJECT_ROOT / 'data' / 'processed'
CHARTS_PATH = PROJECT_ROOT / 'charts'

# Input Files

SALES_FILE = RAW_DATA_PATH / "Sales_Adjusted.csv"
INVENTORIES_FILE = RAW_DATA_PATH / "Inventories_Adjusted.csv"
3.2. Data Loading and Cleaning Pipeline
Code Section: Data Loading and Header Correction

Python

def load_and_clean_data(file_path: Path, column_name: str) -> pd.DataFrame: # Loads raw U.S. Census Bureau CSV files...
try:
df = pd.read_csv(file_path, header=16) # ...
3.3. Core Processing and Metric Calculation
Code Section: Data Merging

Python

    # Merge both DataFrames by Date
    merged_df = pd.merge(sales_df, inventories_df, on='Date', how='inner')

Code Section: Inventory-to-Sales (I/S) Ratio Calculation

Python

    # Key Metric Calculations
    merged_df['Inventories_to_Sales_Ratio_Nominal'] = (
        merged_df['Inventories_Total_Nominal'] / merged_df['Sales_Total_Nominal']
    )

Explanation:

Formula: I/S Ratio = (Inventories_Nominal) / (Sales_Nominal)

Code Section: Year-over-Year (YoY) Sales Growth Calculation

Python

    merged_df['Sales_YoY_Growth'] = merged_df['Sales_Total_Nominal'].pct_change(periods=12) * 100

Explanation:

Formula: YoY Growth = ((Sales_Current - Sales_12_Months_Ago) / Sales_12_Months_Ago) \* 100

3.4. Chart Generation (Verification)
Code Section: Chart 3 Setup (YoY Growth Example)

Python

    # 3. YoY Sales Growth
    plt.figure(figsize=(12, 6))
    growth_df = df.dropna(subset=['Sales_YoY_Growth'])
    plt.plot(growth_df['Date'], growth_df['Sales_YoY_Growth'], color='#2ca02c', label='YoY Sales Growth')
    plt.axhline(0, color='red', linestyle='-', linewidth=1)
    # ... title, labels, savefig ...

4. 📈 Tableau Dashboard Documentation
   The final deliverable is a Tableau dashboard built from the processed file, merged_wts_data_nominal.csv.

4.1. Chart 1: Nominal Sales Trend (Context)
Analysis: Provides the absolute dollar value and confirms the long-term secular growth trend.

4.2. Chart 2: Inventory-to-Sales Ratio (Inventory Risk)
Reference Line: Analytical reference line set to the Average of the ratio field.

Diagnostic Use: Position above the average signals overstocked risk.

4.3. Chart 3: Year-over-Year Sales Growth (Sales Momentum)
Reference Line: Analytical reference line set to a Constant Value of 0.

Diagnostic Use: Line below 0% immediately identifies periods of market contraction (recession).

4.4. Chart 4: Sales vs. Inventories Levels (Comparative Validation)
Rows Shelf: Measure Values (Filtered to Sales and Inventories).

Diagnostic Use: Visually validates the I/S Ratio by showing when Inventories (Supply) grows faster than Sales (Demand).

5. 🎯 Key Analytical Findings
   The final analysis, derived from the four calculated metrics, provides a clear, objective assessment of the wholesale sector's health:

A. Sales Momentum Assessment (YoY Growth)
Contraction Signal: The Year-over-Year (YoY) Sales Growth (Chart 3) is the definitive signal for market momentum. Periods of market contraction are explicitly identified when the growth line drops below the 0% baseline.

B. Inventory Risk Assessment (I/S Ratio)
Risk Signal: The Inventory-to-Sales (I/S) Ratio (Chart 2) provides the risk level:

Overstocked (High Risk): When the ratio line rises above the historical average.

Understocked (Low Risk/High Demand): When the ratio falls below the historical average.

C. Contextual Validation
Supply/Demand Disconnect (Chart 4): The Sales vs. Inventories Levels chart visually confirms that every major I/S Ratio peak is preceded by the Inventories line growing at a steeper rate than the Sales line.

Market Context (Chart 1): Confirms that, despite cyclical volatility, the sector maintains a long-term secular growth trajectory in absolute dollar terms.
