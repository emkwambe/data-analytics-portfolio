# Portfolio Data Analytics Projects
## Complete Implementation Guide for Mastercard-Relevant Analysis

**Author:** Eddy Mkwambe  
**Target Timeline:** 1-2 days per project  
**Purpose:** Demonstrate analytics, product thinking, and domain expertise for fintech roles

---

## Quick Reference: All Data Sources (Verified & Free)

| Dataset | Project | Download Link | Format |
|---------|---------|---------------|--------|
| FINRA NFCS 2024 | #2 | https://finrafoundation.org/nfcs-data-and-downloads | CSV, DTA, SAV |
| FINRA NFCS 2021 | #2 | https://finrafoundation.org/nfcs-data-and-downloads | CSV, DTA, SAV |
| CFPB Complaints | #2 | https://www.consumerfinance.gov/data-research/consumer-complaints/ | CSV, JSON |
| BLS Consumer Expenditure | #1 | https://www.bls.gov/cex/pumd_data.htm | CSV, SAS, STATA |
| Census Small Business Pulse | #3 | https://portal.census.gov/pulse/data/ | CSV |
| Fed Small Business Credit | #3 | https://www.fedsmallbusiness.org/reports/survey | PDF/Charts |
| BLS Employment Data | #3 | https://www.bls.gov/data/ | CSV |

---

# PROJECT 1: Subscription Fatigue Index

## The Hook
Americans average 6+ recurring subscriptions. At what point does subscription saturation predict payment delinquency or financial stress?

## Business Relevance to Mastercard
- Card issuers need to understand subscription load impact on payment behavior
- Opportunity for "subscription management" product features
- Risk modeling for credit decisions

## Data Sources

### Primary: BLS Consumer Expenditure Survey (PUMD)
**Download:** https://www.bls.gov/cex/pumd_data.htm

Key variables to extract:
- `MEMBSUB` - Membership/subscription fees
- `STREAMSV` - Streaming services
- `ENTERTMN` - Entertainment subscriptions
- `NEWSPPRS` - News/publication subscriptions
- `PHONECC` - Phone service (recurring)
- `CABLSVC` - Cable/internet service
- Total income and expenditure data

### Secondary: CFPB Complaints (Credit Card Late Payments)
**Download:** https://www.consumerfinance.gov/data-research/consumer-complaints/

Filter for:
- Product: "Credit card"
- Issue: "Problem with a purchase shown on your statement" (recurring billing)
- Issue: "Closing your account" 

## Analysis Methodology

### Step 1: Calculate Subscription Burden Ratio
```
Subscription_Burden = Total_Subscription_Spending / Net_Income
```

### Step 2: Segment by Burden Level
- Low: < 5% of income
- Moderate: 5-10%
- High: 10-15%
- Critical: > 15%

### Step 3: Correlate with Financial Stress Indicators
- Savings rate
- Credit card debt levels
- Payment delinquency rates

### Step 4: Build Predictive Model
- Features: subscription burden, income, age, household size
- Target: financial distress indicators

## Key Deliverables
1. Interactive dashboard showing subscription saturation by demographic
2. "Fatigue Threshold" visualization
3. Predictive model for subscription-related financial stress
4. Recommendations for card issuers

---

# PROJECT 2: Financial Literacy-Debt Nexus (RECOMMENDED)

## The Hook
Which *specific* financial literacy gaps most predict problematic debt? Not just "literacy = good" but granular intervention points.

## Business Relevance to Mastercard
- Directly relevant to Mastercard's financial inclusion initiatives
- Informs customer education programs
- Supports responsible lending practices

## Data Sources

### Primary: FINRA NFCS 2024 (25,000+ respondents)
**Download:** https://finrafoundation.org/nfcs-data-and-downloads

Click "2024 State-by-State Survey" → "Data & Data Info" to download ZIP file containing:
- CSV dataset
- Codebook with variable descriptions
- Questionnaire

### Key Variables

**Financial Knowledge Questions (7 quiz questions):**
| Variable | Topic | Question Theme |
|----------|-------|----------------|
| M6 | Interest Rates | Compound interest understanding |
| M7 | Inflation | Purchasing power erosion |
| M8 | Bond Prices | Interest rate relationship |
| M9 | Mortgages | 15 vs 30 year costs |
| M10 | Risk Diversification | Portfolio risk reduction |
| M31 | Stock/Mutual Fund | Investment basics |
| M4 | Numeracy | Basic calculation |

**Debt/Financial Behavior Variables:**
| Variable | Description |
|----------|-------------|
| A3 | Spending vs income comparison |
| A5 | Emergency savings adequacy |
| A8 | Financial satisfaction |
| C1 | Credit card balance behavior |
| C2 | Minimum payment only |
| C5 | Late fees in past year |
| B1-B13 | Various debt types held |
| J1-J50 | Detailed financial product usage |

**Demographics:**
| Variable | Description |
|----------|-------------|
| A1 | Household income |
| A3A | State |
| A11 | Age |
| A4A | Education |
| A41 | Gender |

### Secondary: CFPB Complaint Database
**Download:** https://www.consumerfinance.gov/data-research/consumer-complaints/

Use for geographic correlation analysis of complaint patterns vs literacy levels.

## Analysis Methodology

