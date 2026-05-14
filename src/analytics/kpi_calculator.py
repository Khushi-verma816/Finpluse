import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class KPICalculator:
    """Advanced KPI Calculator for Fintech Analytics"""

    def __init__(self, data):
        self.data = data

    def calculate_transaction_volume(self, period='all'):
        """Calculate Total Transaction Volume"""
        if period == 'monthly':
            return self.data.groupby(['Year', 'Month'])['Transaction_count'].sum()
        elif period == 'quarterly':
            return self.data.groupby(['Year', 'Quarter'])['Transaction_count'].sum()
        else:
            return self.data['Transaction_count'].sum()

    def calculate_transaction_value(self, period='all'):
        """Calculate Total Transaction Value"""
        if period == 'monthly':
            return self.data.groupby(['Year', 'Month'])['Transaction_amount'].sum()
        elif period == 'quarterly':
            return self.data.groupby(['Year', 'Quarter'])['Transaction_amount'].sum()
        else:
            return self.data['Transaction_amount'].sum()

    def calculate_avg_transaction_value(self):
        """Calculate Average Transaction Value"""
        return self.data['Transaction_amount'].sum() / self.data['Transaction_count'].sum()

    def calculate_growth_rate(self, period='monthly', growth_type='percentage'):
        """Calculate Growth Rates"""
        if period == 'monthly':
            grouped = self.data.groupby(['Year', 'Month'])['Transaction_amount'].sum()
        else:  # quarterly
            grouped = self.data.groupby(['Year', 'Quarter'])['Transaction_amount'].sum()

        growth = grouped.pct_change() * 100 if growth_type == 'percentage' else grouped.pct_change()
        return growth

    def calculate_active_users(self):
        """Estimate Active Users (simplified)"""
        # Assuming transaction count correlates with unique users
        return self.data['Transaction_count'].sum() * 0.7  # 70% estimation

    def calculate_repeat_users(self):
        """Calculate Repeat User Rate (simplified)"""
        # This would require user-level data in real scenario
        return 0.65  # 65% repeat user rate assumption

    def calculate_success_rate(self):
        """Calculate Transaction Success Rate"""
        # Assuming 98% success rate for digital payments
        return 0.98

    def calculate_merchant_contribution(self):
        """Calculate Merchant Category Contribution"""
        return self.data.groupby('Transaction_type')['Transaction_amount'].sum() / self.data['Transaction_amount'].sum() * 100

    def get_top_states(self, top_n=10):
        """Get Top Performing States"""
        return self.data.groupby('State')['Transaction_amount'].sum().nlargest(top_n)

class BusinessInsights:
    """Business Insights Engine"""

    def __init__(self, data):
        self.data = data
        self.kpi_calc = KPICalculator(data)

    def top_states_by_value(self, top_n=10):
        """Top 10 States by Transaction Value"""
        return self.kpi_calc.get_top_states(top_n)

    def fastest_growing_states(self, periods=6):
        """Identify Fastest Growing States"""
        recent_data = self.data[self.data['Year'] >= 2021]
        growth_rates = {}

        for state in recent_data['State'].unique():
            state_data = recent_data[recent_data['State'] == state]
            if len(state_data) >= periods:
                growth = state_data['Transaction_amount'].pct_change(periods=periods).iloc[-1]
                growth_rates[state] = growth * 100

        return sorted(growth_rates.items(), key=lambda x: x[1], reverse=True)[:10]

    def highest_digital_adoption_states(self):
        """States with Highest Digital Adoption"""
        adoption_metrics = self.data.groupby('State').agg({
            'Transaction_count': 'sum',
            'Transaction_amount': 'sum'
        })

        # Calculate adoption score (transactions per capita estimation)
        adoption_metrics['adoption_score'] = adoption_metrics['Transaction_count'] / 1000000  # Normalized
        return adoption_metrics.nlargest(10, 'adoption_score')

    def most_used_payment_categories(self):
        """Most Used Payment Categories"""
        return self.kpi_calc.calculate_merchant_contribution().nlargest(5)

    def quarter_over_quarter_growth(self):
        """QoQ Growth Analysis"""
        quarterly_data = self.data.groupby(['Year', 'Quarter'])['Transaction_amount'].sum()
        return quarterly_data.pct_change() * 100

    def user_growth_analysis(self):
        """User Growth Trends"""
        user_growth = self.data.groupby(['Year', 'Quarter'])['Transaction_count'].sum()
        return user_growth.pct_change() * 100

    def revenue_trend_insights(self):
        """Revenue Trend Analysis"""
        monthly_revenue = self.data.groupby(['Year', 'Month'])['Transaction_amount'].sum()
        return {
            'trend': monthly_revenue.pct_change().mean() * 100,
            'volatility': monthly_revenue.pct_change().std() * 100,
            'peak_month': monthly_revenue.idxmax(),
            'growth_acceleration': monthly_revenue.pct_change().diff().mean()
        }

    def generate_business_recommendations(self):
        """Generate AI-powered Business Recommendations"""
        insights = []

        # Growth recommendations
        qoq_growth = self.quarter_over_quarter_growth()
        if qoq_growth.iloc[-1] > 10:
            insights.append("🚀 Strong QoQ growth detected. Consider expanding marketing in high-growth regions.")

        # State-specific recommendations
        top_states = self.top_states_by_value(5).index.tolist()
        insights.append(f"📍 Focus expansion efforts in top states: {', '.join(top_states[:3])}")

        # Category recommendations
        top_categories = self.most_used_payment_categories().index.tolist()
        insights.append(f"💳 Prioritize development for categories: {', '.join(top_categories[:3])}")

        return insights