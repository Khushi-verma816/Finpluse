import pandas as pd
import numpy as np
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

class TimeSeriesAnalyzer:
    """Advanced Time Series Analysis Engine"""

    def __init__(self, data):
        self.data = data
        self.prepare_time_series_data()

    def prepare_time_series_data(self):
        """Prepare data for time series analysis"""
        # Create date column
        self.data['Date'] = pd.to_datetime(
            self.data['Year'].astype(str) + '-' +
            (self.data['Quarter'] * 3).astype(str) + '-01'
        )

        # Aggregate by date
        self.ts_data = self.data.groupby('Date').agg({
            'Transaction_amount': 'sum',
            'Transaction_count': 'sum'
        }).reset_index()

        # Sort by date
        self.ts_data = self.ts_data.sort_values('Date')

    def calculate_monthly_trends(self):
        """Calculate monthly transaction trends"""
        monthly_data = self.data.groupby(['Year', 'Month']).agg({
            'Transaction_amount': 'sum',
            'Transaction_count': 'sum'
        }).reset_index()

        monthly_data['Date'] = pd.to_datetime(
            monthly_data['Year'].astype(str) + '-' +
            monthly_data['Month'].astype(str) + '-01'
        )

        return monthly_data.sort_values('Date')

    def calculate_quarterly_trends(self):
        """Calculate quarterly transaction trends"""
        quarterly_data = self.data.groupby(['Year', 'Quarter']).agg({
            'Transaction_amount': 'sum',
            'Transaction_count': 'sum'
        }).reset_index()

        return quarterly_data.sort_values(['Year', 'Quarter'])

    def calculate_cagr(self, start_year=None, end_year=None):
        """Calculate Compound Annual Growth Rate"""
        if start_year is None:
            start_year = self.data['Year'].min()
        if end_year is None:
            end_year = self.data['Year'].max()

        start_value = self.data[self.data['Year'] == start_year]['Transaction_amount'].sum()
        end_value = self.data[self.data['Year'] == end_year]['Transaction_amount'].sum()

        if start_value == 0:
            return 0

        years = end_year - start_year
        cagr = (end_value / start_value) ** (1 / years) - 1

        return cagr * 100  # Return as percentage

    def calculate_rolling_averages(self, window=3):
        """Calculate rolling averages"""
        self.ts_data[f'rolling_avg_{window}m'] = self.ts_data['Transaction_amount'].rolling(window=window).mean()
        self.ts_data[f'rolling_std_{window}m'] = self.ts_data['Transaction_amount'].rolling(window=window).std()

        return self.ts_data

    def prophet_forecasting(self, periods=12):
        """Prophet-based forecasting"""
        # Prepare data for Prophet
        prophet_data = self.ts_data[['Date', 'Transaction_amount']].copy()
        prophet_data.columns = ['ds', 'y']

        # Initialize and fit Prophet model
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            changepoint_prior_scale=0.05
        )

        model.fit(prophet_data)

        # Create future dataframe
        future = model.make_future_dataframe(periods=periods, freq='M')

        # Generate forecast
        forecast = model.predict(future)

        return forecast, model

    def arima_forecasting(self, periods=12):
        """ARIMA-based forecasting"""
        try:
            # Fit ARIMA model
            model = ARIMA(self.ts_data['Transaction_amount'], order=(1, 1, 1))
            model_fit = model.fit()

            # Generate forecast
            forecast = model_fit.forecast(steps=periods)

            return forecast, model_fit
        except:
            # Fallback to simple exponential smoothing
            return self.exponential_smoothing_forecasting(periods)

    def exponential_smoothing_forecasting(self, periods=12):
        """Exponential Smoothing forecasting"""
        try:
            model = ExponentialSmoothing(self.ts_data['Transaction_amount'], trend='add', seasonal=None)
            model_fit = model.fit()

            forecast = model_fit.forecast(periods)

            return forecast, model_fit
        except:
            # Simple moving average fallback
            last_values = self.ts_data['Transaction_amount'].tail(3)
            forecast = [last_values.mean()] * periods
            return forecast, None

    def calculate_forecast_accuracy(self, actual, predicted):
        """Calculate forecast accuracy metrics"""
        mae = mean_absolute_error(actual, predicted)
        rmse = np.sqrt(mean_squared_error(actual, predicted))
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100

        return {
            'MAE': mae,
            'RMSE': rmse,
            'MAPE': mape
        }

    def generate_trend_insights(self):
        """Generate automated trend insights"""
        insights = []

        # CAGR insight
        cagr = self.calculate_cagr()
        if cagr > 0:
            insights.append(f"📈 Overall CAGR: {cagr:.1f}% - Strong growth trajectory")
        else:
            insights.append(f"📉 Overall CAGR: {cagr:.1f}% - Growth needs attention")

        # Recent trend analysis
        recent_data = self.calculate_monthly_trends().tail(6)
        recent_growth = recent_data['Transaction_amount'].pct_change().mean() * 100

        if recent_growth > 5:
            insights.append(f"🚀 Recent 6-month growth: {recent_growth:.1f}% - Accelerating growth")
        elif recent_growth > 0:
            insights.append(f"📊 Recent 6-month growth: {recent_growth:.1f}% - Steady growth")
        else:
            insights.append(f"⚠️ Recent 6-month growth: {recent_growth:.1f}% - Declining trend")

        # Seasonality detection
        quarterly_data = self.calculate_quarterly_trends()
        quarterly_growth = quarterly_data.groupby('Quarter')['Transaction_amount'].mean()

        peak_quarter = quarterly_growth.idxmax()
        insights.append(f"🎯 Peak transaction quarter: Q{peak_quarter} - Optimal timing for campaigns")

        return insights

    def get_forecasting_dashboard_data(self):
        """Prepare forecasting data for dashboard"""
        # Generate forecasts
        prophet_forecast, prophet_model = self.prophet_forecasting()
        arima_forecast, arima_model = self.arima_forecasting()

        return {
            'monthly_trends': self.calculate_monthly_trends(),
            'quarterly_trends': self.calculate_quarterly_trends(),
            'cagr': self.calculate_cagr(),
            'rolling_averages': self.calculate_rolling_averages(),
            'prophet_forecast': prophet_forecast,
            'arima_forecast': arima_forecast,
            'trend_insights': self.generate_trend_insights()
        }