WholesaleTrade_TimeSeries_Analysis

U.S. Wholesale Trade Sales & Inventory Health
This project provides a direct, diagnostic time series analysis of the U.S. wholesale trade sector (NAICS 42). The goal is to quickly assess market momentum and inventory risk using fundamental economic indicators derived from seasonally adjusted, current-dollar data.
________________________________________
1.  Problem Statement: Diagnostic Analysis of Wholesale Trade Health
This analysis translates raw U.S. Census Bureau data into four easy-to-read charts to provide immediate clarity on the sector's health. The analysis is built to answer two practical questions using the available data (1992–Present):
A. Sales Momentum Assessment (YoY Growth)
•	Question: Is the wholesale market currently expanding or shrinking?
•	Metric: Year-over-Year (YoY) Sales Growth, using the 0% baseline as the signal for contraction.
B. Inventory Risk Assessment (I/S Ratio)
•	Question: Are wholesalers holding too much stock relative to sales (overstocked) or too little (understocked)?
•	Metric: Inventory-to-Sales (I/S) Ratio, comparing the current ratio against its historical average.
________________________________________
2. Significance: Data Objectives and Utility
This project's significance lies in its ability to generate immediate, objective insights by translating raw government data into actionable economic signals. The analysis is designed to accomplish the following utility goals:
•	Quantify Inventory Balance: Determine if the sector is currently overstocked or understocked by measuring the Inventory-to-Sales (I/S) Ratio against its historical average. This objective directly informs procurement decisions.
•	Identify Market Contraction: Identify periods of expansion and precisely locate drops below the 0% baseline using the Year-over-Year (YoY) Sales Growth. This provides an objective signal of market contraction for forecasting.
•	Establish Data Context: Provide the long-term context (Nominal Sales Trend) and validate the key I/S Ratio by charting the underlying absolute dollar levels of Sales and Inventories.
________________________________________
3. Configuration and Methodology
This project utilizes monthly time series data for Total Merchant Wholesalers (NAICS 42), specifically the Seasonally Adjusted Nominal Estimates, accessed from the U.S. Census Bureau. The data is public and can be accessed from https://www.census.gov/wholesale/current/index.html.
Data Acquisition and Preparation
•	Original Data Format: The raw data was sourced as a single Excel file (.xlsx) containing multiple sheets.
•	Conversion: The necessary sales and inventory sheets were extracted and saved into the required Comma Separated Value (.csv) format (Sales_Adjusted.csv and Inventories_Adjusted.csv) for standardized processing.
•	Configuration: The script utilizes the pathlib module to define project directories (data/raw, data/processed, charts) using absolute paths. This ensures the script runs correctly regardless of the user's current working directory.
Methodology
The analysis is executed using a structured Python script (analysis_script.py) designed for reliability and reproducibility.
3.1. Project Configuration and Path Management
This section ensures the script can consistently locate input files and save output files by defining absolute paths relative to the project root.
Code Section: Imports and Root Definition
Python
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import os

# Ensures the script works regardless of where it’s run from
PROJECT_ROOT = Path(__file__).parent.parent
Explanation:
•	Imports necessary libraries for file handling (Path), data manipulation (pandas), plotting (matplotlib.pyplot), and directory creation (os).
•	PROJECT_ROOT is defined by navigating two levels up from the script's location, establishing the top-level directory as the reference point for all file operations.
Code Section: Path Definitions
Python
# Define key directories
RAW_DATA_PATH = PROJECT_ROOT / 'data' / 'raw'
PROCESSED_DATA_PATH = PROJECT_ROOT / 'data' / 'processed'
CHARTS_PATH = PROJECT_ROOT / 'charts'

# Input Files
SALES_FILE = RAW_DATA_PATH / "Sales_Adjusted.csv"
INVENTORIES_FILE = RAW_DATA_PATH / "Inventories_Adjusted.csv"
Explanation:
•	The pathlib module is used to construct platform-independent paths to the raw data folder, the processed output folder, and the charts folder.
•	Input file paths are defined based on their location within the data/raw folder.
________________________________________
3.2. Data Loading and Cleaning Pipeline
The load_and_clean_data function standardizes the raw data, handling header information, data types, and footnotes.
Code Section: Data Loading and Header Correction
Python
def load_and_clean_data(file_path: Path, column_name: str) -> pd.DataFrame:
    # Loads raw U.S. Census Bureau CSV files...
    try:
        df = pd.read_csv(file_path, header=16)
    # ... error handling omitted for brevity ...
