"""
Financial Literacy Dashboard Visualizations
============================================
Creates publication-ready visualizations for the Financial Literacy-Debt Nexus analysis.

Run after: financial_literacy_analysis.py

Dependencies:
    pip install pandas matplotlib seaborn plotly

Author: Eddy Mkwambe
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Custom colors
PRIMARY = '#1a365d'
ACCENT = '#2b6cb0'
DANGER = '#e53e3e'
SUCCESS = '#38a169'

def create_knowledge_gap_heatmap(gap_results):
    """Create heatmap showing knowledge gaps vs distress rates."""
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Prepare data
    data = gap_results[['Knowledge Area', 'Distress Rate (Wrong)', 'Distress Rate (Right)']].copy()
    data = data.set_index('Knowledge Area')
    data.columns = ['Gap Present\n(Answered Wrong)', 'No Gap\n(Answered Right)']
    
    # Create heatmap
    sns.heatmap(data, annot=True, fmt='.1f', cmap='RdYlGn_r', 
                center=data.values.mean(), ax=ax,
                cbar_kws={'label': 'Debt Distress Rate (%)'})
    
    ax.set_title('Knowledge Gaps and Debt Distress\n', fontsize=14, fontweight='bold', color=PRIMARY)
    ax.set_xlabel('\nKnowledge Status', fontsize=11)
    ax.set_ylabel('')
    
    plt.tight_layout()
    plt.savefig('viz_knowledge_gap_heatmap.png', dpi=300, bbox_inches='tight')
    print("Saved: viz_knowledge_gap_heatmap.png")
    plt.close()

def create_risk_ratio_chart(gap_results):
    """Create bar chart of risk ratios by knowledge area."""
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    data = gap_results.sort_values('Risk Ratio', ascending=True)
    
    colors = [DANGER if r > 1.5 else ACCENT for r in data['Risk Ratio']]
    
    bars = ax.barh(data['Knowledge Area'], data['Risk Ratio'], color=colors, edgecolor='white')
    
    # Add reference line at 1.0
    ax.axvline(x=1.0, color='gray', linestyle='--', linewidth=1, label='No difference')
    
    # Add value labels
    for bar, val in zip(bars, data['Risk Ratio']):
        ax.text(val + 0.05, bar.get_y() + bar.get_height()/2, 
                f'{val:.2f}x', va='center', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('\nRisk Ratio (Distress Rate Wrong ÷ Distress Rate Right)', fontsize=11)
    ax.set_title('Impact of Knowledge Gaps on Debt Distress\n"How much more likely to be distressed if you got this wrong?"', 
                 fontsize=12, fontweight='bold', color=PRIMARY)
    ax.set_xlim(0, max(data['Risk Ratio']) * 1.2)
    
    plt.tight_layout()
    plt.savefig('viz_risk_ratio_chart.png', dpi=300, bbox_inches='tight')
    print("Saved: viz_risk_ratio_chart.png")
    plt.close()

def create_accuracy_chart(gap_results):
    """Create chart showing accuracy rates for each knowledge area."""
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    data = gap_results.sort_values('% Correct', ascending=True)
    
    colors = [DANGER if p < 40 else (ACCENT if p < 60 else SUCCESS) for p in data['% Correct']]
    
    bars = ax.barh(data['Knowledge Area'], data['% Correct'], color=colors, edgecolor='white')
    
    # Add value labels
    for bar, val in zip(bars, data['% Correct']):
        ax.text(val + 1, bar.get_y() + bar.get_height()/2, 
                f'{val:.0f}%', va='center', fontsize=10)
    
    ax.axvline(x=50, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    
    ax.set_xlabel('\nPercentage of Respondents Answering Correctly', fontsize=11)
    ax.set_title('Financial Knowledge Quiz Results\nNational Financial Capability Study 2024', 
                 fontsize=12, fontweight='bold', color=PRIMARY)
    ax.set_xlim(0, 100)
    
    plt.tight_layout()
    plt.savefig('viz_accuracy_chart.png', dpi=300, bbox_inches='tight')
    print("Saved: viz_accuracy_chart.png")
    plt.close()

def create_quadrant_plot(gap_results):
    """Create quadrant plot: Knowledge Gap Size vs Impact on Distress."""
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    x = 100 - gap_results['% Correct']  # Gap size (% who got it wrong)
    y = gap_results['Risk Ratio']
    labels = gap_results['Knowledge Area']
    
    # Size based on sample (uniform here)
    sizes = [200] * len(x)
    
    scatter = ax.scatter(x, y, s=sizes, c=y, cmap='RdYlGn_r', 
                        edgecolors='white', linewidth=2, alpha=0.8)
    
    # Add labels
    for i, label in enumerate(labels):
        ax.annotate(label, (x.iloc[i], y.iloc[i]), 
                   textcoords="offset points", xytext=(10, 5),
                   fontsize=9, fontweight='bold')
    
    # Quadrant lines
    ax.axhline(y=y.median(), color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=x.median(), color='gray', linestyle='--', alpha=0.5)
    
    # Quadrant labels
    ax.text(0.25, 0.95, 'Low Priority\nSmall gap, low impact', 
            transform=ax.transAxes, fontsize=9, alpha=0.7, ha='center')
    ax.text(0.75, 0.95, 'HIGH PRIORITY\nLarge gap, high impact', 
            transform=ax.transAxes, fontsize=9, alpha=0.7, ha='center', 
            color=DANGER, fontweight='bold')
    ax.text(0.25, 0.05, 'Monitor\nSmall gap, high impact', 
            transform=ax.transAxes, fontsize=9, alpha=0.7, ha='center')
    ax.text(0.75, 0.05, 'Education Focus\nLarge gap, lower impact', 
            transform=ax.transAxes, fontsize=9, alpha=0.7, ha='center')
    
    ax.set_xlabel('\nKnowledge Gap Size (% answering incorrectly)', fontsize=11)
    ax.set_ylabel('Impact on Debt Distress (Risk Ratio)\n', fontsize=11)
    ax.set_title('Intervention Priority Matrix\nWhere to Focus Financial Education Efforts', 
                 fontsize=12, fontweight='bold', color=PRIMARY)
    
    plt.colorbar(scatter, label='Risk Ratio')
    plt.tight_layout()
    plt.savefig('viz_quadrant_priority.png', dpi=300, bbox_inches='tight')
    print("Saved: viz_quadrant_priority.png")
    plt.close()

def create_state_map_data(state_results):
    """Create data file for state-level visualization."""
    
    if state_results is None:
        print("No state data available for map")
        return
    
    # Export for use with mapping tools
    state_results.to_csv('state_map_data.csv')
    print("Saved: state_map_data.csv (use with Plotly/Tableau for mapping)")

def create_executive_summary_slide(gap_results):
    """Create a summary visualization for presentations."""
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Panel 1: Top 3 Priority Gaps
    ax1 = axes[0]
    top3 = gap_results.head(3)
    colors = [DANGER, '#ed8936', '#ecc94b']
    bars = ax1.barh(range(3), top3['Risk Ratio'], color=colors)
    ax1.set_yticks(range(3))
    ax1.set_yticklabels(top3['Knowledge Area'])
    ax1.set_xlabel('Risk Ratio')
    ax1.set_title('Top 3 Priority\nKnowledge Gaps', fontweight='bold', color=PRIMARY)
    for bar, val in zip(bars, top3['Risk Ratio']):
        ax1.text(val + 0.02, bar.get_y() + bar.get_height()/2, 
                f'{val:.2f}x', va='center', fontsize=10)
    
    # Panel 2: Overall Accuracy Distribution
    ax2 = axes[1]
    ax2.pie([gap_results['% Correct'].mean(), 100 - gap_results['% Correct'].mean()],
            labels=['Correct', 'Incorrect'],
            colors=[SUCCESS, DANGER],
            autopct='%1.0f%%',
            startangle=90,
            explode=[0.05, 0])
    ax2.set_title('Average Financial\nKnowledge Score', fontweight='bold', color=PRIMARY)
    
    # Panel 3: Key Insight Box
    ax3 = axes[2]
    ax3.axis('off')
    
    top_gap = gap_results.iloc[0]
    insight_text = f"""
