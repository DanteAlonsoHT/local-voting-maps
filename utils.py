import numpy as np
import pandas as pd
import geopandas as gpd
from constants import shapefile_path, columns_to_clean, politic_partys

# Función para cargar y limpiar datos
def load_and_clean_data(voting_file):
    voting_data = pd.read_csv(voting_file)
    geo_data = gpd.read_file(shapefile_path)
    clean_column(voting_data, 'SECCION')
    clean_column(geo_data, 'SECCION')
    merged_data = geo_data.merge(voting_data, on='SECCION')
    for column in columns_to_clean:
        remove_strings_from_votation_colum(merged_data, column)
    make_calculate_votation_rate(merged_data, politic_partys)
    return merged_data

# Definir la función para convertir y limpiar la columna
def clean_column(df, column_name):
    df[column_name] = df[column_name].fillna(0)  # Replace NaN with 0
    df[column_name] = df[column_name].replace(['N/A', 'NULL', '', ' '], 0)  # Replace 'N/A', 'NULL', empty strings with 0
    df[column_name] = df[column_name].apply(lambda x: 0 if isinstance(x, str) and not x.isdigit() else x)  # Replace non-numeric strings with 0
    df[column_name] = df[column_name].apply(lambda x: 0 if isinstance(x, (int, float)) and x < 0 else x)  # Replace negative numbers with 0
    df[column_name] = df[column_name].astype(float).astype(int).astype(str)  # Convert to float, then int, then str
    df[column_name] = df[column_name].str.strip()  # Strip whitespace

def remove_strings_from_votation_colum(df, column_name):
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce').fillna(0)

# Función para calcular la tasa de votos
def calculate_votation_rate(data, partys, name_column):
    # Si es una lista de partidos, sumamos sus votos
    if isinstance(partys, list):
        votos = data[partys].sum(axis=1)
    else:
        votos = data[partys]
    
    # Calculamos la tasa
    data[name_column] = ((votos / data['TOTAL_VOTOS_CALCULADO']) * 100).round(1)
    
    # Reemplazamos infinitos y convertimos a numérico
    data[name_column].replace([float('inf'), -float('inf')], 0, inplace=True)
    data[name_column] = pd.to_numeric(data[name_column], errors='coerce').fillna(0)

def make_calculate_votation_rate(merged_data, politic_partys):
    for party in politic_partys:
        if isinstance(party, list):
            column_name = '_'.join(party)
        else:
            column_name = party
        new_column_name = f'TASA_VOTOS_{column_name}'
        calculate_votation_rate(merged_data, party, new_column_name)

def format_map_name(file_name):
    # Remove 'folium_map_' and '.html'
    formatted_name = file_name.replace('static/folium_map_', '').replace('.html', '')
    # Replace underscores with spaces and convert to title case
    formatted_name = formatted_name.replace('_', ' ').title()
    return formatted_name.upper()
