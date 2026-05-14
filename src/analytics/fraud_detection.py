import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class FraudDetectionEngine:
    """Advanced Fraud Detection System"""

    def __init__(self, data):
        self.data = data
        self.scaler = StandardScaler()

    def detect_unusual_transactions(self, threshold=3):
        """Detect unusually high transactions using Z-score"""
        # Calculate z-scores for transaction amounts
        amounts = self.data['Transaction_amount']
        z_scores = np.abs(stats.zscore(amounts))

        # Flag transactions above threshold
        anomalies = self.data[z_scores > threshold].copy()
        anomalies['anomaly_type'] = 'high_value_transaction'
        anomalies['z_score'] = z_scores[z_scores > threshold]

        return anomalies

    def detect_transaction_spikes(self, window=7):
        """Detect transaction volume spikes"""
        # Group by date and calculate rolling statistics
        daily_volume = self.data.groupby(['Year', 'Month', 'State'])['Transaction_count'].sum().reset_index()

        # Calculate rolling mean and std
        daily_volume['rolling_mean'] = daily_volume['Transaction_count'].rolling(window=window).mean()
        daily_volume['rolling_std'] = daily_volume['Transaction_count'].rolling(window=window).std()

        # Detect spikes (2+ standard deviations above mean)
        daily_volume['is_spike'] = daily_volume['Transaction_count'] > (daily_volume['rolling_mean'] + 2 * daily_volume['rolling_std'])

        return daily_volume[daily_volume['is_spike']]

    def detect_suspicious_state_activity(self):
        """Detect suspicious activity patterns by state"""
        state_stats = self.data.groupby('State').agg({
            'Transaction_amount': ['sum', 'mean', 'std', 'count'],
            'Transaction_count': ['sum', 'mean', 'std']
        }).round(2)

        # Flatten column names
        state_stats.columns = ['_'.join(col).strip() for col in state_stats.columns]

        # Calculate suspicious indicators
        state_stats['amount_per_transaction'] = state_stats['Transaction_amount_sum'] / state_stats['Transaction_count_sum']
        state_stats['volatility_score'] = state_stats['Transaction_amount_std'] / state_stats['Transaction_amount_mean']

        # Flag states with high volatility or unusual patterns
        suspicious_states = state_stats[
            (state_stats['volatility_score'] > state_stats['volatility_score'].quantile(0.95)) |
            (state_stats['amount_per_transaction'] > state_stats['amount_per_transaction'].quantile(0.95))
        ]

        return suspicious_states

    def isolation_forest_anomaly_detection(self, contamination=0.1):
        """Isolation Forest for multi-dimensional anomaly detection"""
        # Prepare features for ML model
        features = self.data[['Transaction_count', 'Transaction_amount']].copy()

        # Add derived features
        features['amount_per_transaction'] = features['Transaction_amount'] / features['Transaction_count']
        features['log_amount'] = np.log1p(features['Transaction_amount'])
        features['log_count'] = np.log1p(features['Transaction_count'])

        # Handle any infinite or NaN values
        features = features.replace([np.inf, -np.inf], np.nan).fillna(0)

        # Scale features
        scaled_features = self.scaler.fit_transform(features)

        # Train Isolation Forest
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        anomaly_scores = iso_forest.fit_predict(scaled_features)

        # Add results to dataframe
        self.data['anomaly_score'] = anomaly_scores
        self.data['is_anomaly'] = anomaly_scores == -1

        return self.data[self.data['is_anomaly']]

    def z_score_anomaly_detection(self, threshold=3):
        """Z-score based anomaly detection"""
        # Select numerical columns for analysis
        numerical_cols = ['Transaction_count', 'Transaction_amount']

        anomalies = []
        for col in numerical_cols:
            z_scores = np.abs(stats.zscore(self.data[col]))
            col_anomalies = self.data[z_scores > threshold].copy()
            col_anomalies['anomaly_column'] = col
            col_anomalies['z_score'] = z_scores[z_scores > threshold]
            anomalies.append(col_anomalies)

        return pd.concat(anomalies, ignore_index=True)

    def generate_fraud_alerts(self):
        """Generate comprehensive fraud alerts"""
        alerts = []

        # High value transaction alerts
        high_value = self.detect_unusual_transactions()
        if not high_value.empty:
            alerts.append(f"🚨 {len(high_value)} unusually high transactions detected")

        # Spike detection alerts
        spikes = self.detect_transaction_spikes()
        if not spikes.empty:
            alerts.append(f"📈 {len(spikes)} transaction volume spikes detected")

        # Suspicious state activity
        suspicious_states = self.detect_suspicious_state_activity()
        if not suspicious_states.empty:
            alerts.append(f"⚠️ {len(suspicious_states)} states showing suspicious activity patterns")

        # ML-based anomalies
        ml_anomalies = self.isolation_forest_anomaly_detection()
        if not ml_anomalies.empty:
            alerts.append(f"🤖 {len(ml_anomalies)} anomalies detected by ML model")

        return alerts

    def get_fraud_dashboard_data(self):
        """Prepare data for fraud detection dashboard"""
        return {
            'high_value_transactions': self.detect_unusual_transactions(),
            'transaction_spikes': self.detect_transaction_spikes(),
            'suspicious_states': self.detect_suspicious_state_activity(),
            'ml_anomalies': self.isolation_forest_anomaly_detection(),
            'alerts': self.generate_fraud_alerts()
        }