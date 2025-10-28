# 🏪 WholesaleTrade_TimeSeries_Analysis

## 🌟 Project Abstract
This repository contains an automated diagnostic analysis of the **U.S. Wholesale Trade Sector (NAICS 42)** health, translating raw U.S. Census Bureau time series data (1992–Present) into actionable economic signals.  
The project utilizes a reproducible Python script to clean and process data, calculate two crucial metrics — the **Inventory-to-Sales (I/S) Ratio** and **Year-over-Year (YoY) Sales Growth** — and outputs a final dataset for immediate visualization.  

The resulting Tableau dashboard provides clear, objective insights, allowing users to instantly assess:
- **Inventory risk:** by comparing the I/S Ratio to its historical average.  
- **Market momentum:** by tracking YoY growth against the 0% contraction baseline.

---

## 📘 Table of Contents
1. [Introduction](#introduction)
2. [❓ Problem Statement: Diagnostic Analysis of Wholesale Trade Health](#-problem-statement-diagnostic-analysis-of-wholesale-trade-health)
3. [🌟 Significance: Data Objectives and Utility](#-significance-data-objectives-and-utility)
4. [🔬 Configuration and Methodology](#-configuration-and-methodology)
   - [3.1 Project Configuration and Path Management](#31-project-configuration-and-path-management)
   - [3.2 Data Loading and Cleaning Pipeline](#32-data-loading-and-cleaning-pipeline)
   - [3.3 Core Processing and Metric Calculation](#33-core-processing-and-metric-calculation)
   - [3.4 Chart Generation (Verification)](#34-chart-generation-verification)
5. [📈 Tableau Dashboard Documentation](#-tableau-dashboard-documentation)
6. [🎯 Key Analytical Findings](#-key-analytical-findings)

---

## Introduction
This project provides a direct, diagnostic time series analysis of the U.S. wholesale trade sector (NAICS 42). The goal is to quickly assess market momentum and inventory risk using fundamental economic indicators derived from seasonally adjusted, current-dollar data.

---

## 1. ❓ Problem Statement: Diagnostic Analysis of Wholesale Trade Health
This analysis translates raw U.S. Census Bureau data into four easy-to-read charts to provide immediate clarity on the sector's health.

### A. Sales Momentum Assessment (YoY Growth)
- **Question:** Is the wholesale market currently expanding or shrinking?  
- **Metric:** Year-over-Year (YoY) Sales Growth, using the 0% baseline as the signal for contraction.

### B. Inventory Risk Assessment (I/S Ratio)
- **Question:** Are wholesalers holding too much stock relative to sales (overstocked) or too little (understocked)?  
- **Metric:** Inventory-to-Sales (I/S) Ratio, comparing the current ratio against its historical average.

---

## 2. 🌟 Significance: Data Objectives and Utility
This project’s significance lies in its ability to generate immediate, objective insights by translating raw government data into actionable economic signals.

**Objectives:**
- Quantify **Inventory Balance** by measuring the I/S Ratio against its historical average.  
- Identify **Market Contraction** via YoY Sales Growth relative to the 0% baseline.  
- Establish **Data Context** by validating trends in Nominal Sales and Inventories.

---

## 3. 🔬 Configuration and Methodology
This project utilizes **monthly time series data** for Total Merchant Wholesalers (NAICS 42), sourced from the [U.S. Census Bureau](https://www.census.gov/wholesale/current/index.html).

### 3.1 Project Configuration and Path Management
```python
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import os

PROJECT_ROOT = Path(__file__).parent.parent
```
**Explanation:** Defines the root project directory and imports core libraries.

```python
RAW_DATA_PATH = PROJECT_ROOT / 'data' / 'raw'
PROCESSED_DATA_PATH = PROJECT_ROOT / 'data' / 'processed'
CHARTS_PATH = PROJECT_ROOT / 'charts'

SALES_FILE = RAW_DATA_PATH / "Sales_Adjusted.csv"
INVENTORIES_FILE = RAW_DATA_PATH / "Inventories_Adjusted.csv"
```
**Explanation:** Pathlib ensures cross-platform compatibility for data access.

---

### 3.2 Data Loading and Cleaning Pipeline
#### Load and Clean Data
```python
def load_and_clean_data(file_path: Path, column_name: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, header=16)
```
**Explanation:** Reads CSV files and skips the first 16 rows of metadata.

#### Column Selection
```python
df = df.rename(columns={'Month': 'Month', 'Year': 'Year', '42': column_name})
df_clean = df[['Month', 'Year', column_name]].copy()
```
**Explanation:** Renames columns for clarity and selects only necessary fields.

#### Cleaning
```python
df_clean['Month'] = (
    df_clean['Month']
    .astype(str)
    .str.replace(r'[^\w\s]', '', regex=True)
    .str.strip()
)
df_clean[column_name] = pd.to_numeric(df_clean[column_name].astype(str).str.replace(',', ''), errors='coerce')
```
**Explanation:** Removes footnotes, commas, and converts data to numeric types.

#### Date Conversion
```python
df_clean['Date_Str'] = df_clean['Month'] + ' ' + df_clean['Year']
df_clean['Date'] = pd.to_datetime(df_clean['Date_Str'], format='%B %Y', errors='coerce')
df_clean.dropna(subset=['Date'], inplace=True)
```

---

### 3.3 Core Processing and Metric Calculation
#### Merge Data
```python
merged_df = pd.merge(sales_df, inventories_df, on='Date', how='inner')
```
**Explanation:** Combines Sales and Inventory datasets.

#### Inventory-to-Sales Ratio
```python
merged_df['Inventories_to_Sales_Ratio_Nominal'] = merged_df['Inventories_Total_Nominal'] / merged_df['Sales_Total_Nominal']
```
**Formula:**
$$ I/S = rac{Inventories_{Nominal}}{Sales_{Nominal}} $$

#### YoY Sales Growth
```python
merged_df['Sales_YoY_Growth'] = merged_df['Sales_Total_Nominal'].pct_change(periods=12) * 100
```
**Formula:**
$$ YoY = rac{Sales_t - Sales_{t-12}}{Sales_{t-12}} 	imes 100 $$

---

### 3.4 Chart Generation (Verification)
```python
plt.figure(figsize=(12, 6))
growth_df = df.dropna(subset=['Sales_YoY_Growth'])
plt.plot(growth_df['Date'], growth_df['Sales_YoY_Growth'], color='#2ca02c', label='YoY Sales Growth')
plt.axhline(0, color='red', linestyle='-', linewidth=1)
```
**Explanation:** Generates diagnostic charts with Matplotlib.

---

## 4. 📈 Tableau Dashboard Documentation

**Source:** `merged_wts_data_nominal.csv`  

**Key Fields:**
- Date  
- Sales_YoY_Growth  
- Inventories_to_Sales_Ratio_Nominal

### 4.1 Nominal Sales Trend
Shows overall sector growth over time.

### 4.2 Inventory-to-Sales Ratio
Adds average reference line for overstock/understock risk.

### 4.3 YoY Sales Growth
Highlights periods below 0% as contraction signals.

### 4.4 Sales vs Inventories Levels
Compares trends in supply (Inventories) and demand (Sales).

---

## 5. 🎯 Key Analytical Findings

### A. Sales Momentum Assessment (YoY Growth)
- **Contraction Signal:** Market contraction occurs when YoY Growth falls below 0%.  
- **Historical Validation:** Captures major downturns such as 2008–09 and 2020.

### B. Inventory Risk Assessment (I/S Ratio)
- **Overstocked:** Ratio above historical average → oversupply risk.  
- **Understocked:** Ratio below average → unmet demand.

### C. Contextual Validation
- **Supply/Demand Disconnect:** Confirmed when inventory levels rise faster than sales.  
- **Long-Term Context:** Nominal Sales Trend confirms structural growth in the sector.