### Phase 1: Data Preparation
```python
# Key literacy score calculation
literacy_vars = ['M6', 'M7', 'M8', 'M9', 'M10', 'M31', 'M4']
# Each correct answer = 1, calculate total score 0-7
```

### Phase 2: Granular Gap Analysis
For each of the 7 knowledge areas:
1. Calculate % correct by demographic group
2. Correlate each knowledge gap with specific debt behaviors
3. Identify which gaps are most predictive of distress

### Phase 3: Debt Distress Index
Create composite score from:
- Late payment frequency (C5)
- Minimum payment behavior (C2)
- Spending exceeds income (A3)
- Inadequate emergency savings (A5)
- High-cost credit usage (payday loans, etc.)

### Phase 4: Predictive Modeling
```python
# Logistic regression to predict debt distress
# Features: individual knowledge scores (not just total)
# This reveals which specific gaps matter most
```

## Key Insights to Discover

1. **Which knowledge gap matters most?**
   - Is it compound interest understanding?
   - Or inflation comprehension?
   - Or risk diversification?

2. **Geographic patterns**
   - Map state-by-state literacy and correlate with CFPB complaints

3. **Intervention opportunities**
   - Identify the 2-3 specific knowledge areas where education would have biggest impact

## Deliverables
1. Heatmap: Knowledge gaps × Debt behaviors
2. State-level financial literacy map
3. "Intervention Priority" ranking of knowledge gaps
4. Demographic breakdowns
5. Actionable recommendations for financial education programs

---

# PROJECT 3: Small Business Payment Velocity Index

## The Hook
Can B2B payment timing predict local economic health 60-90 days ahead of traditional indicators?

## Business Relevance to Mastercard
- Mastercard literally has this data at scale
- Demonstrates you think like a payments company
- Economic indicator potential = thought leadership opportunity

## Data Sources

### Primary: Census Small Business Pulse Survey
**Download:** https://portal.census.gov/pulse/data/

Select "Download Data" and filter by:
- State
- Sector (NAICS)
- Time period (weekly data available)

Key variables:
- Revenue changes
- Cash on hand
- Expected business survival
- Payment delays experienced
- Credit application status

### Secondary: Federal Reserve Small Business Credit Survey
**Download:** https://www.fedsmallbusiness.org/reports/survey/2025/2025-report-on-employer-firms

Key metrics:
- Credit application rates
- Approval rates by lender type
- Financial challenges reported
- Revenue and employment trends

### Validation: BLS Employment Data
**Download:** https://www.bls.gov/data/

For backtesting the predictive power of your index.

## Analysis Methodology

### Phase 1: Payment Health Score Construction
```python
# Combine signals into composite score
payment_health = weighted_average([
    cash_on_hand_indicator,
    payment_delays_received,
    payment_delays_given,
    credit_access_score,
    revenue_change_momentum
])
```

### Phase 2: Geographic Aggregation
- Calculate scores by MSA (Metropolitan Statistical Area)
- 50 largest MSAs have good sample sizes

### Phase 3: Leading Indicator Validation
- Lag your Payment Health Score by 30/60/90 days
- Correlate with actual employment/GDP data
- Test Granger causality

### Phase 4: Visualization
- Time series showing leading indicator behavior
- Geographic dashboard of current "payment health"

## Deliverables
1. Payment Health Score methodology documentation
2. Interactive map of current scores by metro area
3. Backtesting results showing predictive power
4. API mock-up for how this could be productized

---

# Implementation Timeline

## Day 1 (Project 2 - Financial Literacy)

| Time | Task |
|------|------|
| Morning | Download FINRA NFCS 2024 data, explore codebook |
| 11am | Data cleaning, calculate literacy scores |
| 1pm | Gap analysis: which knowledge areas correlate with debt behaviors |
| 3pm | Build predictive model |
| 5pm | Create visualizations |
| Evening | Polish dashboard, write insights summary |

## Day 2 (Project 1 or 3)

Choose based on interest:
- **Project 1** if you want consumer behavior angle
- **Project 3** if you want B2B/economic indicator angle

---

# Tech Stack Recommendations

## For Quick Execution
- **Python** (pandas, sklearn, plotly)
- **Jupyter Notebook** for exploration
- **Streamlit** for interactive dashboard

## For Portfolio Polish
- **Next.js + React** (your strength)
- **Recharts or D3** for visualizations
- **Supabase** for data backend if deploying

## Dashboard Hosting
- Vercel (for Next.js)
- Streamlit Cloud (free, quick)
- GitHub Pages (for static export)

---

# What Makes These Projects Stand Out

1. **Original angle** - Not just descriptive analysis but predictive/prescriptive
2. **Mastercard-relevant** - Each connects to payments/fintech domain
3. **Actionable insights** - Moves beyond "interesting" to "useful"
4. **Methodology transparency** - Shows analytical rigor
5. **Professional visualization** - Dashboard-ready outputs

---

# Next Steps

1. Download the FINRA NFCS 2024 data first (most comprehensive, best for Project 2)
2. Run the analysis code (included in separate files)
3. Create visualizations
4. Write a 1-page executive summary of findings
5. Deploy dashboard for portfolio

Would you like me to generate the actual Python analysis code for any of these projects?
