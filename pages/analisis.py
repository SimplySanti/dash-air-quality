import dash
from dash import html, dcc
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import base64
import os

dash.register_page(__name__)

# Load the data

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
registros_filtrados = pd.read_excel(os.path.join(project_dir, "assets", "registros_filtrados.xlsx"))
sensores = pd.read_excel(os.path.join(project_dir, "assets", "sensores_airenuevoleon.xlsx"))

def graficar_intervalos_confianza(df, sensores_df, variable, nombre_variable=None):
  
    """
    Genera subplots por sensor con los intervalos de confianza 1,2,3 sigmas
    para la variable dada (PM2.5, O3, etc.).

    Parámetros:
    - df: DataFrame con los registros
    - sensores_df: DataFrame con los sensores válidos (ANL)
    - variable: nombre de la columna a analizar (str)
    - nombre_variable: nombre legible para títulos y ejes (str), opcional
    """
    if nombre_variable is None:
        nombre_variable = variable

    df_validos = df[df[variable].notnull() & (df[variable] >= 0)].copy()

    sensores_anl = sensores_df["Sensor_id"].unique()
    df_validos = df_validos[df_validos["Sensor_id"].isin(sensores_anl)]

    stats = df_validos.groupby("Sensor_id")[variable].agg(["mean", "std"]).dropna()

    fig, axs = plt.subplots(nrows=5, ncols=3, figsize=(18, 16))
    axs = axs.flatten()

    for i, sensor in enumerate(sensores_anl):
        df_sensor = df_validos[df_validos["Sensor_id"] == sensor]

        if df_sensor.empty or sensor not in stats.index:
            continue

        media = stats.loc[sensor, "mean"]
        std = stats.loc[sensor, "std"]

        axs[i].xaxis.set_major_locator(mdates.YearLocator())
        axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

        axs[i].plot(df_sensor["Dia"], df_sensor[variable], alpha=0.5, label=nombre_variable)
        axs[i].axhline(media, color="green", linestyle="--", label="Media")
        axs[i].axhline(media + std, color="orange", linestyle="--", label="±1σ")
        axs[i].axhline(media - std, color="orange", linestyle="--")
        axs[i].axhline(media + 2*std, color="red", linestyle="--", label="±2σ")
        axs[i].axhline(media - 2*std, color="red", linestyle="--")
        axs[i].axhline(media + 3*std, color="purple", linestyle="--", label="±3σ")
        axs[i].axhline(media - 3*std, color="purple", linestyle="--")
        axs[i].set_title(sensor)
        axs[i].set_ylabel(nombre_variable)
        axs[i].set_ylim(bottom=0)
        
    plt.suptitle(f"{nombre_variable} – Intervalos de confianza por sensor (1σ, 2σ, 3σ)", fontsize=16)
    plt.xlabel("Fecha")
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    
    # Save the figure to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    
    # Encode the image to base64 string
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{img_str}"

# Generate the PM2.5 confidence interval plot
pm25_plot = graficar_intervalos_confianza(registros_filtrados, sensores, "PM25", "PM2.5")
pm10_plot = graficar_intervalos_confianza(registros_filtrados, sensores, "PM10", "PM10")
o3_plot = graficar_intervalos_confianza(registros_filtrados, sensores, "O3", "Ozono")

layout = html.Div(
    [
        html.H1("Análisis de los Datos", className="mb-5"),
        html.Div(
            className="d-flex flex-column gap-1 w-100",
            children=[
                html.Div(
                    className="card shadow-sm p-4 mb-4",
                    children=[
                        html.H6(
                            "PM2.5 Gráficas de intervalos de confianza",
                            className="mb-2",
                        ),
                        html.P(
                            "Esta sección analiza la distribución de los valores de PM2.5 por sensor ANL, aplicando intervalos de confianza con 1σ, 2σ y 3σ (desviación estándar).\n\nEsto nos permite detectar posibles lecturas atípicas o inconsistentes que se desvían significativamente de los valores esperados."
                        ),
                        html.Div(
                            className="mt-3",
                            children=[
                                html.Img(
                                    src=pm25_plot,
                                    className="img-fluid w-100",
                                    style={"maxHeight": "800px", "objectFit": "contain"}
                                )
                            ]
                        )
                    ],
                ),
                html.Div(
                    className="card shadow-sm p-4 mb-4",
                    children=[
                        html.H6(
                            "PM10 Gráficas de intervalos de confianza",
                            className="mb-2",
                        ),
                        html.P(
                            "Esta sección analiza la distribución de los valores de PM10 por sensor ANL, aplicando intervalos de confianza con 1σ, 2σ y 3σ (desviación estándar). Esto nos permite detectar posibles lecturas atípicas o inconsistentes que se desvían significativamente de los valores esperados."
                        ),
                        html.Div(
                            className="mt-3",
                            children=[
                                html.Img(
                                    src=pm10_plot,
                                    className="img-fluid w-100",
                                    style={"maxHeight": "800px", "objectFit": "contain"}
                                )
                            ]
                        )
                    ],
                ),
                html.Div(
                    className="card shadow-sm p-4 mb-4",
                    children=[
                        html.H6(
                            "Ozono Gráficas de intervalos de confianza",
                            className="mb-2",
                        ),
                        html.P(
                            "Esta sección analiza la distribución de los valores de Ozono por sensor ANL, aplicando intervalos de confianza con 1σ, 2σ y 3σ (desviación estándar). Esto nos permite detectar posibles lecturas atípicas o inconsistentes que se desvían significativamente de los valores esperados."
                        ),
                        html.Div(
                            className="mt-3",
                            children=[
                                html.Img(
                                    src=o3_plot,
                                    className="img-fluid w-100",
                                    style={"maxHeight": "800px", "objectFit": "contain"}
                                )
                            ]
                        )
                    ],
                ),
            ],
        ),
    ],
    style={"height": "calc(100dvh - 64px)"},
)
