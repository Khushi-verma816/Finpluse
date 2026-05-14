import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import base64
from io import BytesIO

class DashboardComponents:
    """Professional Dashboard UI Components"""

    @staticmethod
    def create_kpi_card(title, value, change=None, change_type="percentage", icon="KPI"):
        """Create a professional KPI card"""
        if isinstance(value, (int, float)):
            if value >= 1e9:
                display_value = f"Rs {value/1e9:.1f}B"
            elif value >= 1e6:
                display_value = f"Rs {value/1e6:.1f}M"
            elif value >= 1e3:
                display_value = f"Rs {value/1e3:.1f}K"
            else:
                display_value = f"Rs {value:,.0f}"
        else:
            display_value = str(value)

        # Determine change color and icon
        if change is not None:
            if change_type == "percentage":
                change_display = f"{change:+.1f}%"
            else:
                change_display = f"{change:+.2f}"

            if change > 0:
                change_color = "#00C853"
                change_icon = "UP"
            elif change < 0:
                change_color = "#D32F2F"
                change_icon = "DOWN"
            else:
                change_color = "#757575"
                change_icon = "FLAT"
        else:
            change_display = ""
            change_color = "#757575"
            change_icon = ""

        is_light_theme = st.session_state.get("theme", "dark") == "light"

        if is_light_theme:
            card_background = "#FFFFFF"
            card_border = "1px solid #E2E8F0"
            card_shadow = "0 1px 3px rgba(0,0,0,0.08)"
            card_text = "#1A202C"
            title_color = "#4A5568"
        else:
            card_background = "linear-gradient(135deg, #14264A 0%, #2B4F8D 100%)"
            card_border = "1px solid rgba(255,255,255,0.08)"
            card_shadow = "0 18px 40px rgba(0,0,0,0.16)"
            card_text = "#F5F7FF"
            title_color = "#E9F1FF"

        # Create card HTML
        card_html = f"""
        <div style="
            background: {card_background};
            border-radius: 18px;
            padding: 22px;
            margin: 10px 0;
            box-shadow: {card_shadow};
            border: {card_border};
            color: {card_text};
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0; font-size: 14px; color: {title_color};">{icon} {title}</h3>
                    <h2 style="margin: 5px 0; font-size: 28px; font-weight: bold; color: {card_text};">{display_value}</h2>
                    <p style="margin: 0; font-size: 14px; color: {change_color};">
                        {change_icon} {change_display}
                    </p>
                </div>
            </div>
        </div>
        """

        return card_html

    @staticmethod
    def create_metric_grid(kpis_data):
        """Create a responsive grid of KPI cards"""
        cols = st.columns(len(kpis_data))

        for i, (col, kpi) in enumerate(zip(cols, kpis_data)):
            with col:
                card_html = DashboardComponents.create_kpi_card(
                    kpi['title'],
                    kpi['value'],
                    kpi.get('change'),
                    kpi.get('change_type', 'percentage'),
                    kpi.get('icon', 'KPI')
                )
                components.html(card_html, height=180)

    @staticmethod
    def create_advanced_chart(data, chart_type="bar", **kwargs):
        """Create advanced, professional charts"""
        is_light_theme = st.session_state.get("theme", "dark") == "light"
        chart_template = "plotly_white" if is_light_theme else "plotly_dark"
        chart_text = "#102A43" if is_light_theme else "#E9F1FF"
        chart_grid = "rgba(148, 163, 184, 0.35)" if is_light_theme else "rgba(148, 163, 184, 0.28)"

        if chart_type == "bar":
            fig = px.bar(
                data,
                **kwargs,
                color_discrete_sequence=["#4FD1C5"],
                template=chart_template
            )

        elif chart_type == "line":
            fig = px.line(
                data,
                **kwargs,
                color_discrete_sequence=px.colors.qualitative.Set1,
                template=chart_template
            )

        elif chart_type == "area":
            fig = px.area(
                data,
                **kwargs,
                color_discrete_sequence=px.colors.qualitative.Pastel,
                template=chart_template
            )

        elif chart_type == "scatter":
            fig = px.scatter(
                data,
                **kwargs,
                color_discrete_sequence=px.colors.qualitative.Set2,
                template=chart_template
            )

        # Apply professional styling
        fig.update_layout(
            font_family="Arial",
            font_size=12,
            title_font_size=20,
            title_font_color=chart_text,
            font_color=chart_text,
            legend_font_color=chart_text,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=40, b=20),
        )

        # Add grid lines
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=chart_grid, tickfont_color=chart_text, title_font_color=chart_text)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=chart_grid, tickfont_color=chart_text, title_font_color=chart_text)

        return fig

    @staticmethod
    def create_geo_map(data, location_col, value_col, title="Geographic Distribution"):
        """Create interactive geographic map"""
        fig = px.choropleth(
            data,
            locations=location_col,
            locationmode="country names",
            color=value_col,
            hover_name=location_col,
            color_continuous_scale="Viridis",
            title=title,
            template="plotly_white"
        )

        fig.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            ),
            margin=dict(l=0, r=0, t=40, b=0)
        )

        return fig

    @staticmethod
    def create_forecast_chart(historical_data, forecast_data, title="Forecast Analysis"):
        """Create forecast visualization with confidence intervals"""
        is_light_theme = st.session_state.get("theme", "dark") == "light"
        chart_template = "plotly_white" if is_light_theme else "plotly_dark"
        chart_text = "#102A43" if is_light_theme else "#E9F1FF"
        chart_grid = "rgba(148, 163, 184, 0.35)" if is_light_theme else "rgba(148, 163, 184, 0.28)"

        fig = go.Figure()

        # Historical data
        fig.add_trace(go.Scatter(
            x=historical_data['Date'],
            y=historical_data['Transaction_amount'],
            mode='lines+markers',
            name='Historical',
            line=dict(color='#2E86AB', width=2)
        ))

        # Forecast data
        if 'yhat' in forecast_data.columns:
            fig.add_trace(go.Scatter(
                x=forecast_data['ds'],
                y=forecast_data['yhat'],
                mode='lines',
                name='Forecast',
                line=dict(color='#A23B72', width=2, dash='dash')
            ))

            # Confidence intervals
            if 'yhat_lower' in forecast_data.columns and 'yhat_upper' in forecast_data.columns:
                fig.add_trace(go.Scatter(
                    x=forecast_data['ds'],
                    y=forecast_data['yhat_upper'],
                    mode='lines',
                    name='Upper Bound',
                    line=dict(width=0),
                    showlegend=False
                ))

                fig.add_trace(go.Scatter(
                    x=forecast_data['ds'],
                    y=forecast_data['yhat_lower'],
                    mode='lines',
                    name='Lower Bound',
                    line=dict(width=0),
                    fill='tonexty',
                    fillcolor='rgba(162, 59, 114, 0.2)',
                    showlegend=False
                ))

        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Transaction Amount",
            template=chart_template,
            hovermode="x unified",
            font_color=chart_text,
            title_font_color=chart_text,
            legend_font_color=chart_text,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=chart_grid, tickfont_color=chart_text, title_font_color=chart_text)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=chart_grid, tickfont_color=chart_text, title_font_color=chart_text)

        return fig

    @staticmethod
    def export_to_excel(data, filename="finpulse_report.xlsx"):
        """Export data to Excel with formatting"""
        output = BytesIO()

        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            data.to_excel(writer, sheet_name='Data', index=False)

            # Get workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets['Data']

            # Add formats
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#2E86AB',
                'font_color': 'white',
                'border': 1
            })

            # Apply formatting
            for col_num, value in enumerate(data.columns.values):
                worksheet.write(0, col_num, value, header_format)
                worksheet.set_column(col_num, col_num, 15)

        output.seek(0)
        return output

    @staticmethod
    def create_download_button(data, filename, button_text="Download Report"):
        """Create download button for data export"""
        if isinstance(data, pd.DataFrame):
            csv = data.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{button_text}</a>'
        else:
            # For Excel files
            b64 = base64.b64encode(data.getvalue()).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">{button_text}</a>'

        return href
