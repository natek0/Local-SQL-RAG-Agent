import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from typing import Optional

class VizGenerator:
    """
    The 'Artist' of the system.
    Analyzes the topology of the data (Data Types) to deterministically 
    select the best visualization.
    """
    
    def generate(self, df: pd.DataFrame, title: str) -> Optional[go.Figure]:
        if df.empty:
            return None
            
        # 1. Identify Column Types
        num_cols = df.select_dtypes(include=['number']).columns
        date_cols = df.select_dtypes(include=['datetime', 'datetimetz']).columns
        # Also check for string columns that look like dates
        if len(date_cols) == 0:
            for col in df.select_dtypes(include=['object']):
                try:
                    pd.to_datetime(df[col])
                    date_cols = [col]
                    break
                except:
                    pass
        
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        
        # Rule 1: Time Series -> Line Chart [cite: 98]
        # Condition: Has a Date column and at least one Metric
        if len(date_cols) > 0 and len(num_cols) > 0:
            print("Detected Topology: Time Series -> Generating Line Chart")
            return px.line(df, x=date_cols[0], y=num_cols[0], title=title, markers=True)
            
        # Rule 2: Categorical Comparison -> Bar Chart [cite: 99]
        # Condition: Has a Category and a Metric (and small number of categories)
        if len(cat_cols) > 0 and len(num_cols) > 0:
            if df[cat_cols[0]].nunique() < 20: # Don't plot bar charts with 1000 bars
                print("Detected Topology: Categorical -> Generating Bar Chart")
                return px.bar(df, x=cat_cols[0], y=num_cols[0], title=title)
                
        # Rule 3: Correlation -> Scatter Plot
        # Condition: Two numeric columns
        if len(num_cols) >= 2:
            print("Detected Topology: Correlation -> Generating Scatter Plot")
            return px.scatter(df, x=num_cols[0], y=num_cols[1], title=title)
            
        print("Detected Topology: Tabular -> No Visualization")
        return None
