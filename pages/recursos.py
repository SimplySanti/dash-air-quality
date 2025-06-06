import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = html.Div(
    className="d-flex flex-column gap-3",
    style={"height": "calc(100dvh - 64px)"},
    children=[
        html.H1("Recursos Utilizados Para Este Estudio"),
        html.P(
            className="text-muted",
            children=[
                "Los datos presentados en este dashboard provienen de estaciones de monitoreo ambiental ubicadas en distintos puntos estratégicos de la zona metropolitana de Monterrey, Nuevo León. Estas estaciones recolectan información en tiempo real sobre diversos contaminantes atmosféricos, tales como partículas PM2.5, PM10, ozono (O₃), dióxido de nitrógeno (NO₂), dióxido de azufre (SO₂) y monóxido de carbono (CO). La infraestructura de monitoreo es operada por organismos oficiales y complementada, en algunos casos, con sensores independientes instalados para fines de investigación. La decisión de compartir públicamente estos datos responde a un compromiso con la transparencia, la ciencia abierta y la colaboración interdisciplinaria. Al poner esta información a disposición de la comunidad académica, centros de investigación y universidades, buscamos fomentar el desarrollo de nuevos proyectos que contribuyan a una comprensión más profunda de la calidad del aire en la región. Asimismo, se espera que esta iniciativa sirva como base para propuestas de mejora en políticas públicas, estrategias de mitigación y soluciones tecnológicas enfocadas en el bienestar ambiental y la salud de la población."
            ],
        ),
        html.Div(
            className="d-flex gap-4",
            children=[
                html.A(
                    style={
                        "textDecoration": "none",
                    },
                    children=[
                        dbc.Card(
                            className="h-100",
                            children=[
                                dbc.CardBody(
                                    [
                                        html.H4(
                                            "Registros de Aire Nuevo León",
                                            className="mb-3",
                                        ),
                                        html.P(
                                            "Descargar los registros de calidad del aire en formato Excel.",
                                            className="card-text",
                                        ),
                                    ]
                                )
                            ],
                        )
                    ],
                    href="/assets/registros_airenuevoleon.xlsx",
                    download="registros_airenuevoleon.xlsxf",
                ),
                html.A(
                    style={
                        "textDecoration": "none",
                    },
                    children=[
                        dbc.Card(
                            className="h-100",
                            children=[
                                dbc.CardBody(
                                    [
                                        html.H4(
                                            "Sensores\u00a0de\u00a0Aire Nuevo León",
                                            className="mb-3",
                                        ),
                                        html.P(
                                            "Descargar registros de sensores de calidad de aire en el área metropolitana.",
                                            className="card-text",
                                        ),
                                    ]
                                )
                            ],
                        )
                    ],
                    href="/assets/sensores_airenuevoleon.xlsx",
                    download="sensores_airenuevoleon.pdf",
                ),
                html.A(
                    style={
                        "textDecoration": "none",
                    },
                    children=[
                        dbc.Card(
                            className="h-100",
                            children=[
                                dbc.CardBody(
                                    [
                                        html.H4(
                                            "Articulo de Investigación",
                                            className="mb-3",
                                        ),
                                        html.P(
                                            "Descarga un estudio detallado sobre el análisis realizado.",
                                            className="card-text",
                                        ),
                                    ]
                                )
                            ],
                        )
                    ],
                    href="/assets/TODO",
                    download="TODO.pdf",
                ),
            ],
        ),
    ],
)
