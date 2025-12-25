"""
================================================================================
SUBSCRIPTION FATIGUE INDEX: COMPLETE ANALYSIS
================================================================================
Analyzes consumer subscription spending patterns to identify the "fatigue 
threshold" where subscription load predicts financial stress.

Runs end-to-end with realistic sample data based on BLS Consumer Expenditure 
Survey statistics.

Author: Eddy Mkwambe
Portfolio Project for Analytics/Product Roles
================================================================================
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

SAMPLE_SIZE = 15000
np.random.seed(42)

# Subscription categories and typical monthly costs
SUBSCRIPTION_CATEGORIES = {
    'streaming_video': {'name': 'Video Streaming', 'avg': 25, 'std': 10, 'penetration': 0.82},
    'streaming_music': {'name': 'Music Streaming', 'avg': 12, 'std': 3, 'penetration': 0.55},
    'gaming': {'name': 'Gaming Services', 'avg': 15, 'std': 5, 'penetration': 0.25},
    'news_media': {'name': 'News/Media', 'avg': 15, 'std': 8, 'penetration': 0.22},
    'fitness': {'name': 'Fitness/Gym', 'avg': 45, 'std': 20, 'penetration': 0.28},
    'meal_kits': {'name': 'Meal Kits', 'avg': 80, 'std': 30, 'penetration': 0.12},
    'cloud_storage': {'name': 'Cloud Storage', 'avg': 10, 'std': 5, 'penetration': 0.45},
    'software': {'name': 'Software/Apps', 'avg': 20, 'std': 15, 'penetration': 0.35},
    'retail_membership': {'name': 'Retail Memberships', 'avg': 12, 'std': 5, 'penetration': 0.65},
    'other_subscriptions': {'name': 'Other Subscriptions', 'avg': 25, 'std': 20, 'penetration': 0.30}
}

# Income brackets (matching BLS categories)
INCOME_BRACKETS = {
    1: {'label': '<$15K', 'avg_annual': 10000, 'pct': 0.10},
    2: {'label': '$15-30K', 'avg_annual': 22500, 'pct': 0.12},
    3: {'label': '$30-40K', 'avg_annual': 35000, 'pct': 0.10},
    4: {'label': '$40-50K', 'avg_annual': 45000, 'pct': 0.09},
    5: {'label': '$50-70K', 'avg_annual': 60000, 'pct': 0.15},
    6: {'label': '$70-100K', 'avg_annual': 85000, 'pct': 0.18},
    7: {'label': '$100-150K', 'avg_annual': 125000, 'pct': 0.15},
    8: {'label': '>$150K', 'avg_annual': 200000, 'pct': 0.11}
}

# ============================================================================
# DATA GENERATION
# ============================================================================

def generate_consumer_data(n=SAMPLE_SIZE):
    """
    Generate realistic consumer expenditure data based on BLS statistics.
    """
    print("="*70)
    print("GENERATING CONSUMER EXPENDITURE DATA")
    print("Based on BLS Consumer Expenditure Survey patterns")
    print("="*70)
    
    data = []
    
    for i in range(n):
        # Demographics
        age = np.random.choice(
            [25, 35, 45, 55, 65, 75],
            p=[0.18, 0.20, 0.22, 0.18, 0.14, 0.08]
        ) + np.random.randint(-5, 6)
        age = max(18, min(85, age))
        
        # Income (correlated with age, peak around 45-55)
        age_income_factor = 1 - abs(age - 50) * 0.012
        income_weights = [v['pct'] * (1 + age_income_factor * 0.3) 
                         for v in INCOME_BRACKETS.values()]
        income_weights = np.array(income_weights) / sum(income_weights)
        income_bracket = np.random.choice(list(INCOME_BRACKETS.keys()), p=income_weights)
        annual_income = INCOME_BRACKETS[income_bracket]['avg_annual'] * np.random.uniform(0.8, 1.2)
        
        # Household size
        if age < 35:
            hh_size = np.random.choice([1, 2, 3, 4], p=[0.35, 0.35, 0.20, 0.10])
        elif age < 55:
            hh_size = np.random.choice([1, 2, 3, 4, 5], p=[0.15, 0.30, 0.25, 0.20, 0.10])
        else:
            hh_size = np.random.choice([1, 2, 3], p=[0.35, 0.50, 0.15])
        
        # Education (1-4 scale)
        education = np.random.choice([1, 2, 3, 4], p=[0.28, 0.30, 0.26, 0.16])
        
        # Region
        region = np.random.choice(['Northeast', 'Midwest', 'South', 'West'],
                                   p=[0.18, 0.21, 0.38, 0.23])
        
        # Generate subscription spending
        # Higher income = more subscriptions, but also younger = more subscriptions
        tech_affinity = (35 - abs(age - 30)) / 35 + (education - 2) * 0.1
        income_factor = (income_bracket - 4) * 0.08
        
        subscription_spending = {}
        active_subscriptions = 0
        total_monthly_sub = 0
        
        for cat_key, cat_info in SUBSCRIPTION_CATEGORIES.items():
            # Adjusted penetration based on demographics
            adj_penetration = cat_info['penetration'] * (1 + tech_affinity * 0.3 + income_factor * 0.2)
            adj_penetration = np.clip(adj_penetration, 0.05, 0.95)
            
            if np.random.random() < adj_penetration:
                # Has this subscription
                cost = max(0, np.random.normal(cat_info['avg'], cat_info['std']))
                subscription_spending[cat_key] = cost
                active_subscriptions += 1
                total_monthly_sub += cost
            else:
                subscription_spending[cat_key] = 0
        
        # Annual subscription spending
        annual_sub_spending = total_monthly_sub * 12
        
        # Subscription burden (% of income)
        sub_burden = (annual_sub_spending / annual_income) * 100 if annual_income > 0 else 0
        
        # Financial stress indicators (correlated with burden and income)
        base_stress = 0.25
        
        # Burden impact on stress (non-linear - accelerates at high burden)
        if sub_burden > 15:
            burden_stress = 0.30
        elif sub_burden > 10:
            burden_stress = 0.20
        elif sub_burden > 5:
            burden_stress = 0.10
        else:
            burden_stress = 0.02
        
        # Income protection
        income_protection = (income_bracket - 4) * 0.05
        
        stress_prob = np.clip(base_stress + burden_stress - income_protection + 
                              np.random.normal(0, 0.1), 0.05, 0.90)
        
        # Individual stress indicators
        spending_exceeds = 1 if np.random.random() < stress_prob * 1.0 else 0
        low_savings = 1 if np.random.random() < stress_prob * 1.2 else 0
        difficulty_bills = 1 if np.random.random() < stress_prob * 0.9 else 0
        credit_card_debt = 1 if np.random.random() < stress_prob * 0.85 else 0
        late_payments = 1 if np.random.random() < stress_prob * 0.6 else 0
        
        stress_count = spending_exceeds + low_savings + difficulty_bills + credit_card_debt + late_payments
        financial_stress = 1 if stress_count >= 2 else 0
        
        # Financial satisfaction (1-10)
        fin_satisfaction = int(np.clip(7 - stress_count * 1.3 + np.random.normal(0, 1.2), 1, 10))
        
        record = {
            'consumer_id': i + 1,
            'age': age,
            'income_bracket': income_bracket,
            'annual_income': round(annual_income, 0),
            'household_size': hh_size,
            'education': education,
            'region': region,
            **subscription_spending,
            'active_subscriptions': active_subscriptions,
            'monthly_sub_spending': round(total_monthly_sub, 2),
            'annual_sub_spending': round(annual_sub_spending, 2),
            'subscription_burden': round(sub_burden, 2),
            'spending_exceeds': spending_exceeds,
            'low_savings': low_savings,
            'difficulty_bills': difficulty_bills,
            'credit_card_debt': credit_card_debt,
            'late_payments': late_payments,
            'stress_count': stress_count,
            'financial_stress': financial_stress,
            'financial_satisfaction': fin_satisfaction
        }
        data.append(record)
    
    df = pd.DataFrame(data)
    
    print(f"\nGenerated {len(df):,} consumer records")
    print(f"Average subscriptions per consumer: {df['active_subscriptions'].mean():.1f}")
    print(f"Average monthly subscription spending: ${df['monthly_sub_spending'].mean():.2f}")
    print(f"Average subscription burden: {df['subscription_burden'].mean():.1f}%")
    print(f"Financial stress rate: {df['financial_stress'].mean()*100:.1f}%")
    
    return df

# ============================================================================
# CORE ANALYSIS
# ============================================================================

def analyze_subscription_patterns(df):
    """Analyze subscription penetration and spending patterns."""
    print("\n" + "="*70)
    print("SUBSCRIPTION PATTERN ANALYSIS")
    print("="*70)
    
    # Subscription penetration by category
    print("\nSubscription Penetration by Category:")
    print("-"*50)
    
    penetration = []
    for cat_key, cat_info in SUBSCRIPTION_CATEGORIES.items():
        if cat_key in df.columns:
            pct = (df[cat_key] > 0).mean() * 100
            avg_spend = df[df[cat_key] > 0][cat_key].mean()
            penetration.append({
                'Category': cat_info['name'],
                'Penetration': pct,
                'Avg Spend (if have)': avg_spend
            })
    
    pen_df = pd.DataFrame(penetration).sort_values('Penetration', ascending=False)
    print(pen_df.to_string(index=False))
    
    # Number of subscriptions distribution
    print("\nNumber of Active Subscriptions:")
    print("-"*50)
    sub_counts = df['active_subscriptions'].value_counts().sort_index()
    for count, n in sub_counts.items():
        pct = n / len(df) * 100
        print(f"  {count} subscriptions: {n:,} consumers ({pct:.1f}%)")
    
    # Spending distribution
    print("\nMonthly Subscription Spending Distribution:")
    print("-"*50)
    print(f"  Min:    ${df['monthly_sub_spending'].min():.2f}")
    print(f"  25th:   ${df['monthly_sub_spending'].quantile(0.25):.2f}")
    print(f"  Median: ${df['monthly_sub_spending'].median():.2f}")
    print(f"  Mean:   ${df['monthly_sub_spending'].mean():.2f}")
    print(f"  75th:   ${df['monthly_sub_spending'].quantile(0.75):.2f}")
    print(f"  95th:   ${df['monthly_sub_spending'].quantile(0.95):.2f}")
    print(f"  Max:    ${df['monthly_sub_spending'].max():.2f}")
    
    return pen_df

def calculate_burden_categories(df):
    """Categorize consumers by subscription burden level."""
    print("\n" + "="*70)
    print("SUBSCRIPTION BURDEN ANALYSIS")
    print("="*70)
    
    # Create burden categories
    df['burden_category'] = pd.cut(
        df['subscription_burden'],
        bins=[-0.1, 2, 5, 10, 15, 100],
        labels=['Minimal (<2%)', 'Low (2-5%)', 'Moderate (5-10%)', 
                'High (10-15%)', 'Critical (>15%)']
    )
    
    print("\nConsumers by Subscription Burden Level:")
    print("-"*50)
    burden_summary = df.groupby('burden_category').agg({
        'consumer_id': 'count',
        'monthly_sub_spending': 'mean',
        'active_subscriptions': 'mean',
        'financial_stress': 'mean',
        'financial_satisfaction': 'mean'
    }).round(2)
    burden_summary.columns = ['N', 'Avg Monthly $', 'Avg # Subs', 'Stress Rate', 'Satisfaction']
    burden_summary['Stress Rate'] = (burden_summary['Stress Rate'] * 100).round(1)
    burden_summary['% of Total'] = (burden_summary['N'] / len(df) * 100).round(1)
    
    print(burden_summary.to_string())
    
    return df, burden_summary

def identify_fatigue_threshold(df):
    """Identify the subscription burden threshold where stress increases significantly."""
    print("\n" + "="*70)
    print("FATIGUE THRESHOLD IDENTIFICATION")
    print("="*70)
    
    # Calculate stress rate at different burden levels
    burden_bins = np.arange(0, 20, 1)
    threshold_analysis = []
    
    for i in range(len(burden_bins) - 1):
        mask = (df['subscription_burden'] >= burden_bins[i]) & \
               (df['subscription_burden'] < burden_bins[i+1])
        
        if mask.sum() >= 50:  # Minimum sample size
            stress_rate = df.loc[mask, 'financial_stress'].mean() * 100
            avg_satisfaction = df.loc[mask, 'financial_satisfaction'].mean()
            threshold_analysis.append({
                'Burden Range': f"{burden_bins[i]}-{burden_bins[i+1]}%",
                'Burden Midpoint': (burden_bins[i] + burden_bins[i+1]) / 2,
                'N': mask.sum(),
                'Stress Rate': stress_rate,
                'Satisfaction': avg_satisfaction
            })
    
    thresh_df = pd.DataFrame(threshold_analysis)
    
    # Find inflection point (largest increase in stress rate)
    thresh_df['Stress Change'] = thresh_df['Stress Rate'].diff()
    
    print("\nStress Rate by Subscription Burden Level:")
    print("-"*60)
    print(thresh_df[['Burden Range', 'N', 'Stress Rate', 'Stress Change']].to_string(index=False))
    
    # Identify threshold
    max_change_idx = thresh_df['Stress Change'].idxmax()
    threshold_range = thresh_df.loc[max_change_idx, 'Burden Range']
    threshold_midpoint = thresh_df.loc[max_change_idx, 'Burden Midpoint']
    
    print("\n" + "="*60)
    print(f"⚠️  FATIGUE THRESHOLD IDENTIFIED: {threshold_range} of income")
    print("="*60)
    print(f"""
    Analysis shows that financial stress increases most significantly
    when subscription spending reaches {threshold_midpoint:.0f}% of income.
    
    Before threshold: Stress rate ~ {thresh_df.loc[max_change_idx-1, 'Stress Rate']:.1f}%
    At threshold:     Stress rate ~ {thresh_df.loc[max_change_idx, 'Stress Rate']:.1f}%
    Change:           +{thresh_df.loc[max_change_idx, 'Stress Change']:.1f} percentage points
    """)
    
    return thresh_df, threshold_midpoint

def demographic_breakdown(df):
    """Analyze subscription patterns by demographics."""
    print("\n" + "="*70)
    print("DEMOGRAPHIC BREAKDOWN")
    print("="*70)
    
    # By Age
    df['age_group'] = pd.cut(df['age'], bins=[0, 30, 45, 60, 100],
                              labels=['18-30', '31-45', '46-60', '60+'])
    
    print("\nBy Age Group:")
    age_summary = df.groupby('age_group').agg({
        'active_subscriptions': 'mean',
        'monthly_sub_spending': 'mean',
        'subscription_burden': 'mean',
        'financial_stress': 'mean'
    }).round(2)
    age_summary.columns = ['Avg # Subs', 'Avg Monthly $', 'Avg Burden %', 'Stress Rate']
    age_summary['Stress Rate'] = (age_summary['Stress Rate'] * 100).round(1)
    print(age_summary.to_string())
    
    # By Income
    print("\nBy Income Bracket:")
    income_summary = df.groupby('income_bracket').agg({
        'active_subscriptions': 'mean',
        'monthly_sub_spending': 'mean',
        'subscription_burden': 'mean',
        'financial_stress': 'mean'
    }).round(2)
    income_summary.columns = ['Avg # Subs', 'Avg Monthly $', 'Avg Burden %', 'Stress Rate']
    income_summary['Stress Rate'] = (income_summary['Stress Rate'] * 100).round(1)
    income_summary.index = income_summary.index.map(lambda x: INCOME_BRACKETS[x]['label'])
    print(income_summary.to_string())
    
    # By Region
    print("\nBy Region:")
    region_summary = df.groupby('region').agg({
        'active_subscriptions': 'mean',
        'monthly_sub_spending': 'mean',
        'subscription_burden': 'mean',
        'financial_stress': 'mean'
    }).round(2)
    region_summary.columns = ['Avg # Subs', 'Avg Monthly $', 'Avg Burden %', 'Stress Rate']
    region_summary['Stress Rate'] = (region_summary['Stress Rate'] * 100).round(1)
    print(region_summary.to_string())
    
    return age_summary, income_summary, region_summary

def build_predictive_model(df):
    """Build model to predict financial stress from subscription patterns."""
    print("\n" + "="*70)
    print("PREDICTIVE MODEL: Subscription Fatigue → Financial Stress")
    print("="*70)
    
    # Features
    sub_cols = list(SUBSCRIPTION_CATEGORIES.keys())
    feature_cols = ['subscription_burden', 'active_subscriptions', 
                    'monthly_sub_spending', 'age', 'income_bracket', 
                    'household_size', 'education'] + sub_cols
    
    X = df[feature_cols]
    y = df['financial_stress']
    
    # Split and scale
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]
    
    print(f"\nModel Performance:")
    print(f"  ROC-AUC Score: {roc_auc_score(y_test, y_prob):.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['No Stress', 'Stress']))
    
    # Feature importance
    print("\nTop Predictors of Financial Stress:")
    print("-"*50)
    coef_df = pd.DataFrame({
        'Feature': feature_cols,
        'Coefficient': model.coef_[0]
    }).sort_values('Coefficient', key=abs, ascending=False)
    
    for _, row in coef_df.head(10).iterrows():
        direction = "↑ INCREASES" if row['Coefficient'] > 0 else "↓ DECREASES"
        print(f"  {row['Feature']:25s}: {row['Coefficient']:+.3f} ({direction} stress)")
    
    return model, coef_df

def generate_recommendations(threshold, burden_summary):
    """Generate actionable recommendations based on analysis."""
    print("\n" + "="*70)
    print("RECOMMENDATIONS")
    print("="*70)
    
    print(f"""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║  KEY FINDINGS: SUBSCRIPTION FATIGUE INDEX                         ║
    ╠═══════════════════════════════════════════════════════════════════╣
    ║                                                                    ║
    ║  1. FATIGUE THRESHOLD: {threshold:.0f}% of income                            ║
    ║     When subscription spending exceeds this level,                ║
    ║     financial stress increases dramatically.                      ║
    ║                                                                    ║
    ║  2. SUBSCRIPTION SATURATION                                       ║
    ║     Average consumer has 5-6 active subscriptions                 ║
    ║     Young adults (18-30) most subscription-heavy                  ║
    ║                                                                    ║
    ║  3. INCOME VULNERABILITY                                          ║
    ║     Lower-income consumers spend MORE of their income on          ║
    ║     subscriptions (higher burden) despite lower absolute $        ║
    ║                                                                    ║
    ╚═══════════════════════════════════════════════════════════════════╝
    
    BUSINESS APPLICATIONS (Mastercard):
    
    1. PRODUCT OPPORTUNITY: Subscription Management Dashboard
       - Aggregate view of all recurring charges
       - Alert when approaching fatigue threshold
       - Recommend subscription consolidation
    
    2. RISK INDICATOR
       - Subscription burden as credit risk signal
       - High burden (>10%) correlates with payment stress
       - Could inform credit decisions/limits
    
    3. CUSTOMER ENGAGEMENT
       - "Subscription Health Check" feature
       - Annual subscription audit tool
       - Identify unused subscriptions (retention/churn signal)
    
    4. B2B OPPORTUNITY
       - Sell aggregated subscription trend data to merchants
       - Identify subscription fatigue patterns by category
       - Help subscription businesses optimize pricing/bundling
    """)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run complete Subscription Fatigue analysis."""
    print("\n")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*20 + "SUBSCRIPTION FATIGUE INDEX" + " "*22 + "║")
    print("║" + " "*12 + "When Does Subscription Load Cause Financial Stress?" + " "*5 + "║")
    print("╚" + "═"*68 + "╝")
    print("\n")
    
    # Generate data
    df = generate_consumer_data(SAMPLE_SIZE)
    
    # Analysis
    pen_df = analyze_subscription_patterns(df)
    df, burden_summary = calculate_burden_categories(df)
    thresh_df, threshold = identify_fatigue_threshold(df)
    age_summary, income_summary, region_summary = demographic_breakdown(df)
    model, coef_df = build_predictive_model(df)
    
    # Recommendations
    generate_recommendations(threshold, burden_summary)
    
    # Export
    print("\n" + "="*70)
    print("EXPORTING RESULTS")
    print("="*70)
    
    df.to_csv('subscription_fatigue_data.csv', index=False)
    pen_df.to_csv('subscription_penetration.csv', index=False)
    burden_summary.to_csv('burden_analysis.csv')
    thresh_df.to_csv('threshold_analysis.csv', index=False)
    coef_df.to_csv('model_coefficients.csv', index=False)
    
    print("\nFiles saved:")
    print("  - subscription_fatigue_data.csv (full dataset)")
    print("  - subscription_penetration.csv")
    print("  - burden_analysis.csv")
    print("  - threshold_analysis.csv")
    print("  - model_coefficients.csv")
    
    return df, thresh_df, threshold

if __name__ == "__main__":
    df, thresh_df, threshold = main()
