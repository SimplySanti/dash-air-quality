import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd
import folium
from folium import plugins
from folium.plugins import HeatMap
import os
import numpy as np
import polars as pl
import pickle

dash.register_page(__name__, path="/")


current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)


def create_map(fecha_objetivo="2023-01-01", contaminante="PM10"):

    try:
        registros = pl.read_csv(
            os.path.join(project_dir, "assets", "DailyWeatherData.csv")
        ).to_pandas()

        registros["Fecha"] = pd.to_datetime(
            registros["Fecha"], format="%Y-%m-%d", errors="coerce"
        )
        registros = registros.dropna(subset=["Fecha"])

        sensores = pd.read_excel(
            os.path.join(project_dir, "assets", "sensores_airenuevoleon.xlsx")
        )
        registros = registros.merge(
            sensores[["Sensor_id", "Latitud", "Longitud"]], on="Sensor_id", how="left"
        )
        registros = registros.dropna(subset=["Latitud", "Longitud"])

        def gaussian_plume(
            lat, lon, velocidad, direccion, contaminante_val, n_puntos=50
        ):
            lat_rad = np.radians(lat)
            lon_rad = np.radians(lon)
            dir_rad = np.radians(direccion)
            distancias = np.linspace(0.001, 0.02, n_puntos)
            puntos = []
            for d in distancias:
                sigma = 0.002 + d * 2
                for _ in range(10):
                    lat_disp = lat + d * np.cos(dir_rad)
                    lon_disp = lon + d * np.sin(dir_rad)
                    lat_disp += np.random.normal(0, sigma)
                    lon_disp += np.random.normal(0, sigma)
                    intensidad = contaminante_val * np.exp(-d * 100)
                    puntos.append([lat_disp, lon_disp, intensidad / 150])
            return puntos

        def mostrar_mapa_contaminante(fecha_objetivo: str, contaminante: str):
            if contaminante not in registros.columns:
                raise ValueError(f"Contaminante '{contaminante}' no encontrado.")

            datos_dia = registros[
                (registros["Fecha"].dt.strftime("%Y-%m-%d") == fecha_objetivo)
                & (registros[contaminante].notna())
                & (registros[contaminante] >= 0)
            ].copy()

            heat_data = []
            for _, fila in datos_dia.iterrows():
                velocidad = fila["VIENTOVEL"] if pd.notna(fila["VIENTOVEL"]) else 1
                direccion = fila["RS"] if pd.notna(fila["RS"]) else 0

                puntos = gaussian_plume(
                    lat=fila["Latitud"],
                    lon=fila["Longitud"],
                    velocidad=velocidad,
                    direccion=direccion,
                    contaminante_val=fila[contaminante],
                )
                heat_data.extend(puntos)

            mapa = folium.Map(
                location=[25.67, -100.31],
                max_zoom=11,
                zoom_start=10,
                tiles="CartoDB positron",
            )
            HeatMap(
                heat_data,
                radius=30,
                max_opacity=0.7,
                blur=20,
                gradient={
                    0.1: "blue",
                    0.4: "lime",
                    0.6: "yellow",
                    0.8: "orange",
                    1.0: "red",
                },
                min_opacity=0.3,
            ).add_to(mapa)

            return mapa

        # Generate the map with default parameters or specified ones
        mapa = mostrar_mapa_contaminante(fecha_objetivo, contaminante)

        # Load municipios geojson for boundaries
        municipios = gpd.read_file(
            os.path.join(project_dir, "assets", "municipios.geojson")
        )

        # Add municipality boundaries
        folium.GeoJson(
            municipios,
            name="Municipios",
            style_function=lambda x: {
                "fillColor": "#eeeeee",
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.1,
            },
            tooltip=folium.GeoJsonTooltip(fields=["NOMBRE"]),
        ).add_to(mapa)

        # Save to HTML string
        map_html = mapa._repr_html_()
        return map_html

    except Exception as e:
        print(f"Error creating map: {e}")
        # Return a simple map in case of error
        mapa = folium.Map(
            location=[25.67, -100.31], zoom_start=10, tiles="CartoDB positron"
        )
        map_html = mapa._repr_html_()
        return map_html


