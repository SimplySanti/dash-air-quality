import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "column",
        "gap": "24px",
    },
    children=[
        html.Div(
            style={"display": "flex", "flexDirection": "column", "gap": "12px"},
            children=[
                html.H1("Análisis de Datos de Sensores de Calidad del Aire"),
                html.Div(
                    className="secondaryText",
                    children=[
                        "Iniciativa de análisis de datos ambientales centrada en la calidad del aire en la zona metropolitana de Monterrey, Nuevo León. Este proyecto recopila, analiza y visualiza información relevante sobre contaminantes atmosféricos para facilitar la toma de decisiones, concientización ciudadana y formulación de políticas públicas."
                    ],
                ),
            ],
        ),
        html.Div(
            style={"display": "flex", "flexDirection": "column", "gap": "12px"},
            children=[
                html.H2("Objetivos del Proyecto"),
                html.Div(
                    className="secondaryText",
                    children=[
                        "Proporcionar una representación clara, confiable y actualizada de los niveles de calidad del aire en Monterrey mediante un dashboard interactivo. Este dashboard permite consultar métricas clave como concentraciones de PM2.5, PM10, ozono (O₃), dióxido de nitrógeno (NO₂), dióxido de azufre (SO₂) y monóxido de carbono (CO)."
                    ],
                ),
            ],
        ),
    ],
)
