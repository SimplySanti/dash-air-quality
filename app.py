import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.LITERA, dbc_css, dbc.icons.FONT_AWESOME],
)
server = app.server

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "padding": "2rem 1rem",
    "flex": "1",
    "min-height": "100vh",  # This makes the content take full viewport height
}

sidebar = html.Div(
    [
        html.Img(
            className="img-fluid mb-2",
            src="/assets/perficientLogo.png",
        ),
        html.Hr(),
        html.P("Made by Students from Tec de Monterrey", className="lead"),
        dbc.Nav(
            className="flex-column",
            children=[
                dbc.NavLink("Inicio", href="/", active="exact"),
                dbc.NavLink("Insights", href="/insights", active="exact"),
                dbc.NavLink("Análisis", href="/analisis", active="exact"),
                dbc.NavLink("Recursos", href="/recursos", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

app.layout = html.Div(
    className="d-flex",
    children=[
        sidebar,
        html.Div(
            style=CONTENT_STYLE,
            className="pe-5",
            children=[dash.page_container],
        ),
    ],
)


if __name__ == "__main__":
    app.run(debug=True)
