#!/usr/bin/env python3
"""
Claude Research Projects - Web Dashboard

Real-time monitoring dashboard for all research projects.
"""

import os
from pathlib import Path
from datetime import datetime

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path.cwd().parent.parent))
MONITORING_PORT = int(os.getenv("MONITORING_PORT", 8050))

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    title="Claude Research Projects Monitor"
)

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("🔬 Claude Research Projects", className="text-center text-primary mb-4"),
            html.H5("Real-time Monitoring Dashboard", className="text-center text-muted mb-4"),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📊 Project Overview"),
                dbc.CardBody([
                    html.Div(id="project-overview")
                ])
            ])
        ], width=12, className="mb-4"),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📈 Implementation Progress"),
                dbc.CardBody([
                    dcc.Graph(id="progress-chart")
                ])
            ])
        ], width=6),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader("💰 Credit Usage"),
                dbc.CardBody([
                    dcc.Graph(id="credit-gauge")
                ])
            ])
        ], width=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🎯 Project Details"),
                dbc.CardBody([
                    html.Div(id="project-details")
                ])
            ])
        ], width=12),
    ]),

    dcc.Interval(
        id='interval-component',
        interval=30*1000,  # Update every 30 seconds
        n_intervals=0
    )
], fluid=True)


@app.callback(
    Output("project-overview", "children"),
    Input("interval-component", "n_intervals")
)
def update_overview(n):
    """Update project overview cards"""
    projects = [
        {"name": "Heretic Enhancement", "status": "active", "papers": "2/6", "progress": 33},
        {"name": "DevTools TBD", "status": "planned", "papers": "0/6", "progress": 0},
        {"name": "Data Processing TBD", "status": "planned", "papers": "0/6", "progress": 0},
        {"name": "Web/API TBD", "status": "planned", "papers": "0/6", "progress": 0},
        {"name": "Scientific Computing TBD", "status": "planned", "papers": "0/6", "progress": 0},
    ]

    cards = []
    for proj in projects:
        color = "success" if proj["status"] == "active" else "secondary"
        card = dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5(proj["name"], className="card-title"),
                    html.P(f"Papers: {proj['papers']}", className="card-text"),
                    dbc.Progress(value=proj["progress"], color=color),
                ])
            ], color=color, outline=True)
        ], width=12, md=6, lg=2, className="mb-3")
        cards.append(card)

    return dbc.Row(cards)


@app.callback(
    Output("progress-chart", "figure"),
    Input("interval-component", "n_intervals")
)
def update_progress_chart(n):
    """Update implementation progress chart"""
    projects = ["Heretic\nEnhancement", "DevTools\nTBD", "Data\nProcessing", "Web/API\nTBD", "Scientific\nComputing"]
    implemented = [2, 0, 0, 0, 0]
    total = [6, 6, 6, 6, 6]

    fig = go.Figure(data=[
        go.Bar(name='Implemented', x=projects, y=implemented, marker_color='#00d09c'),
        go.Bar(name='Remaining', x=projects, y=[t-i for t, i in zip(total, implemented)], marker_color='#404040')
    ])

    fig.update_layout(
        barmode='stack',
        title="Papers Implementation Progress",
        xaxis_title="Project",
        yaxis_title="Papers",
        template="plotly_dark",
        height=400
    )

    return fig


@app.callback(
    Output("credit-gauge", "figure"),
    Input("interval-component", "n_intervals")
)
def update_credit_gauge(n):
    """Update credit usage gauge"""
    # Placeholder values - would integrate with actual tracking
    used = 125000
    total = 1000000
    percent = (used / total) * 100

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=used,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Tokens Used", 'font': {'size': 24}},
        delta={'reference': total, 'suffix': ' remaining'},
        gauge={
            'axis': {'range': [None, total], 'ticksuffix': 'K', 'tickformat': '.0f'},
            'bar': {'color': "#00d09c"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, total*0.5], 'color': '#2d3e50'},
                {'range': [total*0.5, total*0.8], 'color': '#4a5f7f'},
                {'range': [total*0.8, total], 'color': '#ff6b6b'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': total*0.9
            }
        }
    ))

    fig.update_layout(
        template="plotly_dark",
        height=400,
        font={'size': 16}
    )

    return fig


@app.callback(
    Output("project-details", "children"),
    Input("interval-component", "n_intervals")
)
def update_project_details(n):
    """Update detailed project information"""
    # This would fetch from actual metrics DB
    details = [
        {"project": "Heretic Enhancement", "commits": 12, "tests": "85%", "last": "2 hours ago"},
        {"project": "DevTools TBD", "commits": 0, "tests": "-", "last": "Never"},
        {"project": "Data Processing TBD", "commits": 0, "tests": "-", "last": "Never"},
        {"project": "Web/API TBD", "commits": 0, "tests": "-", "last": "Never"},
        {"project": "Scientific Computing TBD", "commits": 0, "tests": "-", "last": "Never"},
    ]

    return dbc.Table.from_dataframe(
        __import__('pandas').DataFrame(details),
        striped=True,
        bordered=True,
        hover=True,
        dark=True,
        responsive=True
    )


if __name__ == "__main__":
    print(f"🚀 Starting dashboard at http://{os.getenv('MONITORING_HOST', 'localhost')}:{MONITORING_PORT}")
    app.run_server(
        host=os.getenv("MONITORING_HOST", "0.0.0.0"),
        port=MONITORING_PORT,
        debug=os.getenv("DEBUG", "false").lower() == "true"
    )
