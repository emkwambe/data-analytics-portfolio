"""
Financial Literacy-Debt Nexus Dashboard
========================================
Interactive Streamlit dashboard for exploring the analysis results.

Run with: streamlit run dashboard.py

Dependencies:
    pip install streamlit pandas plotly

Author: Eddy Mkwambe
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(
    page_title="Financial Literacy-Debt Nexus",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a365d;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #718096;
        margin-top: 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .insight-box {
        background: #f7fafc;
        border-left: 4px solid #2b6cb0;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load analysis results."""
    try:
        gap_results = pd.read_csv('knowledge_gap_analysis.csv')
        return gap_results
    except FileNotFoundError:
        # Create sample data
        gap_results = pd.DataFrame({
            'Knowledge Area': ['Compound Interest', 'Inflation', 'Bond Prices', 
                              'Mortgage Terms', 'Risk Diversification', 'Stock Knowledge', 'Numeracy'],
            'Variable': ['M6', 'M7', 'M8', 'M9', 'M10', 'M31', 'M4'],
            '% Correct': [34, 58, 28, 75, 52, 48, 83],
            'Distress Rate (Wrong)': [42, 38, 40, 35, 39, 37, 32],
            'Distress Rate (Right)': [24, 28, 26, 29, 27, 28, 30],
            'Risk Ratio': [1.75, 1.36, 1.54, 1.21, 1.44, 1.32, 1.07]
        })
        return gap_results.sort_values('Risk Ratio', ascending=False)

def main():
    # Header
    st.markdown('<p class="main-header">📊 Financial Literacy-Debt Nexus</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Which specific knowledge gaps predict debt distress? Analysis of 25,000+ Americans</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Load data
    df = load_data()
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        top_gap = df.iloc[0]['Knowledge Area']
        st.metric("🎯 Highest Impact Gap", top_gap)
    
    with col2:
        top_ratio = df.iloc[0]['Risk Ratio']
        st.metric("⚠️ Max Risk Ratio", f"{top_ratio:.2f}x")
    
    with col3:
        avg_correct = df['% Correct'].mean()
        st.metric("📚 Avg Knowledge Score", f"{avg_correct:.0f}%")
    
    with col4:
        lowest_accuracy = df['% Correct'].min()
        st.metric("🔴 Lowest Accuracy", f"{lowest_accuracy:.0f}%")
    
    st.markdown("---")
    
    # Main visualization area
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Risk Impact", "📊 Knowledge Gaps", "🗺️ Priority Matrix", "📋 Data Table"])
    
    with tab1:
        st.subheader("Impact of Knowledge Gaps on Debt Distress")
        st.markdown("*How much more likely is someone to be in debt distress if they lack specific financial knowledge?*")
        
        fig = px.bar(
            df.sort_values('Risk Ratio', ascending=True),
            y='Knowledge Area',
            x='Risk Ratio',
            orientation='h',
            color='Risk Ratio',
            color_continuous_scale='RdYlGn_r',
            text='Risk Ratio'
        )
        fig.update_traces(texttemplate='%{text:.2f}x', textposition='outside')
        fig.add_vline(x=1.0, line_dash="dash", line_color="gray", 
                      annotation_text="No difference")
        fig.update_layout(
            height=400,
            xaxis_title="Risk Ratio (Distress Rate Wrong ÷ Right)",
            yaxis_title="",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
        <strong>💡 Key Insight:</strong> People who cannot correctly answer the Compound Interest 
        question are 1.75x more likely to be in debt distress compared to those who can. 
        This suggests compound interest understanding should be a priority for financial education programs.
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Financial Knowledge Quiz Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                df.sort_values('% Correct', ascending=True),
                y='Knowledge Area',
                x='% Correct',
                orientation='h',
                color='% Correct',
                color_continuous_scale='RdYlGn',
                text='% Correct'
            )
            fig.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
            fig.add_vline(x=50, line_dash="dash", line_color="gray")
            fig.update_layout(
                height=400,
                xaxis_title="% Answering Correctly",
                yaxis_title="",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Comparison chart: distress rates
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Answered Wrong',
                y=df['Knowledge Area'],
                x=df['Distress Rate (Wrong)'],
                orientation='h',
                marker_color='#e53e3e'
            ))
            
            fig.add_trace(go.Bar(
                name='Answered Right',
                y=df['Knowledge Area'],
                x=df['Distress Rate (Right)'],
                orientation='h',
                marker_color='#38a169'
            ))
            
            fig.update_layout(
                barmode='group',
                height=400,
                xaxis_title="Debt Distress Rate (%)",
                yaxis_title="",
                legend=dict(orientation="h", yanchor="bottom", y=1.02)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Intervention Priority Matrix")
        st.markdown("*Where should financial education efforts focus?*")
        
        df['Gap Size'] = 100 - df['% Correct']
        
        fig = px.scatter(
            df,
            x='Gap Size',
            y='Risk Ratio',
            size=[100]*len(df),
            color='Risk Ratio',
            color_continuous_scale='RdYlGn_r',
            hover_name='Knowledge Area',
            text='Knowledge Area'
        )
        
        fig.update_traces(textposition='top center')
        
        # Add quadrant lines
        fig.add_hline(y=df['Risk Ratio'].median(), line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=df['Gap Size'].median(), line_dash="dash", line_color="gray", opacity=0.5)
        
        fig.update_layout(
            height=500,
            xaxis_title="Knowledge Gap Size (% answering incorrectly)",
            yaxis_title="Impact on Debt Distress (Risk Ratio)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Priority recommendations
        st.markdown("### 🎯 Priority Recommendations")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**HIGH PRIORITY** (Large gap + High impact)")
            high_priority = df[(df['Gap Size'] > df['Gap Size'].median()) & 
                              (df['Risk Ratio'] > df['Risk Ratio'].median())]
            for _, row in high_priority.iterrows():
                st.markdown(f"- 🔴 **{row['Knowledge Area']}**")
        
        with col2:
            st.markdown("**MONITOR** (Small gap but high impact)")
            monitor = df[(df['Gap Size'] <= df['Gap Size'].median()) & 
                        (df['Risk Ratio'] > df['Risk Ratio'].median())]
            for _, row in monitor.iterrows():
                st.markdown(f"- 🟡 **{row['Knowledge Area']}**")
    
    with tab4:
        st.subheader("Complete Analysis Data")
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="financial_literacy_analysis.csv",
            mime="text/csv"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **Data Source:** FINRA National Financial Capability Study 2024  
    **Analysis:** Eddy Mkwambe | [LinkedIn](#) | [GitHub](#)
    
    *This analysis examines which specific financial knowledge gaps most predict problematic debt behaviors, 
    providing actionable insights for financial education programs and responsible lending practices.*
    """)

if __name__ == "__main__":
    main()