KEY FINDING

People who lack knowledge about
{top_gap['Knowledge Area']} are 
{top_gap['Risk Ratio']:.1f}x more likely to 
experience debt distress.

Only {top_gap['% Correct']:.0f}% of Americans
answer this correctly.

RECOMMENDATION:
Prioritize education on
{', '.join(gap_results.head(3)['Knowledge Area'].tolist())}
"""
    ax3.text(0.1, 0.5, insight_text, fontsize=11, 
             verticalalignment='center',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    ax3.set_title('Actionable Insight', fontweight='bold', color=PRIMARY)
    
    plt.suptitle('Financial Literacy-Debt Nexus: Executive Summary', 
                 fontsize=14, fontweight='bold', y=1.02, color=PRIMARY)
    plt.tight_layout()
    plt.savefig('viz_executive_summary.png', dpi=300, bbox_inches='tight')
    print("Saved: viz_executive_summary.png")
    plt.close()

def main():
    """Generate all visualizations."""
    print("="*60)
    print("GENERATING VISUALIZATIONS")
    print("="*60)
    
    # Try to load results from analysis
    try:
        gap_results = pd.read_csv('knowledge_gap_analysis.csv')
        print(f"Loaded knowledge gap analysis ({len(gap_results)} knowledge areas)")
    except FileNotFoundError:
        print("ERROR: Run financial_literacy_analysis.py first!")
        print("Creating sample data for demonstration...")
        
        # Create sample data for demonstration
        gap_results = pd.DataFrame({
            'Knowledge Area': ['Compound Interest', 'Inflation', 'Bond Prices', 
                              'Mortgage Terms', 'Risk Diversification', 'Stock Knowledge', 'Numeracy'],
            'Variable': ['M6', 'M7', 'M8', 'M9', 'M10', 'M31', 'M4'],
            '% Correct': [34, 58, 28, 75, 52, 48, 83],
            'Distress Rate (Wrong)': [42, 38, 40, 35, 39, 37, 32],
            'Distress Rate (Right)': [24, 28, 26, 29, 27, 28, 30],
            'Risk Ratio': [1.75, 1.36, 1.54, 1.21, 1.44, 1.32, 1.07]
        })
        gap_results = gap_results.sort_values('Risk Ratio', ascending=False)
        gap_results.to_csv('knowledge_gap_analysis.csv', index=False)
        print("Sample data created!")
    
    try:
        state_results = pd.read_csv('state_analysis.csv', index_col=0)
    except:
        state_results = None
    
    # Generate all visualizations
    create_knowledge_gap_heatmap(gap_results)
    create_risk_ratio_chart(gap_results)
    create_accuracy_chart(gap_results)
    create_quadrant_plot(gap_results)
    create_executive_summary_slide(gap_results)
    create_state_map_data(state_results)
    
    print("\n" + "="*60)
    print("ALL VISUALIZATIONS GENERATED!")
    print("="*60)
    print("\nOutput files:")
    print("  - viz_knowledge_gap_heatmap.png")
    print("  - viz_risk_ratio_chart.png")  
    print("  - viz_accuracy_chart.png")
    print("  - viz_quadrant_priority.png")
    print("  - viz_executive_summary.png")
    print("  - state_map_data.csv")

if __name__ == "__main__":
    main()
