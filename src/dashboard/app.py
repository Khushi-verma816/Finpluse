import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Import our custom modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analytics.kpi_calculator import KPICalculator, BusinessInsights
from analytics.fraud_detection import FraudDetectionEngine
from analytics.time_series import TimeSeriesAnalyzer
from dashboard.components import DashboardComponents

class FinPulseDashboard:
    """Main FinPulse Analytics Dashboard Application"""

    def __init__(self):
        st.set_page_config(
            page_title="FinPulse Analytics Platform",
            page_icon="FP",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # Initialize session state
        self.initialize_session_state()

        # Load data (in real implementation, this would connect to database)
        self.load_sample_data()

        # Initialize analytics engines
        self.kpi_calc = KPICalculator(self.data)
        self.business_insights = BusinessInsights(self.data)
        self.fraud_detector = FraudDetectionEngine(self.data)
        self.time_series_analyzer = TimeSeriesAnalyzer(self.data)

    def initialize_session_state(self):
        """Initialize Streamlit session state"""
        if 'theme' not in st.session_state:
            st.session_state.theme = 'dark'
        if 'sidebar_state' not in st.session_state:
            st.session_state.sidebar_state = 'expanded'

    def load_sample_data(self):
        """Load sample data for demonstration"""
        # Create sample transaction data
        np.random.seed(42)
        dates = pd.date_range('2020-01-01', '2023-12-31', freq='M')

        states = ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Uttar Pradesh',
                 'Gujarat', 'Rajasthan', 'Punjab', 'Haryana', 'Delhi', 'West Bengal']

        transaction_types = ['Peer-to-peer payments', 'Merchant payments',
                           'Financial Services', 'Recharge & bill payments', 'Others']

        data = []
        for date in dates:
            for state in states:
                for tx_type in transaction_types:
                    count = np.random.randint(1000, 50000)
                    amount = count * np.random.uniform(50, 500)
                    data.append({
                        'Year': date.year,
                        'Month': date.month,
                        'Quarter': (date.month - 1) // 3 + 1,
                        'State': state,
                        'Transaction_type': tx_type,
                        'Transaction_count': count,
                        'Transaction_amount': amount
                    })

        self.data = pd.DataFrame(data)

    def apply_theme(self):
        """Apply custom theme based on session state"""
        if st.session_state.theme == 'dark':
            st.markdown("""
            <style>
            body, .stApp, .main, .block-container, [data-testid="stAppViewContainer"] {
                background-color: #061225 !important;
                color: #E9F1FF !important;
            }
            [data-testid="stSidebar"] > div {
                background: linear-gradient(180deg, #081A33 0%, #0E2B54 100%) !important;
                color: #F1F8FF !important;
            }
            .css-1emrehy.edgvbvh3, .css-1d391kg, .css-145kmo2 {
                background: transparent !important;
            }
            .stButton>button {
                background-color: #3F7DFE !important;
                color: white !important;
                border-radius: 10px !important;
                border: none !important;
            }
            .stRadio>div label,
            .stMarkdown h1,
            .stMarkdown h2,
            .stMarkdown h3,
            .stMarkdown p,
            .stText {
                color: #E9F1FF !important;
            }
            .stTextInput>div>div>input,
            .stSelectbox>div>div>div>div,
            .stDateInput>div>div>input,
            .stMultiSelect {
                background-color: #0D203D !important;
                color: #E9F1FF !important;
                border: 1px solid #3F7DFE !important;
            }
            .stSelectbox>div>div>div>div:hover,
            .stTextInput>div>div>input:focus {
                border-color: #7FA7FF !important;
            }
            .stRadio>div label:hover {
                color: #A6C8FF !important;
            }
            .css-1sb8s9s.edgvbvh3 {
                background-color: #0D203D !important;
            }
            </style>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <style>
            :root {
                --fp-bg: #F4F7FB;
                --fp-surface: #FFFFFF;
                --fp-input-bg: #FFFFFF;
                --fp-border: #D7E0EC;
                --fp-text: #102A43;
                --fp-muted: #486581;
                --fp-sidebar-text: #1F3A56;
                --fp-primary: #1D4ED8;
                --fp-primary-hover: #1E40AF;
                --fp-hover-bg: #EAF2FF;
            }
            body, .stApp, .main, .block-container, [data-testid="stAppViewContainer"] {
                background-color: var(--fp-bg) !important;
                color: var(--fp-text) !important;
            }
            .block-container {
                padding: 2rem 2rem 3rem 2rem !important;
            }
            [data-testid="stHeader"] {
                background-color: #0A1324 !important;
                border-bottom: 1px solid #0A1324 !important;
            }
            [data-testid="stHeader"] * {
                color: #FFFFFF !important;
            }
            [data-testid="stSidebar"] > div {
                background: linear-gradient(180deg, #F8FBFF 0%, #ECF3FF 100%) !important;
                color: var(--fp-sidebar-text) !important;
                border-right: 1px solid var(--fp-border) !important;
                box-shadow: 2px 0 16px rgba(16, 42, 67, 0.08) !important;
            }
            [data-testid="stSidebar"] * {
                color: var(--fp-sidebar-text) !important;
            }
            [data-testid="stSidebar"] hr {
                border-color: var(--fp-border) !important;
            }
            .stMarkdown h1,
            .stMarkdown h2,
            .stMarkdown h3,
            .stMarkdown h4,
            .stMarkdown p,
            .stText,
            .st-emotion-cache-10trblm,
            .st-emotion-cache-16txtl3 {
                color: var(--fp-text) !important;
            }
            .stButton > button {
                background-color: var(--fp-primary) !important;
                color: #FFFFFF !important;
                border-radius: 12px !important;
                border: 1px solid transparent !important;
                box-shadow: 0 10px 24px rgba(29, 78, 216, 0.2) !important;
                font-weight: 600 !important;
            }
            .stButton > button:hover {
                background-color: var(--fp-primary-hover) !important;
            }
            [data-testid="stSidebar"] .stButton > button {
                background-color: var(--fp-primary) !important;
                color: #FFFFFF !important;
                border: 1px solid transparent !important;
                box-shadow: 0 10px 24px rgba(29, 78, 216, 0.2) !important;
            }
            [data-testid="stSidebar"] .stButton > button:hover {
                background-color: var(--fp-primary-hover) !important;
            }
            [data-testid="stSidebar"] div[role="radiogroup"] > label {
                border-radius: 10px !important;
                padding: 0.35rem 0.5rem !important;
                margin-bottom: 0.2rem !important;
                transition: all 0.2s ease !important;
                border-left: 3px solid transparent !important;
            }
            [data-testid="stSidebar"] div[role="radiogroup"] > label > div {
                color: var(--fp-sidebar-text) !important;
                font-weight: 500 !important;
            }
            [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
                background-color: var(--fp-hover-bg) !important;
            }
            [data-testid="stSidebar"] div[role="radiogroup"] > label:hover > div {
                color: var(--fp-primary) !important;
            }
            [data-testid="stSidebar"] div[role="radiogroup"] > label input[type="radio"]:checked + div {
                color: var(--fp-primary) !important;
                font-weight: 600 !important;
                background-color: var(--fp-hover-bg) !important;
                border-radius: 8px !important;
                padding: 0.25rem 0.35rem !important;
            }
            [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input[type="radio"]:checked) {
                background-color: var(--fp-hover-bg) !important;
                border-left-color: var(--fp-primary) !important;
            }
            .stTextInput > div > div > input,
            .stDateInput > div > div > input {
                background-color: var(--fp-input-bg) !important;
                color: var(--fp-text) !important;
                border: 1px solid var(--fp-border) !important;
                border-radius: 12px !important;
            }
            .stSelectbox [data-baseweb="select"] > div,
            .stMultiSelect [data-baseweb="select"] > div {
                background-color: var(--fp-input-bg) !important;
                color: var(--fp-text) !important;
                border: 1px solid var(--fp-border) !important;
                border-radius: 12px !important;
            }
            .stTextInput > div > div > input:focus,
            .stDateInput > div > div:focus-within,
            .stSelectbox [data-baseweb="select"] > div:focus-within,
            .stMultiSelect [data-baseweb="select"] > div:focus-within {
                border-color: var(--fp-primary) !important;
                box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.14) !important;
            }
            .stDateInput > div > div,
            .stSelectbox > div > div,
            .stMultiSelect > div > div {
                background: transparent !important;
            }
            .stDateInput > div > div > input {
                background-color: var(--fp-input-bg) !important;
            }
            .stDateInput > div > div:focus-within,
            .stSelectbox > div > div:focus-within,
            .stMultiSelect > div > div:focus-within {
                border-color: var(--fp-primary) !important;
                box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.14) !important;
            }
            [data-baseweb="tag"] {
                background-color: #DBEAFE !important;
                border: 1px solid #BFDBFE !important;
                color: #1D4ED8 !important;
                border-radius: 8px !important;
            }
            [data-baseweb="tag"] * {
                color: #1D4ED8 !important;
            }
            [data-baseweb="tag"] button {
                color: #1D4ED8 !important;
                background: transparent !important;
            }
            [data-baseweb="tag"] button:hover {
                color: #1E40AF !important;
                background: #DBEAFE !important;
            }
            [data-testid="metric-container"] {
                background: var(--fp-surface) !important;
                border: 1px solid var(--fp-border) !important;
                border-radius: 14px !important;
                box-shadow: 0 8px 20px rgba(16, 42, 67, 0.08) !important;
                padding: 0.8rem 1rem !important;
            }
            [data-testid="metric-container"] label,
            [data-testid="metric-container"] [data-testid="stMetricLabel"] {
                color: var(--fp-muted) !important;
                font-weight: 600 !important;
            }
            [data-testid="stMetricLabel"] *,
            [data-testid="stMetricLabel"] p {
                color: var(--fp-muted) !important;
            }
            [data-testid="metric-container"] [data-testid="stMetricValue"] {
                color: var(--fp-text) !important;
                font-weight: 700 !important;
            }
            [data-testid="stMetricValue"] *,
            [data-testid="stMetricValue"] div {
                color: var(--fp-text) !important;
            }
            [data-testid="stMetricDelta"] * {
                color: #0F766E !important;
            }
            [data-testid="stPlotlyChart"],
            [data-testid="stDataFrame"] {
                background: var(--fp-surface) !important;
                border: 1px solid var(--fp-border) !important;
                border-radius: 14px !important;
                box-shadow: 0 8px 20px rgba(16, 42, 67, 0.07) !important;
                padding: 0.35rem !important;
            }
            .stAlert {
                border-radius: 12px !important;
                border: 1px solid var(--fp-border) !important;
            }
            .stAlert, [data-testid="stAlert"] {
                background-color: #E0F2FE !important;
                color: #0369A1 !important;
                border: 1px solid #BAE6FD !important;
            }
            .stAlert h4, [data-testid="stAlert"] h4,
            .stAlert p, [data-testid="stAlert"] p,
            .stAlert div, [data-testid="stAlert"] div {
                color: #0369A1 !important;
            }
            .stInfo, [data-testid="stInfo"] {
                background-color: #E0F2FE !important;
                color: #0369A1 !important;
                border: 1px solid #BAE6FD !important;
            }
            .stInfo h4, [data-testid="stInfo"] h4,
            .stInfo p, [data-testid="stInfo"] p,
            .stInfo div, [data-testid="stInfo"] div {
                color: #0369A1 !important;
            }
            .stSuccess, [data-testid="stSuccess"] {
                background-color: #E0F2FE !important;
                color: #0369A1 !important;
                border: 1px solid #BAE6FD !important;
            }
            .stSuccess h4, [data-testid="stSuccess"] h4,
            .stSuccess p, [data-testid="stSuccess"] p,
            .stSuccess div, [data-testid="stSuccess"] div {
                color: #0369A1 !important;
            }
            .stWarning, [data-testid="stWarning"] {
                background-color: #E0F2FE !important;
                color: #0369A1 !important;
                border: 1px solid #BAE6FD !important;
            }
            .stWarning h4, [data-testid="stWarning"] h4,
            .stWarning p, [data-testid="stWarning"] p,
            .stWarning div, [data-testid="stWarning"] div {
                color: #0369A1 !important;
            }
            .css-1nmdi4k.edgvbvh3,
            .css-1rlr5ld.e16nr0p32,
            .css-1d391kg,
            .css-145kmo2 {
                background-color: transparent !important;
            }
            </style>
            """, unsafe_allow_html=True)

    def create_sidebar(self):
        """Create professional sidebar with navigation"""
        with st.sidebar:
            st.title("FinPulse Analytics")

            # Theme toggle
            theme_col1, theme_col2 = st.columns(2)
            with theme_col1:
                toggle_label = "Dark" if st.session_state.theme == 'light' else "Light"
                if st.button(toggle_label, key="theme_toggle_button"):
                    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
                    st.rerun()

            # Navigation menu
            st.markdown("---")
            selected_page = st.radio(
                "Navigation",
                ["Overview", "KPIs Dashboard", "Business Insights",
                 "Time Series Analysis", "Fraud Detection", "Reports"],
                label_visibility="collapsed"
            )

            # Filters section
            st.markdown("---")
            st.markdown("### Filters")

            # Date range filter
            date_range = st.date_input(
                "Date Range",
                value=(datetime(2020, 1, 1), datetime(2023, 12, 31)),
                key="date_filter"
            )

            # State filter
            selected_states = st.multiselect(
                "States",
                options=self.data['State'].unique(),
                default=self.data['State'].unique()[:5],
                key="state_filter"
            )

            # Transaction type filter
            selected_types = st.multiselect(
                "Transaction Types",
                options=self.data['Transaction_type'].unique(),
                default=self.data['Transaction_type'].unique(),
                key="type_filter"
            )

            return selected_page, date_range, selected_states, selected_types

    def filter_data(self, date_range, selected_states, selected_types):
        """Apply filters to data"""
        filtered_data = self.data.copy()

        # Date filter
        start_date, end_date = date_range
        filtered_data = filtered_data[
            (filtered_data['Year'] >= start_date.year) &
            (filtered_data['Year'] <= end_date.year)
        ]

        # State filter
        if selected_states:
            filtered_data = filtered_data[filtered_data['State'].isin(selected_states)]

        # Type filter
        if selected_types:
            filtered_data = filtered_data[filtered_data['Transaction_type'].isin(selected_types)]

        return filtered_data

    def show_overview_page(self):
        """Display overview dashboard"""
        st.title("FinPulse Analytics Overview")

        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_volume = self.kpi_calc.calculate_transaction_volume()
            st.metric("Total Transactions", f"{total_volume:,.0f}")

        with col2:
            total_value = self.kpi_calc.calculate_transaction_value()
            st.metric("Total Value", f"Rs {total_value/1e9:.1f}B")

        with col3:
            avg_value = self.kpi_calc.calculate_avg_transaction_value()
            st.metric("Avg Transaction", f"Rs {avg_value:.0f}")

        with col4:
            success_rate = self.kpi_calc.calculate_success_rate() * 100
            st.metric("Success Rate", f"{success_rate:.1f}%")

        # Charts row
        col1, col2 = st.columns(2)

        with col1:
            # Transaction volume by state
            state_volume = self.data.groupby('State')['Transaction_count'].sum().nlargest(10)
            fig = DashboardComponents.create_advanced_chart(
                state_volume.reset_index(),
                chart_type="bar",
                x="State",
                y="Transaction_count",
                title="Top 10 States by Transaction Volume"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Transaction types distribution
            type_distribution = self.data.groupby('Transaction_type')['Transaction_amount'].sum()
            is_light_theme = st.session_state.get("theme", "dark") == "light"
            chart_template = "plotly_white" if is_light_theme else "plotly_dark"
            title_color = "#102A43" if is_light_theme else "#E9F1FF"
            legend_color = "#334155" if is_light_theme else "#D5E5FF"
            fig = px.pie(
                type_distribution.reset_index(),
                values='Transaction_amount',
                names='Transaction_type',
                title='Transaction Types Distribution',
                template=chart_template,
                color_discrete_sequence=['#3B82F6', '#60A5FA', '#22C55E', '#F59E0B', '#EF4444']
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title_font_color=title_color,
                legend_font_color=legend_color,
                font_color=legend_color
            )
            st.plotly_chart(fig, use_container_width=True)

    def show_kpi_dashboard(self):
        """Display advanced KPI dashboard"""
        st.title("Advanced KPIs Dashboard")

        kpis_data = [
            {
                'title': 'Total Transaction Volume',
                'value': self.kpi_calc.calculate_transaction_volume(),
                'icon': 'VOL'
            },
            {
                'title': 'Total Transaction Value',
                'value': self.kpi_calc.calculate_transaction_value(),
                'icon': 'VAL'
            },
            {
                'title': 'Average Transaction Value',
                'value': self.kpi_calc.calculate_avg_transaction_value(),
                'icon': 'AVG'
            },
            {
                'title': 'Monthly Growth %',
                'value': self.kpi_calc.calculate_growth_rate('monthly').iloc[-1] if len(self.kpi_calc.calculate_growth_rate('monthly')) > 0 else 0,
                'change': self.kpi_calc.calculate_growth_rate('monthly').iloc[-1] if len(self.kpi_calc.calculate_growth_rate('monthly')) > 0 else 0,
                'icon': 'GRW'
            },
            {
                'title': 'Active Users',
                'value': self.kpi_calc.calculate_active_users(),
                'icon': 'USR'
            },
            {
                'title': 'Transaction Success Rate',
                'value': self.kpi_calc.calculate_success_rate() * 100,
                'icon': 'SUC'
            }
        ]

        DashboardComponents.create_metric_grid(kpis_data)

        st.markdown("### Detailed KPI Analysis")

        col1, col2 = st.columns(2)

        with col1:
            monthly_growth = self.kpi_calc.calculate_growth_rate('monthly')
            monthly_growth_df = monthly_growth.reset_index()
            monthly_growth_df['Date'] = pd.to_datetime(
                monthly_growth_df['Year'].astype(str) + '-' +
                monthly_growth_df['Month'].astype(str) + '-01'
            )
            fig = DashboardComponents.create_advanced_chart(
                monthly_growth_df,
                chart_type="line",
                x="Date",
                y="Transaction_amount",
                title="Monthly Growth Trend"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            top_states = self.kpi_calc.get_top_states(10)
            fig = DashboardComponents.create_advanced_chart(
                top_states.reset_index(),
                chart_type="bar",
                x="State",
                y="Transaction_amount",
                title="Top 10 States by Transaction Value"
            )
            st.plotly_chart(fig, use_container_width=True)

    def show_business_insights(self):
        """Display business insights page"""
        st.title("Business Insights")

        # Key insights
        insights = self.business_insights.generate_business_recommendations()

        st.markdown("### AI-Generated Business Recommendations")
        for insight in insights:
            st.info(insight)

        # Insights grid
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Top 10 States by Value")
            top_states = self.business_insights.top_states_by_value(10)
            st.dataframe(top_states.reset_index(), use_container_width=True)

            st.markdown("#### Most Used Payment Categories")
            categories = self.business_insights.most_used_payment_categories()
            is_light_theme = st.session_state.get("theme", "dark") == "light"
            chart_template = "plotly_white" if is_light_theme else "plotly_dark"
            chart_text = "#102A43" if is_light_theme else "#E9F1FF"
            fig = px.bar(
                categories.reset_index(),
                x='Transaction_type',
                y='Transaction_amount',
                title='Payment Categories Usage',
                template=chart_template
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title_font_color=chart_text,
                font_color=chart_text
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Fastest Growing States")
            growing_states = self.business_insights.fastest_growing_states()
            growth_df = pd.DataFrame(growing_states, columns=['State', 'Growth_Rate'])
            st.dataframe(growth_df, use_container_width=True)

            st.markdown("#### Quarter-over-Quarter Growth")
            qoq_growth = self.business_insights.quarter_over_quarter_growth()
            qoq_growth_df = qoq_growth.reset_index()
            qoq_growth_df['Month'] = (qoq_growth_df['Quarter'] * 3).astype(int).astype(str).str.zfill(2)
            qoq_growth_df['Date'] = pd.to_datetime(
                qoq_growth_df['Year'].astype(str) + '-' + qoq_growth_df['Month'] + '-01'
            )
            fig = DashboardComponents.create_advanced_chart(
                qoq_growth_df,
                chart_type="line",
                x="Date",
                y="Transaction_amount",
                title="QoQ Growth Trend"
            )
            st.plotly_chart(fig, use_container_width=True)

    def show_time_series_analysis(self):
        """Display time series analysis page"""
        st.title("Time Series Analysis & Forecasting")

        # Forecasting data
        forecast_data = self.time_series_analyzer.get_forecasting_dashboard_data()

        # Key metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            cagr = forecast_data['cagr']
            st.metric("Overall CAGR", f"{cagr:.1f}%")

        with col2:
            monthly_trend = forecast_data['monthly_trends']
            recent_growth = monthly_trend['Transaction_amount'].pct_change().tail(6).mean() * 100
            st.metric("6-Month Growth", f"{recent_growth:.1f}%")

        with col3:
            quarterly_peak = forecast_data['quarterly_trends']['Transaction_amount'].max()
            st.metric("Peak Quarterly Value", f"Rs {quarterly_peak/1e9:.1f}B")

        with col4:
            volatility = forecast_data['monthly_trends']['Transaction_amount'].pct_change().std() * 100
            st.metric("Volatility", f"{volatility:.1f}%")

        # Trend insights
        st.markdown("### Automated Trend Insights")
        for insight in forecast_data['trend_insights']:
            st.success(insight)

        # Forecasting charts
        col1, col2 = st.columns(2)

        with col1:
            # Monthly trends
            fig = DashboardComponents.create_forecast_chart(
                forecast_data['monthly_trends'],
                forecast_data['prophet_forecast'],
                "Transaction Amount Forecast (Prophet)"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Quarterly trends
            quarterly_data = forecast_data['quarterly_trends'].copy()
            quarterly_data['QuarterLabel'] = quarterly_data['Year'].astype(str) + ' Q' + quarterly_data['Quarter'].astype(str)
            fig = DashboardComponents.create_advanced_chart(
                quarterly_data,
                chart_type="area",
                x='QuarterLabel',
                y='Transaction_amount',
                title="Quarterly Transaction Trends"
            )
            st.plotly_chart(fig, use_container_width=True)

    def show_fraud_detection(self):
        """Display fraud detection dashboard"""
        st.title("Fraud Detection & Anomaly Analysis")

        # Fraud alerts
        fraud_data = self.fraud_detector.get_fraud_dashboard_data()

        st.markdown("### Active Fraud Alerts")
        for alert in fraud_data['alerts']:
            st.error(alert)

        # Anomaly analysis
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Unusual High-Value Transactions")
            if not fraud_data['high_value_transactions'].empty:
                st.dataframe(
                    fraud_data['high_value_transactions'][['State', 'Transaction_amount', 'z_score']].head(10),
                    use_container_width=True
                )
            else:
                st.info("No unusual high-value transactions detected")

            st.markdown("#### Transaction Volume Spikes")
            if not fraud_data['transaction_spikes'].empty:
                st.dataframe(
                    fraud_data['transaction_spikes'][['State', 'Transaction_count', 'is_spike']].head(10),
                    use_container_width=True
                )
            else:
                st.info("No transaction spikes detected")

        with col2:
            st.markdown("#### Suspicious State Activity")
            if not fraud_data['suspicious_states'].empty:
                st.dataframe(
                    fraud_data['suspicious_states'][['amount_per_transaction', 'volatility_score']].head(10),
                    use_container_width=True
                )
            else:
                st.info("No suspicious state activity detected")

            st.markdown("#### ML-Detected Anomalies")
            if not fraud_data['ml_anomalies'].empty:
                st.dataframe(
                    fraud_data['ml_anomalies'][['Transaction_amount', 'anomaly_score']].head(10),
                    use_container_width=True
                )
            else:
                st.info("No ML-detected anomalies")

    def show_reports_page(self):
        """Display reports and export functionality"""
        st.title("Reports & Analytics Export")

        st.markdown("### Export Options")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Export KPI Summary"):
                kpi_summary = pd.DataFrame({
                    'Metric': ['Total Volume', 'Total Value', 'Avg Value', 'Success Rate'],
                    'Value': [
                        self.kpi_calc.calculate_transaction_volume(),
                        self.kpi_calc.calculate_transaction_value(),
                        self.kpi_calc.calculate_avg_transaction_value(),
                        self.kpi_calc.calculate_success_rate() * 100
                    ]
                })
                st.markdown(
                    DashboardComponents.create_download_button(
                        kpi_summary, "kpi_summary.csv", "Download KPI Summary"
                    ),
                    unsafe_allow_html=True
                )

        with col2:
            if st.button("Export Business Insights"):
                insights_data = self.business_insights.top_states_by_value(10).reset_index()
                st.markdown(
                    DashboardComponents.create_download_button(
                        insights_data, "business_insights.xlsx", "Download Insights"
                    ),
                    unsafe_allow_html=True
                )

        with col3:
            if st.button("Export Time Series Data"):
                ts_data = self.time_series_analyzer.calculate_monthly_trends()
                st.markdown(
                    DashboardComponents.create_download_button(
                        ts_data, "time_series_data.csv", "Download Time Series"
                    ),
                    unsafe_allow_html=True
                )

        st.markdown("### Generated Reports")

        # Sample report
        st.markdown("""
        #### Monthly Performance Report - December 2023

        **Key Highlights:**
        - Total transactions increased by 15.2% MoM
        - Maharashtra leads with Rs 2.1B in transaction value
        - Digital adoption rate reached 78%
        - Fraud detection flagged 23 suspicious transactions

        **Recommendations:**
        - Focus marketing campaigns in high-growth states
        - Enhance fraud detection algorithms
        - Optimize user experience for peak hours
        """)

    def run(self):
        """Main application runner"""
        # Apply theme
        self.apply_theme()

        # Create sidebar and get filters
        selected_page, date_range, selected_states, selected_types = self.create_sidebar()

        # Filter data
        self.filtered_data = self.filter_data(date_range, selected_states, selected_types)

        # Update analytics engines with filtered data
        self.kpi_calc = KPICalculator(self.filtered_data)
        self.business_insights = BusinessInsights(self.filtered_data)
        self.fraud_detector = FraudDetectionEngine(self.filtered_data)
        self.time_series_analyzer = TimeSeriesAnalyzer(self.filtered_data)

        # Display selected page
        if selected_page == "Overview":
            self.show_overview_page()
        elif selected_page == "KPIs Dashboard":
            self.show_kpi_dashboard()
        elif selected_page == "Business Insights":
            self.show_business_insights()
        elif selected_page == "Time Series Analysis":
            self.show_time_series_analysis()
        elif selected_page == "Fraud Detection":
            self.show_fraud_detection()
        elif selected_page == "Reports":
            self.show_reports_page()

# Run the application
if __name__ == "__main__":
    dashboard = FinPulseDashboard()
    dashboard.run()

