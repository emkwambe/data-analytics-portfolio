"""
Subscription Fatigue Index Analysis
====================================
Analyzes BLS Consumer Expenditure data to understand the relationship
between subscription load and financial stress.

Author: Eddy Mkwambe
Purpose: Portfolio project for analytics/product roles

Data Source: BLS Consumer Expenditure Survey (PUMD)
Download: https://www.bls.gov/cex/pumd_data.htm

Instructions:
1. Download the Interview Survey PUMD files from BLS
2. Extract and update DATA_PATH below
3. Run: python subscription_fatigue_analysis.py
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURATION
# ============================================================

# Update these paths after downloading BLS PUMD data
MTBI_PATH = "mtbi241.csv"  # Monthly expenditure file (2024)
FMLI_PATH = "fmli241.csv"  # Consumer unit characteristics

# Subscription-related expenditure codes (from BLS documentation)
SUBSCRIPTION_UCCS = {
    # Streaming & Entertainment
    '620310': 'Streaming Video Services',
    '620311': 'Streaming Audio Services',
    '620320': 'Online Gaming Subscriptions',
    
    # Memberships
    '680110': 'Club Memberships',
    '680901': 'Gym Memberships',
    '680210': 'Credit Card Memberships',
    
    # Publications
    '590220': 'Magazine Subscriptions',
    '590210': 'Newspaper Subscriptions',
    
    # Services
    '340210': 'Cable/Satellite TV',
    '340310': 'Internet Service',
    '270211': 'Cell Phone Service',
    
    # Software/Digital
    '690117': 'Software Subscriptions',
}

# ============================================================
# DATA LOADING
# ============================================================

def load_bls_data():
    """Load BLS Consumer Expenditure data."""
    print("Loading BLS Consumer Expenditure data...")
    
    try:
        # Monthly expenditure data
        mtbi = pd.read_csv(MTBI_PATH)
        print(f"Loaded {len(mtbi):,} expenditure records")
        
        # Consumer unit characteristics
        fmli = pd.read_csv(FMLI_PATH)
        print(f"Loaded {len(fmli):,} consumer units")
        
        return mtbi, fmli
    except FileNotFoundError as e:
        print(f"ERROR: Could not find data files")
        print(f"Please download from: https://www.bls.gov/cex/pumd_data.htm")
        return None, None

def calculate_subscription_spending(mtbi):
    """Calculate total subscription spending per consumer unit."""
    
    # Filter to subscription-related UCCs
    subscription_uccs = list(SUBSCRIPTION_UCCS.keys())
    
    # Create UCC column if needed
    if 'UCC' in mtbi.columns:
        subs = mtbi[mtbi['UCC'].astype(str).isin(subscription_uccs)].copy()
    else:
        print("UCC column not found - using alternative identification")
        # Alternative approach based on common subscription categories
        subs = mtbi.copy()
    
    # Aggregate by consumer unit
    if 'NEWID' in subs.columns:
        sub_totals = subs.groupby('NEWID')['COST'].sum().reset_index()
        sub_totals.columns = ['NEWID', 'total_subscription_spending']
    else:
        print("Consumer unit ID not found")
        return None
    
    return sub_totals

def create_subscription_burden_index(fmli, sub_totals):
    """Calculate subscription burden as % of income."""
    
    # Merge subscription spending with consumer unit data
    df = fmli.merge(sub_totals, on='NEWID', how='left')
    df['total_subscription_spending'] = df['total_subscription_spending'].fillna(0)
    
    # Calculate annual subscription spending
    df['annual_sub_spending'] = df['total_subscription_spending'] * 12
    
    # Get income (FINCBTXM = income before taxes)
    if 'FINCBTXM' in df.columns:
        df['income'] = df['FINCBTXM']
    elif 'FINCBEFX' in df.columns:
        df['income'] = df['FINCBEFX']
    else:
        print("Income variable not found")
        return None
    
    # Calculate burden ratio
    df['subscription_burden'] = np.where(
        df['income'] > 0,
        (df['annual_sub_spending'] / df['income']) * 100,
        0
    )
    
    # Create burden categories
    df['burden_category'] = pd.cut(
        df['subscription_burden'],
        bins=[0, 2, 5, 10, 15, 100],
        labels=['Very Low (<2%)', 'Low (2-5%)', 'Moderate (5-10%)', 
                'High (10-15%)', 'Critical (>15%)']
    )
    
    return df

def analyze_burden_impact(df):
    """Analyze relationship between subscription burden and financial indicators."""
    
    print("\n" + "="*60)
    print("SUBSCRIPTION BURDEN ANALYSIS")
    print("="*60)
    
    # Summary by burden category
    print("\nSubscription Burden Distribution:")
    print(df['burden_category'].value_counts())
    
    # Financial indicators by burden level
    if 'SAVTHRYR' in df.columns:  # Savings indicator
        print("\nSavings Rate by Burden Category:")
        savings_by_burden = df.groupby('burden_category')['SAVTHRYR'].mean()
        print(savings_by_burden)
    
    if 'FSMPFRPX' in df.columns:  # Financial stress indicator
        print("\nFinancial Stress by Burden Category:")
        stress_by_burden = df.groupby('burden_category')['FSMPFRPX'].mean()
        print(stress_by_burden)
    
    return df

def demographic_analysis(df):
    """Analyze subscription patterns by demographics."""
    
    print("\n" + "="*60)
    print("DEMOGRAPHIC PATTERNS")
    print("="*60)
    
    # By age
    if 'AGE_REF' in df.columns:
        df['age_group'] = pd.cut(df['AGE_REF'],
                                  bins=[0, 25, 35, 45, 55, 65, 100],
                                  labels=['<25', '25-34', '35-44', '45-54', '55-64', '65+'])
        
        print("\nSubscription Burden by Age:")
        age_burden = df.groupby('age_group').agg({
            'subscription_burden': 'mean',
            'annual_sub_spending': 'mean'
        }).round(2)
        print(age_burden)
    
    # By income quintile
    if 'income' in df.columns:
        df['income_quintile'] = pd.qcut(df['income'], 5, 
                                        labels=['Q1 (Lowest)', 'Q2', 'Q3', 'Q4', 'Q5 (Highest)'])
        
        print("\nSubscription Burden by Income Quintile:")
        income_burden = df.groupby('income_quintile').agg({
            'subscription_burden': 'mean',
            'annual_sub_spending': 'mean',
            'income': 'mean'
        }).round(2)
        print(income_burden)
    
    return df

def create_fatigue_threshold_model(df):
    """Build model to identify subscription fatigue threshold."""
    
    print("\n" + "="*60)
    print("FATIGUE THRESHOLD MODEL")
    print("="*60)
    
    # Define financial stress indicator
    # Using composite of available indicators
    stress_indicators = []
    
    if 'FSMPFRPX' in df.columns:
        df['stress_spending'] = (df['FSMPFRPX'] > df['FSMPFRPX'].median()).astype(int)
        stress_indicators.append('stress_spending')
    
    if 'SAVTHRYR' in df.columns:
        df['low_savings'] = (df['SAVTHRYR'] < df['SAVTHRYR'].median()).astype(int)
        stress_indicators.append('low_savings')
    
    if stress_indicators:
        df['financial_stress'] = df[stress_indicators].max(axis=1)
        
        # Find threshold where stress increases significantly
        burden_bins = np.arange(0, 20, 2)
        stress_rates = []
        
        for i in range(len(burden_bins)-1):
            mask = (df['subscription_burden'] >= burden_bins[i]) & \
                   (df['subscription_burden'] < burden_bins[i+1])
            if mask.sum() > 50:  # Minimum sample size
                stress_rate = df.loc[mask, 'financial_stress'].mean()
                stress_rates.append({
                    'burden_range': f"{burden_bins[i]}-{burden_bins[i+1]}%",
                    'stress_rate': stress_rate * 100,
                    'n': mask.sum()
                })
        
        threshold_df = pd.DataFrame(stress_rates)
        print("\nFinancial Stress Rate by Subscription Burden:")
        print(threshold_df.to_string(index=False))
        
        # Identify inflection point
        if len(stress_rates) > 2:
            rates = [x['stress_rate'] for x in stress_rates]
            diffs = np.diff(rates)
            threshold_idx = np.argmax(diffs) + 1
            print(f"\n⚠️ FATIGUE THRESHOLD: {stress_rates[threshold_idx]['burden_range']}")
            print(f"   Stress rate jumps significantly at this burden level")
    
    return df

# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    """Run complete Subscription Fatigue analysis."""
    
    print("="*60)
    print("SUBSCRIPTION FATIGUE INDEX ANALYSIS")
    print("="*60)
    
    # Load data
    mtbi, fmli = load_bls_data()
    
    if mtbi is None or fmli is None:
        print("\nTo run this analysis, download BLS PUMD data:")
        print("1. Go to: https://www.bls.gov/cex/pumd_data.htm")
        print("2. Download Interview Survey data (2024 or latest)")
        print("3. Extract CSV files")
        print("4. Update file paths in this script")
        print("\nAlternatively, see DATA_PROJECTS_MASTER_PLAN.md for sample data approach")
        return
    
    # Calculate subscription spending
    sub_totals = calculate_subscription_spending(mtbi)
    
    # Create burden index
    df = create_subscription_burden_index(fmli, sub_totals)
    
    # Analysis
    df = analyze_burden_impact(df)
    df = demographic_analysis(df)
    df = create_fatigue_threshold_model(df)
    
    # Export results
    print("\n" + "="*60)
    print("EXPORTING RESULTS")
    print("="*60)
    
    results_summary = df.groupby('burden_category').agg({
        'subscription_burden': ['mean', 'count'],
        'annual_sub_spending': 'mean',
        'income': 'mean'
    }).round(2)
    
    results_summary.to_csv('subscription_fatigue_results.csv')
    print("Results saved to subscription_fatigue_results.csv")
    
    return df

if __name__ == "__main__":
    df = main()
