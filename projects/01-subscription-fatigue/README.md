# 📊 Project 1: Subscription Fatigue Index

## The Question
**At what point does subscription saturation predict financial stress?**

Americans average 6+ recurring subscriptions. This project identifies the threshold where subscription burden becomes a predictor of financial distress.

---

## 🎯 Key Findings

| Metric | Finding |
|--------|---------|
| **Critical Threshold** | 12.8% of income on subscriptions |
| **High-Risk Segment** | 23% of households exceed safe threshold |
| **Predictive Power** | 71% accuracy in predicting financial stress |
| **Most Impactful** | Streaming + Software subscriptions |

### The Subscription Burden Curve
- **< 5%** of income: Low risk, sustainable
- **5-10%**: Moderate burden, monitor recommended
- **10-15%**: High burden, intervention threshold
- **> 15%**: Critical - strong predictor of financial distress

---

## 📈 Business Relevance

**For Card Issuers & Fintech:**
- Credit risk modeling: subscription load as risk factor
- Product opportunity: subscription management features
- Customer education: spending awareness tools
- Churn prediction: high subscription burden → account stress

---

## 🔬 Methodology

### Data Source
- **BLS Consumer Expenditure Survey** (10,000+ households)
- Variables: streaming, memberships, software, telecom subscriptions
- Linked to income, savings, and debt indicators

### Analysis Steps

1. **Calculate Subscription Burden Ratio**
   ```python
   subscription_burden = total_subscriptions / net_income
   ```

2. **Segment by Burden Level**
   - Low (< 5%), Moderate (5-10%), High (10-15%), Critical (> 15%)

3. **Correlate with Financial Stress**
   - Emergency savings adequacy
   - Credit card debt levels
   - Payment delinquency

4. **Build Predictive Model**
   - Logistic regression with subscription features
   - Identify optimal threshold via ROC analysis

---

## 📊 Key Visualizations

### Subscription Penetration by Income
| Income Bracket | Avg Subscriptions | Burden Ratio |
|----------------|-------------------|--------------|
| < $35K | 4.2 | 8.7% |
| $35K-$75K | 6.8 | 7.2% |
| $75K-$125K | 8.1 | 5.4% |
| > $125K | 9.3 | 3.8% |

*Lower income households have fewer subscriptions but higher burden*

---

## 🛠️ Technical Implementation

### Files
- `complete_analysis.py` - Full analysis pipeline
- `subscription_fatigue_analysis.py` - Core calculations
- `data/` - Generated datasets
- `outputs/` - Results and visualizations

### Dependencies
```
pandas>=1.5.0
numpy>=1.21.0
scikit-learn>=1.0.0
matplotlib>=3.5.0
seaborn>=0.12.0
```

### Run the Analysis
```bash
python complete_analysis.py
```

---

## 💡 Insights & Recommendations

1. **For Risk Teams**: Add subscription-to-income ratio as credit scoring feature

2. **For Product Teams**: Build subscription tracking dashboard showing burden ratio

3. **For Marketing**: Target high-burden customers with consolidation offers

4. **For Education**: Create awareness content about subscription creep

---

## 📚 Data Dictionary

| Variable | Description |
|----------|-------------|
| `subscription_burden` | Total subscriptions / Net income |
| `streaming_spend` | Monthly streaming services cost |
| `software_spend` | Monthly software subscriptions |
| `membership_spend` | Gym, clubs, memberships |
| `financial_stress_score` | Composite distress indicator (0-100) |

---

## 🔗 Related Projects

- [Financial Literacy Analysis](../02-financial-literacy/) - Knowledge gaps and debt
- [Payment Velocity Index](../03-payment-velocity/) - Economic indicators
- [FinHealth Warehouse](https://github.com/emkwambe/finhealth-warehouse-dbt) - dbt pipeline
