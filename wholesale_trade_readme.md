# 📊 WholesaleTrade_TimeSeries_Analysis
## U.S. Wholesale Trade Sales & Inventory Health

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Tableau](https://img.shields.io/badge/Tableau-2024-blue?logo=tableau&logoColor=white)](https://www.tableau.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📑 Table of Contents
1. [Project Abstract](#-project-abstract)  
2. [Problem Statement](#-problem-statement-diagnostic-analysis-of-wholesale-trade-health)  
   - [Sales Momentum Assessment (YoY Growth)](#a-sales-momentum-assessment-yoy-growth)  
   - [Inventory Risk Assessment (I/S Ratio)](#b-inventory-risk-assessment-is-ratio)  
3. [Significance: Data Objectives and Utility](#-significance-data-objectives-and-utility)  
4. [Configuration and Methodology](#-configuration-and-methodology)  
   - [Project Configuration and Path Management](#31-project-configuration-and-path-management)  
   - [Data Loading and Cleaning Pipeline](#32-data-loading-and-cleaning-pipeline)  
   - [Core Processing and Metric Calculation](#33-core-processing-and-metric-calculation)  
   - [Chart Generation (Verification)](#34-chart-generation-verification)  
   - [Usage: Running the Analysis Script](#35-usage-running-the-analysis-script)  
5. [Tableau Dashboard Documentation](#-tableau-dashboard-documentation)  
   - [Chart 1: Nominal Sales Trend (Context)](#41-chart-1-nominal-sales-trend-context)  
   - [Chart 2: Inventory-to-Sales Ratio (Inventory Risk)](#42-chart-2-inventory-to-sales-ratio-inventory-risk)  
   - [Chart 3: Year-over-Year Sales Growth (Sales Momentum)](#43-chart-3-year-over-year-sales-growth-sales-momentum)  
   - [Chart 4: Sales vs. Inventories Levels (Comparative Validation)](#44-chart-4-sales-vs-inventories-levels-comparative-validation)  
6. [Key Analytical Findings](#-key-analytical-findings)  

---

## 🌟 Project Abstract
This repository contains an automated diagnostic analysis of the U.S. Wholesale Trade Sector (NAICS 42) health, translating raw U.S. Census Bureau time series data (1992–Present) into actionable economic signals. The project utilizes a reproducible Python script to clean and process data, calculate two crucial metrics—the **Inventory-to-Sales (I/S) Ratio** and **Year-over-Year (YoY) Sales Growth)**—and outputs a final dataset for immediate visualization. The resulting Tableau dashboard provides clear, objective insights, allowing users to instantly assess:

- **Inventory risk:** by comparing the I/S Ratio to its historical average.  
- **Market momentum:** by tracking YoY growth against the 0% contraction baseline.

---

## 1. ❓ Problem Statement: Diagnostic Analysis of Wholesale Trade Health
This analysis translates raw U.S. Census Bureau data into **four easy-to-read charts** to provide immediate clarity on the sector's health. The analysis is built to answer two practical questions using the available data (1992–Present):

### A. Sales Momentum Assessment (YoY Growth)
- **Question:** Is the wholesale market currently expanding or shrinking?  
- **Metric:** Year-over-Year (YoY) Sales Growth, using the 0% baseline as the signal for contraction.

### B. Inventory Risk Assessment (I/S Ratio)
- **Question:** Are wholesalers holding too much stock relative to sales (overstocked) or too little (understocked)?  
- **Metric:** Inventory-to-Sales (I/S) Ratio, comparing the current ratio against its historical average.

---

## 2. 🌟 Significance: Data Objectives and Utility
This project's significance lies in its ability to generate immediate, objective insights by translating raw government data into actionable economic signals. The analysis is designed to accomplish the following utility goals:

- **Quantify Inventory Balance:** Determine if the sector is currently overstocked or understocked by measuring the Inventory-to-Sales (I/S) Ratio against its historical average.  
- **Identify Market Contraction:** Identify periods of expansion and precisely locate drops below the 0% baseline using the Year-over-Year (YoY) Sales Growth.  
- **Establish Data Context:** Provide the long-term context (Nominal Sales Trend) and validate the key I/S Ratio by charting the underlying absolute dollar levels of Sales and Inventories.

---

## 3. 🔬 Configuration and Methodology
This project utilizes monthly time series data for Total Merchant Wholesalers (NAICS 42), specifically the Seasonally Adjusted Nominal Estimates, accessed from the U.S. Census Bureau. The data is public and can be accessed from [U.S. Census Bureau Wholesale Trade Data](https://www.census.gov/wholesale/current/index.html).

### Data Acquisition and Preparation
- **Original Data Format:** The raw data was sourced as a single Excel file (.xlsx).  
- **Conversion:** The necessary sales and inventory sheets were extracted and saved into the required Comma Separated Value (.csv) format (`Sales_Adjusted.csv` and `Inventories_Adjusted.csv`).  
- **Configuration:** The script utilizes the `pathlib` module to define project directories (`data/raw`, `data/processed`, `charts`) using absolute paths.

### Methodology
The analysis is executed using a structured Python script (`analysis_script.py`) designed for reliability and reproducibility.

---

### 3.1. Project Configuration and Path Management
<details>
<summary>Click to expand Python code: Imports and Root Definition</summary>

```python
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import os

# Ensures the script works regardless of where it’s run from
PROJECT_ROOT = Path(__file__).parent.parent
```
</details>

<details>
<summary>Click to expand Python code: Path Definitions</summary>

```python
# Define key directories
RAW_DATA_PATH = PROJECT_ROOT / 'data' / 'raw'
PROCESSED_DATA_PATH = PROJECT_ROOT / 'data' / 'processed'
CHARTS_PATH = PROJECT_ROOT / 'charts'

# Input Files
SALES_FILE = RAW_DATA_PATH / "Sales_Adjusted.csv"
INVENTORIES_FILE = RAW_DATA_PATH / "Inventories_Adjusted.csv"
```
</details>

---

### 3.2. Data Loading and Cleaning Pipeline
<details>
<summary>Click to expand Python code: Data Loading and Header Correction</summary>

```python
def load_and_clean_data(file_path: Path, column_name: str) -> pd.DataFrame:
    # Loads raw U.S. Census Bureau CSV files...
    try:
        df = pd.read_csv(file_path, header=16)
    # ...
```
</details>

---

### 3.3. Core Processing and Metric Calculation
<details>
<summary>Click to expand Python code: Data Merging</summary>

```python
# Merge both DataFrames by Date
merged_df = pd.merge(sales_df, inventories_df, on='Date', how='inner')
```
</details>

<details>
<summary>Click to expand Python code: Inventory-to-Sales (I/S) Ratio</summary>

```python
# Key Metric Calculations
merged_df['Inventories_to_Sales_Ratio_Nominal'] = (
    merged_df['Inventories_Total_Nominal'] / merged_df['Sales_Total_Nominal']
)
```
**Formula:** `I/S Ratio = (Inventories_Nominal) / (Sales_Nominal)`
</details>

<details>
<summary>Click to expand Python code: Year-over-Year (YoY) Sales Growth</summary>

```python
merged_df['Sales_YoY_Growth'] = merged_df['Sales_Total_Nominal'].pct_change(periods=12) * 100
```
**Formula:** `YoY Growth = ((Sales_Current - Sales_12_Months_Ago) / Sales_12_Months_Ago) * 100`
</details>

---

### 3.4. Chart Generation (Verification)
<details>
<summary>Click to expand Python code: Chart 3 Setup (YoY Growth Example)</summary>

```python
# 3. YoY Sales Growth
plt.figure(figsize=(12, 6))
growth_df = df.dropna(subset=['Sales_YoY_Growth'])
plt.plot(growth_df['Date'], growth_df['Sales_YoY_Growth'], color='#2ca02c', label='YoY Sales Growth')
plt.axhline(0, color='red', linestyle='-', linewidth=1)
# ... title, labels, savefig ...
```
</details>

---

### 3.5. ⚙️ Usage: Running the Analysis Script

Follow these steps to reproduce the analysis and generate charts:

#### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/WholesaleTrade_TimeSeries_Analysis.git
cd WholesaleTrade_TimeSeries_Analysis
```

#### 2. Install Required Python Packages
```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
**Dependencies include:**  
- `pandas`  
- `matplotlib`  
- `numpy`  

#### 3. Prepare Data Files
Ensure the raw CSV files are in the correct folder:
```
data/raw/Sales_Adjusted.csv
data/raw/Inventories_Adjusted.csv
```
The script automatically reads these files and outputs processed data to:
```
data/processed/merged_wts_data_nominal.csv
```

#### 4. Run the Analysis Script
```bash
python src/analysis_script.py
```
- Calculates key metrics: **I/S Ratio** and **YoY Sales Growth**.
- Generates verification charts in `charts/`.

#### 5. Review Output Charts
Saved in `charts/`:
1. `nominal_sales_trend.png`  
2. `inventories_to_sales_ratio.png` 

