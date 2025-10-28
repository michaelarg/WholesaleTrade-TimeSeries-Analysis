# 📊 WholesaleTrade_TimeSeries_Analysis
## U.S. Wholesale Trade Sales & Inventory Health

### 🌟 Project Abstract
This repository contains an automated diagnostic analysis of the U.S. Wholesale Trade Sector (NAICS 42) health, translating raw U.S. Census Bureau time series data (1992–Present) into actionable economic signals. The project utilizes a reproducible Python script to clean and process data, calculate two crucial metrics—the Inventory-to-Sales (I/S) Ratio and Year-over-Year (YoY) Sales Growth—and outputs a final dataset for immediate visualization. The resulting Tableau dashboard provides clear, objective insights, allowing users to instantly assess inventory risk (by comparing the I/S Ratio to its historical average) and market momentum (by tracking YoY growth against the 0% contraction baseline).

---

## 1. ❓ Problem Statement: Diagnostic Analysis of Wholesale Trade Health
This analysis translates raw U.S. Census Bureau data into four easy-to-read charts to provide immediate clarity on the sector's health. The analysis is built to answer two practical questions using the available data (1992–Present):

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
**Code Section: Imports and Root Definition**
```python
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import os

# Ensures the script works regardless of where it’s run from
PROJECT_ROOT = Path(__file__).parent.parent

Code Section: Path Definitions
# Define key directories
RAW_DATA_PATH = PROJECT_ROOT / 'data' / 'raw'
PROCESSED_DATA_PATH = PROJECT_ROOT / 'data' / 'processed'
CHARTS_PATH = PROJECT_ROOT / 'charts'

# Input Files
SALES_FILE = RAW_DATA_PATH / "Sales_Adjusted.csv"
INVENTORIES_FILE = RAW_DATA_PATH / "Inventories_Adjusted.csv"
