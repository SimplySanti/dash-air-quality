import dash
from dash import html

dash.register_page(__name__)

layout = html.Div(
    [
        html.H1("Resumen de Hallazgos", className="mb-5"),
        html.Div(
            className="d-flex flex-column gap-1 w-100",
            children=[
                html.Div(
                    className="card shadow-sm p-4 mb-4",
                    children=[
                        html.H6(
                            "Número alto de datos faltantes y defectuosos en sensores",
                            className="mb-2",
                        ),
                        html.P(
                            "Múltiples sensores tienen hasta un 98.4% de datos nulos y múltiples valores negativos, lo que refleja deficiencias críticas."
                        ),
                    ],
                ),
                html.Div(
                    className="card shadow-sm p-4 mb-4",
                    children=[
                        html.H6(
                            "Concentraciones de PM2.5 exceden estándares",
                            className="mb-2",
                        ),
                        html.P(
                            "Se registraron picos de hasta 45 µg/m³ en enero, superando ampliamente el límite de 25 µg/m³ de la OMS, especialmente durante las horas pico de tráfico (6-10 a.m.)."
                        ),
                    ],
                ),
                html.Div(
                    className="card shadow-sm p-4 mb-4",
                    children=[
                        html.H6(
                            "Ozono presenta patrón diario y estacional claro",
                            className="mb-2",
                        ),
                        html.P(
                            "Se observó un incremento consistente de O₃ al mediodía (12–3 p.m.), correlacionado con la radiación solar."
                        ),
                    ],
                ),
                html.Div(
                    className="card shadow-sm p-4 mb-4",
                    children=[
                        html.H6(
                            "Relación significativa entre humedad y PM2.5",
                            className="mb-2",
                        ),
                        html.P(
                            "Correlación negativa fuerte, lo que sugiere que la humedad favorece la deposición húmeda de partículas suspendidas."
                        ),
                    ],
                ),
                html.Div(
                    className="card shadow-sm p-4 mb-4",
                    children=[
                        html.H6(
                            "Distribución espacial desigual de sensores",
                            className="mb-2",
                        ),
                        html.P(
                            "Monterrey y San Nicolás tienen buena cobertura, pero otras zonas críticas como Pesquería tienen apenas 1 sensor por cada 400 km², lo que limita el análisis espacial completo."
                        ),
                    ],
                ),
                html.Div(
                    className="card shadow-sm p-4 mb-4",
                    children=[
                        html.H6(
                            "Interpolación temporal y reindexado horario exitosos",
                            className="mb-2",
                        ),
                        html.P(
                            "Se logró transformar el dataset en una serie temporal continua, interpolando valores perdidos y reindexando a frecuencia horaria, habilitando modelos basados en series de tiempo."
                        ),
                    ],
                ),
                html.Div(
                    className="card shadow-sm p-4 mb-4",
                    children=[
                        html.H6(
                            "Se descartaron sensores con más de 55% de valores faltantes",
                            className="mb-2",
                        ),
                        html.P(
                            "Esta decisión mejoró la calidad del conjunto de datos al enfocarse en fuentes más confiables para la etapa de modelado."
                        ),
                    ],
                ),
                html.Div(
                    className="card shadow-sm p-4 mb-4",
                    children=[
                        html.H6(
                            "Implementación exitosa de un modelo VAR multivariado",
                            className="mb-2",
                        ),
                        html.P(
                            "Se utilizó un modelo Vector Auto Regression para predecir simultáneamente PM2.5, O₃ y NO₁, con base en dependencias cruzadas entre variables."
                        ),
                    ],
                ),
                html.Div(
                    className="card shadow-sm p-4 mb-4",
                    children=[
                        html.H6(
                            "Validación visual sugiere buen seguimiento de tendencias, pero errores en picos",
                            className="mb-2",
                        ),
                        html.P(
                            "Las gráficas de comparación entre valores reales y predichos muestran que el modelo captura bien las tendencias generales, aunque presenta limitaciones para anticipar eventos extremos."
                        ),
                    ],
                ),
            ],
        ),
    ],
    style={"height": "calc(100dvh - 64px)"},
)
