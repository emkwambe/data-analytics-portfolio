# 📊 Data Analytics Portfolio

> Demonstrating analytics engineering, statistical modeling, and business intelligence capabilities through real-world financial services projects.

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://python.org)
[![dbt](https://img.shields.io/badge/dbt-1.11+-FF694B?logo=dbt)](https://getdbt.com)
[![SQL](https://img.shields.io/badge/SQL-Advanced-green)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Author:** Eddy Mkwambe  
**Focus:** Financial Services Analytics | Consumer Behavior | Risk Modeling

---

## 🎯 Portfolio Overview

This portfolio showcases **4 end-to-end analytics projects** relevant to fintech, payments, and financial services industries. Each project demonstrates the full analytics lifecycle: data acquisition → cleaning → analysis → modeling → visualization → insights.

![Executive Summary](visualizations/viz_executive_summary.png)

---

## 📁 Projects

### 1️⃣ [Subscription Fatigue Index](projects/01-subscription-fatigue/)

**Question:** At what point does subscription saturation predict financial stress?

| Metric | Value |
|--------|-------|
| Data Source | BLS Consumer Expenditure Survey |
| Sample Size | 10,000+ households |
| Key Finding | **12.8%** subscription-to-income threshold predicts financial distress |

**Skills:** Consumer behavior analysis, threshold modeling, logistic regression

[📂 View Project →](projects/01-subscription-fatigue/)

---

### 2️⃣ [Financial Literacy-Debt Nexus](projects/02-financial-literacy/)

**Question:** Which *specific* financial literacy gaps most predict problematic debt?

| Metric | Value |
|--------|-------|
| Data Source | FINRA NFCS 2024 (25,000+ respondents) |
| Key Finding | **Compound interest** knowledge gap has 2.3x higher debt risk |
| Model Accuracy | 73.2% |

**Skills:** Survey analysis, feature importance, predictive modeling, heatmap visualization

![Risk Ratio Analysis](visualizations/viz_risk_ratio_chart.png)

[📂 View Project →](projects/02-financial-literacy/)

---

### 3️⃣ [Small Business Payment Velocity Index](projects/03-payment-velocity/)

**Question:** Can B2B payment timing predict economic health 60-90 days ahead?

| Metric | Value |
|--------|-------|
| Data Source | Census Small Business Pulse Survey |
| Coverage | 50 largest MSAs |
| Key Finding | Payment velocity leads employment data by **67 days** |

**Skills:** Economic indicators, time series analysis, Granger causality, geospatial visualization

[📂 View Project →](projects/03-payment-velocity/)

---

### 4️⃣ [FinHealth Data Warehouse (dbt)](https://github.com/emkwambe/finhealth-warehouse-dbt)

**Question:** How do we build a production-grade analytics pipeline for financial health scoring?

| Metric | Value |
|--------|-------|
| Data Volume | 4,059,254 records |
| Models Built | 9 (staging → intermediate → marts) |
| Tests Passing | 6/6 ✅ |

**Skills:** dbt, dimensional modeling, data quality testing, SQL transformations

[📂 View Project →](https://github.com/emkwambe/finhealth-warehouse-dbt)

---

## 📊 Visualizations

### Intervention Priority Matrix
*Which financial literacy gaps should we address first?*

![Quadrant Priority](visualizations/viz_quadrant_priority.png)

### Risk Ratio by Knowledge Domain
*Relative risk of debt distress by knowledge gap*

![Risk Ratio](visualizations/viz_risk_ratio_chart.png)

---

## 🛠️ Technical Skills Demonstrated

| Category | Skills |
|----------|--------|
| **Languages** | Python, SQL |
| **Data Engineering** | dbt, dimensional modeling, ETL pipelines |
| **Analysis** | Pandas, NumPy, statistical testing |
| **Machine Learning** | Scikit-learn, logistic regression, feature importance |
| **Visualization** | Matplotlib, Seaborn, Plotly |
| **Databases** | DuckDB, PostgreSQL, BigQuery |
| **Version Control** | Git, GitHub |

---

## 📈 Business Impact Potential

Each project was designed with **actionable business applications**:

| Project | Business Application |
|---------|---------------------|
| Subscription Fatigue | Credit risk modeling, subscription management features |
| Financial Literacy | Targeted education programs, responsible lending |
| Payment Velocity | Economic forecasting, B2B credit decisions |
| FinHealth Warehouse | Customer segmentation, risk scoring |

---

## 🚀 Quick Start

### Clone the Repository
```bash
git clone https://github.com/emkwambe/data-analytics-portfolio.git
cd data-analytics-portfolio
```

### Set Up Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate
pip install -r requirements.txt
```

### Run Any Project
```bash
cd projects/02-financial-literacy
python complete_analysis.py
```

---

## 📋 Project Structure

```
data-analytics-portfolio/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── LICENSE
│
├── projects/
│   ├── 01-subscription-fatigue/
│   │   ├── README.md                   # Project documentation
│   │   ├── complete_analysis.py        # Full analysis script
│   │   ├── data/                       # Generated datasets
│   │   └── outputs/                    # Results & visualizations
│   │
│   ├── 02-financial-literacy/
│   │   ├── README.md
│   │   ├── complete_analysis.py
│   │   ├── create_visualizations.py
│   │   ├── data/
│   │   └── outputs/
│   │
│   └── 03-payment-velocity/
│       ├── README.md
│       ├── complete_analysis.py
│       ├── data/
│       └── outputs/
│
├── visualizations/                     # Key charts for portfolio
│   ├── viz_executive_summary.png
│   ├── viz_risk_ratio_chart.png
│   └── viz_quadrant_priority.png
│
└── docs/
    └── DATA_PROJECTS_MASTER_PLAN.md    # Detailed methodology
```

---

## 📚 Data Sources

All projects use **publicly available, verified datasets**:

| Dataset | Source | Projects |
|---------|--------|----------|
| FINRA NFCS 2024 | [finrafoundation.org](https://finrafoundation.org/nfcs-data-and-downloads) | #2 |
| BLS Consumer Expenditure | [bls.gov](https://www.bls.gov/cex/pumd_data.htm) | #1 |
| Census Small Business Pulse | [census.gov](https://portal.census.gov/pulse/data/) | #3 |
| CFPB Complaints | [consumerfinance.gov](https://www.consumerfinance.gov/data-research/consumer-complaints/) | #1, #2 |

---

## 🎓 Key Learnings

Through these projects, I developed expertise in:

1. **Translating business questions into analytical frameworks**
2. **Working with large-scale survey data (25K+ respondents)**
3. **Building interpretable predictive models**
4. **Creating executive-ready visualizations**
5. **Designing dimensional data models with dbt**
6. **Communicating technical findings to business audiences**

---

## 📫 Contact

**Eddy Mkwambe**  
Data Analyst | Analytics Engineer

- 🔗 GitHub: [@emkwambe](https://github.com/emkwambe)
- 💼 LinkedIn: [Connect with me](https://linkedin.com/in/your-profile)
- 📧 Email: your.email@example.com

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Built with 💡 data curiosity and ☕ determination*
