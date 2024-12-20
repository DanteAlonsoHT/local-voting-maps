from flask import Flask, render_template, request
import folium
from folium import Choropleth
import asyncio
import pandas as pd
import numpy as np
from utils import load_and_clean_data, format_map_name
from concurrent.futures import ThreadPoolExecutor
from constants import voting_files, columns_to_show_in_table, file_names, rate_column_names, secciones_distritos_iv, secciones_distritos_v
import time

app = Flask(__name__)

# Cargar y limpiar todos los archivos de votación
all_merged_data = [load_and_clean_data(file) for file in voting_files]

def generate_map(merged_data, column_to_show, sections, distrit):
    start = time.time()
    m = folium.Map(location=[21.12, -101.68], zoom_start=12)  # Ajusta la ubicación y el nivel de zoom según tus datos
    merged_data = merged_data[merged_data['SECCION'].isin(sections)]
    if column_to_show == 'Distrito':
        print('Distrito')
        print(sections)
        print(len(sections))
        Choropleth(
            geo_data=merged_data,
            data=merged_data,
            columns=['SECCION', 'TASA_VOTOS_PAN'],
            key_on='feature.properties.SECCION',
            fill_color='YlGn',
            nan_fill_color="purple",
            nan_fill_opacity=0,
            fill_opacity=0,
            line_opacity=1,
            threshold_scale=np.linspace(0, 100, 100).tolist(),
            legend_name=f'Distrito {distrit}'
        ).add_to(m)
    else:
        Choropleth(
            geo_data=merged_data,
            data=merged_data,
            columns=['SECCION', column_to_show],
            key_on='feature.properties.SECCION',
            fill_color='YlGn',
            nan_fill_color="purple",
            nan_fill_opacity=0.4,
            fill_opacity=0.5,
            line_opacity=0.3,
            threshold_scale=np.linspace(0, 100, 100).tolist(),
            legend_name=f'Porcentaje de Votos para {column_to_show}'
        ).add_to(m)

    file_path = f'static/folium_map_{column_to_show}-{distrit}.html'
    m.save(file_path)
    end = time.time()
    print(f'Porcentaje de Votos para {column_to_show} en', end - start, 'seconds')
    return file_path

@app.route('/')
def index():
    # Parámetros de la solicitud
    print('Starting...')
    file_index = int(request.args.get('file_index', 0))
    merged_data = all_merged_data[file_index]
    merged_data.to_csv('./merged_data.csv', index=False)
    merged_data = merged_data.drop_duplicates(subset=['SECCION'], keep='first')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print('Starting...')
    map_files = loop.run_until_complete(generate_all_maps_async(merged_data, secciones_distritos_iv, 'IV'))
    map_files += loop.run_until_complete(generate_all_maps_async(merged_data, secciones_distritos_v, 'V'))
    print('Finishing...')

    corrected_paths = [(path.replace('static/', ''), format_map_name(path)) for path in map_files]

    filtered_data = merged_data[columns_to_show_in_table]
    table_html = filtered_data.to_html(classes='responsive-table', index=False)

    # Renderizar la página con el mapa y la tabla
    return render_template(
        'index.html', 
        file_index=file_index, 
        files=len(voting_files), 
        table=table_html,
        file_names=file_names,
        map_files=corrected_paths
    )

async def generate_all_maps_async(merged_data, sections, distrit):
  with ThreadPoolExecutor() as executor:
      loop = asyncio.get_event_loop()
      tasks = [
          loop.run_in_executor(executor, generate_map, merged_data, column, sections, distrit)
          for column in rate_column_names
      ]
      completed_tasks = await asyncio.gather(*tasks)
  return completed_tasks

if __name__ == '__main__':
    app.run(debug=True)
