import dash
from dash import html, dcc, callback, Output, Input
import pandas as pd
import geopandas as gpd
import folium
from folium import plugins
import os

dash.register_page(__name__)

layout = html.Div([])