Explanation:
•	Reads the CSV file using pd.read_csv.
•	The crucial parameter header=16 is used because the first 16 rows of the Census data files contain metadata, and the actual column headers (Month, Year, NAICS Code) start on line 17.
Code Section: Column Selection and Naming
Python
    # Rename first three columns to standard names
    df = df.rename(columns={
        'Month': 'Month',
        'Year': 'Year',
        '42': column_name
    })
    # Keep only necessary columns
    df_clean = df[['Month', 'Year', column_name]].copy()
Explanation:
•	Renames the column corresponding to the total wholesale trade (NAICS code '42') to a descriptive name (e.g., Sales_Total_Nominal).
•	Drops all irrelevant columns, retaining only the date components and the required value column.
Code Section: Date and Value Cleaning
Python
    # Remove footnotes (like 'p', 'r') from Month and clean whitespace
    df_clean['Month'] = (
        df_clean['Month']
        .astype(str)
        .str.replace(r'[^\w\s]', '', regex=True)
        .str.strip()
    )
    # Convert to numeric, remove commas in values
    df_clean[column_name] = pd.to_numeric(
        df_clean[column_name].astype(str).str.replace(',', ''), errors='coerce'
    )
Explanation:
•	Footnote Removal: Uses string methods and regular expressions (.str.replace(...)) to strip statistical footnotes (like 'p' for preliminary) from the Month column, ensuring clean date parsing.
•	Value Cleaning: Removes commas from the number strings and converts the entire column to a reliable numeric (float) type using pd.to_numeric.
Code Section: Date Conversion
Python
    # Create date string and convert to datetime
    df_clean['Date_Str'] = df_clean['Month'] + ' ' + df_clean['Year']
    df_clean['Date'] = pd.to_datetime(df_clean['Date_Str'], format='%B %Y', errors='coerce')
    df_clean.dropna(subset=['Date'], inplace=True)
Explanation:
•	Combines the cleaned Month and Year strings into a full date string.
•	Uses pd.to_datetime with the specific format '%B %Y' to reliably parse the dates into datetime objects. Rows that could not be parsed are dropped (.dropna).
________________________________________
3.3. Core Processing and Metric Calculation (run_data_processing)
This function merges the two datasets and computes the final economic indicators.
Code Section: Data Merging
Python
    # Merge both DataFrames by Date
    merged_df = pd.merge(sales_df, inventories_df, on='Date', how='inner')
Explanation:
•	Combines the cleaned Sales and Inventories DataFrames.
•	Uses an inner join (how='inner') on the common Date column to ensure the final dataset only contains time periods where both sales and inventory data are present.
Code Section: Inventory-to-Sales (I/S) Ratio Calculation
Python
    # Key Metric Calculations
    merged_df['Inventories_to_Sales_Ratio_Nominal'] = (
        merged_df['Inventories_Total_Nominal'] / merged_df['Sales_Total_Nominal']
    )
Explanation:
•	Calculates the primary market health metric by dividing the nominal Inventories by the nominal Sales for each month.
•	Formula: 
$$\text{I/S Ratio} = \frac{\text{Inventories}_{\text{Nominal}}}{\text{Sales}_{\text{Nominal}}}$$
Code Section: Year-over-Year (YoY) Sales Growth Calculation
Python
    merged_df['Sales_YoY_Growth'] = merged_df['Sales_Total_Nominal'].pct_change(periods=12) * 100
Explanation:
•	Calculates the market momentum metric.
•	The .pct_change(periods=12) function computes the percentage difference between the current month's sales and sales from 12 months prior. The result is multiplied by 100 for a percentage value.
•	Formula: 
$$\text{YoY Growth} = \frac{\text{Sales}_t - \text{Sales}_{t-12}}{\text{Sales}_{t-12}} \times 100$$
________________________________________
3.4. Chart Generation (Verification)
The generate_charts function produces four verification charts using Matplotlib and saves them to the project's charts directory.
Code Section: Chart 3 Setup (YoY Growth Example)
Python
    # 3. YoY Sales Growth
    plt.figure(figsize=(12, 6))
    growth_df = df.dropna(subset=['Sales_YoY_Growth'])
    plt.plot(growth_df['Date'], growth_df['Sales_YoY_Growth'], color='#2ca02c', label='YoY Sales Growth')
    plt.axhline(0, color='red', linestyle='-', linewidth=1)
    # ... title, labels, savefig ...
Explanation:
•	Plots the Sales_YoY_Growth metric to assess market momentum.
•	A critical component is the plt.axhline(0, ...) command, which draws a horizontal line at 0%. This line serves as the visual signal for market expansion (above 0%) versus contraction (below 0%).

