import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

app = Dash(__name__, use_pages=True)

# Requires Dash 2.17.0 or later
app.layout = html.Div(
    className="windowContainer",
    children=[
        html.Div(
            className="sidebarContainer",
            children=[
                html.Div(
                    className="logoContainer",
                    children=[
                        html.Img(
                            src="/assets/perficientLogo.png",
                        ),
                    ],
                ),
                html.Div(
                    className="sidebarOptions",
                    children=[
                        html.Div(
                            className="sidebarLinks",
                            children=[
                                dcc.Link(
                                    [
                                        html.Span(" ▶", style={"marginRight": "12px"}),
                                        html.Span("Inicio"),
                                    ],
                                    href="/",
                                ),
                                html.Br(),
                                dcc.Link(
                                    [
                                        html.Span(" ▶", style={"marginRight": "12px"}),
                                        html.Span("Informacion"),
                                    ],
                                    href="/informacion",
                                ),
                                html.Br(),
                                dcc.Link(
                                    [
                                        html.Span(" ▶", style={"marginRight": "12px"}),
                                        html.Span("Recursos"),
                                    ],
                                    href="/recursos",
                                ),
                            ],
                        ),
                        html.Div(
                            children=[
                                html.P("Made with ♡ by students from Tec de Monterrey"),
                            ],
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            className="pageContent", id="pageContent", children=[dash.page_container]
        ),
    ],
)


if __name__ == "__main__":
    app.run(debug=True)
