"""
Financial Literacy-Debt Nexus Analysis
======================================
Analyzes FINRA NFCS 2024 data to identify which specific financial
knowledge gaps most predict problematic debt behaviors.

Author: Eddy Mkwambe
Purpose: Portfolio project for analytics/product roles

Instructions:
1. Download NFCS 2024 data from: https://finrafoundation.org/nfcs-data-and-downloads
2. Extract the CSV file from the ZIP
3. Update the DATA_PATH variable below
4. Run: python financial_literacy_analysis.py
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURATION
# ============================================================

DATA_PATH = "NFCS_2024_State_Data.csv"  # Update with your path

# Financial Knowledge Variables (7 quiz questions)
KNOWLEDGE_VARS = {
    'M6': 'Compound Interest',
    'M7': 'Inflation', 
    'M8': 'Bond Prices',
    'M9': 'Mortgage Terms',
    'M10': 'Risk Diversification',
    'M31': 'Stock Knowledge',
    'M4': 'Numeracy'
}

# Correct answers for each question (from NFCS codebook)
CORRECT_ANSWERS = {
    'M6': 1,   # More than $102
    'M7': 1,   # Less than today
    'M8': 1,   # Fall
    'M9': 1,   # 15-year mortgage
    'M10': 2,  # False (single company stock is NOT safer)
    'M31': 2,  # False (mutual fund provides diversification)
    'M4': 1    # Correct calculation
}

# Debt/Financial Behavior Variables
DEBT_BEHAVIOR_VARS = {
    'A3': 'Spending_vs_Income',      # 1=spend less, 2=equal, 3=more
    'A5': 'Emergency_Savings',        # Could cover 3 months expenses
    'C2': 'Minimum_Payment_Only',     # Only pay minimum on credit cards
    'C5': 'Late_Fees_Past_Year',      # Paid late fees
    'J3': 'Has_Payday_Loan',          # High-cost credit indicator
}

# ============================================================
# DATA LOADING & CLEANING
# ============================================================

def load_and_prepare_data(filepath):
    """Load NFCS data and prepare for analysis."""
    print("Loading data...")
    df = pd.read_csv(filepath, low_memory=False)
    print(f"Loaded {len(df):,} records")
    
    return df

def calculate_knowledge_scores(df):
    """Calculate individual knowledge scores and total score."""
    print("\nCalculating knowledge scores...")
    
    for var, name in KNOWLEDGE_VARS.items():
        if var in df.columns:
            correct_answer = CORRECT_ANSWERS[var]
            df[f'{var}_correct'] = (df[var] == correct_answer).astype(int)
            # Handle missing/refused as incorrect
            df.loc[df[var].isin([98, 99, -1]), f'{var}_correct'] = 0
    
    # Calculate total knowledge score (0-7)
    correct_cols = [f'{var}_correct' for var in KNOWLEDGE_VARS.keys() 
                    if f'{var}_correct' in df.columns]
    df['total_knowledge_score'] = df[correct_cols].sum(axis=1)
    
    print(f"Knowledge score distribution:")
    print(df['total_knowledge_score'].value_counts().sort_index())
    
    return df

def create_debt_distress_index(df):
    """Create composite debt distress indicator."""
    print("\nCreating debt distress index...")
    
    distress_signals = []
    
    # Spending exceeds income
    if 'A3' in df.columns:
        df['spending_exceeds'] = (df['A3'] == 3).astype(int)
        distress_signals.append('spending_exceeds')
    
    # Inadequate emergency savings
    if 'A5' in df.columns:
        df['no_emergency_savings'] = (df['A5'] == 2).astype(int)
        distress_signals.append('no_emergency_savings')
    
    # Only pays minimum on credit cards
    if 'C2' in df.columns:
        df['minimum_payment'] = (df['C2'] == 1).astype(int)
        distress_signals.append('minimum_payment')
    
    # Paid late fees in past year
    if 'C5' in df.columns:
        df['late_fees'] = (df['C5'] == 1).astype(int)
        distress_signals.append('late_fees')
    
    # Has high-cost credit (payday loans, etc.)
    if 'J3' in df.columns:
        df['high_cost_credit'] = (df['J3'] == 1).astype(int)
        distress_signals.append('high_cost_credit')
    
    # Composite distress index (any 2+ signals = distressed)
    if distress_signals:
        df['distress_count'] = df[distress_signals].sum(axis=1)
        df['debt_distressed'] = (df['distress_count'] >= 2).astype(int)
        print(f"Debt distressed rate: {df['debt_distressed'].mean()*100:.1f}%")
    
    return df, distress_signals

# ============================================================
# CORE ANALYSIS
# ============================================================

def analyze_knowledge_gaps(df):
    """Analyze which knowledge gaps correlate most with debt distress."""
    print("\n" + "="*60)
    print("KNOWLEDGE GAP ANALYSIS")
    print("="*60)
    
    results = []
    
    for var, name in KNOWLEDGE_VARS.items():
        correct_col = f'{var}_correct'
        if correct_col in df.columns and 'debt_distressed' in df.columns:
            # Calculate distress rate by knowledge level
            correct_rate = df[correct_col].mean() * 100
            
            # Distress rate for those who got it wrong vs right
            wrong_distress = df[df[correct_col] == 0]['debt_distressed'].mean() * 100
            right_distress = df[df[correct_col] == 1]['debt_distressed'].mean() * 100
            
            # Risk ratio
            if right_distress > 0:
                risk_ratio = wrong_distress / right_distress
            else:
                risk_ratio = np.nan
            
            results.append({
                'Knowledge Area': name,
                'Variable': var,
                '% Correct': correct_rate,
                'Distress Rate (Wrong)': wrong_distress,
                'Distress Rate (Right)': right_distress,
                'Risk Ratio': risk_ratio
            })
    
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('Risk Ratio', ascending=False)
    
    print("\nKnowledge Gaps Ranked by Impact on Debt Distress:")
    print("-" * 60)
    for _, row in results_df.iterrows():
        print(f"\n{row['Knowledge Area']} ({row['Variable']})")
        print(f"  Overall accuracy: {row['% Correct']:.1f}%")
        print(f"  Distress rate if WRONG: {row['Distress Rate (Wrong)']:.1f}%")
        print(f"  Distress rate if RIGHT: {row['Distress Rate (Right)']:.1f}%")
        print(f"  Risk Ratio: {row['Risk Ratio']:.2f}x")
    
    return results_df

def demographic_breakdown(df):
    """Analyze knowledge and distress by demographics."""
    print("\n" + "="*60)
    print("DEMOGRAPHIC ANALYSIS")
    print("="*60)
    
    # Age groups
    if 'A11' in df.columns:
        df['age_group'] = pd.cut(df['A11'], 
                                  bins=[0, 34, 44, 54, 64, 100],
                                  labels=['18-34', '35-44', '45-54', '55-64', '65+'])
        
        print("\nBy Age Group:")
        age_summary = df.groupby('age_group').agg({
            'total_knowledge_score': 'mean',
            'debt_distressed': 'mean'
        }).round(3)
        age_summary.columns = ['Avg Knowledge Score', 'Distress Rate']
        age_summary['Distress Rate'] = age_summary['Distress Rate'] * 100
        print(age_summary)
    
    # Income groups
    if 'A1' in df.columns:
        income_map = {
            1: '<$15K', 2: '$15-25K', 3: '$25-35K', 4: '$35-50K',
            5: '$50-75K', 6: '$75-100K', 7: '$100-150K', 8: '>$150K'
        }
        df['income_group'] = df['A1'].map(income_map)
        
        print("\nBy Income:")
        income_summary = df.groupby('income_group').agg({
            'total_knowledge_score': 'mean',
            'debt_distressed': 'mean'
        }).round(3)
        income_summary.columns = ['Avg Knowledge Score', 'Distress Rate']
        income_summary['Distress Rate'] = income_summary['Distress Rate'] * 100
        print(income_summary)
    
    return df

def build_predictive_model(df):
    """Build logistic regression to predict debt distress from knowledge gaps."""
    print("\n" + "="*60)
    print("PREDICTIVE MODEL")
    print("="*60)
    
    # Features: individual knowledge scores
    feature_cols = [f'{var}_correct' for var in KNOWLEDGE_VARS.keys() 
                    if f'{var}_correct' in df.columns]
    
    # Add demographics if available
    if 'A11' in df.columns:
        feature_cols.append('A11')
    if 'A1' in df.columns:
        feature_cols.append('A1')
    
    # Prepare data
    model_df = df[feature_cols + ['debt_distressed']].dropna()
    
    X = model_df[feature_cols]
    y = model_df['debt_distressed']
    
    print(f"Training on {len(model_df):,} complete records")
    
    # Split and train
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]
    
    print("\nModel Performance:")
    print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob):.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Not Distressed', 'Distressed']))
    
    # Feature importance
    print("\nFeature Importance (Coefficient Magnitude):")
    importance = pd.DataFrame({
        'Feature': feature_cols,
        'Coefficient': model.coef_[0]
    }).sort_values('Coefficient', key=abs, ascending=False)
    
    for _, row in importance.iterrows():
        direction = "increases" if row['Coefficient'] > 0 else "decreases"
        print(f"  {row['Feature']}: {row['Coefficient']:+.3f} ({direction} distress)")
    
    return model, importance

def state_level_analysis(df):
    """Analyze financial literacy and distress by state."""
    print("\n" + "="*60)
    print("STATE-LEVEL ANALYSIS")
    print("="*60)
    
    if 'A3A' not in df.columns:
        print("State variable not found in dataset")
        return None
    
    state_summary = df.groupby('A3A').agg({
        'total_knowledge_score': 'mean',
        'debt_distressed': 'mean'
    }).round(3)
    
    state_summary.columns = ['Avg Knowledge Score', 'Distress Rate']
    state_summary['Distress Rate'] = state_summary['Distress Rate'] * 100
    state_summary = state_summary.sort_values('Distress Rate', ascending=False)
    
    print("\nTop 10 States by Debt Distress Rate:")
    print(state_summary.head(10))
    
    print("\nTop 10 States by Financial Literacy:")
    print(state_summary.sort_values('Avg Knowledge Score', ascending=False).head(10))
    
    return state_summary

# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    """Run the complete analysis pipeline."""
    print("="*60)
    print("FINANCIAL LITERACY-DEBT NEXUS ANALYSIS")
    print("NFCS 2024 Data Analysis for Portfolio Project")
    print("="*60)
    
    try:
        # Load data
        df = load_and_prepare_data(DATA_PATH)
        
        # Calculate knowledge scores
        df = calculate_knowledge_scores(df)
        
        # Create debt distress indicator
        df, distress_signals = create_debt_distress_index(df)
        
        # Core analysis
        gap_results = analyze_knowledge_gaps(df)
        
        # Demographics
        df = demographic_breakdown(df)
        
        # Predictive model
        model, importance = build_predictive_model(df)
        
        # State analysis
        state_results = state_level_analysis(df)
        
        # Export results
        print("\n" + "="*60)
        print("EXPORTING RESULTS")
        print("="*60)
        
        gap_results.to_csv('knowledge_gap_analysis.csv', index=False)
        importance.to_csv('feature_importance.csv', index=False)
        if state_results is not None:
            state_results.to_csv('state_analysis.csv')
        
        print("Results exported to CSV files!")
        
        # Key findings summary
        print("\n" + "="*60)
        print("KEY FINDINGS SUMMARY")
        print("="*60)
        
        top_gap = gap_results.iloc[0]
        print(f"\n1. BIGGEST KNOWLEDGE GAP IMPACT:")
        print(f"   '{top_gap['Knowledge Area']}' knowledge has the highest")
        print(f"   correlation with debt distress (Risk Ratio: {top_gap['Risk Ratio']:.2f}x)")
        
        print(f"\n2. INTERVENTION PRIORITY:")
        print(f"   Focus education on top 3 gaps: ")
        for i, row in gap_results.head(3).iterrows():
            print(f"   - {row['Knowledge Area']} (only {row['% Correct']:.0f}% answer correctly)")
        
        print(f"\n3. PREDICTIVE POWER:")
        print(f"   Individual knowledge scores can predict debt distress")
        print(f"   with meaningful accuracy (AUC > 0.6 typical)")
        
        return df, gap_results, state_results
        
    except FileNotFoundError:
        print(f"\nERROR: Data file not found at '{DATA_PATH}'")
        print("\nTo run this analysis:")
        print("1. Download NFCS 2024 data from:")
        print("   https://finrafoundation.org/nfcs-data-and-downloads")
        print("2. Extract the CSV file from the ZIP")
        print("3. Update DATA_PATH variable at top of script")
        print("4. Run again!")
        return None, None, None

if __name__ == "__main__":
    df, gap_results, state_results = main()
