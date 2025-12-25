# 📊 Project 2: Financial Literacy-Debt Nexus

## The Question
**Which *specific* financial literacy gaps most predict problematic debt?**

Moving beyond "literacy = good" to identify the exact knowledge gaps that drive financial distress — enabling targeted interventions.

---

## 🎯 Key Findings

| Metric | Finding |
|--------|---------|
| **Highest Risk Gap** | Compound Interest (2.3x debt risk) |
| **Second Highest** | Risk Diversification (1.9x debt risk) |
| **Model Accuracy** | 73.2% predicting debt distress |
| **Sample Size** | 25,000+ respondents (FINRA NFCS 2024) |

### Knowledge Gap Risk Ranking
| Rank | Knowledge Area | Risk Ratio | % Incorrect |
|------|---------------|------------|-------------|
| 1 | Compound Interest | 2.31x | 65% |
| 2 | Risk Diversification | 1.89x | 48% |
| 3 | Bond Prices | 1.76x | 72% |
| 4 | Inflation | 1.54x | 42% |
| 5 | Mortgage Terms | 1.43x | 25% |

---

## 📈 Business Relevance

**For Financial Services:**
- **Financial Inclusion**: Target education where it matters most
- **Risk Modeling**: Use literacy gaps as credit risk features
- **Product Design**: Simplify products in low-comprehension areas
- **Responsible Lending**: Identify customers needing additional support

**Directly relevant to Mastercard's financial inclusion initiatives.**

---

## 🔬 Methodology

### Data Source
- **FINRA National Financial Capability Study 2024**
- 25,000+ respondents across all 50 states
- 7 financial knowledge quiz questions
- Comprehensive debt and behavior variables

### The 7 Knowledge Questions

| Code | Topic | Question Theme |
|------|-------|----------------|
| M4 | Numeracy | Basic calculation (2% of 100) |
| M6 | Compound Interest | $100 at 2% for 5 years |
| M7 | Inflation | Purchasing power erosion |
| M8 | Bond Prices | Interest rate relationship |
| M9 | Mortgages | 15 vs 30 year total cost |
| M10 | Risk Diversification | Stock vs mutual fund risk |
| M31 | Investment Basics | Stock/company relationship |

### Analysis Pipeline

1. **Calculate Individual Knowledge Scores**
   ```python
   # Each question scored separately (not just total)
   literacy_scores = {
       'compound_interest': M6_correct,
       'inflation': M7_correct,
       'bond_prices': M8_correct,
       # ... etc
   }
   ```

2. **Build Debt Distress Index**
   ```python
   distress_score = (
       late_payment_flag * 0.3 +
       minimum_payment_only * 0.25 +
       spending_exceeds_income * 0.25 +
       no_emergency_fund * 0.2
   )
   ```

3. **Correlate Gaps with Distress**
   - Calculate risk ratios for each knowledge gap
   - Control for income, age, education

4. **Predictive Modeling**
   - Logistic regression with individual knowledge features
   - Feature importance reveals which gaps matter most

---

## 📊 Key Visualizations

### Risk Ratio Chart
![Risk Ratio](../../visualizations/viz_risk_ratio_chart.png)

*Compound interest knowledge gap shows 2.3x higher debt distress risk*

### Intervention Priority Matrix
![Priority Matrix](../../visualizations/viz_quadrant_priority.png)

*High impact + High prevalence gaps should be addressed first*

---

## 🛠️ Technical Implementation

### Files
- `complete_analysis.py` - Full analysis pipeline
- `financial_literacy_analysis.py` - Core calculations
- `create_visualizations.py` - Chart generation
- `dashboard.py` - Interactive Streamlit app
- `data/` - Analysis outputs (CSV)
- `outputs/` - Visualizations (PNG)

### Key Outputs
| File | Description |
|------|-------------|
| `analysis_knowledge_gaps.csv` | Gap prevalence by demographic |
| `analysis_intervention_priority.csv` | Ranked intervention targets |
| `analysis_model_coefficients.csv` | Regression coefficients |
| `analysis_state_level.csv` | State-by-state literacy scores |

### Run the Analysis
```bash
# Full analysis
python complete_analysis.py

# Generate visualizations
python create_visualizations.py

# Launch dashboard
streamlit run dashboard.py
```

---

## 💡 Insights & Recommendations

### For Education Programs
1. **Priority 1**: Compound interest education
   - 65% get this wrong
   - 2.3x debt risk when incorrect
   - Focus on "future value" concepts

2. **Priority 2**: Risk diversification
   - Critical for investment decisions
   - 48% don't understand portfolio risk reduction

### For Product Teams
- Simplify interest rate disclosures
- Add "what this means for you" calculators
- Visual risk explanations for investments

### For Risk Teams
- Add literacy proxies to credit models
- Consider "financial IQ" as soft factor
- Identify customers for additional support

---

## 📚 Data Dictionary

| Variable | Description |
|----------|-------------|
| `literacy_score` | Total correct (0-7) |
| `compound_interest_correct` | M6 question (1/0) |
| `debt_distress_index` | Composite distress score (0-1) |
| `risk_ratio` | Relative risk vs. knowledgeable group |
| `state_code` | Two-letter state identifier |

---

## 🔗 Related Projects

- [Subscription Fatigue](../01-subscription-fatigue/) - Consumer spending patterns
- [Payment Velocity Index](../03-payment-velocity/) - Economic indicators
- [FinHealth Warehouse](https://github.com/emkwambe/finhealth-warehouse-dbt) - dbt pipeline
