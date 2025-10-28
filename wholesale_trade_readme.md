# 📊 WholesaleTrade_TimeSeries_Analysis
## U.S. Wholesale Trade Sales & Inventory Health

---

## 📑 Table of Contents
1. [🌟 Project Abstract](#-project-abstract)
2. [❓ Problem Statement: Diagnostic Analysis of Wholesale Trade Health](#-problem-statement-diagnostic-analysis-of-wholesale-trade-health)
3. [🌟 Significance: Data Objectives and Utility](#-significance-data-objectives-and-utility)
4. [🔬 Configuration and Methodology](#-configuration-and-methodology)
    - [3.1 Data Loading and Cleaning Pipeline](#31-data-loading-and-cleaning-pipeline)
    - [3.2 Core Processing and Metric Calculation](#32-core-processing-and-metric-calculation)
    - [3.3 Chart Generation (Verification)](#33-chart-generation-verification)
5. [📈 Tableau Dashboard Documentation](#-tableau-dashboard-documentation)
    - [4.1 Chart 1: Nominal Sales Trend (Context)](#41-chart-1-nominal-sales-trend-context)
    - [4.2 Chart 2: Inventory-to-Sales Ratio (Inventory Risk)](#42-chart-2-inventory-to-sales-ratio-inventory-risk)
    - [4.3 Chart 3: Year-over-Year Sales Growth (Sales Momentum)](#43-chart-3-year-over-year-sales-growth-sales-momentum)
    - [4.4 Chart 4: Sales vs Inventories Levels (Comparative Validation)](#44-chart-4-sales-vs-inventories-levels-comparative-validation)
6. [🎯 Key Analytical Findings](#-key-analytical-findings)

---

## 🌟 Project Abstract
This repository contains an automated diagnostic analysis of the U.S. Wholesale Trade Sector (NAICS 42) health, translating raw U.S. Census Bureau time series data (1992–Present) into actionable economic signals. The project utilizes a reproducible Python script to clean and process data, calculate two crucial metrics—the Inventory-to-Sales (I/S) Ratio and Year-over-Year (YoY) Sales Growth—and outputs a final dataset for immediate visualization.

The resulting Tableau dashboard provides clear, objective insights, allowing users to instantly assess **inventory risk** (by comparing the I/S Ratio to its historical average) and **market momentum** (by tracking YoY growth against the 0% contraction baseline).

---

## ❓ Problem Statement: Diagnostic Analysis of Wholesale Trade Health
This project addresses the need for a rapid, objective assessment of the wholesale sector's health. The Python analysis pipeline transforms complex, raw government data into four simple, easy-to-read charts that provide immediate clarity on the sector's current financial and supply/demand dynamics.

The analysis is structured to answer two critical, practical questions using the full historical dataset (1992–Present):

### A. Sales Momentum Assessment (YoY Growth)
- **Question:** What is the current velocity of the wholesale market—is it expanding, decelerating, or actively contracting?  
- **Metric:** *Year-over-Year (YoY) Sales Growth* – the definitive measure of momentum, using the 0% baseline as the non-negotiable signal for market contraction.

### B. Inventory Risk Assessment (I/S Ratio)
- **Question:** Is the supply chain currently balanced, or are wholesalers holding an unsustainable volume of stock relative to consumption?  
- **Metric:** *Inventory-to-Sales (I/S) Ratio* – diagnoses supply-demand health by comparing the current ratio against its long-term historical average, establishing a clear benchmark for risk.

---

## 🌟 Significance: Data Objectives and Utility
The significance of this project lies in its ability to translate raw government data into clear, objective signals, bypassing subjective interpretation of large datasets. The analysis serves three primary utility goals:

### Quantify Inventory Balance (Risk Indicator)
Determines if the sector is **overstocked** (signaling future markdowns) or **understocked** (signaling potentially lost revenue) by measuring the I/S Ratio against its established historical average.

### Identify Market Contraction (Recession Indicator)
Calculates and charts the YoY Sales Growth to precisely locate drops below the 0% baseline, providing an objective, data-driven signal of market contraction necessary for economic forecasting.

### Establish Data Context (Validation)
Provides long-term context (Nominal Sales Trend) and validates the I/S Ratio by visualizing absolute dollar levels of Sales and Inventories to confirm any supply-demand disconnect.

---

## 🔬 Configuration and Methodology
This project processes monthly time series data for Total Merchant Wholesalers (NAICS 42), specifically the Seasonally Adjusted Nominal Estimates in millions of dollars, sourced from the [U.S. Census Bureau](https://www.census.gov/wholesale/current/index.html).

### Data Acquisition and Preparation
- **Original Data Format:** Multi-sheet Excel file (.xlsx).  
- **Conversion:** Extracted, cleaned, and saved as `.csv` (Sales_Adjusted.csv and Inventories_Adjusted.csv).  
- **Configuration:** Uses `pathlib` and `PROJECT_ROOT = Path(__file__).parent.parent` for platform-independent execution.

### Methodology
Executed using `analysis_script.py`, structured into three core components:  
**Data Loading/Cleaning**, **Core Processing**, and **Chart Generation**.

---

### 3.1 Data Loading and Cleaning Pipeline
The `load_and_clean_data` function standardizes and sanitizes Census data.

| **Code Feature** | **Implementation** | **Explanation** |
|------------------|--------------------|-----------------|
| Header Handling | `pd.read_csv(file_path, header=16)` | Skips the 16-line metadata, reading correct headers. |
| Footnote Stripping | `.str.replace(r'[^\w\s]', '', regex=True)` | Removes statistical symbols like *p* or *r*. |
| Date Parsing | `pd.to_datetime(..., format='%B %Y', errors='coerce')` | Ensures consistent and accurate date conversion. |
| Value Conversion | `pd.to_numeric(..., errors='coerce')` | Cleans commas and ensures numeric type reliability. |

---

### 3.2 Core Processing and Metric Calculation
The `run_data_processing` function merges Sales and Inventories data and calculates economic indicators.

| **Metric** | **Formula (Plain Text)** | **Python Implementation** | **Economic Interpretation** |
|-------------|--------------------------|----------------------------|------------------------------|
| I/S Ratio | (Inventories_Nominal) / (Sales_Nominal) | `merged_df['Inventories_Total_Nominal'] / merged_df['Sales_Total_Nominal']` | Indicates months to clear stock; higher = supply outpacing demand. |
| YoY Sales Growth | ((Sales_Current - Sales_12_Months_Ago) / Sales_12_Months_Ago) * 100 | `merged_df['Sales_Total_Nominal'].pct_change(periods=12) * 100` | Shows annualized growth rate; adjusts for seasonality. |

---

### 3.3 Chart Generation (Verification)
`generate_charts` uses Matplotlib to produce verification charts for validation.

**Example: YoY Growth Plot**
```python
plt.plot(growth_df['Date'], growth_df['Sales_YoY_Growth'], color='#2ca02c', label='YoY Sales Growth')
plt.axhline(0, color='red', linestyle='-', linewidth=1)
```
- The red **0% baseline** serves as the clear contraction threshold.  
- Any data below this line signals economic stress.

---

## 📈 Tableau Dashboard Documentation
The final output (`merged_wts_data_nominal.csv`) is visualized in Tableau through four analytical charts.

### 4.1 Chart 1: Nominal Sales Trend (Context)
- **Purpose:** Establishes macroeconomic context and confirms long-term growth.
- **Feature:** Upward slope shows compounding inflation and real growth.

### 4.2 Chart 2: Inventory-to-Sales Ratio (Inventory Risk)
- **Purpose:** Diagnoses supply-demand balance.  
- **Feature:** Average reference line acts as a risk benchmark.

### 4.3 Chart 3: Year-over-Year Sales Growth (Sales Momentum)
- **Purpose:** Acts as a reliable expansion/contraction indicator.  
- **Feature:** The red 0% line is the definitive signal for recessionary stress.

### 4.4 Chart 4: Sales vs Inventories Levels (Comparative Validation)
- **Purpose:** Validates signals generated by the I/S Ratio.  
- **Feature:** Divergence of inventory from sales indicates supply-demand disconnect.

---

## 🎯 Key Analytical Findings
### A. Sales Momentum Assessment (YoY Growth)
- **Contraction Signal:** When YoY Growth < 0%, the market is contracting.  
- **Historical Validation:** Matches the 2008 and 2020 economic downturns.

### B. Inventory Risk Assessment (I/S Ratio)
- **Overstocked (High Risk):** Ratio above average → excess inventory buildup.  
- **Understocked (Low Risk):** Ratio below average → demand outpaces supply.

### C. Contextual Validation
- **Supply/Demand Disconnect:** Confirmed when inventories grow faster than sales.  
- **Market Context:** Despite volatility, long-term sales growth remains strong.

---