try:
    with open(os.path.join(project_dir, "assets", "scaler.pkl"), "rb") as f:
        scaler = pickle.load(f)

    with open(
        os.path.join(project_dir, "assets", "Clasificacion_Calidad_Aire.pkl"), "rb"
    ) as f:
        loaded_kmeans = pickle.load(f)
except Exception as e:
    print(f"Error loading models: {e}")
    scaler = None
    loaded_kmeans = None


def get_air_quality(fecha_objetivo, contaminante=None):
    try:

        df = pd.read_csv(os.path.join(project_dir, "assets", "DailyWeatherData.csv"))
        df["Fecha"] = pd.to_datetime(df["Fecha"], format="%Y-%m-%d")

        # ANL12 = Obispado, ANL4 = San Pedro, ANL8 = Cadereyta
        datos_dia = (
            df.loc[
                (df["Fecha"].dt.strftime("%Y-%m-%d") == fecha_objetivo)
                & (df["Sensor_id"].isin(["ANL11", "ANL4", "ANL8"])),
                ["Sensor_id", "PM10", "PM25"],
            ]
            .sort_values(by="Sensor_id")
            .copy()
        )

        if datos_dia.empty:
            return {"Obispado": -1, "San Pedro": -1, "Cadereyta": -1}

        datos_dia[["PM10^2", "PM25^2"]] = datos_dia[["PM10", "PM25"]] ** 2

        df_standardized = scaler.transform(datos_dia.drop(columns="Sensor_id"))
        clasification = loaded_kmeans.predict(df_standardized)

        score = {
            "Obispado": int(clasification[0]),
            "San Pedro": int(clasification[1]),
            "Cadereyta": int(clasification[2]),
        }

        return score
    except Exception as e:
        print(f"Error getting air quality: {e}")
        return {"Obispado": -1, "San Pedro": -1, "Cadereyta": -1}