You're correct that tables can be difficult to manage in different environments. Here is the revised Tableau Dashboard Documentation formatted using clear headings and bullet points for easy copying into your README.md.

4. Tableau Dashboard Documentation
The final deliverable is a Tableau dashboard built from the processed file, merged_wts_data_nominal.csv. This section details the creation of the four visualizations that directly answer the core problem questions.

Data Connection
Source: merged_wts_data_nominal.csv

Key Fields: The following metrics are used for all visualizations:

Date (Used as a Continuous Date field)

Sales_YoY_Growth (Primary Measure for Momentum)

Inventories_to_Sales_Ratio_Nominal (Primary Measure for Risk)

4.1. Chart 1: Nominal Sales Trend (Context)
This chart establishes the overall size and long-term trend of the market.

Columns Shelf: Date (Set to Continuous Month).

Rows Shelf: Sales_Total_Nominal.

Analysis: Provides the absolute dollar value and confirms the long-term secular growth trend of the wholesale sector.

![alt text](1_nominal_sales_trend.png)

4.2. Chart 2: Inventory-to-Sales Ratio (Inventory Risk)
This chart is the key diagnostic for inventory balance.

Columns Shelf: Date (Set to Continuous Month).

Rows Shelf: Inventories_to_Sales_Ratio_Nominal.

Reference Line: Add an analytical reference line set to the Average of the ratio field.

Diagnostic Use: The line's position above the average signals a period of overstocked risk.

![alt text](2_nominal_is_ratio_trend.png)

4.3. Chart 3: Year-over-Year Sales Growth (Sales Momentum)
This chart is the key diagnostic for market expansion vs. contraction.

Columns Shelf: Date (Set to Continuous Month).

Rows Shelf: Sales_YoY_Growth.

Reference Line: Add an analytical reference line set to a Constant Value of 0.

Diagnostic Use: A data line below 0% immediately identifies periods of market contraction (recession).

![alt text](3_yoy_sales_growth.png)

4.4. Chart 4: Sales vs. Inventories Levels (Comparative Validation)
This chart validates the I/S ratio by showing the raw input data.

Columns Shelf: Date (Set to Continuous Month).

Rows Shelf: Measure Values.

Measure Filter: Filter to include only Sales_Total_Nominal and Inventories_Total_Nominal.

Diagnostic Use: Visually validates the I/S Ratio by showing when the absolute value of Inventories (Supply) grows faster than Sales (Demand).

![alt text](4_sales_vs_inventories_levels.png)

Yes, let's finalize your README.md with the most critical section: the Key Analytical Findings. This section synthesizes the results of your four charts to provide a direct answer to your problem statement.

5. Key Analytical Findings
The final analysis, derived from the four calculated metrics, provides a clear, objective assessment of the wholesale trade sector's health:

A. Sales Momentum Assessment (YoY Growth)
Contraction Signal: The Year-over-Year (YoY) Sales Growth (Chart 3) is the definitive signal for market momentum. Periods of market contraction (recessionary stress) are explicitly identified when the growth line drops below the 0% baseline (the red reference line).

Historical Validation: The chart accurately captures previous economic downturns (e.g., 2008-2009 and the 2020 pandemic shock) by showing rapid drops into negative territory. Monitoring the line's current position relative to zero provides immediate market intelligence on expansion or contraction.

B. Inventory Risk Assessment (I/S Ratio)
Risk Signal: The Inventory-to-Sales (I/S) Ratio (Chart 2) directly answers the inventory balance question. The ratio's position relative to the historical average (the dashed gray line) dictates the risk level:

Overstocked (High Risk): When the ratio line rises above the average, it signals that inventories are accumulating faster than sales, forecasting potential future price markdowns or production cuts.

Understocked (Low Risk/High Demand): When the ratio falls below the average, it signals strong demand outstripping supply, leading to potentially lost revenue opportunities.

C. Contextual Validation
Supply/Demand Disconnect (Chart 4): The Sales vs. Inventories Levels (Chart 4) visually confirms the I/S Ratio signals. Every major peak in the I/S Ratio is visibly preceded by the Inventories line (Orange) growing at a steeper rate than the Sales line (Blue), validating the underlying buildup of unsold stock.

Market Context (Chart 1): The Nominal Sales Trend (Chart 1) provides crucial context, confirming that, despite cyclical volatility, the sector maintains a long-term secular growth trajectory in absolute dollar terms.