layout = html.Div(
    className="d-flex flex-column gap-4 w-100",
    style={"height": "calc(100dvh - 64px)"},
    children=[
        html.Div(
            children=[
                html.H1("Calidad del Aire en Monterrey"),
                html.Div(
                    className="text-muted small",
                    style={"maxWidth": "800px"},
                    children=[
                        "Iniciativa de análisis de datos ambientales centrada en la calidad del aire en la zona metropolitana de Monterrey, Nuevo León. Este proyecto recopila, analiza y visualiza información relevante sobre contaminantes atmosféricos para facilitar la toma de decisiones, concientización ciudadana y formulación de políticas públicas."
                    ],
                ),
            ],
        ),
        html.Div(
            className="d-flex gap-4 mt-xs-2 mt-sm-2 mt-md-2 w-100",
            children=[
                html.Div(
                    className="d-flex gap-4 w-xs-100 w-sm-100 w-md-50 align-items-end h-100",
                    children=[
                        html.Div(
                            [
                                dbc.Label("Contaminante:"),
                                dbc.Select(
                                    id="select",
                                    value="PM10",
                                    options=[
                                        {"label": "PM10", "value": "PM10"},
                                        {"label": "PM25", "value": "PM25"},
                                        {"label": "O3", "value": "O3"},
                                    ],
                                    style={"height": "40px"},
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                dbc.Label("Fecha:"),
                                dbc.Input(
                                    id="input",
                                    type="date",
                                    value="2025-03-22",
                                    placeholder="Ingrese un valor",
                                    min="2022-01-01",
                                    max="2025-04-04",
                                    style={"height": "40px"},
                                ),
                            ]
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            className="d-flex gap-3 gap-xs-5 gap-sm-5 h-auto w-100 flex-xs-column flex-sm-column flex-md-row flex-lg-row",
            style={"minWidth": "100%", "minHeight": "300px"},
            children=[
                html.Div(
                    className="h-100 w-75 w-sm-100 w-xs-100 mb-2",
                    children=[
                        html.H6(
                            className="mb-3 text-muted", children=["Mapa de Calor"]
                        ),
                        dbc.Card(
                            className="d-flex justify-content-center align-items-center h-100 pt-1 bg-light",
                            style={
                                "height": "auto",
                            },
                            children=[
                                html.Iframe(
                                    id="map-iframe",
                                    srcDoc=create_map(),
                                    style={
                                        "height": "100%",
                                        "width": "100%",
                                        "border": "none",
                                        "display": "block",
                                    },
                                )
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="h-100 w-50 w-sm-100 w-xs-100",
                    children=[
                        html.H6(
                            className="mb-3 text-muted", children=["Calidad General del Aire"]
                        ),
                        html.Div(
                            className="d-flex flex-column align-items-center gap-2 h-100 mb-1",
                            children=[
                                html.Div(
                                    className="d-flex flex-column w-100 mb-2 gap-1",
                                    id="obispado-quality",
                                    children=[
                                        html.Div(
                                            "Obispado:",
                                            className="small fw-bold",
                                        ),
                                        dbc.Badge(
                                            "Cargando...",
                                            color="secondary",
                                            className="w-100 text-start p-2",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="d-flex flex-column w-100 mb-2 gap-1",
                                    id="sanpedro-quality",
                                    children=[
                                        html.Div(
                                            "San Pedro:",
                                            className="small fw-bold",
                                        ),
                                        dbc.Badge(
                                            "Cargando...",
                                            color="secondary",
                                            className="w-100 text-start p-2",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="d-flex flex-column w-100 mb-2 gap-1",
                                    id="cadereyta-quality",
                                    children=[
                                        html.Div(
                                            "Cadereyta:",
                                            className="small fw-bold",
                                        ),
                                        dbc.Badge(
                                            "Cargando...",
                                            color="secondary",
                                            className="w-100 text-start p-2",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@callback(
    Output("map-iframe", "srcDoc"), [Input("select", "value"), Input("input", "value")]
)
def update_map(contaminante, fecha):
    # Default to valid values if none provided
    contaminante = contaminante if contaminante else "PM10"
    fecha = fecha if fecha else "2023-01-01"
    return create_map(fecha_objetivo=fecha, contaminante=contaminante)


@callback(
    [
        Output("obispado-quality", "children"),
        Output("sanpedro-quality", "children"),
        Output("cadereyta-quality", "children"),
    ],
    [Input("input", "value"), Input("select", "value")],
)
def update_air_quality(fecha, contaminante):
    fecha = fecha if fecha else "2023-01-01"
    quality_scores = get_air_quality(fecha_objetivo=fecha, contaminante=contaminante)

    def get_quality_description(score):
        if score == 0:
            return {"text": "Buena", "color": "success"}
        elif score == 1:
            return {"text": "Regular", "color": "warning"}
        else:
            return {"text": "Sin datos", "color": "secondary"}

    obispado_quality = get_quality_description(quality_scores["Obispado"])
    sanpedro_quality = get_quality_description(quality_scores["San Pedro"])
    cadereyta_quality = get_quality_description(quality_scores["Cadereyta"])

    return [
        [
            html.Div("Obispado:", className="small fw-bold"),
            dbc.Badge(
                obispado_quality["text"],
                color=obispado_quality["color"],
                className="w-100 text-start p-2",
            ),
        ],
        [
            html.Div("San Pedro:", className="small fw-bold"),
            dbc.Badge(
                sanpedro_quality["text"],
                color=sanpedro_quality["color"],
                className="w-100 text-start p-2",
            ),
        ],
        [
            html.Div("Cadereyta:", className="small fw-bold"),
            dbc.Badge(
                cadereyta_quality["text"],
                color=cadereyta_quality["color"],
                className="w-100 text-start p-2",
            ),
        ],
    ]
